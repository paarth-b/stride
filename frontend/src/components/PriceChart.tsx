/**
 * Interactive price chart component using Recharts
 * Displays multi-line chart for price comparison
 */
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { format } from 'date-fns';
import type { ChartData } from '../utils/types';
import { getChartColor, formatPrice } from '../utils/helpers';

interface PriceChartProps {
  data: ChartData[];
  isLoading?: boolean;
}

export function PriceChart({ data, isLoading = false }: PriceChartProps) {
  if (isLoading) {
    return (
      <div className="card-clean p-8 flex items-center justify-center h-[450px] mb-6">
        <div className="text-center">
          <div className="spinner h-12 w-12 mx-auto mb-4"></div>
          <p className="text-sm text-gray-600">Loading price data...</p>
        </div>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="card-clean p-12 flex items-center justify-center h-[450px] mb-6">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gray-100 rounded-full mb-4">
            <svg
              className="h-10 w-10 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={1.5}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
              />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-1">
            No Data Available
          </h3>
          <p className="text-sm text-gray-600">
            Select sneakers above to view their price history
          </p>
        </div>
      </div>
    );
  }

  // Get all keys except timestamp
  const dataKeys = Object.keys(data[0] || {}).filter(
    (key) => key !== 'timestamp'
  );


  return (
    <div className="card-clean p-6 mb-6">
      <div className="flex items-baseline justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-900">Price History</h3>
        <span className="text-xs text-gray-500 font-medium">90-Day Trend</span>
      </div>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart
          data={data}
          margin={{ top: 5, right: 30, left: 0, bottom: 5 }}
        >
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="#e5e7eb"
            strokeOpacity={0.6}
          />
          <XAxis
            dataKey="timestamp"
            tickFormatter={(timestamp) => format(new Date(timestamp), 'MMM dd')}
            stroke="#9ca3af"
            tick={{ fill: '#6b7280', fontSize: 12 }}
            axisLine={{ stroke: '#e5e7eb' }}
          />
          <YAxis
            domain={['auto', 'auto']}
            tickFormatter={(value) => `$${value}`}
            stroke="#9ca3af"
            tick={{ fill: '#6b7280', fontSize: 12 }}
            axisLine={{ stroke: '#e5e7eb' }}
          />
          <Tooltip
            formatter={(value: number) => formatPrice(value)}
            labelFormatter={(timestamp) =>
              format(new Date(timestamp), 'MMM dd, yyyy')
            }
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '0.5rem',
              padding: '12px',
              fontSize: '13px',
              boxShadow: '0 10px 25px rgba(0, 0, 0, 0.1)',
            }}
            labelStyle={{
              color: '#1f2937',
              fontWeight: 600,
              marginBottom: '8px',
            }}
            itemStyle={{
              color: '#6b7280',
              padding: '2px 0',
            }}
          />
          <Legend
            wrapperStyle={{
              fontSize: '13px',
              paddingTop: '20px',
            }}
            iconType="line"
          />
          {dataKeys.map((key, index) => (
            <Line
              key={key}
              type="monotone"
              dataKey={key}
              stroke={getChartColor(index)}
              strokeWidth={2.5}
              dot={false}
              activeDot={{
                r: 5,
                fill: getChartColor(index),
                stroke: 'white',
                strokeWidth: 2,
              }}
              animationDuration={600}
              animationEasing="ease-out"
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
