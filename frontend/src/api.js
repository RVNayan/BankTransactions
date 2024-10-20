// src/api.js
const API_URL = 'http://localhost:8080'; // Your Flask backend URL

export const testApiRequest = async () => {
  try {
    const response = await fetch(`${API_URL}/test`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching test API:", error);
    throw error;
  }
};
