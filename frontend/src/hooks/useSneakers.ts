/**
 * Custom hook for fetching all sneakers
 * Uses SWR for automatic caching and revalidation
 */
import useSWR from 'swr';
import { fetchSneakers } from '../utils/api';
import type { Sneaker } from '../utils/types';

export function useSneakers() {
  const { data, error, isLoading, mutate } = useSWR<Sneaker[]>(
    '/api/sneakers',
    fetchSneakers,
    {
      revalidateOnFocus: false,
      revalidateOnReconnect: true,
    }
  );

  return {
    sneakers: data || [],
    isLoading,
    error,
    refresh: mutate,
  };
}
