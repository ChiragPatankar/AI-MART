import { createSlice } from '@reduxjs/toolkit';
import api from '../../services/api';

const initialState = {
  items: [],
  loading: false,
  error: null,
};

const cartSlice = createSlice({
  name: 'cart',
  initialState,
  reducers: {
    setCartItems: (state, action) => {
      state.items = action.payload;
      state.error = null;
    },
    addToCart: (state, action) => {
      const existingItem = state.items.find(
        (item) => item.product_id === action.payload.product_id
      );
      if (existingItem) {
        existingItem.quantity += action.payload.quantity;
      } else {
        state.items.push(action.payload);
      }
    },
    removeFromCart: (state, action) => {
      state.items = state.items.filter(
        (item) => item.product_id !== action.payload
      );
    },
    updateQuantity: (state, action) => {
      const item = state.items.find(
        (item) => item.product_id === action.payload.product_id
      );
      if (item) {
        item.quantity = action.payload.quantity;
      }
    },
    clearCart: (state) => {
      state.items = [];
    },
    setLoading: (state, action) => {
      state.loading = action.payload;
    },
    setError: (state, action) => {
      state.error = action.payload;
    },
  },
});

export const {
  setCartItems,
  addToCart,
  removeFromCart,
  updateQuantity,
  clearCart,
  setLoading,
  setError,
} = cartSlice.actions;

// Thunks
export const fetchCartItems = () => async (dispatch) => {
  dispatch(setLoading(true));
  try {
    const response = await api.get('/api/cart/');
    dispatch(setCartItems(response.data.items));
  } catch (error) {
    dispatch(setError(error.message));
  } finally {
    dispatch(setLoading(false));
  }
};

export const addItemToCart = (productId, quantity) => async (dispatch) => {
  dispatch(setLoading(true));
  try {
    await api.post('/api/cart/', {
      product_id: productId,
      quantity: quantity,
    });
    dispatch(fetchCartItems());
  } catch (error) {
    dispatch(setError(error.message));
  } finally {
    dispatch(setLoading(false));
  }
};

export const removeItemFromCart = (productId) => async (dispatch) => {
  dispatch(setLoading(true));
  try {
    await api.delete(`/api/cart/${productId}`);
    dispatch(removeFromCart(productId));
  } catch (error) {
    dispatch(setError(error.message));
  } finally {
    dispatch(setLoading(false));
  }
};

export const updateItemQuantity = (productId, quantity) => async (dispatch) => {
  dispatch(setLoading(true));
  try {
    await api.put(`/api/cart/${productId}`, {
      quantity: quantity,
    });
    dispatch(updateQuantity({ product_id: productId, quantity }));
  } catch (error) {
    dispatch(setError(error.message));
  } finally {
    dispatch(setLoading(false));
  }
};

export default cartSlice.reducer; 