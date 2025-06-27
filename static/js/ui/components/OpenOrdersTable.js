import { ArrowTrendingUpIcon, ArrowTrendingDownIcon, ArrowUpCircleIcon, ArrowDownCircleIcon } from './icons.js';

const OpenOrdersTable = ({ title, data }) => {
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', minimumFractionDigits: 2 }).format(amount);
  };

  const calculatePnl = (item) => {
    if (item.type === 'BUY') {
      return (item.current_price - item.entry_price) * item.quantity;
    } else { // SELL
      return (item.entry_price - item.current_price) * item.quantity;
    }
  };

  return `
    <div class="bg-white dark:bg-dark-mode-card p-6 rounded-xl shadow-lg">
      <h2 class="text-xl font-semibold text-dark-text dark:text-dark-mode-text-primary mb-6">${title}</h2>
      ${data.length === 0 ? `
        <p class="text-medium-text dark:text-dark-mode-text-secondary text-center py-4">No open orders at the moment.</p>
      ` : `
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-dark-mode-border">
            <thead class="bg-gray-50 dark:bg-dark-mode-table-header">
              <tr>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary uppercase tracking-wider">Strategy</th>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary uppercase tracking-wider">Symbol</th>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary uppercase tracking-wider">Type</th>
                <th scope="col" class="px-4 py-3 text-right text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary uppercase tracking-wider">Qty</th>
                <th scope="col" class="px-4 py-3 text-right text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary uppercase tracking-wider">Entry Price</th>
                <th scope="col" class="px-4 py-3 text-right text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary uppercase tracking-wider">Current Price</th>
                <th scope="col" class="px-4 py-3 text-right text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary uppercase tracking-wider">P&amp;L</th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-dark-mode-card divide-y divide-gray-200 dark:divide-dark-mode-border">
              ${data.map((item) => {
                const pnl = calculatePnl(item);
                return `
                  <tr class="hover:bg-gray-50 dark:hover:bg-dark-mode-hover-bg transition-colors duration-150">
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-dark-text dark:text-dark-mode-text-primary">${item.strategy}</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-medium-text dark:text-dark-mode-text-secondary">${item.symbol}</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm">
                      <div class="flex items-center ${item.type === 'BUY' ? 'text-secondary dark:text-green-400' : 'text-danger dark:text-red-400'}">
                        ${item.type === 'BUY' ? 
                          ArrowUpCircleIcon({ className: "h-5 w-5 mr-1" }) : 
                          ArrowDownCircleIcon({ className: "h-5 w-5 mr-1" })}
                        ${item.type}
                      </div>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-medium-text dark:text-dark-mode-text-secondary text-right">${item.quantity}</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-medium-text dark:text-dark-mode-text-secondary text-right">${formatCurrency(item.entry_price)}</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-medium-text dark:text-dark-mode-text-secondary text-right">${formatCurrency(item.current_price)}</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-semibold text-right ${pnl >= 0 ? 'text-secondary dark:text-green-400' : 'text-danger dark:text-red-400'}">
                      <div class="flex items-center justify-end">
                        ${pnl >= 0 ? 
                          ArrowTrendingUpIcon({ className: "h-4 w-4 mr-1" }) : 
                          ArrowTrendingDownIcon({ className: "h-4 w-4 mr-1" })}
                        ${formatCurrency(pnl)}
                      </div>
                    </td>
                  </tr>
                `;
              }).join('')}
            </tbody>
          </table>
        </div>
      `}
    </div>
  `;
};

export default OpenOrdersTable;