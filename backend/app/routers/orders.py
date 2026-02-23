from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import Optional
from app.models import Order, CartItem, MenuItem, OrderItem
from datetime import datetime

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
    cart_items = await CartItem.find(CartItem.user_id == request.user_id).to_list()
    
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    restaurant_id = cart_items[0].restaurant_id
    order_items = []
    total_amount = 0.0
    
    for cart_item in cart_items:
        menu_item = await MenuItem.get(cart_item.menu_item_id)
        if menu_item:
            subtotal = menu_item.price * cart_item.quantity
            total_amount += subtotal
            order_items.append(OrderItem(
                menu_item_id=str(menu_item.id),
                name=menu_item.name,
                quantity=cart_item.quantity,
                unit_price=menu_item.price
            ))
    
    delivery_fee = 30.0
    taxes = total_amount * 0.05
    grand_total = total_amount + delivery_fee + taxes
    
    order = Order(
        user_id=request.user_id,
        restaurant_id=restaurant_id,
        status="pending",
        total_amount=grand_total,
        delivery_address=request.delivery_address,
        delivery_lat=request.delivery_lat,
        delivery_lng=request.delivery_lng,
        items=order_items
    )
    await order.insert()
    
    for cart_item in cart_items:
        await cart_item.delete()
    
    return {
        "order_id": str(order.id),
        "status": order.status,
        "total_amount": grand_total,
        "message": "Order placed successfully"
    }


@router.get("/user/{user_id}")
async def get_user_orders(user_id: str):
    orders = await Order.find(Order.user_id == user_id).sort(-Order.created_at).to_list()
    
    from app.models import Restaurant
    
    result = []
    for order in orders:
        restaurant = await Restaurant.get(order.restaurant_id)
        result.append({
            "_id": str(order.id),
            "restaurant_id": order.restaurant_id,
            "restaurant_name": restaurant.name if restaurant else "Unknown",
            "status": order.status,
            "total_amount": order.total_amount,
            "delivery_address": order.delivery_address,
            "items": [item.dict() for item in order.items],
            "created_at": order.created_at.isoformat()
        })
    
    return result


@router.get("/{order_id}")
async def get_order(order_id: str):
    order = await Order.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    from app.models import Restaurant
    restaurant = await Restaurant.get(order.restaurant_id)
    
    return {
        "_id": str(order.id),
        "user_id": order.user_id,
        "restaurant_id": order.restaurant_id,
        "restaurant_name": restaurant.name if restaurant else "Unknown",
        "status": order.status,
        "total_amount": order.total_amount,
        "delivery_address": order.delivery_address,
        "delivery_lat": order.delivery_lat,
        "delivery_lng": order.delivery_lng,
        "items": [item.dict() for item in order.items],
        "created_at": order.created_at.isoformat()
    }


@router.patch("/{order_id}/status")
async def update_order_status(order_id: str, request: UpdateStatusRequest):
    valid_statuses = ["pending", "confirmed", "preparing", "out_for_delivery", "delivered", "cancelled"]
    if request.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
    
    order = await Order.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = request.status
    await order.save()
    
    return {
        "order_id": str(order.id),
        "status": order.status,
        "message": "Order status updated"
    }
