import { ArrowTrendingUpIcon, ArrowTrendingDownIcon, ArrowUpCircleIcon, ArrowDownCircleIcon } from './icons.js';

const OpenOrdersTable = ({ title, data }) => {
  const formatCurrency = (amount) =>
    new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', minimumFractionDigits: 2 }).format(amount);

  const calculatePnl = (item) =>
    item.type === 'BUY'
      ? (item.current_price - item.entry_price) * item.quantity
      : (item.entry_price - item.current_price) * item.quantity;

  return `
    <div class="card p-4 lg:p-5">
      <h2 class="text-sm font-semibold text-surface-50 mb-4">${title}</h2>
      ${!data?.length ? `
        <p class="text-sm text-surface-400 text-center py-6">No open orders at the moment.</p>
      ` : `
        <div class="overflow-x-auto -mx-4 lg:-mx-5">
          <table class="w-full text-sm">
            <thead>
              <tr class="text-surface-400 text-xs uppercase tracking-wider border-b border-surface-700">
                <th class="text-left py-3 px-4 lg:px-5 font-medium">Strategy</th>
                <th class="text-left py-3 px-4 lg:px-5 font-medium">Symbol</th>
                <th class="text-left py-3 px-4 lg:px-5 font-medium">Type</th>
                <th class="text-right py-3 px-4 lg:px-5 font-medium">Qty</th>
                <th class="text-right py-3 px-4 lg:px-5 font-medium">Entry</th>
                <th class="text-right py-3 px-4 lg:px-5 font-medium">Current</th>
                <th class="text-right py-3 px-4 lg:px-5 font-medium">P&amp;L</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-surface-700/50">
              ${data.map((item) => {
                const pnl = calculatePnl(item);
                return `
                  <tr class="hover:bg-surface-700/30 transition-colors">
                    <td class="py-3 px-4 lg:px-5 text-surface-50">${item.strategy}</td>
                    <td class="py-3 px-4 lg:px-5 text-surface-400">${item.symbol}</td>
                    <td class="py-3 px-4 lg:px-5">
                      <span class="inline-flex items-center gap-1 ${item.type === 'BUY' ? 'text-emerald-400' : 'text-red-400'}">
                        ${item.type === 'BUY' ? ArrowUpCircleIcon({ className: "h-4 w-4" }) : ArrowDownCircleIcon({ className: "h-4 w-4" })}
                        ${item.type}
                      </span>
                    </td>
                    <td class="py-3 px-4 lg:px-5 text-surface-400 text-right">${item.quantity}</td>
                    <td class="py-3 px-4 lg:px-5 text-surface-400 text-right">${formatCurrency(item.entry_price)}</td>
                    <td class="py-3 px-4 lg:px-5 text-surface-400 text-right">${formatCurrency(item.current_price)}</td>
                    <td class="py-3 px-4 lg:px-5 text-right font-semibold ${pnl >= 0 ? 'text-emerald-400' : 'text-red-400'}">
                      <div class="flex items-center justify-end gap-1">
                        ${pnl >= 0 ? ArrowTrendingUpIcon({ className: "h-3.5 w-3.5" }) : ArrowTrendingDownIcon({ className: "h-3.5 w-3.5" })}
                        ${formatCurrency(pnl)}
                      </div>
                    </td>
                  </tr>`;
              }).join('')}
            </tbody>
          </table>
        </div>`}
    </div>`;
};

export default OpenOrdersTable;
