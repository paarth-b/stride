/**
 * Main App component for Stride
 * Integrates all components and manages application state
 */
import { useState } from 'react';
import { SneakerSelect } from './components/SneakerSelect';
import { PriceChart } from './components/PriceChart';
import { StatisticsCards } from './components/StatisticsCards';
import { useSneakers } from './hooks/useSneakers';
import { usePriceHistory } from './hooks/usePriceHistory';
import { useSelection } from './hooks/useSelection';
import { useChartData } from './hooks/useChartData';
import { initializeData } from './utils/api';

function App() {
  const [isInitializing, setIsInitializing] = useState(false);
  const [initMessage, setInitMessage] = useState('');

  // Fetch all sneakers
  const {
    sneakers,
    isLoading: sneakersLoading,
    error: sneakersError,
  } = useSneakers();

  // Manage selection state
  const {
    selectedSneakers,
    selectedIds,
    handleSelectionChange,
    clearSelection,
  } = useSelection();

  // Fetch price history for selected sneakers
  const { priceHistory, isLoading: priceLoading } =
    usePriceHistory(selectedIds);

  // Transform data for chart
  const selectedSneakerObjects = sneakers.filter((s) =>
    selectedIds.includes(s.sneaker_id)
  );
  const chartData = useChartData(priceHistory, selectedSneakerObjects);

  // Initialize database with sample data
  const handleInitialize = async () => {
    setIsInitializing(true);
    setInitMessage('');
    try {
      await initializeData();
      setInitMessage(
        'Database initialized successfully! Refresh the page to see data.'
      );
    } catch (error) {
      setInitMessage(
        'Failed to initialize database. Make sure the backend is running.'
      );
      console.error('Initialization error:', error);
    } finally {
      setIsInitializing(false);
    }
  };

  return (
    <div className="min-h-screen py-6 px-4 md:py-8 md:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="card-clean p-6 md:p-8 mb-6 fade-in opacity-0 stagger-1">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
            <div>
              <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-2 tracking-tight">
                Stride
              </h1>
              <p className="text-gray-600">
                Compare sneaker prices and track market trends
              </p>
              <div className="mt-4 flex flex-wrap gap-2">
                <span className="badge badge-primary">90-Day History</span>
                <span className="badge badge-primary">Multi-Compare</span>
                <span className="badge badge-primary">Live Updates</span>
              </div>
            </div>
            <div className="flex flex-col sm:flex-row gap-3">
              {selectedSneakers.length > 0 && (
                <button onClick={clearSelection} className="btn-outline">
                  Clear Selection
                </button>
              )}
              <button
                onClick={handleInitialize}
                disabled={isInitializing}
                className="btn-primary"
              >
                {isInitializing ? 'Initializing...' : 'Initialize Data'}
              </button>
            </div>
          </div>
          {initMessage && (
            <div
              className={`mt-4 p-4 rounded-lg border ${
                initMessage.includes('success')
                  ? 'bg-green-50 border-green-200 text-green-800'
                  : 'bg-red-50 border-red-200 text-red-800'
              }`}
            >
              <p className="text-sm font-medium">{initMessage}</p>
            </div>
          )}
        </div>

        {/* Error State */}
        {sneakersError && (
          <div className="card-clean p-8 mb-6 fade-in opacity-0 stagger-2">
            <div className="text-center max-w-2xl mx-auto">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-red-100 rounded-full mb-4">
                <svg
                  className="h-8 w-8 text-red-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={2}
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                  />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Connection Error
              </h3>
              <p className="text-gray-600 mb-6">
                Unable to connect to the backend server
              </p>
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 text-left">
                <p className="text-sm font-semibold text-gray-700 mb-3">
                  Please make sure the following services are running:
                </p>
                <ul className="space-y-2 text-sm text-gray-600">
                  <li className="flex items-start gap-2">
                    <svg
                      className="w-5 h-5 text-gray-400 mt-0.5"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 5l7 7-7 7"
                      />
                    </svg>
                    PostgreSQL database (docker-compose up)
                  </li>
                  <li className="flex items-start gap-2">
                    <svg
                      className="w-5 h-5 text-gray-400 mt-0.5"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 5l7 7-7 7"
                      />
                    </svg>
                    Backend server (python -m app.main)
                  </li>
                  <li className="flex items-start gap-2">
                    <svg
                      className="w-5 h-5 text-gray-400 mt-0.5"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 5l7 7-7 7"
                      />
                    </svg>
                    Backend accessible at http://localhost:8000
                  </li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* Sneaker Selection */}
        <div className="card-clean p-6 mb-6 fade-in opacity-0 stagger-3">
          <SneakerSelect
            sneakers={sneakers}
            selectedSneakers={selectedSneakers}
            onChange={handleSelectionChange}
            isLoading={sneakersLoading}
          />
          {sneakersLoading && (
            <div className="flex items-center gap-2 mt-4">
              <div className="spinner h-4 w-4"></div>
              <p className="text-sm text-gray-500">Loading sneakers...</p>
            </div>
          )}
          {!sneakersLoading && sneakers.length === 0 && !sneakersError && (
            <div className="mt-4 p-3 bg-amber-50 border border-amber-200 rounded-lg">
              <p className="text-sm text-amber-800">
                No sneakers found. Click "Initialize Data" to populate the
                database.
              </p>
            </div>
          )}
        </div>

        {/* Price Chart */}
        <div className="fade-in opacity-0 stagger-4">
          <PriceChart data={chartData} isLoading={priceLoading} />
        </div>

        {/* Statistics Cards */}
        {selectedSneakerObjects.length > 0 && (
          <div className="fade-in opacity-0 stagger-5">
            <StatisticsCards
              sneakers={selectedSneakerObjects}
              priceHistory={priceHistory}
            />
          </div>
        )}

      </div>
    </div>
  );
}

export default App;
