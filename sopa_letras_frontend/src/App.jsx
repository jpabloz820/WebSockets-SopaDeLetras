import React, { useState } from 'react';
import { ThemeProvider, CssBaseline } from '@mui/material';
import darkTheme from './theme';
import NicknameForm from './components/NicknameForm';
import GameScreen from './components/GameScreen';

const App = () => {
  const [userId, setUserId] = useState(null);

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline /> {/* Aplica estilos base para modo oscuro */}
      <div style={{ padding: 20 }}>
        {!userId ? (
          <NicknameForm onSuccess={(id) => setUserId(id)} />
        ) : (
          <GameScreen userId={userId} />
        )}
      </div>
    </ThemeProvider>
  );
};

export default App;
