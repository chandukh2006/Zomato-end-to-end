import axios from 'axios';
import { useAuthStore } from '@/store/authStore';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor: attach token
api.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor: handle 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
      if (typeof window !== 'undefined') {
        window.location.href = '/auth/login';
      }
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (data: { name: string; email: string; password: string; phone: string }) =>
    api.post('/auth/register', data),
  login: (data: { email: string; password: string }) =>
    api.post('/auth/login', data),
};

export const menuAPI = {
  getRestaurants: (params?: { lat?: number; lng?: number; filter?: string }) =>
    api.get('/menu/restaurants', { params }),
  getRestaurant: (id: string) =>
    api.get(`/menu/restaurants/${id}`),
  getMenuItems: (restaurantId: string) =>
    api.get(`/menu/restaurants/${restaurantId}/items`),
  search: (q: string) =>
    api.get('/menu/search', { params: { q } }),
};

export const cartAPI = {
  getCart: (userId: string) =>
    api.get(`/cart/${userId}`),
  addItem: (data: { user_id: string; menu_item_id: string; quantity?: number }) =>
    api.post('/cart/add', data),
  updateItem: (cartId: string, quantity: number) =>
    api.put(`/cart/update/${cartId}`, { quantity }),
  removeItem: (cartId: string) =>
    api.delete(`/cart/remove/${cartId}`),
  clearCart: (userId: string) =>
    api.delete(`/cart/clear/${userId}`),
};

export const orderAPI = {
  placeOrder: (data: {
    user_id: string;
    delivery_address: string;
    delivery_lat: number;
    delivery_lng: number;
  }) => api.post('/orders/place', data),
  getOrders: (userId: string) =>
    api.get(`/orders/user/${userId}`),
  getOrder: (orderId: string) =>
    api.get(`/orders/${orderId}`),
  updateStatus: (orderId: string, status: string) =>
    api.patch(`/orders/${orderId}/status`, { status }),
};

export const geoAPI = {
  geocode: (address: string) =>
    api.get('/geo/geocode', { params: { address } }),
  reverse: (lat: number, lng: number) =>
    api.get('/geo/reverse', { params: { lat, lng } }),
};

export default api;
