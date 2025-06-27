import { ArrowTrendingUpIcon, ArrowTrendingDownIcon } from './icons.js';

// Note: In vanilla JS conversion, filtering state would be handled globally in App.js.
// This component becomes a pure template function, displaying all data passed to it.

const OrderBookTable = ({ title, data }) => {
  const formatCurrency = (amount) => {
    const numAmount = typeof amount === 'string' ? parseFloat(amount) : amount;
    if (isNaN(numAmount)) return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', minimumFractionDigits: 2 }).format(0);
    return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', minimumFractionDigits: 2 }).format(numAmount);
  };

  const formatTimestamp = (timestamp) => {
    if (!timestamp) return '-';
    const numTimestamp = parseFloat(timestamp) * 1000; 
    if (isNaN(numTimestamp) || numTimestamp === 0) return "-";
    try {
      return new Date(numTimestamp).toLocaleString('en-IN', { 
        year: '2-digit', month: 'short', day: 'numeric', 
        hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true 
      });
    } catch (e) {
      return "Invalid Date";
    }
  };

  const totals = {
    totalOrders: data.length,
    totalPnl: data.reduce((acc, item) => acc + parseFloat(item.total || '0'), 0)
  };

  return `
    <div class="bg-white dark:bg-dark-mode-card p-4 md:p-6 rounded-xl shadow-lg mt-8">
      <h2 class="text-xl font-semibold text-dark-text dark:text-dark-mode-text-primary mb-4">${title}</h2>
      
      <div class="mb-6 p-4 bg-gray-50 dark:bg-dark-mode-hover-bg rounded-lg shadow-sm">
        <div class="flex flex-col sm:flex-row justify-between items-center text-sm">
            <p class="text-medium-text dark:text-dark-mode-text-secondary mb-2 sm:mb-0">
              Displaying <span class="font-semibold text-dark-text dark:text-dark-mode-text-primary">${totals.totalOrders}</span> orders.
            </p>
            <div class="text-right">
              <span class="text-medium-text dark:text-dark-mode-text-secondary">Total P&amp;L: </span>
              <span class="font-semibold ${totals.totalPnl >= 0 ? 'text-secondary dark:text-green-400' : 'text-danger dark:text-red-400'}">
                ${formatCurrency(totals.totalPnl)}
              </span>
            </div>
        </div>
      </div>

      ${data.length === 0 ? `
        <p class="text-medium-text dark:text-dark-mode-text-secondary text-center py-8">No order book data available.</p>
      ` : `
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-dark-mode-border">
            <thead class="bg-gray-50 dark:bg-dark-mode-table-header">
              <tr>
                <th scope="col" class="px-3 py-3 text-left text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary uppercase tracking-wider">User ID</th>
                <th scope="col" class="px-3 py-3 text-left text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary uppercase tracking-wider">Entry Time</th>
                <th scope="col" class="px-3 py-3 text-left text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary uppercase tracking-wider">Exit Time</th>
                <th scope="col" class="px-3 py-3 text-left text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary uppercase tracking-wider">Script Name</th>
                <th scope="col" class="px-3 py-3 text-right text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary uppercase tracking-wider">Qty</th>
                <th scope="col" class="px-3 py-3 text-right text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary uppercase tracking-wider">Entry Price</th>
                <th scope="col" class="px-3 py-3 text-right text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary uppercase tracking-wider">Exit Price</th>
                <th scope="col" class="px-3 py-3 text-left text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary uppercase tracking-wider">Status</th>
                <th scope="col" class="px-3 py-3 text-right text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary uppercase tracking-wider">P&amp;L</th>
                <th scope="col" class="px-3 py-3 text-left text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary uppercase tracking-wider">Strategy</th>
                <th scope="col" class="px-3 py-3 text-left text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary uppercase tracking-wider">Index</th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-dark-mode-card divide-y divide-gray-200 dark:divide-dark-mode-border">
              ${data.map((item, index) => {
                const pnl = parseFloat(item.total);
                return `
                  <tr class="hover:bg-gray-50 dark:hover:bg-dark-mode-hover-bg transition-colors duration-150">
                    <td class="px-3 py-4 whitespace-nowrap text-xs text-medium-text dark:text-dark-mode-text-secondary truncate max-w-[100px] sm:max-w-xs" title="${item.user_id}">${item.user_id}</td>
                    <td class="px-3 py-4 whitespace-nowrap text-xs text-medium-text dark:text-dark-mode-text-secondary">${formatTimestamp(item.entry_time)}</td>
                    <td class="px-3 py-4 whitespace-nowrap text-xs text-medium-text dark:text-dark-mode-text-secondary">${formatTimestamp(item.exit_time)}</td>
                    <td class="px-3 py-4 whitespace-nowrap text-xs font-medium text-dark-text dark:text-dark-mode-text-primary">${item.script_name}</td>
                    <td class="px-3 py-4 whitespace-nowrap text-xs text-medium-text dark:text-dark-mode-text-secondary text-right">${item.qty}</td>
                    <td class="px-3 py-4 whitespace-nowrap text-xs text-medium-text dark:text-dark-mode-text-secondary text-right">${formatCurrency(item.entry_price)}</td>
                    <td class="px-3 py-4 whitespace-nowrap text-xs text-medium-text dark:text-dark-mode-text-secondary text-right">${formatCurrency(item.exit_price)}</td>
                    <td class="px-3 py-4 whitespace-nowrap text-xs">
                      <span class="px-2 inline-flex text-[0.7rem] leading-5 font-semibold rounded-full 
                        ${item.status?.toLowerCase().includes('exited') ? 'bg-green-100 text-green-800 dark:bg-green-700 dark:text-green-100' : 
                          item.status?.toLowerCase().includes('open') || item.status?.toLowerCase().includes('pending') ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-700 dark:text-yellow-100' :
                          item.status?.toLowerCase().includes('cancelled') || item.status?.toLowerCase().includes('rejected') ? 'bg-red-100 text-red-800 dark:bg-red-700 dark:text-red-100' :
                          'bg-gray-100 text-gray-800 dark:bg-gray-600 dark:text-gray-100'}">
                        ${item.status || 'N/A'}
                      </span>
                    </td>
                    <td class="px-3 py-4 whitespace-nowrap text-xs font-semibold text-right ${pnl >= 0 ? 'text-secondary dark:text-green-400' : 'text-danger dark:text-red-400'}">
                      <div class="flex items-center justify-end">
                        ${pnl !== 0 ? (pnl >= 0 ? ArrowTrendingUpIcon({ className: "h-4 w-4 mr-1" }) : ArrowTrendingDownIcon({ className: "h-4 w-4 mr-1" })) : ''}
                        ${formatCurrency(pnl)}
                      </div>
                    </td>
                    <td class="px-3 py-4 whitespace-nowrap text-xs text-medium-text dark:text-dark-mode-text-secondary">${item.strategy || 'N/A'}</td>
                    <td class="px-3 py-4 whitespace-nowrap text-xs text-medium-text dark:text-dark-mode-text-secondary">${item.index_name || 'N/A'}</td>
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

export default OrderBookTable;