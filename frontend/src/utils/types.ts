/**
 * TypeScript type definitions for Stride application
 * Matches backend API models
 */

// Entity Types
export interface Brand {
  brand_id: number;
  name: string;
  website?: string;
}

export interface Retailer {
  retailer_id: number;
  name: string;
  location?: string;
  website?: string;
}

export interface Sneaker {
  sneaker_id: number;
  name: string;
  sku: string;
  release_date?: string;
  colorway?: string;
  available_sizes?: string;
  price: number;
  ratings?: number;
  brand_id: number;
  brand_name: string;
  retailer_id: number;
}

// Price History Type
export interface PricePoint {
  timestamp: string;
  price: number;
  sneaker_id: number;
}

export interface PriceHistoryRequest {
  sneaker_ids: number[];
  start_date?: string;
  end_date?: string;
}

// UI-specific types
export interface SelectOption {
  value: number;
  label: string;
  brand: string;
  colorway?: string;
}

export interface ChartData {
  timestamp: Date;
  [key: string]: number | Date | string; // Dynamic keys for each sneaker
}

export interface SneakerStats {
  sneaker_id: number;
  name: string;
  sku: string;
  current_price: number;
  retail_price: number;
  price_change: number;
  price_change_percent: number;
  min_price: number;
  max_price: number;
  avg_price: number;
  release_date: string;
  available_sizes: string;
  ratings: number;
}
