/**
 * Application constants
 */

export const API_BASE_URL =
  import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const CHART_CONFIG = {
  height: 400,
  margin: { top: 5, right: 30, left: 20, bottom: 5 },
  animationDuration: 300,
};

export const SWR_CONFIG = {
  revalidateOnFocus: false,
  revalidateOnReconnect: true,
  dedupingInterval: 2000,
};

export const DEFAULT_DATE_RANGE_DAYS = 90;

export const MAX_SELECTED_SNEAKERS = 5;
