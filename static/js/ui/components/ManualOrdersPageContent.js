import { PencilSquareIcon, ClipboardIcon } from './icons.js';

const ManualOrdersPageContent = ({ orders = [], webhookToken, strategyName }) => {

  const getWebhookDetails = () => {
      if (webhookToken && orders.length > 0) {
        return orders.map(order => ({
          id: `wd-${order.id}`,
          indexName: order.index_name,
          buyUrl: `/trigger_buy?token=${webhookToken}`,
          sellUrl: `/trigger_sell?token=${webhookToken}`,
          exitUrl: `/trigger_exit?token=${webhookToken}`,
          inputData: JSON.stringify({token: webhookToken, instrument: order.index_name, action: "buy/sell/exit", strike: order.strike, lots: order.lots}, null, 2)
        }));
      }
      return [];
  };

  const webhookDetails = getWebhookDetails();

  return `
    <div class="space-y-6 mt-2">
      <div class="flex items-center justify-between mb-0">
         <h1 class="text-xl lg:text-2xl font-bold text-surface-50 flex items-center gap-3">
            ${PencilSquareIcon({ className: "h-6 w-6 text-primary-400" })}
            Manual Orders
        </h1>
      </div>

      <div class="card p-4 lg:p-5">
        <label for="strategy-name-input" class="block text-sm font-medium text-surface-50 mb-1">
          Strategy Name
        </label>
        <input
          type="text"
          id="strategy-name-input"
          value="${strategyName || 'DefaultStrategy'}"
          class="mt-1 block w-full md:w-1/3 px-3 py-2 bg-surface-800 border border-surface-700 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-primary-400 sm:text-sm text-surface-50 placeholder-surface-500"
          aria-label="Strategy Name"
        />
      </div>

      <div class="card p-4 lg:p-5">
        <div class="overflow-x-auto -mx-4 lg:-mx-5">
          <table class="w-full text-sm">
            <thead>
              <tr class="text-surface-400 text-xs uppercase tracking-wider border-b border-surface-700">
                <th scope="col" class="text-left py-3 px-4 lg:px-5 font-medium">Actions</th>
                <th scope="col" class="text-left py-3 px-4 lg:px-5 font-medium">Index Name</th>
                <th scope="col" class="text-right py-3 px-4 lg:px-5 font-medium">Lots</th>
                <th scope="col" class="text-right py-3 px-4 lg:px-5 font-medium">Trigger</th>
                <th scope="col" class="text-right py-3 px-4 lg:px-5 font-medium">Stop Loss</th>
                <th scope="col" class="text-right py-3 px-4 lg:px-5 font-medium">Target</th>
                <th scope="col" class="text-right py-3 px-4 lg:px-5 font-medium">Strike</th>
                <th scope="col" class="text-left py-3 px-4 lg:px-5 font-medium">Current Order Status</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-surface-700/50">
              ${orders.map((order) => `
                <tr class="hover:bg-surface-700/30">
                  <td class="py-3 px-4 lg:px-5">
                    <div class="flex gap-1.5">
                      <button data-index="${order.index_name}" data-action="buy" class="manual-order-btn bg-emerald-500 hover:bg-emerald-600 text-surface-50 text-xs py-1 px-2.5 rounded shadow-sm hover:shadow-md transition-all duration-150">Buy</button>
                      <button data-index="${order.index_name}" data-action="sell" class="manual-order-btn bg-red-500 hover:bg-red-600 text-surface-50 text-xs py-1 px-2.5 rounded shadow-sm hover:shadow-md transition-all duration-150">Sell</button>
                      <button data-index="${order.index_name}" data-action="exit" class="manual-order-btn bg-amber-500 hover:bg-amber-600 text-surface-50 text-xs py-1 px-2.5 rounded shadow-sm hover:shadow-md transition-all duration-150">Exit</button>
                    </div>
                  </td>
                  <td class="py-3 px-4 lg:px-5 text-surface-50">${order.index_name}</td>
                  <td class="py-3 px-4 lg:px-5 text-surface-400 text-right">${order.lots}</td>
                  <td class="py-3 px-4 lg:px-5 text-surface-400 text-right">${order.trigger}</td>
                  <td class="py-3 px-4 lg:px-5 text-surface-400 text-right">${order.stop_loss}</td>
                  <td class="py-3 px-4 lg:px-5 text-surface-400 text-right">${order.target}</td>
                  <td class="py-3 px-4 lg:px-5 text-surface-400 text-right">${order.strike}</td>
                  <td class="py-3 px-4 lg:px-5 text-surface-400">${order.order_status || 'N/A'}</td>
                </tr>
              `).join('')}
              ${orders.length === 0 ? `
                <tr><td colspan="8" class="py-8 text-center text-sm text-surface-400">No manual orders configured.</td></tr>
              ` : ''}
            </tbody>
          </table>
        </div>
      </div>

      <div class="card p-4 lg:p-5">
        <h2 class="text-sm font-semibold text-surface-50 mb-4">Webhook Details</h2>
        <div class="flex flex-col sm:flex-row items-center gap-3 mb-6">
          <button id="regenerate-token-button" class="w-full sm:w-auto px-4 py-2 text-sm font-medium text-surface-50 bg-surface-800 border border-surface-700 rounded-md shadow-sm hover:bg-surface-700 focus:outline-none focus:ring-2 focus:ring-primary-400 transition-colors whitespace-nowrap">
            Regenerate Token
          </button>
          <div class="flex-grow w-full flex items-center gap-2">
            <input id="webhook-token-input" type="text" value="${webhookToken || ''}" readonly class="flex-grow w-full p-2 text-sm text-surface-50 bg-surface-800 border border-surface-700 rounded-md focus:outline-none focus:ring-1 focus:ring-primary-400 font-mono" aria-label="Webhook Token" />
            <button id="copy-token-btn" class="p-2 rounded-lg hover:bg-surface-700 text-surface-400 hover:text-surface-50 transition-colors" title="Copy token">
              ${ClipboardIcon({ className: 'h-4 w-4' })}
            </button>
          </div>
        </div>

        <div class="overflow-x-auto -mx-4 lg:-mx-5">
          <table class="w-full text-sm">
            <thead>
              <tr class="text-surface-400 text-xs uppercase tracking-wider border-b border-surface-700">
                <th class="text-left py-3 px-4 lg:px-5 font-medium">Index Name</th>
                <th class="text-left py-3 px-4 lg:px-5 font-medium">Buy URL</th>
                <th class="text-left py-3 px-4 lg:px-5 font-medium">Sell URL</th>
                <th class="text-left py-3 px-4 lg:px-5 font-medium">Exit URL</th>
                <th class="text-left py-3 px-4 lg:px-5 font-medium">Input Data</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-surface-700/50">
              ${webhookDetails.map((detail) => `
                <tr class="hover:bg-surface-700/30">
                  <td class="py-3 px-4 lg:px-5 text-surface-50">${detail.indexName}</td>
                  <td class="py-3 px-4 lg:px-5">
                    <div class="flex items-center gap-1">
                      <code class="text-surface-400 text-xs break-all flex-1 copy-content cursor-pointer hover:text-surface-50 transition-colors" title="Click to copy">${detail.buyUrl}</code>
                      <button class="copy-btn flex-shrink-0 p-1 rounded hover:bg-surface-700 text-surface-500 hover:text-surface-50 transition-colors" title="Copy URL">${ClipboardIcon({ className: 'h-3.5 w-3.5' })}</button>
                    </div>
                  </td>
                  <td class="py-3 px-4 lg:px-5">
                    <div class="flex items-center gap-1">
                      <code class="text-surface-400 text-xs break-all flex-1 copy-content cursor-pointer hover:text-surface-50 transition-colors" title="Click to copy">${detail.sellUrl}</code>
                      <button class="copy-btn flex-shrink-0 p-1 rounded hover:bg-surface-700 text-surface-500 hover:text-surface-50 transition-colors" title="Copy URL">${ClipboardIcon({ className: 'h-3.5 w-3.5' })}</button>
                    </div>
                  </td>
                  <td class="py-3 px-4 lg:px-5">
                    <div class="flex items-center gap-1">
                      <code class="text-surface-400 text-xs break-all flex-1 copy-content cursor-pointer hover:text-surface-50 transition-colors" title="Click to copy">${detail.exitUrl}</code>
                      <button class="copy-btn flex-shrink-0 p-1 rounded hover:bg-surface-700 text-surface-500 hover:text-surface-50 transition-colors" title="Copy URL">${ClipboardIcon({ className: 'h-3.5 w-3.5' })}</button>
                    </div>
                  </td>
                  <td class="py-3 px-4 lg:px-5 text-surface-400 text-xs max-w-xs">
                    <pre class="whitespace-pre-wrap text-xs bg-surface-800 p-2 rounded copy-content cursor-pointer hover:text-surface-50 transition-colors" title="Click to copy">${detail.inputData}</pre>
                  </td>
                </tr>
              `).join('')}
              ${webhookDetails.length === 0 ? `
                <tr><td colspan="5" class="py-8 text-center text-sm text-surface-400">No webhook details to display. Configure orders above or regenerate token.</td></tr>
              ` : ''}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `;
};

export default ManualOrdersPageContent;
