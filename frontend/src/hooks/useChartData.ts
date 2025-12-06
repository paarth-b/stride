/**
 * Custom hook for transforming price data for charts
 */
import { useMemo } from 'react';
import { transformPriceData } from '../utils/helpers';
import type { PricePoint, Sneaker, ChartData } from '../utils/types';

export function useChartData(priceHistory: PricePoint[], sneakers: Sneaker[]) {
  const chartData = useMemo(() => {
    if (priceHistory.length === 0 || sneakers.length === 0) {
      return [];
    }
    return transformPriceData(priceHistory, sneakers);
  }, [priceHistory, sneakers]);

  return chartData;
}
