import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Rating,
  Divider,
  CircularProgress,
  Alert,
} from '@mui/material';
import api from '../services/api';

function Profile() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [feedback, setFeedback] = useState({
    type: 'recommendation_feedback',
    rating: 0,
    comment: '',
  });
  const [preferences, setPreferences] = useState({
    categories: [],
    price_range: { min: 0, max: 1000 },
    preferred_algorithms: ['hybrid'],
  });
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    setLoading(true);
    try {
      const response = await api.get('/api/customers/', {
        params: { action: 'get_profile' },
      });
      setProfile(response.data.profile);
      const loadedPreferences = response.data.preferences || {
        categories: [],
        price_range: { min: 0, max: 1000 },
        preferred_algorithms: ['hybrid']
      };
      setPreferences(loadedPreferences);
    } catch (error) {
      console.error('Error fetching profile:', error);
      setErrorMessage('Failed to load profile data');
    } finally {
      setLoading(false);
    }
  };

  const handleFeedbackSubmit = async () => {
    try {
      await api.post('/api/feedback/', {
        type: feedback.type,
        rating: feedback.rating,
        comment: feedback.comment,
      });
      setSuccessMessage('Feedback submitted successfully');
      setFeedback({ type: 'recommendation_feedback', rating: 0, comment: '' });
    } catch (error) {
      console.error('Error submitting feedback:', error);
      setErrorMessage('Failed to submit feedback');
    }
  };

  const handlePreferencesUpdate = async () => {
    try {
      await api.post('/api/customers/', {
        action: 'update_preferences',
        preferences: preferences,
      });
      setSuccessMessage('Preferences updated successfully');
    } catch (error) {
      console.error('Error updating preferences:', error);
      setErrorMessage('Failed to update preferences');
    }
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
        My Profile
      </Typography>

      {successMessage && (
        <Alert severity="success" sx={{ mb: 2 }}>
          {successMessage}
        </Alert>
      )}
      {errorMessage && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {errorMessage}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Profile Information */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Profile Information
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Name"
                    value={profile?.name || ''}
                    disabled
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Email"
                    value={profile?.email || ''}
                    disabled
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Member Since"
                    value={profile?.created_at || ''}
                    disabled
                  />
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Preferences */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Preferences
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <FormControl fullWidth>
                    <InputLabel>Preferred Categories</InputLabel>
                    <Select
                      multiple
                      value={preferences?.categories || []}
                      onChange={(e) =>
                        setPreferences({ ...preferences, categories: e.target.value })
                      }
                      renderValue={(selected) => (
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                          {selected.map((value) => (
                            <Chip key={value} label={value} />
                          ))}
                        </Box>
                      )}
                    >
                      <MenuItem value="electronics">Electronics</MenuItem>
                      <MenuItem value="clothing">Clothing</MenuItem>
                      <MenuItem value="books">Books</MenuItem>
                      <MenuItem value="home">Home & Kitchen</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={12}>
                  <Typography gutterBottom>Price Range</Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <TextField
                        fullWidth
                        label="Min"
                        type="number"
                        value={preferences?.price_range?.min || 0}
                        onChange={(e) =>
                          setPreferences({
                            ...preferences,
                            price_range: {
                              ...(preferences?.price_range || { min: 0, max: 1000 }),
                              min: parseInt(e.target.value),
                            },
                          })
                        }
                      />
                    </Grid>
                    <Grid item xs={6}>
                      <TextField
                        fullWidth
                        label="Max"
                        type="number"
                        value={preferences?.price_range?.max || 1000}
                        onChange={(e) =>
                          setPreferences({
                            ...preferences,
                            price_range: {
                              ...(preferences?.price_range || { min: 0, max: 1000 }),
                              max: parseInt(e.target.value),
                            },
                          })
                        }
                      />
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item xs={12}>
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={handlePreferencesUpdate}
                  >
                    Update Preferences
                  </Button>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Feedback */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Provide Feedback
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <FormControl fullWidth>
                    <InputLabel>Feedback Type</InputLabel>
                    <Select
                      value={feedback.type}
                      onChange={(e) =>
                        setFeedback({ ...feedback, type: e.target.value })
                      }
                    >
                      <MenuItem value="recommendation_feedback">
                        Recommendation Feedback
                      </MenuItem>
                      <MenuItem value="system_feedback">System Feedback</MenuItem>
                      <MenuItem value="product_feedback">Product Feedback</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={12}>
                  <Typography component="legend">Rating</Typography>
                  <Rating
                    value={feedback.rating}
                    onChange={(e, newValue) =>
                      setFeedback({ ...feedback, rating: newValue })
                    }
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    multiline
                    rows={4}
                    label="Comments"
                    value={feedback.comment}
                    onChange={(e) =>
                      setFeedback({ ...feedback, comment: e.target.value })
                    }
                  />
                </Grid>
                <Grid item xs={12}>
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={handleFeedbackSubmit}
                  >
                    Submit Feedback
                  </Button>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Profile; 