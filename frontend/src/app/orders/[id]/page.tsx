'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { orderAPI } from '@/lib/api';
import OrderStatusStepper from '@/components/OrderStatusStepper';
import toast from 'react-hot-toast';

export default function OrderTrackingPage() {
  const params = useParams();
  const router = useRouter();
  const orderId = params.id as string;

  const [order, setOrder] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadOrder();
    const interval = setInterval(loadOrder, 10000); // Refresh every 10 seconds
    return () => clearInterval(interval);
  }, [orderId]);

  const loadOrder = async () => {
    try {
      const { data } = await orderAPI.getOrder(orderId);
      setOrder(data);
    } catch (error) {
      toast.error('Failed to load order');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!order) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-600">Order not found</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-secondary py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="mb-6">
          <Link
            href="/orders"
            className="text-primary hover:underline mb-4 inline-block"
          >
            ← Back to Orders
          </Link>
          <h1 className="text-3xl font-bold mb-2">Order Tracking</h1>
          <p className="text-gray-600">
            Order ID: {order._id.slice(-8)} •{' '}
            {new Date(order.created_at).toLocaleString()}
          </p>
        </div>

        {/* Status Stepper */}
        <div className="bg-white rounded-xl shadow-md p-6 mb-6">
          <OrderStatusStepper status={order.status} />
        </div>

        {/* Order Details */}
        <div className="bg-white rounded-xl shadow-md p-6 mb-6">
          <h2 className="text-xl font-bold mb-4">Order Items</h2>
          <div className="space-y-3">
            {order.items.map((item: any, index: number) => (
              <div
                key={index}
                className="flex items-center justify-between py-2 border-b last:border-0"
              >
                <div>
                  <p className="font-semibold">{item.name}</p>
                  <p className="text-sm text-gray-600">
                    Qty: {item.quantity} × ₹{item.unit_price.toFixed(2)}
                  </p>
                </div>
                <p className="font-semibold">
                  ₹{(item.quantity * item.unit_price).toFixed(2)}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Delivery Info */}
        <div className="bg-white rounded-xl shadow-md p-6 mb-6">
          <h2 className="text-xl font-bold mb-4">Delivery Address</h2>
          <p className="text-gray-600">{order.delivery_address}</p>
        </div>

        {/* Total */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <div className="flex justify-between items-center">
            <span className="text-xl font-bold">Grand Total</span>
            <span className="text-2xl font-bold text-primary">
              ₹{order.total_amount.toFixed(2)}
            </span>
          </div>
        </div>

        {/* Back to Home */}
        <div className="mt-6 text-center">
          <Link
            href="/"
            className="px-6 py-3 bg-primary text-white rounded-lg font-semibold hover:bg-opacity-90 transition inline-block"
          >
            Back to Home
          </Link>
        </div>
      </div>
    </div>
  );
}
