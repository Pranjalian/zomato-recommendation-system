import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const getProfile = async (userId) => {
  const response = await api.get(`/profile/${userId}`);
  return response.data;
};

export const updateProfile = async (userId, explicitPreferences) => {
  const response = await api.post('/profile', {
    user_id: userId,
    explicit_preferences: explicitPreferences,
  });
  return response.data;
};

export const getRecommendations = async (userId, query, contextOverrides = {}, topK = 3) => {
  const response = await api.post('/recommend', {
    user_id: userId,
    query: query,
    context_overrides: contextOverrides,
    top_k: topK,
  });
  return response.data;
};

export const sendFeedback = async (userId, eventType, restaurantId) => {
  const response = await api.post('/feedback', {
    user_id: userId,
    event_type: eventType,
    restaurant_id: restaurantId,
  });
  return response.data;
};
