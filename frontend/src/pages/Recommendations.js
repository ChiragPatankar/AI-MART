import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CardMedia,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  Chip,
  CircularProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Divider,
  Snackbar,
  Alert,
} from '@mui/material';
import { ExpandMore as ExpandMoreIcon } from '@mui/icons-material';
import api from '../services/api';
import { addItemToCart } from '../store/slices/cartSlice';

function Recommendations() {
  const dispatch = useDispatch();
  const cartItems = useSelector((state) => state.cart.items);
  const user = useSelector((state) => state.user.user);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [algorithm, setAlgorithm] = useState('hybrid');
  const [expandedExplanation, setExpandedExplanation] = useState(null);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [addedProduct, setAddedProduct] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchRecommendations();
  }, [algorithm, cartItems]); // Re-fetch when cart items change

  const fetchRecommendations = async () => {
    setLoading(true);
    try {
      const response = await api.post('/api/recommendations/', {
        customer_id: user?.id || 1, // Use logged-in user's ID or fallback to 1
        action_type: 'get_recommendations',
        algorithm: algorithm,
        limit: 10
      });
      
      if (response.data?.error) {
        setError(response.data.error);
        setRecommendations([]);
      } else {
        setRecommendations(response.data?.recommendations || []);
        setError(null);
      }
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      setError('Failed to load recommendations. ' + (error.response?.data?.error || error.message));
      setRecommendations([]);
    } finally {
      setLoading(false);
    }
  };

  const handleAlgorithmChange = (event) => {
    setAlgorithm(event.target.value);
  };

  const handleExplanationToggle = (productId) => {
    setExpandedExplanation(expandedExplanation === productId ? null : productId);
  };

  const handleAddToCart = async (product) => {
    try {
      await dispatch(addItemToCart(product.id, 1));
      setAddedProduct(product);
      setSnackbarOpen(true);
    } catch (error) {
      setError('Failed to add item to cart');
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbarOpen(false);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Personalized Recommendations
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* Algorithm Selection */}
      <Box sx={{ mb: 4 }}>
        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel>Recommendation Algorithm</InputLabel>
          <Select
            value={algorithm}
            onChange={handleAlgorithmChange}
            label="Recommendation Algorithm"
          >
            <MenuItem value="hybrid">Hybrid Approach</MenuItem>
            <MenuItem value="collaborative">Collaborative Filtering</MenuItem>
            <MenuItem value="content">Content-Based</MenuItem>
            <MenuItem value="sequential">Sequential Pattern Mining</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {/* Cart-based recommendations info */}
      {recommendations.length > 0 && recommendations[0]?.based_on_cart && (
        <Alert severity="info" sx={{ mb: 2 }}>
          These recommendations are based on items in your cart
        </Alert>
      )}

      {/* No recommendations message */}
      {!loading && recommendations.length === 0 && (
        <Box textAlign="center" my={4}>
          <Typography variant="h6" color="text.secondary">
            {cartItems.length === 0 
              ? "No recommendations available. Try adding some items to your cart first!"
              : "No recommendations available at the moment."}
          </Typography>
        </Box>
      )}

      {/* Recommendations Grid */}
      <Grid container spacing={3}>
        {recommendations?.map((recommendation) => (
          <Grid item xs={12} sm={6} md={4} key={recommendation.product_id}>
            <Card>
              <CardMedia
                component="img"
                height="200"
                image={recommendation.product.image_url || 'https://via.placeholder.com/200'}
                alt={recommendation.product.name}
              />
              <CardContent>
                <Typography gutterBottom variant="h6" component="div">
                  {recommendation.product.name}
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {recommendation.product.description}
                </Typography>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 2 }}>
                  <Typography variant="h6" color="primary">
                    ${recommendation.product.price}
                  </Typography>
                  <Chip label={recommendation.product.category} color="primary" variant="outlined" />
                </Box>

                {/* Explanation Accordion */}
                <Accordion
                  expanded={expandedExplanation === recommendation.product_id}
                  onChange={() => handleExplanationToggle(recommendation.product_id)}
                  sx={{ mt: 2 }}
                >
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography>Why was this recommended?</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Typography variant="body2">
                      {recommendation.explanation}
                    </Typography>
                    <Divider sx={{ my: 2 }} />
                    <Typography variant="body2" color="text.secondary">
                      Algorithm: {recommendation.algorithm}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Confidence Score: {recommendation.confidence_score}
                    </Typography>
                  </AccordionDetails>
                </Accordion>

                <Button
                  variant="contained"
                  color="primary"
                  fullWidth
                  sx={{ mt: 2 }}
                  onClick={() => handleAddToCart(recommendation.product)}
                >
                  Add to Cart
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Snackbar Notification */}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={handleCloseSnackbar}
        message={addedProduct ? `${addedProduct.name} added to cart` : ''}
        action={
          <Button color="secondary" size="small" onClick={() => window.location.href = '/cart'}>
            View Cart
          </Button>
        }
      />
    </Box>
  );
}

export default Recommendations; 