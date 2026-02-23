'use client';

import { useEffect, useState, useRef } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { menuAPI, cartAPI } from '@/lib/api';
import { useAuthStore } from '@/store/authStore';
import { useCartStore } from '@/store/cartStore';
import MenuItemCard from '@/components/MenuItemCard';
import toast from 'react-hot-toast';
import Link from 'next/link';

export default function RestaurantPage() {
  const params = useParams();
  const router = useRouter();
  const restaurantId = params.id as string;
  const { user } = useAuthStore();
  const { items, getTotal, getCount } = useCartStore();

  const [restaurant, setRestaurant] = useState<any>(null);
  const [menuItems, setMenuItems] = useState<Record<string, any[]>>({});
  const [loading, setLoading] = useState(true);
  const [cartLoading, setCartLoading] = useState(false);
  const categoryRefs = useRef<Record<string, HTMLDivElement | null>>({});

  useEffect(() => {
    loadRestaurant();
    loadMenu();
    loadCart();
  }, [restaurantId]);

  const loadRestaurant = async () => {
    try {
      const { data } = await menuAPI.getRestaurant(restaurantId);
      setRestaurant(data);
    } catch (error) {
      toast.error('Failed to load restaurant');
    }
  };

  const loadMenu = async () => {
    setLoading(true);
    try {
      const { data } = await menuAPI.getMenuItems(restaurantId);
      setMenuItems(data);
    } catch (error) {
      toast.error('Failed to load menu');
    } finally {
      setLoading(false);
    }
  };

  const loadCart = async () => {
    if (!user) return;
    setCartLoading(true);
    try {
      const { data } = await cartAPI.getCart(user.id);
      useCartStore.getState().setCart(data.items, data.restaurant_id);
    } catch (error) {
      // Cart might be empty
    } finally {
      setCartLoading(false);
    }
  };

  const scrollToCategory = (category: string) => {
    const element = categoryRefs.current[category];
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  const getItemQuantity = (itemId: string) => {
    const cartItem = items.find((item) => item.menu_item_id === itemId);
    return cartItem?.quantity || 0;
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!restaurant) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-600">Restaurant not found</p>
      </div>
    );
  }

  const categories = Object.keys(menuItems);
  const cartTotal = getTotal();
  const cartCount = getCount();

  return (
    <div className="min-h-screen bg-secondary">
      {/* Cover Image */}
      <div className="relative h-64 md:h-80 w-full">
        <img
          src={restaurant.image_url}
          alt={restaurant.name}
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent" />
        <div className="absolute bottom-8 left-8 text-white">
          <h1 className="text-4xl md:text-5xl font-bold mb-2">
            {restaurant.name}
          </h1>
        </div>
      </div>

      {/* Info Row */}
      <div className="bg-white py-4 px-4 md:px-8">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center gap-6 text-sm">
          <div className="flex items-center gap-1">
            <svg
              className="w-5 h-5 text-yellow-400"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
            <span className="font-semibold">{restaurant.rating}</span>
          </div>
          <div className="flex items-center gap-1">
            <svg
              className="w-5 h-5 text-gray-500"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <span>{restaurant.delivery_time_mins} mins</span>
          </div>
          <div>
            <span className="text-gray-600">{restaurant.cuisine_type}</span>
          </div>
          <div>
            <span className="text-gray-600">Min ₹{restaurant.min_order}</span>
          </div>
        </div>
      </div>

      {/* Category Tabs */}
      {categories.length > 0 && (
        <div className="sticky top-16 bg-white border-b shadow-sm z-40">
          <div className="max-w-7xl mx-auto px-4 overflow-x-auto">
            <div className="flex gap-4 py-3">
              {categories.map((category) => (
                <button
                  key={category}
                  onClick={() => scrollToCategory(category)}
                  className="px-4 py-2 whitespace-nowrap text-sm font-medium text-gray-700 hover:text-primary transition border-b-2 border-transparent hover:border-primary"
                >
                  {category}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Menu Items */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        {categories.map((category) => (
          <div
            key={category}
            ref={(el) => {
              categoryRefs.current[category] = el;
            }}
            className="mb-12"
          >
            <h2 className="text-2xl font-bold mb-6">{category}</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {menuItems[category].map((item) => (
                <MenuItemCard
                  key={item._id}
                  item={item}
                  userId={user?.id || ''}
                  currentQuantity={getItemQuantity(item._id)}
                />
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Floating Cart Bar */}
      {cartCount > 0 && (
        <div className="fixed bottom-0 left-0 right-0 bg-white border-t shadow-lg z-50 p-4">
          <div className="max-w-7xl mx-auto flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">
                {cartCount} item{cartCount !== 1 ? 's' : ''} • ₹{cartTotal.toFixed(2)}
              </p>
            </div>
            <Link
              href="/cart"
              className="px-6 py-3 bg-primary text-white rounded-lg font-semibold hover:bg-opacity-90 transition"
            >
              View Cart
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
