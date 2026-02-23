'use client';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { FaStar, FaClock, FaRupeeSign } from 'react-icons/fa';

interface Restaurant {
  _id: string;
  name: string;
  cuisine_type: string;
  rating: number;
  delivery_time_mins: number;
  min_order: number;
  image_url: string;
  is_open: boolean;
  tags?: string[];
}

export default function RestaurantCard({ restaurant }: { restaurant: Restaurant }) {
  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      transition={{ duration: 0.2 }}
      className="bg-white rounded-xl shadow-md hover:shadow-xl overflow-hidden cursor-pointer"
    >
      <Link href={`/restaurants/${restaurant._id}`}>
        <div className="relative">
          <img
            src={restaurant.image_url || 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400'}
            alt={restaurant.name}
            className="w-full h-48 object-cover"
            onError={(e) => {
              (e.target as HTMLImageElement).src = 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400';
            }}
          />
          <div className="absolute top-3 right-3">
            <span className={`px-2 py-1 rounded-full text-xs font-bold text-white ${restaurant.is_open ? 'bg-green-500' : 'bg-red-500'}`}>
              {restaurant.is_open ? '● OPEN' : '● CLOSED'}
            </span>
          </div>
        </div>
        <div className="p-4">
          <h3 className="font-bold text-lg text-gray-800 truncate">{restaurant.name}</h3>
          <p className="text-gray-500 text-sm mb-3">{restaurant.cuisine_type}</p>
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-1 text-yellow-500 font-semibold">
              <FaStar size={12} />
              <span>{restaurant.rating?.toFixed(1)}</span>
            </div>
            <div className="flex items-center gap-1 text-gray-500">
              <FaClock size={12} />
              <span>{restaurant.delivery_time_mins} mins</span>
            </div>
            <div className="flex items-center gap-1 text-gray-500">
              <FaRupeeSign size={12} />
              <span>Min ₹{restaurant.min_order}</span>
            </div>
          </div>
        </div>
      </Link>
    </motion.div>
  );
}
