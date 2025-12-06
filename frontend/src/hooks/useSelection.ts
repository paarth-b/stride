/**
 * Custom hook for managing sneaker selection state
 */
import { useState, useCallback } from 'react';
import type { SelectOption } from '../utils/types';

export function useSelection() {
  const [selectedSneakers, setSelectedSneakers] = useState<SelectOption[]>([]);

  const handleSelectionChange = useCallback((options: SelectOption[]) => {
    setSelectedSneakers(options);
  }, []);

  const clearSelection = useCallback(() => {
    setSelectedSneakers([]);
  }, []);

  const selectedIds = selectedSneakers.map((s) => s.value);

  return {
    selectedSneakers,
    selectedIds,
    handleSelectionChange,
    clearSelection,
  };
}
