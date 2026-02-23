import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface CartItem {
  _id: string;
  menu_item_id: string;
  restaurant_id: string;
  quantity: number;
  name: string;
  description: string;
  price: number;
  image_url: string;
  is_veg: boolean;
  subtotal: number;
}

interface CartState {
  items: CartItem[];
  restaurantId: string | null;
  setCart: (items: CartItem[], restaurantId: string | null) => void;
  addItem: (item: CartItem) => 'success' | 'conflict';
  removeItem: (id: string) => void;
  updateQty: (id: string, qty: number) => void;
  clearCart: () => void;
  getTotal: () => number;
  getCount: () => number;
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],
      restaurantId: null,
      setCart: (items, restaurantId) => set({ items, restaurantId }),
      addItem: (item) => {
        const state = get();
        if (state.restaurantId && state.restaurantId !== item.restaurant_id) {
          return 'conflict';
        }
        const existingIndex = state.items.findIndex(
          (i) => i.menu_item_id === item.menu_item_id
        );
        if (existingIndex >= 0) {
          const updated = [...state.items];
          updated[existingIndex].quantity += item.quantity;
          updated[existingIndex].subtotal = updated[existingIndex].price * updated[existingIndex].quantity;
          set({ items: updated });
        } else {
          set({
            items: [...state.items, item],
            restaurantId: item.restaurant_id,
          });
        }
        return 'success';
      },
      removeItem: (id) => {
        const state = get();
        const filtered = state.items.filter((item) => item._id !== id);
        set({
          items: filtered,
          restaurantId: filtered.length === 0 ? null : state.restaurantId,
        });
      },
      updateQty: (id, qty) => {
        if (qty <= 0) {
          get().removeItem(id);
          return;
        }
        const state = get();
        const updated = state.items.map((item) =>
          item._id === id
            ? { ...item, quantity: qty, subtotal: item.price * qty }
            : item
        );
        set({ items: updated });
      },
      clearCart: () => set({ items: [], restaurantId: null }),
      getTotal: () => {
        return get().items.reduce((sum, item) => sum + item.subtotal, 0);
      },
      getCount: () => {
        return get().items.reduce((sum, item) => sum + item.quantity, 0);
      },
    }),
    {
      name: 'cart-storage',
    }
  )
);
