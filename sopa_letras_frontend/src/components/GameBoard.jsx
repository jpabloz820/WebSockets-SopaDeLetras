import React, { useRef, useState } from 'react';
import { Box, Paper, Typography } from '@mui/material';

const GameBoard = ({ board, onWordFound, foundWords, targetWords }) => {
  const [selectedCells, setSelectedCells] = useState([]);
  const isMouseDown = useRef(false);

  const handleMouseDown = (row, col) => {
    isMouseDown.current = true;
    setSelectedCells([[row, col]]);
  };

  const handleMouseEnter = (row, col) => {
    if (isMouseDown.current) {
      setSelectedCells((prev) => [...prev, [row, col]]);
    }
  };

  const handleMouseUp = () => {
  isMouseDown.current = false;

  if (selectedCells.length === 0) return;

  const word = selectedCells.map(([r, c]) => board[r][c]).join('').toUpperCase();
  const reversed = word.split('').reverse().join('');

  const isMatch = targetWords.some(w => w === word || w === reversed);
  if (isMatch) {
    onWordFound({
      word: word,
      path: [...selectedCells]
    });
  }

  setSelectedCells([]);
};

  const isCellSelected = (row, col) => selectedCells.some(([r, c]) => r === row && c === col);
  const isCellFound = (row, col) => {
    return foundWords.some(word => {
      const path = word.path || [];
      return path.some(([r, c]) => r === row && c === col);
    });
  };

  if (!board || board.length === 0 || !board[0]) return null;

  return (
    <Paper elevation={3} sx={{ p: 2, backgroundColor: 'background.paper', mt: 3 }}>
      <Typography variant="h6" align="center" gutterBottom>
        Tablero
      </Typography>
      <Box
        sx={{
          display: 'grid',
          gridTemplateColumns: `repeat(${board[0].length}, 40px)`,
          gap: '6px',
          justifyContent: 'center',
          userSelect: 'none'
        }}
        onMouseLeave={() => (isMouseDown.current = false)}
        onMouseUp={handleMouseUp}
      >
        {board.map((row, i) =>
          row.map((cell, j) => (
            <Box
              key={`${i}-${j}`}
              sx={{
                border: '1px solid',
                borderColor: 'divider',
                width: 40,
                height: 40,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontWeight: 'bold',
                bgcolor: isCellFound(i, j)
                  ? 'success.light'
                  : isCellSelected(i, j)
                  ? 'primary.light'
                  : 'background.default',
                color: 'text.primary',
                borderRadius: 1,
                cursor: 'pointer'
              }}
              onMouseDown={() => handleMouseDown(i, j)}
              onMouseEnter={() => handleMouseEnter(i, j)}
            >
              {cell}
            </Box>
          ))
        )}
      </Box>
    </Paper>
  );
};

export default GameBoard;