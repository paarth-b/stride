/**
 * Multi-select component for choosing sneakers
 * Uses react-select for search and multi-selection
 */
import Select from 'react-select';
import type { Sneaker, SelectOption } from '../utils/types';

interface SneakerSelectProps {
  sneakers: Sneaker[];
  selectedSneakers: SelectOption[];
  onChange: (options: SelectOption[]) => void;
  isLoading?: boolean;
}

export function SneakerSelect({
  sneakers,
  selectedSneakers,
  onChange,
  isLoading = false,
}: SneakerSelectProps) {
  // Transform sneakers into select options
  const options: SelectOption[] = sneakers.map((sneaker) => {
    const releaseYear = sneaker.release_date
      ? new Date(sneaker.release_date).getFullYear().toString()
      : 'Unknown';
    return {
      value: sneaker.sneaker_id,
      label: `${sneaker.name} (${releaseYear}) - ${sneaker.colorway || 'Default'}`,
      brand: sneaker.brand_name,
      colorway: sneaker.colorway,
    };
  });

  // Group options by brand
  const groupedOptions = options.reduce(
    (acc, option) => {
      const existingGroup = acc.find((g) => g.label === option.brand);
      if (existingGroup) {
        existingGroup.options.push(option);
      } else {
        acc.push({
          label: option.brand,
          options: [option],
        });
      }
      return acc;
    },
    [] as { label: string; options: SelectOption[] }[]
  );

  return (
    <div className="w-full">
      <div className="flex items-baseline justify-between mb-3">
        <label className="block text-sm font-semibold text-gray-700">
          Select Sneakers to Compare
        </label>
        <span className="text-xs text-gray-500">
          {selectedSneakers.length}/5 selected
        </span>
      </div>
      <Select
        isMulti
        options={groupedOptions}
        value={selectedSneakers}
        onChange={(selected) => onChange(selected as SelectOption[])}
        isLoading={isLoading}
        placeholder="Search by brand or sneaker name..."
        classNamePrefix="select"
        menuPortalTarget={document.body}
        menuPosition="fixed"
        styles={{
          control: (base, state) => ({
            ...base,
            minHeight: '48px',
            backgroundColor: 'white',
            borderColor: state.isFocused
              ? 'var(--color-primary)'
              : 'var(--color-border)',
            borderWidth: '1px',
            borderRadius: '0.5rem',
            boxShadow: state.isFocused
              ? '0 0 0 3px rgba(59, 130, 246, 0.1)'
              : 'none',
            fontSize: '14px',
            transition: 'all 0.15s',
            '&:hover': {
              borderColor: 'var(--color-primary)',
            },
          }),
          menuPortal: (base) => ({
            ...base,
            zIndex: 9999,
          }),
          menu: (base) => ({
            ...base,
            backgroundColor: 'white',
            border: '1px solid var(--color-border)',
            borderRadius: '0.5rem',
            boxShadow: '0 10px 25px rgba(0, 0, 0, 0.1)',
            overflow: 'hidden',
          }),
          menuList: (base) => ({
            ...base,
            padding: '4px',
          }),
          group: (base) => ({
            ...base,
            paddingTop: '8px',
            paddingBottom: '8px',
          }),
          groupHeading: (base) => ({
            ...base,
            color: 'var(--color-primary)',
            fontSize: '11px',
            fontWeight: 700,
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
            padding: '8px 12px 4px',
          }),
          option: (base, state) => ({
            ...base,
            backgroundColor: state.isSelected
              ? 'var(--color-primary)'
              : state.isFocused
                ? '#eff6ff'
                : 'transparent',
            color: state.isSelected ? 'white' : 'var(--color-text-primary)',
            fontSize: '14px',
            padding: '10px 12px',
            cursor: 'pointer',
            transition: 'all 0.1s',
            '&:active': {
              backgroundColor: state.isSelected
                ? 'var(--color-primary-dark)'
                : '#dbeafe',
            },
          }),
          multiValue: (base) => ({
            ...base,
            backgroundColor: '#eff6ff',
            borderRadius: '0.375rem',
            margin: '2px',
          }),
          multiValueLabel: (base) => ({
            ...base,
            color: 'var(--color-primary)',
            fontSize: '13px',
            fontWeight: 500,
            padding: '3px 6px',
          }),
          multiValueRemove: (base) => ({
            ...base,
            color: 'var(--color-primary)',
            borderRadius: '0 0.375rem 0.375rem 0',
            transition: 'all 0.15s',
            '&:hover': {
              backgroundColor: 'var(--color-error)',
              color: 'white',
            },
          }),
          placeholder: (base) => ({
            ...base,
            color: 'var(--color-text-muted)',
            fontSize: '14px',
          }),
          input: (base) => ({
            ...base,
            color: 'var(--color-text-primary)',
          }),
          singleValue: (base) => ({
            ...base,
            color: 'var(--color-text-primary)',
          }),
        }}
        isOptionDisabled={() => selectedSneakers.length >= 5}
      />
      {selectedSneakers.length >= 5 && (
        <div className="mt-2 p-2 bg-amber-50 border border-amber-200 rounded-md">
          <p className="text-xs text-amber-700 font-medium">
            Maximum of 5 sneakers can be compared at once
          </p>
        </div>
      )}
    </div>
  );
}
