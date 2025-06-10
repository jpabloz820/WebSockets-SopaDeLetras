import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000';

export const createUser = async (nickname) => {
    const response = await axios.post(`${BASE_URL}/users/`, { nickname });
    return response.data;
};

export const getUser = async (id) => {
    const response = await axios.get(`${BASE_URL}/users/${id}`);
    return response.data;
};

export const getLevels = async () => {
    const response = await axios.get(`${BASE_URL}/game/levels`);
    return response.data;
};

export const getWordsForLevel = async (levelId) => {
    const response = await axios.get(`${BASE_URL}/game/resolve/${levelId}`);
    return response.data;
};

export const startGame = async (userId, levelId) => {
    const response = await axios.post(`${BASE_URL}/game/start`, null, {
        params: { user_id: userId, level_id: levelId }
    });
    return response.data;
};