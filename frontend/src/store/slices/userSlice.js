import { createSlice } from '@reduxjs/toolkit';
import api from '../../services/api';

const initialState = {
  user: null,
  loading: false,
  error: null,
};

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setUser: (state, action) => {
      state.user = action.payload;
      state.error = null;
    },
    setLoading: (state, action) => {
      state.loading = action.payload;
    },
    setError: (state, action) => {
      state.error = action.payload;
    },
    clearUser: (state) => {
      state.user = null;
      state.error = null;
    },
  },
});

export const { setUser, setLoading, setError, clearUser } = userSlice.actions;

// Thunks
export const fetchUserProfile = () => async (dispatch) => {
  dispatch(setLoading(true));
  try {
    const response = await api.get('/api/customers/', {
      params: { action: 'get_profile' },
    });
    dispatch(setUser(response.data.profile));
  } catch (error) {
    dispatch(setError(error.message));
  } finally {
    dispatch(setLoading(false));
  }
};

export const updateUserPreferences = (preferences) => async (dispatch) => {
  dispatch(setLoading(true));
  try {
    await api.post('/api/customers/', {
      action: 'update_preferences',
      preferences,
    });
    dispatch(fetchUserProfile());
  } catch (error) {
    dispatch(setError(error.message));
  } finally {
    dispatch(setLoading(false));
  }
};

export default userSlice.reducer; 