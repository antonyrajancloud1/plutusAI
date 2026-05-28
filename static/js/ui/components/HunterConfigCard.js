import { CogIcon, ListBulletIcon, PlayCircleIcon, StopCircleIcon, InformationCircleIcon, CheckCircleIcon, XCircleIcon } from './icons.js';

const DetailItem = ({ label, value }) => `
  <div class="flex items-start py-2">
    <div class="flex-shrink-0 w-6 h-6 mr-2"></div>
    <div class="flex-grow">
      <dt class="text-xs font-medium text-surface-400">${label}</dt>
      <dd class="mt-0.5 text-sm text-surface-50">${String(value)}</dd>
    </div>
  </div>
`;

const BooleanDetailItem = ({ label, value }) => `
    <div class="flex items-center py-2">
        <div class="flex-shrink-0 w-6 h-6 mr-2"></div>
        <dt class="text-xs font-medium text-surface-400 mr-2">${label}:</dt>
        <dd class="flex items-center text-sm">
            ${value ? CheckCircleIcon({ className: "h-5 w-5 text-emerald-400 mr-1" }) : XCircleIcon({ className: "h-5 w-5 text-red-400 mr-1" })}
            <span class="${value ? 'text-emerald-400' : 'text-red-400'}">${value ? 'Yes' : 'No'}</span>
        </dd>
    </div>
`;


const HunterConfigCard = ({ config }) => {
  const s = config.status.toLowerCase();
  const statusColor = s === 'stopped' ? 'bg-red-500/10 text-red-400' :
                      s === 'running' || s === 'active' ? 'bg-emerald-500/10 text-emerald-400' :
                      'bg-amber-500/10 text-amber-400';

  const StatusIcon = s === 'stopped' ? StopCircleIcon :
                     s === 'running' || s === 'active' ? PlayCircleIcon :
                     InformationCircleIcon;

  return `
    <div class="card flex flex-col">
      <div class="p-4 lg:p-5 border-b border-surface-700 bg-surface-800/50">
        <div class="flex items-center justify-between">
          <h3 class="text-sm font-semibold text-surface-50 uppercase flex items-center gap-2">
            ${CogIcon({ className: "h-5 w-5 text-primary-400" })}
            ${config.index_name}
          </h3>
          <button
            data-index="${config.index_name}"
            class="hunter-toggle-button px-3 py-1 text-xs font-semibold rounded-full ${statusColor} flex items-center gap-1.5 transition-transform hover:scale-105 cursor-pointer"
            aria-label="Toggle status for ${config.index_name}"
          >
            ${StatusIcon({ className: "h-4 w-4" })}
            ${config.status}
          </button>
        </div>
      </div>

      <div class="p-4 lg:p-5 space-y-4 flex-grow">
        <div>
          <h4 class="text-xs font-semibold text-surface-400 uppercase mb-2 flex items-center gap-1.5">
            ${ListBulletIcon({ className: "h-4 w-4 text-primary-400" })}Levels
          </h4>
          <p class="text-xs text-surface-50 bg-surface-800 p-2 rounded break-all max-h-36 overflow-y-auto">${config.levels || 'N/A'}</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-x-4 gap-y-1">
            ${DetailItem({ label: "Strike", value: config.strike })}
            ${DetailItem({ label: "Lots", value: config.lots })}
            ${DetailItem({ label: "Trend Check Points", value: config.trend_check_points })}
            ${DetailItem({ label: "Trailing Points", value: config.trailing_points })}
            ${DetailItem({ label: "Initial SL", value: config.initial_sl })}
            ${DetailItem({ label: "Safe SL", value: config.safe_sl })}
            ${DetailItem({ label: "Target for Safe SL", value: config.target_for_safe_sl })}
        </div>
         <div class="border-t border-surface-700 pt-3 mt-3">
             ${BooleanDetailItem({ label: "Scheduler Active", value: config.start_scheduler })}
             ${BooleanDetailItem({ label: "Place SL Required", value: config.is_place_sl_required })}
        </div>
      </div>
       <div class="px-4 lg:px-5 py-3 bg-surface-800/50 border-t border-surface-700 text-right">
        <button
          data-index="${config.index_name}"
          class="hunter-edit-button text-xs text-primary-400 hover:text-primary-300 font-medium hover:underline"
          aria-label="Edit configuration for ${config.index_name}"
        >
          Edit Config
        </button>
      </div>
    </div>
  `;
};

export default HunterConfigCard;
