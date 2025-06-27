import { ArrowTrendingUpIcon, ArrowTrendingDownIcon } from './icons.js';

const StrategyTable = ({ title, data }) => {
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', minimumFractionDigits: 2 }).format(amount);
  };

  return `
    <div class="bg-white dark:bg-dark-mode-card p-6 rounded-xl shadow-lg">
      <h2 class="text-xl font-semibold text-dark-text dark:text-dark-mode-text-primary mb-6">${title}</h2>
      ${data.length === 0 ? `
        <p class="text-medium-text dark:text-dark-mode-text-secondary text-center py-4">No data available for this period.</p>
      ` : `
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-dark-mode-border">
            <thead class="bg-gray-50 dark:bg-dark-mode-table-header">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary uppercase tracking-wider">Strategy</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary uppercase tracking-wider">Index</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary uppercase tracking-wider">Orders</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary uppercase tracking-wider">Total Profit</th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-dark-mode-card divide-y divide-gray-200 dark:divide-dark-mode-border">
              ${data.map((item) => `
                <tr class="hover:bg-gray-50 dark:hover:bg-dark-mode-hover-bg transition-colors duration-150">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-dark-text dark:text-dark-mode-text-primary">${item.strategy}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-medium-text dark:text-dark-mode-text-secondary">${item.index_name}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-medium-text dark:text-dark-mode-text-secondary text-center">${item.order_count}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold ${item.total_profit >= 0 ? 'text-secondary dark:text-green-400' : 'text-danger dark:text-red-400'}">
                    <div class="flex items-center">
                      ${item.total_profit >= 0 ? 
                        ArrowTrendingUpIcon({ className: "h-4 w-4 mr-1" }) : 
                        ArrowTrendingDownIcon({ className: "h-4 w-4 mr-1" })}
                      ${formatCurrency(item.total_profit)}
                    </div>
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      `}
    </div>
  `;
};

export default StrategyTable;