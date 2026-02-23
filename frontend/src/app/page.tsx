'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { menuAPI } from '@/lib/api';
import RestaurantCard from '@/components/RestaurantCard';
import SkeletonCard from '@/components/SkeletonCard';
import toast from 'react-hot-toast';

type Filter = 'all' | 'veg' | 'fast' | 'top';

export default function Home() {
  const [restaurants, setRestaurants] = useState<any[]>([]);
  const [allRestaurants, setAllRestaurants] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<Filter>('all');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    loadRestaurants();
  }, [filter]);

  const loadRestaurants = async () => {
    setLoading(true);
    try {
      const { data } = await menuAPI.getRestaurants({
        filter: filter === 'all' ? undefined : filter,
      });
      setRestaurants(data);
      if (filter === 'all') setAllRestaurants(data);
    } catch (error) {
      toast.error('Failed to load restaurants');
    } finally {
      setLoading(false);
    }
  };

  const handleSearchChange = (val: string) => {
    setSearchQuery(val);
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
  };

  // Client-side search on restaurants
  const displayData = searchQuery.trim()
    ? allRestaurants.filter((r: any) => {
        const q = searchQuery.toLowerCase();
        return (
          r.name.toLowerCase().includes(q) ||
          r.cuisine_type.toLowerCase().includes(q) ||
          (r.tags && r.tags.some((t: string) => t.toLowerCase().includes(q)))
        );
      })
    : restaurants;

  return (
    <div className="min-h-screen bg-secondary">
      <div className="bg-gradient-to-r from-[#C0392B] to-[#922B21] text-white py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <motion.h1
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-5xl md:text-6xl font-bold mb-4"
          >
            Craving something?
          </motion.h1>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="text-xl mb-8"
          >
            Order from your favorite restaurants
          </motion.p>
          <form onSubmit={handleSearch} className="max-w-2xl mx-auto">
            <div className="flex gap-2">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => handleSearchChange(e.target.value)}
                placeholder="Search restaurants by name or cuisine..."
                className="flex-1 px-6 py-4 rounded-full text-gray-900 shadow-lg focus:outline-none focus:ring-2 focus:ring-white"
              />
              <button
                type="submit"
                className="px-8 py-4 bg-white text-primary rounded-full font-semibold hover:bg-opacity-90 transition shadow-lg"
              >
                Search
              </button>
            </div>
          </form>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="flex gap-3 flex-wrap">
          {(['all', 'veg', 'fast', 'top'] as Filter[]).map((f) => (
            <button
              key={f}
              onClick={() => { setFilter(f); setSearchQuery(''); }}
              className={`px-6 py-2 rounded-full font-medium transition ${
                filter === f
                  ? 'bg-primary text-white'
                  : 'bg-white text-gray-700 border-2 border-gray-300 hover:border-primary'
              }`}
            >
              {f === 'all' ? 'All' : f === 'veg' ? 'Veg' : f === 'fast' ? 'Fast Delivery' : 'Top Rated'}
            </button>
          ))}
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 pb-12">
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => <SkeletonCard key={i} />)}
          </div>
        ) : displayData.length === 0 ? (
          <div className="text-center py-20">
            <svg className="w-24 h-24 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p className="text-gray-600 text-lg">No results found for "{searchQuery}"</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {displayData.map((restaurant, index) => (
              <RestaurantCard key={restaurant._id} restaurant={restaurant} index={index} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
