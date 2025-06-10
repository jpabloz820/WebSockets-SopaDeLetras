import React, { useState } from 'react';
import NicknameForm from './components/NicknameForm';
import GameScreen from './components/GameScreen';

const App = () => {
    const [userId, setUserId] = useState(null);

    return (
        <div style={{ padding: 20 }}>
            {!userId ? (
                <NicknameForm onSuccess={(id) => setUserId(id)} />
            ) : (
                <GameScreen userId={userId} />
            )}
        </div>
    );
};

export default App;