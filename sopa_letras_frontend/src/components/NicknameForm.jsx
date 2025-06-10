import React, { useState } from 'react';
import { createUser } from '../api/api';
import {
  TextField,
  Button,
  Typography,
  Box,
  Paper,
} from '@mui/material';

const NicknameForm = ({ onSuccess }) => {
  const [nickname, setNickname] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const user = await createUser(nickname);
    onSuccess(user.id);
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        maxWidth: 400,
        margin: 'auto',
        mt: 10,
        px: 2,
      }}
    >
      <Paper elevation={6} sx={{ p: 4, width: '100%', backgroundColor: 'background.paper' }}>
        <Typography variant="h5" align="center" gutterBottom>
          Ingresa tu nombre
        </Typography>
        <TextField
          label="Apodo"
          variant="outlined"
          fullWidth
          value={nickname}
          onChange={(e) => setNickname(e.target.value)}
          sx={{ mb: 3 }}
        />
        <Button
          type="submit"
          variant="contained"
          fullWidth
          color="secondary"
          sx={{ py: 1.5, fontWeight: 'bold', fontSize: '1rem' }}
        >
          Entrar
        </Button>
      </Paper>
    </Box>
  );
};

export default NicknameForm;
