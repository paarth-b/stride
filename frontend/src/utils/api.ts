/**
 * API client for Stride backend
 * Handles all HTTP communication
 */
import axios from 'axios';
import type { Sneaker, PricePoint, PriceHistoryRequest } from './types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    throw error;
  }
);

/**
 * Fetch all sneakers with brand information
 */
export async function fetchSneakers(): Promise<Sneaker[]> {
  const response = await apiClient.get<Sneaker[]>('/api/sneakers');
  return response.data;
}

/**
 * Fetch price history for selected sneakers
 */
export async function fetchPriceHistory(
  request: PriceHistoryRequest
): Promise<PricePoint[]> {
  const response = await apiClient.post<PricePoint[]>(
    '/api/sneakers/prices',
    request
  );
  return response.data;
}

/**
 * Initialize database with sample data
 */
export async function initializeData(): Promise<void> {
  await apiClient.post('/api/init-data');
}

/**
 * Health check
 */
export async function healthCheck(): Promise<boolean> {
  try {
    await apiClient.get('/health');
    return true;
  } catch {
    return false;
  }
}
