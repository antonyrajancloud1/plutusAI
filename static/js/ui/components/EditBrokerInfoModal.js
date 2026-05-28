import { XMarkIcon, BuildingLibraryIcon } from './icons.js';

const TOKEN_STATUS_OPTIONS = ["generated", "active", "expired", "pending", "error", "revoked"];

const EditBrokerInfoModal = ({ config }) => {
  if (!config) return null;

  const formData = config;
  const inputClass = "mt-1 block w-full px-3 py-2 bg-surface-800 text-surface-50 border border-surface-700 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-primary-400 sm:text-sm placeholder-surface-500";
  const labelClass = "block text-sm font-medium text-surface-400";

  return `
    <div
      class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-[100]"
      role="dialog"
      aria-modal="true"
      aria-labelledby="editBrokerInfoModalTitle"
    >
      <div class="bg-surface-800 border border-surface-700 rounded-xl shadow-xl transform transition-all sm:max-w-lg w-full max-h-[90vh] flex flex-col">
        <div class="flex items-center justify-between px-6 py-4 border-b border-surface-700">
          <h2 id="editBrokerInfoModalTitle" class="text-lg font-semibold text-surface-50 flex items-center gap-2">
            ${BuildingLibraryIcon({ className: "h-5 w-5 text-primary-400" })}
            Edit Broker: ${formData.broker_name}
          </h2>
          <button
            class="modal-close-button text-surface-500 hover:text-surface-300"
            data-modal="broker"
            aria-label="Close modal"
          >
            ${XMarkIcon({ className: "h-5 w-5" })}
          </button>
        </div>

        <form id="edit-broker-form" class="overflow-y-auto px-6 py-5 space-y-4">
          <input type="hidden" name="id" value="${formData.id}" />
          <input type="hidden" name="index_group" value="${formData.index_group || ''}" />
          <div>
            <label for="broker_name_display" class="${labelClass}">Broker Name</label>
            <input id="broker_name_display" name="broker_name" type="text" value="${formData.broker_name}" readonly class="${inputClass} bg-surface-700/50 cursor-not-allowed" />
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label for="broker_user_id" class="${labelClass}">User ID</label><input type="text" id="broker_user_id" name="broker_user_id" value="${formData.broker_user_id}" class="${inputClass}"></div>
            <div><label for="broker_user_name" class="${labelClass}">User Name</label><input type="text" id="broker_user_name" name="broker_user_name" value="${formData.broker_user_name}" class="${inputClass}"></div>
          </div>

          <div><label for="broker_mpin" class="${labelClass}">MPIN</label><input type="text" id="broker_mpin" name="broker_mpin" value="${formData.broker_mpin}" class="${inputClass}"></div>
          <div><label for="broker_api_token" class="${labelClass}">API Token</label><input type="text" id="broker_api_token" name="broker_api_token" value="${formData.broker_api_token}" class="${inputClass}"></div>
          <div><label for="broker_qr" class="${labelClass}">QR Code</label><input type="text" id="broker_qr" name="broker_qr" value="${formData.broker_qr}" class="${inputClass}"></div>
          <div>
            <label for="token_status" class="${labelClass}">Token Status</label>
            <select id="token_status" name="token_status" class="${inputClass}">
              ${TOKEN_STATUS_OPTIONS.map(status => `
                <option value="${status}" ${formData.token_status === status ? 'selected' : ''}>${status.charAt(0).toUpperCase() + status.slice(1)}</option>
              `).join('')}
            </select>
          </div>

          <div class="space-y-2 pt-2">
            <div class="flex items-center">
              <input id="is_demo_trading_enabled" name="is_demo_trading_enabled" type="checkbox" ${formData.is_demo_trading_enabled ? 'checked' : ''} class="h-4 w-4 text-primary-500 accent-primary-500 border-surface-700 rounded focus:ring-primary-400" />
              <label for="is_demo_trading_enabled" class="ml-2 block text-sm text-surface-400">Demo Trading Enabled</label>
            </div>
          </div>

          <div class="px-6 py-4 border-t border-surface-700 bg-surface-800/50 flex justify-end gap-3 -mx-6 -mb-5 mt-4 rounded-b-xl">
            <button type="button" class="modal-close-button px-4 py-2 text-sm font-medium text-surface-400 bg-surface-800 border border-surface-700 rounded-md shadow-sm hover:bg-surface-700 focus:outline-none focus:ring-2 focus:ring-primary-400" data-modal="broker">
              Cancel
            </button>
            <button type="submit" class="px-4 py-2 text-sm font-medium text-surface-50 bg-primary-500 border border-transparent rounded-md shadow-sm hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-primary-400">
              Save Changes
            </button>
          </div>
        </form>
      </div>
    </div>
  `;
};

export default EditBrokerInfoModal;
