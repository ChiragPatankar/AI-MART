import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Button,
  IconButton,
  TextField,
  Alert,
  CircularProgress,
  Skeleton,
} from '@mui/material';
import {
  Add as AddIcon,
  Remove as RemoveIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import {
  fetchCartItems,
  removeItemFromCart,
  updateItemQuantity,
} from '../store/slices/cartSlice';

function Cart() {
  const dispatch = useDispatch();
  const { items, loading, error } = useSelector((state) => state.cart);
  const [updatingItems, setUpdatingItems] = useState({});

  useEffect(() => {
    dispatch(fetchCartItems());
  }, [dispatch]);

  const handleQuantityChange = async (productId, newQuantity) => {
    if (newQuantity > 0) {
      setUpdatingItems(prev => ({ ...prev, [productId]: true }));
      await dispatch(updateItemQuantity(productId, newQuantity));
      setUpdatingItems(prev => ({ ...prev, [productId]: false }));
    }
  };

  const handleRemoveItem = async (productId) => {
    setUpdatingItems(prev => ({ ...prev, [productId]: true }));
    await dispatch(removeItemFromCart(productId));
    setUpdatingItems(prev => ({ ...prev, [productId]: false }));
  };

  const calculateTotal = () => {
    return items.reduce((total, item) => total + item.price * item.quantity, 0);
  };

  if (loading && items.length === 0) {
    return (
      <Box>
        <Typography variant="h4" component="h1" gutterBottom>
          Shopping Cart
        </Typography>
        <Grid container spacing={3}>
          {[1, 2, 3].map((i) => (
            <Grid item xs={12} key={i}>
              <Card>
                <CardContent>
                  <Grid container spacing={2} alignItems="center">
                    <Grid item xs={12} sm={3}>
                      <Skeleton variant="rectangular" height={120} />
                    </Grid>
                    <Grid item xs={12} sm={4}>
                      <Skeleton variant="text" width="80%" height={32} />
                      <Skeleton variant="text" width="40%" height={24} />
                    </Grid>
                    <Grid item xs={12} sm={3}>
                      <Skeleton variant="rectangular" width={120} height={40} />
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Shopping Cart
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {items.length === 0 ? (
        <Box sx={{ textAlign: 'center', my: 4 }}>
          <Typography variant="h6" color="text.secondary">
            Your cart is empty
          </Typography>
          <Button
            variant="contained"
            color="primary"
            href="/products"
            sx={{ mt: 2 }}
          >
            Continue Shopping
          </Button>
        </Box>
      ) : (
        <>
          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              {items.map((item) => (
                <Card key={item.product_id} sx={{ mb: 2 }}>
                  <CardContent>
                    <Grid container spacing={2} alignItems="center">
                      <Grid item xs={12} sm={3}>
                        {updatingItems[item.product_id] ? (
                          <Skeleton variant="rectangular" height={120} />
                        ) : (
                          <CardMedia
                            component="img"
                            height="120"
                            image={item.image_url || 'https://via.placeholder.com/120'}
                            alt={item.name}
                          />
                        )}
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="h6" gutterBottom>
                          {item.name}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          ${item.price}
                        </Typography>
                      </Grid>
                      <Grid item xs={12} sm={3}>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <IconButton
                            size="small"
                            onClick={() => handleQuantityChange(item.product_id, item.quantity - 1)}
                            disabled={updatingItems[item.product_id]}
                          >
                            <RemoveIcon />
                          </IconButton>
                          <TextField
                            size="small"
                            value={item.quantity}
                            onChange={(e) =>
                              handleQuantityChange(
                                item.product_id,
                                parseInt(e.target.value) || 0
                              )
                            }
                            disabled={updatingItems[item.product_id]}
                            inputProps={{ min: 1, style: { textAlign: 'center' } }}
                            sx={{ width: '60px', mx: 1 }}
                          />
                          <IconButton
                            size="small"
                            onClick={() => handleQuantityChange(item.product_id, item.quantity + 1)}
                            disabled={updatingItems[item.product_id]}
                          >
                            <AddIcon />
                          </IconButton>
                        </Box>
                      </Grid>
                      <Grid item xs={12} sm={2}>
                        <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                          {updatingItems[item.product_id] ? (
                            <CircularProgress size={24} />
                          ) : (
                            <IconButton
                              color="error"
                              onClick={() => handleRemoveItem(item.product_id)}
                            >
                              <DeleteIcon />
                            </IconButton>
                          )}
                        </Box>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>
              ))}
            </Grid>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Order Summary
                  </Typography>
                  <Box sx={{ my: 2 }}>
                    <Grid container justifyContent="space-between">
                      <Typography>Subtotal</Typography>
                      <Typography>${calculateTotal().toFixed(2)}</Typography>
                    </Grid>
                  </Box>
                  <Button variant="contained" color="primary" fullWidth>
                    Proceed to Checkout
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </>
      )}
    </Box>
  );
}

export default Cart; 