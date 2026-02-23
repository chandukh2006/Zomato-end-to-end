from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.models import Order, CartItem, MenuItem, Restaurant

router = APIRouter()

class PlaceOrderRequest(BaseModel):
    user_id: str
    delivery_address: str
    delivery_lat: float
    delivery_lng: float

class UpdateStatusRequest(BaseModel):
    status: str

@router.post("/place")
async def place_order(request: PlaceOrderRequest):
    """Place order from cart items"""
    # Get cart items
    cart_items = await CartItem.find({"user_id": request.user_id}).to_list()
    
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    restaurant_id = cart_items[0].restaurant_id
    
    # Build order items array
    order_items = []
    total_amount = 0.0
    
    for cart_item in cart_items:
        menu_item = await MenuItem.get(cart_item.menu_item_id)
        if menu_item:
            subtotal = menu_item.price * cart_item.quantity
            total_amount += subtotal
            
            order_items.append({
                "menu_item_id": cart_item.menu_item_id,
                "name": menu_item.name,
                "quantity": cart_item.quantity,
                "unit_price": menu_item.price
            })
    
    # Create order
    order = Order(
        user_id=request.user_id,
        restaurant_id=restaurant_id,
        status="pending",
        total_amount=round(total_amount, 2),
        delivery_address=request.delivery_address,
        delivery_lat=request.delivery_lat,
        delivery_lng=request.delivery_lng,
        items=order_items
    )
    await order.insert()
    
    # Clear cart
    await CartItem.find({"user_id": request.user_id}).delete()
    
    return {
        "order_id": str(order.id),
        "status": order.status,
        "total_amount": order.total_amount
    }

@router.get("/user/{user_id}")
async def get_user_orders(user_id: str):
    """Get all orders for a user, sorted by created_at desc"""
    orders = await Order.find({"user_id": user_id}).sort("-created_at").to_list()
    
    result = []
    for order in orders:
        order_dict = order.dict()
        order_dict["_id"] = str(order.id)
        
        # Get restaurant name
        restaurant = await Restaurant.get(order.restaurant_id)
        if restaurant:
            order_dict["restaurant_name"] = restaurant.name
        
        result.append(order_dict)
    
    return result

@router.get("/{order_id}")
async def get_order(order_id: str):
    """Get single order details"""
    order = await Order.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order_dict = order.dict()
    order_dict["_id"] = str(order.id)
    
    # Get restaurant name
    restaurant = await Restaurant.get(order.restaurant_id)
    if restaurant:
        order_dict["restaurant_name"] = restaurant.name
        order_dict["restaurant_image"] = restaurant.image_url
    
    return order_dict

@router.patch("/{order_id}/status")
async def update_order_status(order_id: str, request: UpdateStatusRequest):
    """Update order status"""
    valid_statuses = ["pending", "confirmed", "preparing", "out_for_delivery", "delivered", "cancelled"]
    if request.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
    
    order = await Order.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = request.status
    await order.save()
    
    return {"message": "Order status updated", "status": order.status}
