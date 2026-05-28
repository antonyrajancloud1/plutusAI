import { CheckCircleIcon, XCircleIcon, InformationCircleIcon, BuildingLibraryIcon, PencilSquareIcon } from './icons.js';

const BrokerInfoTable = ({ title, data }) => {
  const getValueDisplay = (value) => (value && value.trim() !== "") ? value : "Not Set";

  const getBooleanIndicator = (value) => {
    return value ?
      `<span title="Enabled">${CheckCircleIcon({ className: "h-5 w-5 text-emerald-400" })}</span>` :
      `<span title="Disabled">${XCircleIcon({ className: "h-5 w-5 text-red-400" })}</span>`;
  };

  const getTokenStatusIndicator = (status) => {
    const sLower = status.toLowerCase();
    let colorClass = 'bg-surface-500/10 text-surface-400';
    if (sLower === 'generated' || sLower === 'active') {
      colorClass = 'bg-emerald-500/10 text-emerald-400';
    } else if (sLower === 'expired' || sLower === 'revoked' || sLower === 'error') {
      colorClass = 'bg-red-500/10 text-red-400';
    } else if (sLower === 'pending') {
      colorClass = 'bg-amber-500/10 text-amber-400';
    }
    return `<span class="px-2 py-0.5 text-xs font-semibold rounded-full ${colorClass}">${status}</span>`;
  };

  return `
    <div class="card p-4 lg:p-5 mt-2">
       <div class="flex items-center justify-between mb-6">
        <h2 class="text-lg font-bold text-surface-50 flex items-center gap-3">
            ${BuildingLibraryIcon({ className: "h-6 w-6 text-primary-400" })}
            ${title}
        </h2>
      </div>

      ${!data ? `
        <div class="text-center py-10">
          ${InformationCircleIcon({ className: "h-12 w-12 text-surface-500 mx-auto mb-3" })}
          <p class="text-surface-400">No broker information available at the moment.</p>
        </div>
      ` : `
        <div class="overflow-x-auto -mx-4 lg:-mx-5">
          <table class="w-full text-sm">
            <thead>
              <tr class="text-surface-400 text-xs uppercase tracking-wider border-b border-surface-700">
                <th class="text-left py-3 px-4 lg:px-5 font-medium">Broker Name</th>
                <th class="text-left py-3 px-4 lg:px-5 font-medium">User ID</th>
                <th class="text-left py-3 px-4 lg:px-5 font-medium">User Name</th>
                <th class="text-left py-3 px-4 lg:px-5 font-medium">MPIN</th>
                <th class="text-left py-3 px-4 lg:px-5 font-medium">API Token</th>
                <th class="text-left py-3 px-4 lg:px-5 font-medium">QR Code</th>
                <th class="text-left py-3 px-4 lg:px-5 font-medium">Token Status</th>
                <th class="text-center py-3 px-4 lg:px-5 font-medium">Demo Trading</th>
                <th class="text-center py-3 px-4 lg:px-5 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-surface-700/50">
              <tr class="hover:bg-surface-700/30 transition-colors duration-150">
                <td class="py-3 px-4 lg:px-5 text-surface-50">${data.broker_name}</td>
                <td class="py-3 px-4 lg:px-5 text-surface-400 break-all">${getValueDisplay(data.broker_user_id)}</td>
                <td class="py-3 px-4 lg:px-5 text-surface-400 break-all">${getValueDisplay(data.broker_user_name)}</td>
                <td class="py-3 px-4 lg:px-5 text-surface-400 break-all">${getValueDisplay(data.broker_mpin)}</td>
                <td class="py-3 px-4 lg:px-5 text-surface-400 break-all">${getValueDisplay(data.broker_api_token)}</td>
                <td class="py-3 px-4 lg:px-5 text-surface-400 break-all">${getValueDisplay(data.broker_qr)}</td>
                <td class="py-3 px-4 lg:px-5 text-surface-50">${getTokenStatusIndicator(data.token_status)}</td>
                <td class="py-3 px-4 lg:px-5 text-center">${getBooleanIndicator(data.is_demo_trading_enabled)}</td>
                <td class="py-3 px-4 lg:px-5 text-center">
                  <button
                    id="broker-edit-button"
                    class="text-primary-400 hover:text-primary-300 font-medium p-1 rounded-md hover:bg-surface-700/30 transition-colors duration-150"
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
