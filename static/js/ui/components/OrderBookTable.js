import { ArrowTrendingUpIcon, ArrowTrendingDownIcon } from './icons.js';

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

  const statusBadge = (status) => {
    const s = (status || '').toLowerCase();
    if (s.includes('exited')) return 'bg-emerald-500/10 text-emerald-400';
    if (s.includes('open') || s.includes('pending')) return 'bg-amber-500/10 text-amber-400';
    if (s.includes('cancelled') || s.includes('rejected')) return 'bg-red-500/10 text-red-400';
    return 'bg-surface-500/10 text-surface-400';
  };

  return `
    <div class="card p-4 lg:p-5 mt-6">
      <h2 class="text-sm font-semibold text-surface-50 mb-4">${title}</h2>

      <div class="mb-4 p-3 bg-surface-800/50 rounded-lg">
        <div class="flex flex-col sm:flex-row justify-between items-center text-sm">
            <p class="text-surface-400 mb-2 sm:mb-0">
              Displaying <span class="font-semibold text-surface-50">${totals.totalOrders}</span> orders.
            </p>
            <div class="text-right">
              <span class="text-surface-400">Total P&amp;L: </span>
              <span class="font-semibold ${totals.totalPnl >= 0 ? 'text-emerald-400' : 'text-red-400'}">
                ${formatCurrency(totals.totalPnl)}
              </span>
            </div>
        </div>
      </div>

      ${data.length === 0 ? `
        <p class="text-surface-400 text-center py-8">No order book data available.</p>
      ` : `
        <div class="overflow-x-auto -mx-4 lg:-mx-5">
          <table class="w-full text-sm">
            <thead>
              <tr class="text-surface-400 text-xs uppercase tracking-wider border-b border-surface-700">
                <th class="text-left py-3 px-4 lg:px-5 font-medium">User ID</th>
                <th class="text-left py-3 px-4 lg:px-5 font-medium">Entry Time</th>
                <th class="text-left py-3 px-4 lg:px-5 font-medium">Exit Time</th>
                <th class="text-left py-3 px-4 lg:px-5 font-medium">Script Name</th>
                <th class="text-right py-3 px-4 lg:px-5 font-medium">Qty</th>
                <th class="text-right py-3 px-4 lg:px-5 font-medium">Entry Price</th>
                <th class="text-right py-3 px-4 lg:px-5 font-medium">Exit Price</th>
                <th class="text-left py-3 px-4 lg:px-5 font-medium">Status</th>
                <th class="text-right py-3 px-4 lg:px-5 font-medium">P&amp;L</th>
                <th class="text-left py-3 px-4 lg:px-5 font-medium">Strategy</th>
                <th class="text-left py-3 px-4 lg:px-5 font-medium">Index</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-surface-700/50">
              ${data.map((item) => {
                const pnl = parseFloat(item.total);
                return `
                  <tr class="hover:bg-surface-700/30 transition-colors duration-150">
                    <td class="py-3 px-4 lg:px-5 text-surface-400 text-xs truncate max-w-[100px] sm:max-w-xs" title="${item.user_id}">${item.user_id}</td>
                    <td class="py-3 px-4 lg:px-5 text-surface-400 text-xs whitespace-nowrap">${formatTimestamp(item.entry_time)}</td>
                    <td class="py-3 px-4 lg:px-5 text-surface-400 text-xs whitespace-nowrap">${formatTimestamp(item.exit_time)}</td>
                    <td class="py-3 px-4 lg:px-5 text-surface-50 text-xs font-medium">${item.script_name}</td>
                    <td class="py-3 px-4 lg:px-5 text-surface-400 text-xs text-right">${item.qty}</td>
                    <td class="py-3 px-4 lg:px-5 text-surface-400 text-xs text-right">${formatCurrency(item.entry_price)}</td>
                    <td class="py-3 px-4 lg:px-5 text-surface-400 text-xs text-right">${formatCurrency(item.exit_price)}</td>
                    <td class="py-3 px-4 lg:px-5 text-xs">
                      <span class="px-2 py-0.5 text-[0.7rem] font-semibold rounded-full ${statusBadge(item.status)}">
                        ${item.status || 'N/A'}
                      </span>
                    </td>
                    <td class="py-3 px-4 lg:px-5 text-xs font-semibold text-right ${pnl >= 0 ? 'text-emerald-400' : 'text-red-400'}">
                      <div class="flex items-center justify-end gap-1">
                        ${pnl !== 0 ? (pnl >= 0 ? ArrowTrendingUpIcon({ className: "h-3.5 w-3.5" }) : ArrowTrendingDownIcon({ className: "h-3.5 w-3.5" })) : ''}
                        ${formatCurrency(pnl)}
                      </div>
                    </td>
                    <td class="py-3 px-4 lg:px-5 text-surface-400 text-xs">${item.strategy || 'N/A'}</td>
                    <td class="py-3 px-4 lg:px-5 text-surface-400 text-xs">${item.index_name || 'N/A'}</td>
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
