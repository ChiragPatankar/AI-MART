import { configureStore } from '@reduxjs/toolkit';
import userReducer from './slices/userSlice';
import cartReducer from './slices/cartSlice';
import recommendationsReducer from './slices/recommendationsSlice';

export const store = configureStore({
  reducer: {
    user: userReducer,
    cart: cartReducer,
    recommendations: recommendationsReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,
    }),
}); 