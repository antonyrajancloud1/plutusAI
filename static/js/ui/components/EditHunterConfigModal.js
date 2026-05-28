import { XMarkIcon, CogIcon } from './icons.js';

const EditHunterConfigModal = ({ config }) => {
  if (!config) return '';

  const formData = config;
  const inputClass = "mt-1 block w-full px-3 py-2 bg-surface-800 text-surface-50 border border-surface-700 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-primary-400 sm:text-sm placeholder-surface-500";
  const labelClass = "block text-sm font-medium text-surface-400";

  return `
    <div
      class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50"
      role="dialog"
      aria-modal="true"
      aria-labelledby="editConfigModalTitle"
    >
      <div class="bg-surface-800 border border-surface-700 rounded-xl shadow-xl transform transition-all sm:max-w-2xl w-full max-h-[90vh] flex flex-col">
        <div class="flex items-center justify-between px-6 py-4 border-b border-surface-700">
          <h2 id="editConfigModalTitle" class="text-lg font-semibold text-surface-50 flex items-center gap-2">
            ${CogIcon({ className: "h-5 w-5 text-primary-400" })}
            Edit Configuration: ${formData.index_name}
          </h2>
          <button
            class="modal-close-button text-surface-500 hover:text-surface-300"
            data-modal="hunter"
            aria-label="Close modal"
          >
            ${XMarkIcon({ className: "h-5 w-5" })}
          </button>
        </div>

        <form id="edit-hunter-form" class="overflow-y-auto px-6 py-5 space-y-4">
          <input type="hidden" name="original_index_name" value="${formData.index_name}" />
          <div>
            <label for="index_name_display" class="${labelClass}">Index Name</label>
            <input id="index_name_display" name="index_name" type="text" value="${formData.index_name}" readonly class="${inputClass} bg-surface-700/50 cursor-not-allowed" />
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
              <input id="start_scheduler" name="start_scheduler" type="checkbox" ${formData.start_scheduler ? 'checked' : ''} class="h-4 w-4 text-primary-500 accent-primary-500 border-surface-700 rounded focus:ring-primary-400" />
              <label for="start_scheduler" class="ml-2 block text-sm text-surface-400">Start Scheduler Active</label>
            </div>
            <div class="flex items-center">
              <input id="is_place_sl_required" name="is_place_sl_required" type="checkbox" ${formData.is_place_sl_required ? 'checked' : ''} class="h-4 w-4 text-primary-500 accent-primary-500 border-surface-700 rounded focus:ring-primary-400" />
              <label for="is_place_sl_required" class="ml-2 block text-sm text-surface-400">Place SL Required</label>
            </div>
          </div>

          <div class="px-6 py-4 border-t border-surface-700 bg-surface-800/50 flex justify-end gap-3 -mx-6 -mb-5 mt-4 rounded-b-xl">
            <button type="button" class="modal-close-button px-4 py-2 text-sm font-medium text-surface-400 bg-surface-800 border border-surface-700 rounded-md shadow-sm hover:bg-surface-700 focus:outline-none focus:ring-2 focus:ring-primary-400" data-modal="hunter">
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

export default EditHunterConfigModal;
