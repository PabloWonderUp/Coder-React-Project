import styles from './navbar.module.css';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import CartWidget from './CartWidget/CartWidget';



export default function NavBar() {
  return (
    <nav className={styles.navbar}>
        <Box sx={{ display: 'flex', justifyContent:'space-between'}}>
          <Box>
            <Button sx={{color:'whitesmoke'}}>ReadWave</Button>
          </Box>
          <Box sx={{ display: 'flex' }}>
            <Button sx={{color:'whitesmoke'}}>Horror</Button>
            <Button sx={{color:'whitesmoke'}}>Fantasy</Button>
            <Button sx={{color:'whitesmoke'}}>Cookbooks</Button>
            <CartWidget/>
          </Box>
        </Box>
    </nav>
  )
}
