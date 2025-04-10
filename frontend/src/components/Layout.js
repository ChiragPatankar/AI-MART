import React from 'react';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import {
  AppBar,
  Box,
  Toolbar,
  Typography,
  Button,
  Container,
  Link,
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  useTheme,
  useMediaQuery,
  Badge,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Home as HomeIcon,
  ShoppingCart as ShoppingCartIcon,
  Person as PersonIcon,
  AdminPanelSettings as AdminIcon,
  Star as StarIcon,
  ShoppingBasket as CartIcon,
} from '@mui/icons-material';
import { useSelector } from 'react-redux';

const drawerWidth = 240;

function Layout({ children }) {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const [mobileOpen, setMobileOpen] = React.useState(false);
  const location = useLocation();
  const cartItems = useSelector((state) => state.cart.items);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const menuItems = [
    { text: 'Home', icon: <HomeIcon />, path: '/' },
    { text: 'Products', icon: <ShoppingCartIcon />, path: '/products' },
    { text: 'Recommendations', icon: <StarIcon />, path: '/recommendations' },
    { text: 'Profile', icon: <PersonIcon />, path: '/profile' },
    { text: 'Admin', icon: <AdminIcon />, path: '/admin' },
  ];

  const drawer = (
    <List>
      {menuItems.map((item) => (
        <ListItem
          button
          key={item.text}
          component={RouterLink}
          to={item.path}
          selected={location.pathname === item.path}
        >
          <ListItemIcon>{item.icon}</ListItemIcon>
          <ListItemText primary={item.text} />
        </ListItem>
      ))}
      <ListItem
        button
        component={RouterLink}
        to="/cart"
        selected={location.pathname === '/cart'}
      >
        <ListItemIcon>
          <Badge badgeContent={cartItems.length} color="secondary">
            <CartIcon />
          </Badge>
        </ListItemIcon>
        <ListItemText primary="Cart" />
      </ListItem>
    </List>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar position="fixed" sx={{ zIndex: theme.zIndex.drawer + 1 }}>
        <Toolbar>
          {isMobile && (
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={handleDrawerToggle}
              sx={{ mr: 2 }}
            >
              <MenuIcon />
            </IconButton>
          )}
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            AI-Mart
          </Typography>
          {!isMobile && (
            <Box sx={{ display: 'flex' }}>
              {menuItems.map((item) => (
                <Button
                  key={item.text}
                  color="inherit"
                  component={RouterLink}
                  to={item.path}
                  sx={{
                    mx: 1,
                    ...(location.pathname === item.path && {
                      backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    }),
                  }}
                >
                  {item.text}
                </Button>
              ))}
              <Button
                color="inherit"
                component={RouterLink}
                to="/cart"
                sx={{
                  mx: 1,
                  ...(location.pathname === '/cart' && {
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                  }),
                }}
              >
                <Badge badgeContent={cartItems.length} color="secondary">
                  <CartIcon />
                </Badge>
              </Button>
            </Box>
          )}
        </Toolbar>
      </AppBar>

      {isMobile ? (
        <Drawer
          variant="temporary"
          anchor="left"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true, // Better open performance on mobile.
          }}
          sx={{
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
      ) : (
        <Drawer
          variant="permanent"
          sx={{
            width: drawerWidth,
            flexShrink: 0,
            '& .MuiDrawer-paper': {
              width: drawerWidth,
              boxSizing: 'border-box',
              marginTop: '64px',
            },
          }}
          open
        >
          {drawer}
        </Drawer>
      )}

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          marginTop: '64px',
        }}
      >
        <Container maxWidth="lg">{children}</Container>
      </Box>
    </Box>
  );
}

export default Layout; 