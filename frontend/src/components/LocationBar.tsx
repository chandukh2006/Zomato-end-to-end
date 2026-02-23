'use client';

import { useEffect, useState } from 'react';
import { geoAPI } from '@/lib/api';

export default function LocationBar() {
  const [city, setCity] = useState<string>('Detecting...');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          try {
            const { data } = await geoAPI.reverse(
              position.coords.latitude,
              position.coords.longitude
            );
            setCity(data.city || data.address);
            setLoading(false);
          } catch (error) {
            setCity('Location unavailable');
            setLoading(false);
          }
        },
        () => {
          setCity('Location unavailable');
          setLoading(false);
        }
      );
    } else {
      setCity('Location unavailable');
      setLoading(false);
    }
  }, []);

  return (
    <div className="flex items-center gap-2 text-sm text-gray-600">
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
      <span className={loading ? 'animate-pulse' : ''}>{city}</span>
    </div>
  );
}
