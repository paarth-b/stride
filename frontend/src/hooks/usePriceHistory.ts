/**
 * Custom hook for fetching price history
 * Fetches data only when sneakers are selected
 */
import useSWR from 'swr';
import { fetchPriceHistory } from '../utils/api';
import type { PricePoint } from '../utils/types';

export function usePriceHistory(sneakerIds: number[]) {
  const shouldFetch = sneakerIds.length > 0;

  const { data, error, isLoading } = useSWR<PricePoint[]>(
    shouldFetch ? ['/api/sneakers/prices', sneakerIds] : null,
    () =>
      fetchPriceHistory({
        sneaker_ids: sneakerIds,
      }),
    {
      revalidateOnFocus: false,
      dedupingInterval: 5000,
    }
  );

  return {
    priceHistory: data || [],
    isLoading,
    error,
  };
}
