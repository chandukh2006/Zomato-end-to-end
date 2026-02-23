'use client';

import { useState } from 'react';
import { useCartStore } from '@/store/cartStore';
import { cartAPI } from '@/lib/api';
import toast from 'react-hot-toast';

interface MenuItemCardProps {
  item: {
    _id: string;
    name: string;
    description: string;
    price: number;
    image_url: string;
    is_veg: boolean;
    restaurant_id: string;
  };
  userId: string;
  currentQuantity?: number;
}

export default function MenuItemCard({
  item,
  userId,
  currentQuantity = 0,
}: MenuItemCardProps) {
  const [quantity, setQuantity] = useState(currentQuantity);
  const [loading, setLoading] = useState(false);
  const { addItem, updateQty } = useCartStore();

  const handleAdd = async () => {
    if (!userId) {
      toast.error('Please login to add items to cart');
      return;
    }

    setLoading(true);
    try {
      const result = addItem({
        _id: '',
        menu_item_id: item._id,
        restaurant_id: item.restaurant_id,
        quantity: 1,
        name: item.name,
        description: item.description,
        price: item.price,
        image_url: item.image_url,
        is_veg: item.is_veg,
        subtotal: item.price,
      });

      if (result === 'conflict') {
        toast.error('Your cart has items from another restaurant');
        return;
      }

      await cartAPI.addItem({
        user_id: userId,
        menu_item_id: item._id,
        quantity: 1,
      });

      setQuantity(1);
      toast.success('Added to cart!');
    } catch (error: any) {
      if (error.response?.status === 409) {
        toast.error(error.response.data.detail);
      } else {
        toast.error('Failed to add item');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateQty = async (newQty: number) => {
    if (!userId) return;

    setLoading(true);
    try {
      // Find cart item ID from store
      const cartItems = useCartStore.getState().items;
      const cartItem = cartItems.find((ci) => ci.menu_item_id === item._id);
      
      if (!cartItem) return;

      updateQty(cartItem._id, newQty);
      await cartAPI.updateItem(cartItem._id, newQty);
      setQuantity(newQty);
    } catch (error) {
      toast.error('Failed to update quantity');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 p-4">
      <div className="flex gap-4">
        {/* Image */}
        <div className="w-24 h-24 flex-shrink-0">
          <img
            src={item.image_url}
            alt={item.name}
            className="w-full h-full object-cover rounded-lg"
          />
        </div>

        {/* Content */}
        <div className="flex-1">
          <div className="flex items-start justify-between mb-1">
            <div className="flex items-center gap-2">
              <div
                className={`w-4 h-4 rounded border-2 ${
                  item.is_veg ? 'border-green-500' : 'border-red-500'
                }`}
              >
                <div
                  className={`w-2 h-2 rounded-full m-0.5 ${
                    item.is_veg ? 'bg-green-500' : 'bg-red-500'
                  }`}
                />
              </div>
              <h3 className="font-semibold text-lg">{item.name}</h3>
            </div>
            <span className="font-bold text-primary">₹{item.price}</span>
          </div>

          <p className="text-gray-600 text-sm mb-3 line-clamp-2">
            {item.description}
          </p>

          {/* Quantity Controls */}
          {quantity > 0 ? (
            <div className="flex items-center gap-3">
              <button
                onClick={() => handleUpdateQty(quantity - 1)}
                disabled={loading}
                className="w-8 h-8 rounded-full border-2 border-primary text-primary hover:bg-primary hover:text-white transition"
              >
                -
              </button>
              <span className="font-semibold w-8 text-center">{quantity}</span>
              <button
                onClick={() => handleUpdateQty(quantity + 1)}
                disabled={loading}
                className="w-8 h-8 rounded-full border-2 border-primary text-primary hover:bg-primary hover:text-white transition"
              >
                +
              </button>
            </div>
          ) : (
            <button
              onClick={handleAdd}
              disabled={loading}
              className="px-6 py-2 border-2 border-primary text-primary rounded-lg hover:bg-primary hover:text-white transition font-semibold"
            >
              ADD
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
