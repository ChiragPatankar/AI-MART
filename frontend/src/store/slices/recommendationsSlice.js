import { createSlice } from '@reduxjs/toolkit';
import api from '../../services/api';

const initialState = {
  recommendations: [],
  loading: false,
  error: null,
  selectedAlgorithm: 'hybrid',
};

const recommendationsSlice = createSlice({
  name: 'recommendations',
  initialState,
  reducers: {
    setRecommendations: (state, action) => {
      state.recommendations = action.payload;
      state.error = null;
    },
    setSelectedAlgorithm: (state, action) => {
      state.selectedAlgorithm = action.payload;
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
  setRecommendations,
  setSelectedAlgorithm,
  setLoading,
  setError,
} = recommendationsSlice.actions;

// Thunks
export const fetchRecommendations = (algorithm) => async (dispatch) => {
  dispatch(setLoading(true));
  try {
    const response = await api.get('/api/recommendations/', {
      params: {
        action: 'get_recommendations',
        algorithm: algorithm,
      },
    });
    dispatch(setRecommendations(response.data.recommendations));
    dispatch(setSelectedAlgorithm(algorithm));
  } catch (error) {
    dispatch(setError(error.message));
  } finally {
    dispatch(setLoading(false));
  }
};

export const submitFeedback = (feedback) => async (dispatch, getState) => {
  dispatch(setLoading(true));
  try {
    await api.post('/api/feedback/', feedback);
    // Refresh recommendations after feedback using the currently selected algorithm
    const { selectedAlgorithm } = getState().recommendations;
    dispatch(fetchRecommendations(selectedAlgorithm));
  } catch (error) {
    dispatch(setError(error.message));
  } finally {
    dispatch(setLoading(false));
  }
};

export default recommendationsSlice.reducer; 