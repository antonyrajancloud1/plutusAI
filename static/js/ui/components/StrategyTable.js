import { ArrowTrendingUpIcon, ArrowTrendingDownIcon } from './icons.js';

const StrategyTable = ({ title, data }) => {
  const formatCurrency = (amount) =>
    new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', minimumFractionDigits: 2 }).format(amount);

  return `
    <div class="card p-4 lg:p-5">
      <h2 class="text-sm font-semibold text-surface-50 mb-4">${title}</h2>
      ${!data?.length ? `
        <p class="text-sm text-surface-400 text-center py-6">No data available for this period.</p>
      ` : `
        <div class="overflow-x-auto -mx-4 lg:-mx-5">
          <table class="w-full text-sm">
            <thead>
              <tr class="text-surface-400 text-xs uppercase tracking-wider border-b border-surface-700">
                <th class="text-left py-3 px-4 lg:px-5 font-medium">Strategy</th>
                <th class="text-left py-3 px-4 lg:px-5 font-medium">Index</th>
                <th class="text-center py-3 px-4 lg:px-5 font-medium">Orders</th>
                <th class="text-right py-3 px-4 lg:px-5 font-medium">P&L</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-surface-700/50">
              ${data.map((item) => `
                <tr class="hover:bg-surface-700/30 transition-colors">
                  <td class="py-3 px-4 lg:px-5 text-surface-50 font-medium">${item.strategy}</td>
                  <td class="py-3 px-4 lg:px-5 text-surface-400">${item.index_name}</td>
                  <td class="py-3 px-4 lg:px-5 text-surface-400 text-center">${item.order_count}</td>
                  <td class="py-3 px-4 lg:px-5 text-right font-semibold ${item.total_profit >= 0 ? 'text-emerald-400' : 'text-red-400'}">
                    <div class="flex items-center justify-end gap-1">
                      ${item.total_profit >= 0
                        ? ArrowTrendingUpIcon({ className: "h-3.5 w-3.5" })
                        : ArrowTrendingDownIcon({ className: "h-3.5 w-3.5" })}
                      ${formatCurrency(item.total_profit)}
                    </div>
                  </td>
                </tr>`).join('')}
            </tbody>
          </table>
        </div>`}
    </div>`;
};

export default StrategyTable;
