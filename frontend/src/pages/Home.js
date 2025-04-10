import React, { useEffect, useState } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Button,
  Chip,
  CircularProgress,
  Alert,
  LinearProgress,
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import api from '../services/api';

function Home() {
  const [featuredProducts, setFeaturedProducts] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [productsLoading, setProductsLoading] = useState(true);
  const [recommendationsLoading, setRecommendationsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      // Fetch featured products
      setProductsLoading(true);
      try {
        const productsResponse = await api.get('/api/products/', {
          params: { action: 'search_products', limit: 6 },
        });
        setFeaturedProducts(productsResponse.data?.products || []);
      } catch (error) {
        console.error('Error fetching products:', error);
        setError('Failed to load products. Please try again later.');
        setFeaturedProducts([]);
      } finally {
        setProductsLoading(false);
      }

      // Fetch recommendations
      setRecommendationsLoading(true);
      try {
        const recommendationsResponse = await api.get('/api/recommendations/', {
          params: { action: 'get_recommendations', algorithm: 'hybrid' },
        });
        setRecommendations(recommendationsResponse.data?.recommendations || []);
      } catch (error) {
        console.error('Error fetching recommendations:', error);
        if (!error) {
          setError('Failed to load recommendations. Please try again later.');
        }
        setRecommendations([]);
      } finally {
        setRecommendationsLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          bgcolor: 'primary.main',
          color: 'white',
          py: 8,
          textAlign: 'center',
          borderRadius: 2,
          mb: 4,
        }}
      >
        <Typography variant="h3" component="h1" gutterBottom>
          Welcome to AI-Mart
        </Typography>
        <Typography variant="h6" gutterBottom>
          Your personalized shopping experience powered by AI
        </Typography>
        <Button
          variant="contained"
          color="secondary"
          size="large"
          component={RouterLink}
          to="/recommendations"
          sx={{ mt: 2 }}
        >
          Get Personalized Recommendations
        </Button>
      </Box>

      {/* Error Message */}
      {error && (
        <Alert severity="error" sx={{ mb: 4 }}>
          {error}
        </Alert>
      )}

      {/* Featured Products */}
      <Box sx={{ mb: 6 }}>
        <Typography variant="h4" component="h2" gutterBottom>
          Featured Products
        </Typography>
        {productsLoading ? (
          <Box sx={{ width: '100%', mt: 2 }}>
            <LinearProgress />
            <Typography variant="body2" color="text.secondary" align="center" sx={{ mt: 1 }}>
              Loading featured products...
            </Typography>
          </Box>
        ) : featuredProducts.length > 0 ? (
          <Grid container spacing={3}>
            {featuredProducts.map((product) => (
              <Grid item xs={12} sm={6} md={4} key={product?.id || Math.random()}>
                <Card>
                  <CardMedia
                    component="img"
                    height="200"
                    image={product?.image_url || 'https://via.placeholder.com/200'}
                    alt={product?.name || 'Product'}
                  />
                  <CardContent>
                    <Typography gutterBottom variant="h6" component="div">
                      {product?.name || 'Unnamed Product'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      {product?.description || 'No description available'}
                    </Typography>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 2 }}>
                      <Typography variant="h6" color="primary">
                        ${product?.price || '0.00'}
                      </Typography>
                      <Chip label={product?.category || 'Uncategorized'} color="primary" variant="outlined" />
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        ) : (
          <Box sx={{ textAlign: 'center', my: 4 }}>
            <Typography variant="body1" color="text.secondary">
              No featured products available at the moment.
            </Typography>
          </Box>
        )}
      </Box>

      {/* Recommendations */}
      <Box>
        <Typography variant="h4" component="h2" gutterBottom>
          Personalized Recommendations
        </Typography>
        {recommendationsLoading ? (
          <Box sx={{ width: '100%', mt: 2 }}>
            <LinearProgress />
            <Typography variant="body2" color="text.secondary" align="center" sx={{ mt: 1 }}>
              Generating personalized recommendations...
            </Typography>
          </Box>
        ) : recommendations.length > 0 ? (
          <Grid container spacing={3}>
            {recommendations.map((recommendation) => (
              <Grid item xs={12} sm={6} md={4} key={recommendation?.product_id || Math.random()}>
                <Card>
                  <CardMedia
                    component="img"
                    height="200"
                    image={recommendation?.product?.image_url || 'https://via.placeholder.com/200'}
                    alt={recommendation?.product?.name || 'Product'}
                  />
                  <CardContent>
                    <Typography gutterBottom variant="h6" component="div">
                      {recommendation?.product?.name || 'Unnamed Product'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      {recommendation?.explanation || 'No explanation available'}
                    </Typography>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 2 }}>
                      <Typography variant="h6" color="primary">
                        ${recommendation?.product?.price || '0.00'}
                      </Typography>
                      <Chip 
                        label={recommendation?.product?.category || 'Uncategorized'} 
                        color="primary" 
                        variant="outlined" 
                      />
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        ) : (
          <Box sx={{ textAlign: 'center', my: 4 }}>
            <Typography variant="body1" color="text.secondary">
              No recommendations available at the moment.
            </Typography>
          </Box>
        )}
      </Box>
    </Box>
  );
}

export default Home; 