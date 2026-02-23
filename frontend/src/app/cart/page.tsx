'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';
import { useCartStore } from '@/store/cartStore';
import { cartAPI, orderAPI, geoAPI } from '@/lib/api';
import toast from 'react-hot-toast';

export default function CartPage() {
  const router = useRouter();
  const { user } = useAuthStore();
  const { items, getTotal, clearCart, removeItem, updateQty } = useCartStore();

  const [address, setAddress] = useState('');
  const [lat, setLat] = useState<number | null>(null);
  const [lng, setLng] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [placingOrder, setPlacingOrder] = useState(false);
  const [geocoding, setGeocoding] = useState(false);
  const [addressSuggestions, setAddressSuggestions] = useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);

  useEffect(() => {
    if (!user) {
      router.push('/auth/login');
      return;
    }
    loadCart();
  }, [user]);

  const loadCart = async () => {
    if (!user) return;
    setLoading(true);
    try {
      const { data } = await cartAPI.getCart(user.id);
      useCartStore.getState().setCart(data.items, data.restaurant_id);
    } catch (error) {
      toast.error('Failed to load cart');
    } finally {
      setLoading(false);
    }
  };

  const handleUseLocation = () => {
    if (navigator.geolocation) {
      setGeocoding(true);
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          try {
            const { data } = await geoAPI.reverse(
              position.coords.latitude,
              position.coords.longitude
            );
            setAddress(data.address);
            setLat(position.coords.latitude);
            setLng(position.coords.longitude);
            setShowSuggestions(false);
            toast.success('Location detected!');
          } catch (error) {
            toast.error('Failed to get address');
          } finally {
            setGeocoding(false);
          }
        },
        () => {
          toast.error('Location access denied');
          setGeocoding(false);
        }
      );
    } else {
      toast.error('Geolocation not supported');
    }
  };

  const handleAddressChange = async (value: string) => {
    setAddress(value);
    setShowSuggestions(value.length > 2);

    // Clear coordinates when address changes manually
    if (value !== address) {
      setLat(null);
      setLng(null);
    }

    // Simple debounce for geocoding suggestions (optional)
    // For now, we'll geocode on "Place Order" click
  };

  const handleGeocodeAddress = async (addressToGeocode?: string) => {
    const addr = addressToGeocode || address;
    if (!addr.trim()) {
      toast.error('Please enter a delivery address');
      return false;
    }

    setGeocoding(true);
    try {
      const { data } = await geoAPI.geocode(addr);
      setLat(data.latitude);
      setLng(data.longitude);
      // Update address with formatted address from geocoding
      if (!addressToGeocode) {
        setAddress(addr); // Keep user's input or update with formatted
      }
      setGeocoding(false);
      return true;
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to geocode address. Please check the address.');
      setGeocoding(false);
      return false;
    }
  };

  const handlePlaceOrder = async () => {
    if (!user) {
      toast.error('Please login to place order');
      return;
    }

    if (items.length === 0) {
      toast.error('Cart is empty');
      return;
    }

    if (!address.trim()) {
      toast.error('Please enter delivery address');
      return;
    }

    // If lat/lng not set, geocode the address first
    if (lat === null || lng === null) {
      const geocoded = await handleGeocodeAddress();
      if (!geocoded) {
        return; // Geocoding failed, error already shown
      }
    }

    setPlacingOrder(true);
    try {
      const confirmed = window.confirm("Confirm Payment of Rs." + grandTotal.toFixed(2) + "?");
      if (!confirmed) { setPlacingOrder(false); return; }

      const { data } = await orderAPI.placeOrder({
        user_id: user.id,
        delivery_address: address,
        delivery_lat: lat || 12.9762,
        delivery_lng: lng || 76.0342,
      });

      clearCart();
      toast.success('Order placed! 🎉');
      router.push(`/orders/${data.order_id}`);
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to place order');
    } finally {
      setPlacingOrder(false);
    }
  };

  const subtotal = getTotal();
  const deliveryFee = 30;
  const taxes = subtotal * 0.05;
  const grandTotal = subtotal + deliveryFee + taxes;

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-secondary py-8">
      <div className="max-w-7xl mx-auto px-4">
        <h1 className="text-3xl font-bold mb-8">Your Cart</h1>

        {items.length === 0 ? (
          <div className="text-center py-20">
            <svg
              className="w-24 h-24 mx-auto text-gray-400 mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"
              />
            </svg>
            <p className="text-gray-600 text-lg mb-4">Your cart is empty</p>
            <button
              onClick={() => router.push('/')}
              className="px-6 py-3 bg-primary text-white rounded-lg font-semibold hover:bg-opacity-90 transition"
            >
              Browse Restaurants
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Cart Items */}
            <div className="lg:col-span-2 space-y-4">
              {items.map((item) => (
                <div
                  key={item._id}
                  className="bg-white rounded-xl shadow-md p-4 flex gap-4"
                >
                  <img
                    src={item.image_url}
                    alt={item.name}
                    className="w-20 h-20 object-cover rounded-lg"
                  />
                  <div className="flex-1">
                    <h3 className="font-semibold text-lg mb-1">{item.name}</h3>
                    <p className="text-gray-600 text-sm mb-2">
                      ₹{item.price} × {item.quantity}
                    </p>
                    <div className="flex items-center gap-3">
                      <button
                        onClick={() => {
                          updateQty(item._id, item.quantity - 1);
                          cartAPI.updateItem(item._id, item.quantity - 1);
                        }}
                        className="w-8 h-8 rounded-full border-2 border-gray-300 hover:border-primary transition"
                      >
                        -
                      </button>
                      <span className="font-semibold w-8 text-center">
                        {item.quantity}
                      </span>
                      <button
                        onClick={() => {
                          updateQty(item._id, item.quantity + 1);
                          cartAPI.updateItem(item._id, item.quantity + 1);
                        }}
                        className="w-8 h-8 rounded-full border-2 border-gray-300 hover:border-primary transition"
                      >
                        +
                      </button>
                      <button
                        onClick={async () => {
                          removeItem(item._id);
                          await cartAPI.removeItem(item._id);
                          toast.success('Item removed');
                        }}
                        className="ml-auto text-red-500 hover:text-red-700"
                      >
                        <svg
                          className="w-5 h-5"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                          />
                        </svg>
                      </button>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-lg">₹{item.subtotal.toFixed(2)}</p>
                  </div>
                </div>
              ))}
            </div>

            {/* Order Summary */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-xl shadow-md p-6 sticky top-24">
                <h2 className="text-xl font-bold mb-4">Order Summary</h2>
                <div className="space-y-2 mb-4">
                  <div className="flex justify-between text-gray-600">
                    <span>Subtotal</span>
                    <span>₹{subtotal.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between text-gray-600">
                    <span>Delivery Fee</span>
                    <span>₹{deliveryFee.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between text-gray-600">
                    <span>Taxes (5%)</span>
                    <span>₹{taxes.toFixed(2)}</span>
                  </div>
                  <div className="border-t pt-2 mt-4">
                    <div className="flex justify-between font-bold text-lg">
                      <span>Grand Total</span>
                      <span className="text-primary">₹{grandTotal.toFixed(2)}</span>
                    </div>
                  </div>
                </div>

                {/* Delivery Address */}
                <div className="mb-6">
                  <label className="block text-sm font-semibold mb-2">
                    Delivery Address *
                  </label>
                  <div className="relative">
                    <textarea
                      value={address}
                      onChange={(e) => handleAddressChange(e.target.value)}
                      onFocus={() => setShowSuggestions(address.length > 2)}
                      placeholder="Enter your delivery address (e.g., 123 Main St, City)"
                      className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                      rows={3}
                    />
                    {geocoding && (
                      <div className="absolute top-2 right-2">
                        <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-primary"></div>
                      </div>
                    )}
                  </div>
                  
                  <div className="flex gap-2 mt-2">
                    <button
                      onClick={handleUseLocation}
                      disabled={geocoding}
                      className="text-sm text-primary hover:underline disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1"
                    >
                      <svg
                        className="w-4 h-4"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                        />
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                        />
                      </svg>
                      Use My Location
                    </button>
                    {address && (!lat || !lng) && (
                      <button
                        onClick={() => handleGeocodeAddress()}
                        disabled={geocoding}
                        className="text-sm text-primary hover:underline disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1"
                      >
                        <svg
                          className="w-4 h-4"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                          />
                        </svg>
                        Verify Address
                      </button>
                    )}
                  </div>

                  {lat && lng && (
                    <div className="mt-3 p-3 bg-green-50 border border-green-200 rounded-lg">
                      <div className="flex items-start gap-2">
                        <svg
                          className="w-5 h-5 text-green-600 mt-0.5"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                          />
                        </svg>
                        <div className="flex-1">
                          <p className="text-sm font-medium text-green-800">
                            Address verified
                          </p>
                          <p className="text-xs text-green-600 mt-1">
                            Coordinates: {lat.toFixed(4)}, {lng.toFixed(4)}
                          </p>
                        </div>
                      </div>
                    </div>
                  )}

                  {!lat && !lng && address && (
                    <div className="mt-3 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                      <p className="text-xs text-yellow-800">
                        💡 Tip: Click "Verify Address" or "Use My Location" to ensure accurate delivery
                      </p>
                    </div>
                  )}
                </div>

                <button
                  onClick={handlePlaceOrder}
                  disabled={placingOrder || geocoding || !address.trim() || items.length === 0}
                  className="w-full py-4 bg-primary text-white rounded-lg font-semibold hover:bg-opacity-90 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {placingOrder || geocoding ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white"></div>
                      {geocoding ? 'Verifying Address...' : 'Placing Order...'}
                    </>
                  ) : (
                    'Place Order'
                  )}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
