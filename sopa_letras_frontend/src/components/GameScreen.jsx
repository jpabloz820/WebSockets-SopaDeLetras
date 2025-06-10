import React, { useEffect, useState, useRef } from 'react';
import { getLevels, startGame } from '../api/api';
import GameBoard from './GameBoard';
import {
  Box,
  Typography,
  Button,
  Paper,
  List,
  ListItem,
  ListItemText,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material';

const GameScreen = ({ userId }) => {
  const [levelIndex, setLevelIndex] = useState(0);
  const [levels, setLevels] = useState([]);
  const [words, setWords] = useState([]);
  const [board, setBoard] = useState([]);
  const [foundWords, setFoundWords] = useState([]);
  const [timeElapsed, setTimeElapsed] = useState(0);
  const [gameStarted, setGameStarted] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [dialogContent, setDialogContent] = useState('');
  const ws = useRef(null);
  const intervalRef = useRef(null);

  useEffect(() => {
    const fetchLevels = async () => {
      const allLevels = await getLevels();
      setLevels(allLevels);
    };
    fetchLevels();
  }, []);

  useEffect(() => {
    if (!gameStarted || levels.length === 0) return;

    const loadLevel = async () => {
      const currentLevel = levels[levelIndex];
      const gameData = await startGame(userId, currentLevel.id);
      setWords(gameData.words);
      setBoard(gameData.board);
      setFoundWords([]);
      connectSocket();
    };

    loadLevel();

    return () => {
      if (ws.current) ws.current.close();
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [gameStarted, levels, levelIndex, userId]);

  useEffect(() => {
    if (words.length > 0 && foundWords.length === words.length) {
      clearInterval(intervalRef.current);
      setDialogContent('¡Nivel superado! Puedes avanzar al siguiente.');
      setDialogOpen(true);
    }
  }, [foundWords, words]);

  useEffect(() => {
    if (timeElapsed >= 60 && foundWords.length < words.length) {
      clearInterval(intervalRef.current);
      setDialogContent('⛔ Tiempo agotado. Puedes resolver o reiniciar.');
      setDialogOpen(true);
    }
  }, [timeElapsed, foundWords, words]);

  const connectSocket = () => {
    ws.current = new WebSocket('ws://127.0.0.1:8000/ws/game');
    ws.current.onopen = () => {
      console.log('✅ WebSocket conectado');
    };
    ws.current.onmessage = (e) => {
      try {
        const msg = JSON.parse(e.data);
        if (msg.command === 'time') {
          setTimeElapsed(msg.elapsed);
        }
      } catch (err) {
        console.warn('Mensaje no JSON:', e.data);
      }
    };

    intervalRef.current = setInterval(() => {
      ws.current?.send(JSON.stringify({ command: 'time' }));
    }, 1000);
  };

  const handleWordFound = (word) => {
    if (!foundWords.some(w => w.word === word)) {
      setFoundWords([...foundWords, { word }]);
    }
  };

  const nextLevel = () => {
    setDialogOpen(false);
    setLevelIndex((prev) => prev + 1);
    setTimeElapsed(0);
  };

  const restartLevel = () => {
    setDialogOpen(false);
    setTimeElapsed(0);
    setFoundWords([]);
    setLevelIndex((prev) => prev);
  };

  const solveLevel = () => {
    ws.current?.send(JSON.stringify({ command: 'solve' }));
  };

  return (
    <Box sx={{ p: 4 }}>
      <Typography variant="h4" gutterBottom>
        Nivel {levelIndex + 1}
      </Typography>
      <Typography variant="subtitle1" gutterBottom>
        ⏱ Tiempo: {timeElapsed} segundos
      </Typography>

      {!gameStarted ? (
        <Button
          variant="contained"
          size="large"
          color="secondary"
          onClick={() => setGameStarted(true)}
          sx={{ mt: 2 }}
        >
          Iniciar juego ▶
        </Button>
      ) : (
        <>
          <GameBoard
            board={board}
            onWordFound={handleWordFound}
            foundWords={foundWords}
            targetWords={words}
          />

          <Typography variant="h6" gutterBottom>
            🔍 Palabras a buscar:
          </Typography>
          <Paper sx={{ p: 2, mb: 3 }}>
            <List>
              {Array.isArray(words) ? (
                words.map((w) => (
                  <ListItem key={w} disablePadding>
                    <ListItemText
                      primary={w}
                      sx={{ textDecoration: foundWords.some(fw => fw.word === w) ? 'line-through' : 'none' }}
                    />
                  </ListItem>
                ))
              ) : (
                <ListItem>
                  <ListItemText primary="No hay palabras" />
                </ListItem>
              )}
            </List>
          </Paper>

          <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)}>
            <DialogTitle>Resultado</DialogTitle>
            <DialogContent>
              <Typography>{dialogContent}</Typography>
            </DialogContent>
            <DialogActions>
              {foundWords.length === words.length ? (
                <Button onClick={nextLevel} variant="contained" color="success">
                  Siguiente Nivel
                </Button>
              ) : (
                <>
                  <Button onClick={solveLevel} variant="contained" color="warning">
                    Resolver
                  </Button>
                  <Button onClick={restartLevel} variant="outlined" color="error">
                    Reiniciar
                  </Button>
                </>
              )}
            </DialogActions>
          </Dialog>
        </>
      )}
    </Box>
  );
};

export default GameScreen;