import { XMarkIcon, BuildingLibraryIcon } from './icons.js';

const TOKEN_STATUS_OPTIONS = ["generated", "active", "expired", "pending", "error", "revoked"];

const EditBrokerInfoModal = ({ config }) => {
  if (!config) return null;

  const formData = config;
  const inputClass = "mt-1 block w-full px-3 py-2 bg-white text-dark-text dark:bg-dark-mode-input-bg dark:text-dark-mode-text-primary border border-gray-300 dark:border-dark-mode-input-border rounded-md shadow-sm focus:outline-none focus:ring-primary dark:focus:ring-dark-mode-primary-accent focus:border-primary dark:focus:border-dark-mode-primary-accent sm:text-sm";
  const labelClass = "block text-sm font-medium text-gray-700 dark:text-dark-mode-text-secondary";

  return `
    <div 
      class="fixed inset-0 bg-gray-600 bg-opacity-75 dark:bg-black dark:bg-opacity-75 flex items-center justify-center p-4 z-[100] transition-opacity duration-300" 
      role="dialog"
      aria-modal="true"
      aria-labelledby="editBrokerInfoModalTitle"
    >
      <div class="bg-white dark:bg-dark-mode-card rounded-lg shadow-xl transform transition-all sm:max-w-lg w-full max-h-[90vh] flex flex-col">
        <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-dark-mode-border">
          <h2 id="editBrokerInfoModalTitle" class="text-xl font-semibold text-dark-text dark:text-dark-mode-text-primary flex items-center">
            ${BuildingLibraryIcon({ className: "h-6 w-6 mr-2 text-primary dark:text-dark-mode-primary-accent" })}
            Edit Broker: ${formData.broker_name}
          </h2>
          <button 
            class="modal-close-button text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300"
            data-modal="broker"
            aria-label="Close modal"
          >
            ${XMarkIcon({ className: "h-6 w-6" })}
          </button>
        </div>

        <form id="edit-broker-form" class="overflow-y-auto px-6 py-5 space-y-4">
          <input type="hidden" name="id" value="${formData.id}" />
          <div>
            <label for="broker_name_display" class="${labelClass}">Broker Name</label>
            <input id="broker_name_display" name="broker_name" type="text" value="${formData.broker_name}" readonly class="${inputClass} bg-gray-100 dark:bg-gray-700 cursor-not-allowed" />
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
              <input id="is_demo_trading_enabled" name="is_demo_trading_enabled" type="checkbox" ${formData.is_demo_trading_enabled ? 'checked' : ''} class="h-4 w-4 text-primary dark:accent-dark-mode-primary-accent border-gray-300 dark:border-dark-mode-input-border rounded focus:ring-primary dark:focus:ring-dark-mode-primary-accent" />
              <label for="is_demo_trading_enabled" class="ml-2 block text-sm text-gray-900 dark:text-dark-mode-text-secondary">Demo Trading Enabled</label>
            </div>
          </div>
        
          <div class="px-6 py-4 border-t border-gray-200 dark:border-dark-mode-border bg-gray-50 dark:bg-dark-mode-hover-bg flex justify-end space-x-3 -mx-6 -mb-5 mt-4 rounded-b-lg">
            <button type="button" class="modal-close-button px-4 py-2 text-sm font-medium text-gray-700 dark:text-dark-mode-text-secondary bg-white dark:bg-dark-mode-input-bg border border-gray-300 dark:border-dark-mode-input-border rounded-md shadow-sm hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary dark:focus:ring-dark-mode-primary-accent" data-modal="broker">
              Cancel
            </button>
            <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-primary dark:bg-dark-mode-primary-accent border border-transparent rounded-md shadow-sm hover:bg-primary-dark dark:hover:bg-dark-mode-primary-accent-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-dark dark:focus:ring-dark-mode-primary-accent-dark">
              Save Changes
            </button>
          </div>
        </form>
      </div>
    </div>
  `;
};

export default EditBrokerInfoModal;