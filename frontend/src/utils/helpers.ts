/**
 * Helper utility functions
 */
import { format } from 'date-fns';
import type { PricePoint, ChartData, SneakerStats, Sneaker } from './types';

/**
 * Format price with currency symbol
 */
export function formatPrice(price: number): string {
  return `$${price.toFixed(2)}`;
}

/**
 * Format date for display
 */
export function formatDate(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return format(d, 'MMM dd, yyyy');
}

/**
 * Calculate price change percentage
 */
export function calculatePriceChange(
  oldPrice: number,
  newPrice: number
): number {
  return ((newPrice - oldPrice) / oldPrice) * 100;
}

/**
 * Transform price points into chart-friendly format
 */
export function transformPriceData(
  pricePoints: PricePoint[],
  sneakers: Sneaker[]
): ChartData[] {
  if (pricePoints.length === 0 || sneakers.length === 0) {
    return [];
  }

  // Normalize timestamp to date only (removes time component)
  // This ensures price points from the same day get grouped together
  const normalizeTimestamp = (timestamp: string | Date): string => {
    const date = new Date(timestamp);
    // Set to start of day in UTC to ensure consistency
    date.setUTCHours(0, 0, 0, 0);
    return date.toISOString();
  };

  // Group price points by normalized timestamp
  const grouped = new Map<string, Map<number, number>>();

  pricePoints.forEach((point) => {
    const normalizedTimestamp = normalizeTimestamp(point.timestamp);
    if (!grouped.has(normalizedTimestamp)) {
      grouped.set(normalizedTimestamp, new Map());
    }
    grouped.get(normalizedTimestamp)!.set(point.sneaker_id, point.price);
  });

  // Convert to array of chart data
  const chartData: ChartData[] = [];

  grouped.forEach((priceMap, timestamp) => {
    const dataPoint: ChartData = {
      timestamp: new Date(timestamp),
    };

    // Add price for each sneaker
    priceMap.forEach((price, sneakerId) => {
      const sneaker = sneakers.find((s) => s.sneaker_id === sneakerId);
      if (sneaker) {
        const key = `${sneaker.name} - ${sneaker.colorway}`;
        dataPoint[key] = price;
      }
    });

    chartData.push(dataPoint);
  });

  // Sort by timestamp
  return chartData.sort(
    (a, b) => a.timestamp.getTime() - b.timestamp.getTime()
  );
}

/**
 * Calculate statistics for a sneaker
 */
export function calculateStats(
  sneaker: Sneaker,
  pricePoints: PricePoint[]
): SneakerStats {
  const sneakerPrices = pricePoints.filter(
    (p) => p.sneaker_id === sneaker.sneaker_id
  );

  if (sneakerPrices.length === 0) {
    return {
      sneaker_id: sneaker.sneaker_id,
      name: `${sneaker.name} - ${sneaker.colorway}`,
      sku: sneaker.sku,
      current_price: sneaker.price,
      retail_price: sneaker.price,
      price_change: 0,
      price_change_percent: 0,
      min_price: sneaker.price,
      max_price: sneaker.price,
      avg_price: sneaker.price,
      release_date: sneaker.release_date || 'Unknown',
      available_sizes: sneaker.available_sizes || 'N/A',
      ratings: sneaker.ratings || 0,
    };
  }

  const prices = sneakerPrices.map((p) => p.price);
  const currentPrice = prices[prices.length - 1];
  const minPrice = Math.min(...prices);
  const maxPrice = Math.max(...prices);
  const avgPrice = prices.reduce((sum, p) => sum + p, 0) / prices.length;
  const priceChange = currentPrice - sneaker.price;
  const priceChangePercent = calculatePriceChange(sneaker.price, currentPrice);

  return {
    sneaker_id: sneaker.sneaker_id,
    name: `${sneaker.name} - ${sneaker.colorway}`,
    sku: sneaker.sku,
    current_price: currentPrice,
    retail_price: sneaker.price,
    price_change: priceChange,
    price_change_percent: priceChangePercent,
    min_price: minPrice,
    max_price: maxPrice,
    avg_price: avgPrice,
    release_date: sneaker.release_date || 'Unknown',
    available_sizes: sneaker.available_sizes || 'N/A',
    ratings: sneaker.ratings || 0,
  };
}

/**
 * Generate distinct colors for chart lines
 */
const CHART_COLORS = [
  '#3b82f6', // blue
  '#ef4444', // red
  '#10b981', // green
  '#f59e0b', // amber
  '#8b5cf6', // purple
  '#ec4899', // pink
  '#14b8a6', // teal
  '#f97316', // orange
];

export function getChartColor(index: number): string {
  return CHART_COLORS[index % CHART_COLORS.length];
}
