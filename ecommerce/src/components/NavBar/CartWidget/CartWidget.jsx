import Box from '@mui/material/Box';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';

export default function CartWidget() {
  return (
    <Box sx={{display:'flex'}}>
        <ShoppingCartIcon fontSize="large" />
        <div>0</div>
    </Box>
  )
}
