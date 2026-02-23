from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import List
from app.models import CartItem, MenuItem, Restaurant

router = APIRouter()


class AddItemRequest(BaseModel):
    user_id: str
    menu_item_id: str
    quantity: int = 1


class UpdateItemRequest(BaseModel):
    quantity: int


@router.get("/{user_id}")
async def get_cart(user_id: str):
    cart_items = await CartItem.find(CartItem.user_id == user_id).to_list()
    
    if not cart_items:
        return {"items": [], "grand_total": 0.0, "restaurant_id": None}
    
    restaurant_id = cart_items[0].restaurant_id
    
    items_with_details = []
    grand_total = 0.0
    
    for cart_item in cart_items:
        menu_item = await MenuItem.get(cart_item.menu_item_id)
        if menu_item:
            subtotal = menu_item.price * cart_item.quantity
            grand_total += subtotal
            items_with_details.append({
                "_id": str(cart_item.id),
                "menu_item_id": cart_item.menu_item_id,
                "restaurant_id": cart_item.restaurant_id,
                "quantity": cart_item.quantity,
                "name": menu_item.name,
                "description": menu_item.description,
                "price": menu_item.price,
                "image_url": menu_item.image_url,
                "is_veg": menu_item.is_veg,
                "subtotal": subtotal
            })
    
    return {
        "items": items_with_details,
        "grand_total": grand_total,
        "restaurant_id": restaurant_id
    }


@router.post("/add")
async def add_item(request: AddItemRequest):
    menu_item = await MenuItem.get(request.menu_item_id)
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    existing_cart = await CartItem.find(CartItem.user_id == request.user_id).to_list()
    
    if existing_cart:
        existing_restaurant_id = existing_cart[0].restaurant_id
        if existing_restaurant_id != menu_item.restaurant_id:
            restaurant = await Restaurant.get(existing_restaurant_id)
            restaurant_name = restaurant.name if restaurant else "another restaurant"
            raise HTTPException(
                status_code=409,
                detail=f"Your cart has items from {restaurant_name}. Please clear your cart first."
            )
    
    existing_item = await CartItem.find_one(
        CartItem.user_id == request.user_id,
        CartItem.menu_item_id == request.menu_item_id
    )
    
    if existing_item:
        existing_item.quantity += request.quantity
        await existing_item.save()
        return {"message": "Item quantity updated", "cart_item_id": str(existing_item.id)}
    else:
        cart_item = CartItem(
            user_id=request.user_id,
            menu_item_id=request.menu_item_id,
            restaurant_id=menu_item.restaurant_id,
            quantity=request.quantity
        )
        await cart_item.insert()
        return {"message": "Item added to cart", "cart_item_id": str(cart_item.id)}


@router.put("/update/{cart_id}")
async def update_item(cart_id: str, request: UpdateItemRequest):
    cart_item = await CartItem.get(cart_id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    if request.quantity == 0:
        await cart_item.delete()
        return {"message": "Item removed from cart"}
    
    cart_item.quantity = request.quantity
    await cart_item.save()
    return {"message": "Cart item updated"}


@router.delete("/clear/{user_id}")
async def clear_cart(user_id: str):
    cart_items = await CartItem.find(CartItem.user_id == user_id).to_list()
    for item in cart_items:
        await item.delete()
    return {"message": "Cart cleared"}


@router.delete("/remove/{cart_id}")
async def remove_item(cart_id: str):
    cart_item = await CartItem.get(cart_id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    await cart_item.delete()
    return {"message": "Item removed from cart"}
