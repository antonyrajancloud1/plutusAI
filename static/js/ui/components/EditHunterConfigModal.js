import { XMarkIcon, CogIcon } from './icons.js';

const EditHunterConfigModal = ({ config }) => {
  if (!config) return '';

  const formData = config; 
  const inputClass = "mt-1 block w-full px-3 py-2 bg-white text-dark-text dark:bg-dark-mode-input-bg dark:text-dark-mode-text-primary border border-gray-300 dark:border-dark-mode-input-border rounded-md shadow-sm focus:outline-none focus:ring-primary dark:focus:ring-dark-mode-primary-accent focus:border-primary dark:focus:border-dark-mode-primary-accent sm:text-sm";
  const labelClass = "block text-sm font-medium text-gray-700 dark:text-dark-mode-text-secondary";

  return `
    <div 
      class="fixed inset-0 bg-gray-600 bg-opacity-75 dark:bg-black dark:bg-opacity-75 flex items-center justify-center p-4 z-50 transition-opacity duration-300"
      role="dialog"
      aria-modal="true"
      aria-labelledby="editConfigModalTitle"
    >
      <div class="bg-white dark:bg-dark-mode-card rounded-lg shadow-xl transform transition-all sm:max-w-2xl w-full max-h-[90vh] flex flex-col">
        <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-dark-mode-border">
          <h2 id="editConfigModalTitle" class="text-xl font-semibold text-dark-text dark:text-dark-mode-text-primary flex items-center">
            ${CogIcon({ className: "h-6 w-6 mr-2 text-primary dark:text-dark-mode-primary-accent" })}
            Edit Configuration: ${formData.index_name}
          </h2>
          <button 
            class="modal-close-button text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300"
            data-modal="hunter"
            aria-label="Close modal"
          >
            ${XMarkIcon({ className: "h-6 w-6" })}
          </button>
        </div>

        <form id="edit-hunter-form" class="overflow-y-auto px-6 py-5 space-y-4">
          <input type="hidden" name="original_index_name" value="${formData.index_name}" />
          <div>
            <label for="index_name_display" class="${labelClass}">Index Name</label>
            <input id="index_name_display" name="index_name" type="text" value="${formData.index_name}" readonly class="${inputClass} bg-gray-100 dark:bg-gray-700 cursor-not-allowed" />
          </div>

          <div>
            <label for="levels" class="${labelClass}">Levels (comma-separated)</label>
            <textarea id="levels" name="levels" rows="3" class="${inputClass}">${formData.levels}</textarea>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label for="strike" class="${labelClass}">Strike</label><input type="text" id="strike" name="strike" value="${formData.strike}" class="${inputClass}" /></div>
            <div><label for="lots" class="${labelClass}">Lots</label><input type="text" id="lots" name="lots" value="${formData.lots}" class="${inputClass}" /></div>
            <div><label for="trend_check_points" class="${labelClass}">Trend Check Points</label><input type="text" id="trend_check_points" name="trend_check_points" value="${formData.trend_check_points}" class="${inputClass}" /></div>
            <div><label for="trailing_points" class="${labelClass}">Trailing Points</label><input type="text" id="trailing_points" name="trailing_points" value="${formData.trailing_points}" class="${inputClass}" /></div>
            <div><label for="initial_sl" class="${labelClass}">Initial SL</label><input type="text" id="initial_sl" name="initial_sl" value="${formData.initial_sl}" class="${inputClass}" /></div>
            <div><label for="safe_sl" class="${labelClass}">Safe SL</label><input type="text" id="safe_sl" name="safe_sl" value="${formData.safe_sl}" class="${inputClass}" /></div>
            <div><label for="target_for_safe_sl" class="${labelClass}">Target for Safe SL</label><input type="text" id="target_for_safe_sl" name="target_for_safe_sl" value="${formData.target_for_safe_sl}" class="${inputClass}" /></div>
            <div><label for="status" class="${labelClass}">Status</label><input type="text" id="status" name="status" value="${formData.status}" class="${inputClass}" /></div>
          </div>
          
          <div class="space-y-2 pt-2">
            <div class="flex items-center">
              <input id="start_scheduler" name="start_scheduler" type="checkbox" ${formData.start_scheduler ? 'checked' : ''} class="h-4 w-4 text-primary dark:accent-dark-mode-primary-accent border-gray-300 dark:border-dark-mode-input-border rounded focus:ring-primary dark:focus:ring-dark-mode-primary-accent" />
              <label for="start_scheduler" class="ml-2 block text-sm text-gray-900 dark:text-dark-mode-text-secondary">Start Scheduler Active</label>
            </div>
            <div class="flex items-center">
              <input id="is_place_sl_required" name="is_place_sl_required" type="checkbox" ${formData.is_place_sl_required ? 'checked' : ''} class="h-4 w-4 text-primary dark:accent-dark-mode-primary-accent border-gray-300 dark:border-dark-mode-input-border rounded focus:ring-primary dark:focus:ring-dark-mode-primary-accent" />
              <label for="is_place_sl_required" class="ml-2 block text-sm text-gray-900 dark:text-dark-mode-text-secondary">Place SL Required</label>
            </div>
          </div>
        
          <div class="px-6 py-4 border-t border-gray-200 dark:border-dark-mode-border bg-gray-50 dark:bg-dark-mode-hover-bg flex justify-end space-x-3 -mx-6 -mb-5 mt-4 rounded-b-lg">
            <button type="button" class="modal-close-button px-4 py-2 text-sm font-medium text-gray-700 dark:text-dark-mode-text-secondary bg-white dark:bg-dark-mode-input-bg border border-gray-300 dark:border-dark-mode-input-border rounded-md shadow-sm hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary dark:focus:ring-dark-mode-primary-accent" data-modal="hunter">
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

export default EditHunterConfigModal;