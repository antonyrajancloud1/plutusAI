import { CogIcon, PlayCircleIcon, StopCircleIcon, InformationCircleIcon, CheckCircleIcon, XCircleIcon } from './icons.js';

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
            <span class="${value ? 'text-emerald-400' : 'text-red-400'}">${value ? 'Running' : 'Stopped'}</span>
        </dd>
    </div>
`;
const BooleanDetailItemYN = ({ label, value }) => `
    <div class="flex items-center py-2">
        <div class="flex-shrink-0 w-6 h-6 mr-2"></div>
        <dt class="text-xs font-medium text-surface-400 mr-2">${label}:</dt>
        <dd class="flex items-center text-sm">
            ${value ? CheckCircleIcon({ className: "h-5 w-5 text-emerald-400 mr-1" }) : XCircleIcon({ className: "h-5 w-5 text-red-400 mr-1" })}
            <span class="${value ? 'text-emerald-400' : 'text-red-400'}">${value ? 'Yes' : 'No'}</span>
        </dd>
    </div>
`;

const ScalperConfigCard = ({ config }) => {
  const statusToConsider = config.status?.toLowerCase() || 'stopped';
  const isRunning = config.is_active || statusToConsider === 'running' || statusToConsider === 'active';

  const statusColor = isRunning ? 'bg-emerald-500/10 text-emerald-400' :
                      'bg-red-500/10 text-red-400';

  const StatusIcon = isRunning ? PlayCircleIcon : StopCircleIcon;
  const cardStatusText = isRunning ? 'Running' : 'Stopped';

  return `
    <div class="card flex flex-col w-full">
      <div class="p-4 lg:p-5 border-b border-surface-700 bg-surface-800/50">
        <div class="flex items-center justify-between">
          <h3 class="text-sm font-semibold text-surface-50 uppercase flex items-center gap-2">
            ${CogIcon({ className: "h-5 w-5 text-primary-400" })}
            ${config.index_name} Scalper
          </h3>
          <button
            id="scalper-toggle-button"
            class="px-3 py-1 text-xs font-semibold rounded-full ${statusColor} flex items-center gap-1.5 transition-transform hover:scale-105 cursor-pointer"
            aria-label="Toggle status for ${config.index_name} Scalper"
          >
            ${StatusIcon({ className: "h-4 w-4" })}
            ${cardStatusText}
          </button>
        </div>
      </div>

      <div class="p-4 lg:p-5 space-y-3 flex-grow">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-x-4 gap-y-1">
            ${DetailItem({ label: "Strike", value: config.strike })}
            ${DetailItem({ label: "Target Points", value: config.target })}
             ${BooleanDetailItemYN({ label: "On Candle Close", value: config.on_candle_close })}
            ${DetailItem({ label: "Lots", value: config.lots })}
        </div>
         <div class="border-t border-surface-700 pt-3 mt-3">
             ${BooleanDetailItem({ label: "Scalper Status", value: isRunning })}
        </div>
      </div>
       <div class="px-4 lg:px-5 py-3 bg-surface-800/50 border-t border-surface-700 text-right">
        <button
          id="scalper-edit-button"
          class="text-xs text-primary-400 hover:text-primary-300 font-medium hover:underline"
          aria-label="Edit configuration for ${config.index_name} Scalper"
        >
          Edit Config
        </button>
      </div>
    </div>
  `;
};

export default ScalperConfigCard;
