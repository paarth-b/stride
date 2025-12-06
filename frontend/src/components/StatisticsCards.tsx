/**
 * Statistics cards component showing key metrics
 * Displays price changes, min/max, and comparisons
 */
import type { Sneaker, PricePoint } from '../utils/types';
import { calculateStats, formatPrice } from '../utils/helpers';
import { StarRating } from './StarRating';

interface StatisticsCardsProps {
  sneakers: Sneaker[];
  priceHistory: PricePoint[];
}

export function StatisticsCards({
  sneakers,
  priceHistory,
}: StatisticsCardsProps) {
  if (sneakers.length === 0) {
    return null;
  }

  const stats = sneakers.map((sneaker) =>
    calculateStats(sneaker, priceHistory)
  );

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-6">
      {stats.map((stat) => (
        <div key={stat.sneaker_id} className="card-glass p-6">
          <h4 className="text-sm font-semibold text-gray-700 mb-3 truncate">
            {stat.name}
          </h4>

          <div className="space-y-3">
            {/* Current vs Retail Price */}
            <div>
              <div className="flex justify-between items-baseline">
                <span className="text-xs text-gray-600">Current Price</span>
                <span className="text-lg font-bold text-gray-900">
                  {formatPrice(stat.current_price)}
                </span>
              </div>
              <div className="flex justify-between items-baseline mt-1">
                <span className="text-xs text-gray-600">Retail Price</span>
                <span className="text-sm text-gray-700">
                  {formatPrice(stat.retail_price)}
                </span>
              </div>
            </div>

            {/* Price Change */}
            <div className="pt-3 border-t border-gray-200">
              <div className="flex justify-between items-baseline">
                <span className="text-xs text-gray-600">Price Change</span>
                <span
                  className={`text-sm font-semibold ${
                    stat.price_change >= 0 ? 'text-green-600' : 'text-red-600'
                  }`}
                >
                  {stat.price_change >= 0 ? '+' : ''}
                  {formatPrice(stat.price_change)} (
                  {stat.price_change_percent >= 0 ? '+' : ''}
                  {stat.price_change_percent.toFixed(1)}%)
                </span>
              </div>
            </div>

            {/* Min/Max/Avg */}
            <div className="pt-3 border-t border-gray-200 space-y-1">
              <div className="flex justify-between text-xs">
                <span className="text-gray-600">Min Price</span>
                <span className="text-gray-900 font-medium">
                  {formatPrice(stat.min_price)}
                </span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-gray-600">Max Price</span>
                <span className="text-gray-900 font-medium">
                  {formatPrice(stat.max_price)}
                </span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-gray-600">Avg Price</span>
                <span className="text-gray-900 font-medium">
                  {formatPrice(stat.avg_price)}
                </span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-gray-600">Release Date</span>
                <span className="text-gray-900 font-medium">
                  {stat.release_date}
                </span>
              </div>
              <div className="flex justify-between text-xs items-center">
                <span className="text-gray-600">Available Sizes</span>
                <span className="text-gray-900 font-medium text-right">
                  {stat.available_sizes}
                </span>
              </div>
              <div className="flex justify-between text-xs items-center">
                <span className="text-gray-600">Rating</span>
                <div className="flex items-center gap-1">
                  <StarRating rating={stat.ratings} size="sm" showValue />
                </div>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
