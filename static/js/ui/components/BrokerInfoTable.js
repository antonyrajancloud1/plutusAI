import { CheckCircleIcon, XCircleIcon, InformationCircleIcon, BuildingLibraryIcon, PencilSquareIcon } from './icons.js';

const BrokerInfoTable = ({ title, data }) => {
  const getValueDisplay = (value) => (value && value.trim() !== "") ? value : "Not Set";

  const getBooleanIndicator = (value) => {
    return value ? 
      `<span title="Enabled">${CheckCircleIcon({ className: "h-5 w-5 text-secondary dark:text-green-400" })}</span>` :
      `<span title="Disabled">${XCircleIcon({ className: "h-5 w-5 text-danger dark:text-red-400" })}</span>`;
  };

  const getTokenStatusIndicator = (status) => {
    const sLower = status.toLowerCase();
    let colorClass = 'bg-gray-100 text-gray-700 dark:bg-gray-600 dark:text-gray-200';
    if (sLower === 'generated' || sLower === 'active') {
      colorClass = 'bg-green-100 text-green-700 dark:bg-green-700 dark:text-green-100';
    } else if (sLower === 'expired' || sLower === 'revoked' || sLower === 'error') {
      colorClass = 'bg-red-100 text-red-700 dark:bg-red-700 dark:text-red-100';
    } else if (sLower === 'pending') {
      colorClass = 'bg-yellow-100 text-yellow-700 dark:bg-yellow-600 dark:text-yellow-100';
    }
    return `<span class="px-2 py-0.5 text-xs font-semibold rounded-full ${colorClass}">${status}</span>`;
  };
  
  const tableHeaderClass = "px-4 py-3 text-left text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary uppercase tracking-wider bg-gray-50 dark:bg-dark-mode-table-header";
  const tableCellClass = "px-4 py-3 whitespace-nowrap text-sm text-dark-text dark:text-dark-mode-text-primary";
  const valueCellClass = "px-4 py-3 text-sm text-dark-text dark:text-dark-mode-text-primary break-all";

  return `
    <div class="bg-white dark:bg-dark-mode-card p-4 md:p-6 rounded-xl shadow-lg mt-2">
       <div class="flex items-center justify-between mb-6">
        <h2 class="text-3xl font-bold text-dark-text dark:text-dark-mode-text-primary flex items-center">
            ${BuildingLibraryIcon({ className: "h-8 w-8 mr-3 text-primary dark:text-dark-mode-primary-accent" })}
            ${title}
        </h2>
      </div>
      
      ${!data ? `
        <div class="text-center py-10">
          ${InformationCircleIcon({ className: "h-12 w-12 text-medium-text dark:text-dark-mode-text-secondary mx-auto mb-3" })}
          <p class="text-medium-text dark:text-dark-mode-text-secondary">No broker information available at the moment.</p>
        </div>
      ` : `
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-dark-mode-border">
            <thead class="bg-gray-50 dark:bg-dark-mode-table-header">
              <tr>
                <th scope="col" class="${tableHeaderClass}">Broker Name</th>
                <th scope="col" class="${tableHeaderClass}">User ID</th>
                <th scope="col" class="${tableHeaderClass}">User Name</th>
                <th scope="col" class="${tableHeaderClass}">MPIN</th>
                <th scope="col" class="${tableHeaderClass}">API Token</th>
                <th scope="col" class="${tableHeaderClass}">QR Code</th>
                <th scope="col" class="${tableHeaderClass}">Token Status</th>
                <th scope="col" class="${tableHeaderClass} text-center">Demo Trading</th>
                <th scope="col" class="${tableHeaderClass} text-center">Actions</th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-dark-mode-card divide-y divide-gray-200 dark:divide-dark-mode-border">
              <tr class="hover:bg-gray-50 dark:hover:bg-dark-mode-hover-bg transition-colors duration-150">
                <td class="${tableCellClass}">${data.broker_name}</td>
                <td class="${valueCellClass}">${getValueDisplay(data.broker_user_id)}</td>
                <td class="${valueCellClass}">${getValueDisplay(data.broker_user_name)}</td>
                <td class="${valueCellClass}">${getValueDisplay(data.broker_mpin)}</td>
                <td class="${valueCellClass}">${getValueDisplay(data.broker_api_token)}</td>
                <td class="${valueCellClass}">${getValueDisplay(data.broker_qr)}</td>
                <td class="${tableCellClass}">${getTokenStatusIndicator(data.token_status)}</td>
                <td class="${tableCellClass} text-center">${getBooleanIndicator(data.is_demo_trading_enabled)}</td>
                <td class="${tableCellClass} text-center">
                  <button
                    id="broker-edit-button"
                    class="text-primary dark:text-dark-mode-primary-accent hover:text-primary-dark dark:hover:text-blue-300 font-medium p-1 rounded-md hover:bg-blue-100 dark:hover:bg-dark-mode-hover-bg transition-colors duration-150"
                    aria-label="Edit broker ${data.broker_name}"
                  >
                    ${PencilSquareIcon({ className: "h-5 w-5" })}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      `}
    </div>
  `;
};

export default BrokerInfoTable;