import { XMarkIcon, BoltIcon } from './icons.js';

const EditScalperConfigModal = ({ config }) => {
  if (!config) return null;

  const formData = config;
  const inputClass = "mt-1 block w-full px-3 py-2 bg-surface-800 text-surface-50 border border-surface-700 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-primary-400 sm:text-sm placeholder-surface-500";
  const labelClass = "block text-sm font-medium text-surface-400";

  return `
    <div
      class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50"
      role="dialog"
      aria-modal="true"
      aria-labelledby="editScalperConfigModalTitle"
    >
      <div class="bg-surface-800 border border-surface-700 rounded-xl shadow-xl transform transition-all sm:max-w-lg w-full max-h-[90vh] flex flex-col">
        <div class="flex items-center justify-between px-6 py-4 border-b border-surface-700">
          <h2 id="editScalperConfigModalTitle" class="text-lg font-semibold text-surface-50 flex items-center gap-2">
            ${BoltIcon({ className: "h-5 w-5 text-primary-400" })}
            Edit Scalper Config: ${formData.index_name}
          </h2>
          <button
            class="modal-close-button text-surface-500 hover:text-surface-300"
            data-modal="scalper"
            aria-label="Close modal"
          >
            ${XMarkIcon({ className: "h-5 w-5" })}
          </button>
        </div>

        <form id="edit-scalper-form" class="overflow-y-auto px-6 py-5 space-y-4">
          <div>
            <label for="index_name_display_scalper" class="${labelClass}">Index Name</label>
            <input id="index_name_display_scalper" name="index_name" type="text" value="${formData.index_name}" readonly class="${inputClass} bg-surface-700/50 cursor-not-allowed" />
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label for="entry_points" class="${labelClass}">Entry Points</label><input type="text" id="entry_points" name="entry_points" value="${formData.entry_points}" class="${inputClass}" /></div>
            <div><label for="target_points" class="${labelClass}">Target Points</label><input type="text" id="target_points" name="target_points" value="${formData.target_points}" class="${inputClass}" /></div>
            <div><label for="stoploss_points" class="${labelClass}">Stoploss Points</label><input type="text" id="stoploss_points" name="stoploss_points" value="${formData.stoploss_points}" class="${inputClass}" /></div>
            <div><label for="lots" class="${labelClass}">Lots</label><input type="text" id="lots" name="lots" value="${formData.lots}" class="${inputClass}" /></div>
            <div><label for="max_trades_per_day" class="${labelClass}">Max Trades/Day</label><input type="text" id="max_trades_per_day" name="max_trades_per_day" value="${formData.max_trades_per_day}" class="${inputClass}" /></div>
            <div><label for="status_scalper" class="${labelClass}">Status</label><input type="text" id="status_scalper" name="status" value="${formData.status}" class="${inputClass}" /></div>
          </div>

          <div class="space-y-2 pt-2">
            <div class="flex items-center">
              <input id="is_active_scalper" name="is_active" type="checkbox" ${formData.is_active ? 'checked' : ''} class="h-4 w-4 text-primary-500 accent-primary-500 border-surface-700 rounded focus:ring-primary-400" />
              <label for="is_active_scalper" class="ml-2 block text-sm text-surface-400">Scalper Active</label>
            </div>
          </div>

          <div class="px-6 py-4 border-t border-surface-700 bg-surface-800/50 flex justify-end gap-3 -mx-6 -mb-5 mt-4 rounded-b-xl">
            <button type="button" class="modal-close-button px-4 py-2 text-sm font-medium text-surface-400 bg-surface-800 border border-surface-700 rounded-md shadow-sm hover:bg-surface-700 focus:outline-none focus:ring-2 focus:ring-primary-400" data-modal="scalper">
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

export default EditScalperConfigModal;
