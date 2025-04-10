import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  CircularProgress,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Alert,
} from '@mui/material';
import api from '../services/api';

function Admin() {
  const [systemStats, setSystemStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [algorithmStats, setAlgorithmStats] = useState([]);
  const [selectedAlgorithm, setSelectedAlgorithm] = useState('all');
  const [timeRange, setTimeRange] = useState('7d');

  useEffect(() => {
    fetchSystemStats();
    fetchAlgorithmStats();
  }, [timeRange]);

  const fetchSystemStats = async () => {
    setLoading(true);
    try {
      const response = await api.get('/api/admin/stats', {
        params: { time_range: timeRange },
      });
      setSystemStats(response.data);
    } catch (error) {
      console.error('Error fetching system stats:', error);
      setError('Failed to load system statistics');
    } finally {
      setLoading(false);
    }
  };

  const fetchAlgorithmStats = async () => {
    try {
      const response = await api.get('/api/admin/algorithm-stats', {
        params: { time_range: timeRange },
      });
      setAlgorithmStats(response.data);
    } catch (error) {
      console.error('Error fetching algorithm stats:', error);
    }
  };

  const handleAlgorithmUpdate = async (algorithm, action) => {
    try {
      await api.post('/api/admin/update-algorithm', {
        algorithm,
        action,
      });
      setSuccess(`Algorithm ${algorithm} ${action} successfully`);
      fetchAlgorithmStats();
    } catch (error) {
      console.error('Error updating algorithm:', error);
      setError(`Failed to ${action} algorithm ${algorithm}`);
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
        Admin Dashboard
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          {success}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* System Overview */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                System Overview
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} md={4}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography color="textSecondary" gutterBottom>
                        Total Users
                      </Typography>
                      <Typography variant="h4">
                        {systemStats?.total_users || 0}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography color="textSecondary" gutterBottom>
                        Total Products
                      </Typography>
                      <Typography variant="h4">
                        {systemStats?.total_products || 0}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography color="textSecondary" gutterBottom>
                        Total Recommendations
                      </Typography>
                      <Typography variant="h4">
                        {systemStats?.total_recommendations || 0}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Algorithm Performance */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Typography variant="h6">Algorithm Performance</Typography>
                <Box sx={{ display: 'flex', gap: 2 }}>
                  <FormControl sx={{ minWidth: 120 }}>
                    <InputLabel>Time Range</InputLabel>
                    <Select
                      value={timeRange}
                      onChange={(e) => setTimeRange(e.target.value)}
                      label="Time Range"
                    >
                      <MenuItem value="1d">Last 24 Hours</MenuItem>
                      <MenuItem value="7d">Last 7 Days</MenuItem>
                      <MenuItem value="30d">Last 30 Days</MenuItem>
                    </Select>
                  </FormControl>
                  <FormControl sx={{ minWidth: 120 }}>
                    <InputLabel>Algorithm</InputLabel>
                    <Select
                      value={selectedAlgorithm}
                      onChange={(e) => setSelectedAlgorithm(e.target.value)}
                      label="Algorithm"
                    >
                      <MenuItem value="all">All Algorithms</MenuItem>
                      <MenuItem value="hybrid">Hybrid</MenuItem>
                      <MenuItem value="collaborative">Collaborative</MenuItem>
                      <MenuItem value="content">Content-Based</MenuItem>
                      <MenuItem value="sequential">Sequential</MenuItem>
                    </Select>
                  </FormControl>
                </Box>
              </Box>
              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Algorithm</TableCell>
                      <TableCell align="right">Usage Count</TableCell>
                      <TableCell align="right">Success Rate</TableCell>
                      <TableCell align="right">Average Rating</TableCell>
                      <TableCell align="right">Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {algorithmStats
                      .filter(
                        (stat) =>
                          selectedAlgorithm === 'all' ||
                          stat.algorithm === selectedAlgorithm
                      )
                      .map((stat) => (
                        <TableRow key={stat.algorithm}>
                          <TableCell component="th" scope="row">
                            {stat.algorithm}
                          </TableCell>
                          <TableCell align="right">{stat.usage_count}</TableCell>
                          <TableCell align="right">
                            {(stat.success_rate * 100).toFixed(2)}%
                          </TableCell>
                          <TableCell align="right">
                            {stat.average_rating.toFixed(2)}
                          </TableCell>
                          <TableCell align="right">
                            <Button
                              variant="outlined"
                              size="small"
                              onClick={() =>
                                handleAlgorithmUpdate(stat.algorithm, 'update')
                              }
                              sx={{ mr: 1 }}
                            >
                              Update
                            </Button>
                            <Button
                              variant="outlined"
                              color="error"
                              size="small"
                              onClick={() =>
                                handleAlgorithmUpdate(stat.algorithm, 'reset')
                              }
                            >
                              Reset
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* System Configuration */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                System Configuration
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="Minimum Confidence Threshold"
                    type="number"
                    value={systemStats?.min_confidence || 0}
                    InputProps={{ inputProps: { min: 0, max: 1, step: 0.1 } }}
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="Maximum Recommendations per User"
                    type="number"
                    value={systemStats?.max_recommendations || 0}
                    InputProps={{ inputProps: { min: 1, max: 100 } }}
                  />
                </Grid>
                <Grid item xs={12}>
                  <Button variant="contained" color="primary">
                    Save Configuration
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

export default Admin; 