import { PencilSquareIcon } from './icons.js'; 

const ManualOrdersPageContent = ({ orders = [], webhookToken, strategyName }) => {

  const getWebhookDetails = () => {
      if (webhookToken && orders.length > 0) {
        return orders.map(order => ({
          id: `wd-${order.id}`,
          indexName: order.index_name,
          buyUrl: `https://your-api-domain.com/webhook/${webhookToken}/${order.index_name.toLowerCase().replace(/\s+/g, '-')}/buy`,
          sellUrl: `https://your-api-domain.com/webhook/${webhookToken}/${order.index_name.toLowerCase().replace(/\s+/g, '-')}/sell`,
          exitUrl: `https://your-api-domain.com/webhook/${webhookToken}/${order.index_name.toLowerCase().replace(/\s+/g, '-')}/exit`,
          inputData: JSON.stringify({token: webhookToken, instrument: order.index_name, action: "buy/sell/exit", strike: order.strike, lots: order.lots}, null, 2)
        }));
      }
      return [];
  };

  const webhookDetails = getWebhookDetails();

  const lightSectionClass = "bg-white dark:bg-dark-mode-card shadow-xl rounded-lg p-6";
  const tableHeaderClass = "px-4 py-3 text-left text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary uppercase tracking-wider bg-gray-50 dark:bg-dark-mode-table-header";
  const tableCellClass = "px-4 py-3 whitespace-nowrap text-sm text-dark-text dark:text-dark-mode-text-primary";
  const tableNumericCellClass = tableCellClass + " text-right";
  const urlCellClass = "px-4 py-3 text-dark-text dark:text-dark-mode-text-primary text-xs break-all max-w-xs";
  const inputDataTdCellClass = "px-4 py-3 text-dark-text dark:text-dark-mode-text-primary text-xs max-w-xs";

  return `
    <div class="space-y-8 mt-2">
      <div class="flex items-center justify-between mb-0">
         <h1 class="text-3xl font-bold text-dark-text dark:text-dark-mode-text-primary flex items-center">
            ${PencilSquareIcon({ className: "h-8 w-8 mr-3 text-primary dark:text-dark-mode-primary-accent" })}
            Manual Orders
        </h1>
      </div>

      <div class="p-6 bg-white dark:bg-dark-mode-card shadow-lg rounded-lg">
        <label for="strategy-name-input" class="block text-sm font-medium text-black dark:text-dark-mode-text-primary mb-1">
          Strategy Name
        </label>
        <input
          type="text"
          id="strategy-name-input"
          value="DefaultStrategy"
          class="mt-1 block w-full md:w-1/3 px-3 py-2 bg-white dark:bg-dark-mode-input-bg border border-gray-300 dark:border-dark-mode-input-border rounded-md shadow-sm focus:outline-none focus:ring-primary dark:focus:ring-dark-mode-primary-accent focus:border-primary dark:focus:border-dark-mode-primary-accent sm:text-sm text-black dark:text-dark-mode-text-primary"
          aria-label="Strategy Name"
        />
      </div>

      <div class="${lightSectionClass}">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-dark-mode-border">
            <thead>
              <tr>
                <th scope="col" class="${tableHeaderClass}">Actions</th>
                <th scope="col" class="${tableHeaderClass}">Index Name</th>
                <th scope="col" class="${tableHeaderClass} text-right">Lots</th>
                <th scope="col" class="${tableHeaderClass} text-right">Trigger</th>
                <th scope="col" class="${tableHeaderClass} text-right">Stop Loss</th>
                <th scope="col" class="${tableHeaderClass} text-right">Target</th>
                <th scope="col" class="${tableHeaderClass} text-right">Strike</th>
                <th scope="col" class="${tableHeaderClass}">Current Order Status</th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-dark-mode-card divide-y divide-gray-200 dark:divide-dark-mode-border">
              ${orders.map((order) => `
                <tr class="hover:bg-gray-50 dark:hover:bg-dark-mode-hover-bg">
                  <td class="${tableCellClass}">
                    <div class="flex space-x-1">
                      <button class="bg-green-500 hover:bg-green-600 text-white text-xs py-1 px-2.5 rounded shadow-sm hover:shadow-md transition-all duration-150">Buy</button>
                      <button class="bg-red-500 hover:bg-red-600 text-white text-xs py-1 px-2.5 rounded shadow-sm hover:shadow-md transition-all duration-150">Sell</button>
                      <button class="bg-yellow-500 hover:bg-yellow-600 text-white text-xs py-1 px-2.5 rounded shadow-sm hover:shadow-md transition-all duration-150">Exit</button>
                      <button class="bg-blue-500 hover:bg-blue-600 text-white text-xs py-1 px-2.5 rounded shadow-sm hover:shadow-md transition-all duration-150">Edit</button>
                    </div>
                  </td>
                  <td class="${tableCellClass}">${order.index_name}</td>
                  <td class="${tableNumericCellClass}">${order.lots}</td>
                  <td class="${tableNumericCellClass}">${order.trigger}</td>
                  <td class="${tableNumericCellClass}">${order.stop_loss}</td>
                  <td class="${tableNumericCellClass}">${order.target}</td>
                  <td class="${tableNumericCellClass}">${order.strike}</td>
                  <td class="${tableCellClass}">${order.order_status || 'N/A'}</td>
                </tr>
              `).join('')}
              ${orders.length === 0 ? `
                <tr><td colspan="8" class="px-4 py-8 text-center text-sm text-medium-text dark:text-dark-mode-text-secondary">No manual orders configured.</td></tr>
              ` : ''}
            </tbody>
          </table>
        </div>
      </div>

      <div class="${lightSectionClass}">
        <h2 class="text-xl font-semibold text-dark-text dark:text-dark-mode-text-primary mb-4">Webhook Details</h2>
        <div class="flex flex-col sm:flex-row items-center space-y-3 sm:space-y-0 sm:space-x-3 mb-6">
          <button id="regenerate-token-button" class="w-full sm:w-auto px-4 py-2 text-sm font-medium text-dark-text dark:text-dark-mode-text-primary bg-gray-100 dark:bg-dark-mode-input-border border border-gray-300 dark:border-dark-mode-border rounded-md shadow-sm hover:bg-gray-200 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary dark:focus:ring-dark-mode-primary-accent transition-colors">
            Regenerate Token
          </button>
          <input type="text" value="${webhookToken}" readonly class="flex-grow w-full p-2 text-sm text-dark-text dark:text-dark-mode-text-primary bg-gray-50 dark:bg-dark-mode-input-bg border border-gray-300 dark:border-dark-mode-input-border rounded-md focus:outline-none focus:ring-1 focus:ring-primary dark:focus:ring-dark-mode-primary-accent" aria-label="Webhook Token" />
        </div>

        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-dark-mode-border">
            <thead>
              <tr>
                <th scope="col" class="${tableHeaderClass}">Index Name</th>
                <th scope="col" class="${tableHeaderClass}">Buy URL</th>
                <th scope="col" class="${tableHeaderClass}">Sell URL</th>
                <th scope="col" class="${tableHeaderClass}">Exit URL</th>
                <th scope="col" class="${tableHeaderClass}">Input Data</th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-dark-mode-card divide-y divide-gray-200 dark:divide-dark-mode-border">
              ${webhookDetails.map((detail) => `
                <tr class="hover:bg-gray-50 dark:hover:bg-dark-mode-hover-bg">
                  <td class="${tableCellClass}">${detail.indexName}</td>
                  <td class="${urlCellClass}">${detail.buyUrl}</td>
                  <td class="${urlCellClass}">${detail.sellUrl}</td>
                  <td class="${urlCellClass}">${detail.exitUrl}</td>
                  <td class="${inputDataTdCellClass}">
                    <pre class="whitespace-pre-wrap text-xs bg-gray-100 dark:bg-dark-mode-input-bg p-2 rounded">${detail.inputData}</pre>
                  </td>
                </tr>
              `).join('')}
              ${webhookDetails.length === 0 ? `
                <tr><td colspan="5" class="px-4 py-8 text-center text-sm text-medium-text dark:text-dark-mode-text-secondary">No webhook details to display. Configure orders above or regenerate token.</td></tr>
              ` : ''}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `;
};

export default ManualOrdersPageContent;