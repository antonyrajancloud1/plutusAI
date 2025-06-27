import { CogIcon, PlayCircleIcon, StopCircleIcon, InformationCircleIcon, CheckCircleIcon, XCircleIcon } from './icons.js';

const DetailItem = ({ label, value }) => `
  <div class="flex items-start py-2">
    <div class="flex-shrink-0 w-6 h-6 mr-2"></div>
    <div class="flex-grow">
      <dt class="text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary">${label}</dt>
      <dd class="mt-0.5 text-sm text-dark-text dark:text-dark-mode-text-primary">${String(value)}</dd>
    </div>
  </div>
`;

const BooleanDetailItem = ({ label, value }) => `
    <div class="flex items-center py-2">
        <div class="flex-shrink-0 w-6 h-6 mr-2"></div>
        <dt class="text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary mr-2">${label}:</dt>
        <dd class="flex items-center text-sm">
            ${value ? CheckCircleIcon({ className: "h-5 w-5 text-secondary dark:text-green-400 mr-1" }) : XCircleIcon({ className: "h-5 w-5 text-danger dark:text-red-400 mr-1" })}
            <span class="${value ? 'text-secondary dark:text-green-400' : 'text-danger dark:text-red-400'}">${value ? 'Running' : 'Stopped'}</span>
        </dd>
    </div>
`;
const BooleanDetailItemYN = ({ label, value }) => `
    <div class="flex items-center py-2">
        <div class="flex-shrink-0 w-6 h-6 mr-2"></div>
        <dt class="text-xs font-medium text-medium-text dark:text-dark-mode-text-secondary mr-2">${label}:</dt>
        <dd class="flex items-center text-sm">
            ${value ? CheckCircleIcon({ className: "h-5 w-5 text-secondary dark:text-green-400 mr-1" }) : XCircleIcon({ className: "h-5 w-5 text-danger dark:text-red-400 mr-1" })}
            <span class="${value ? 'text-secondary dark:text-green-400' : 'text-danger dark:text-red-400'}">${value ? 'Yes' : 'No'}</span>
        </dd>
    </div>
`;

const ScalperConfigCard = ({ config }) => {
  const statusToConsider = config.status?.toLowerCase() || 'stopped';
  const isRunning = config.is_active || statusToConsider === 'running' || statusToConsider === 'active';
  
  const statusColor = isRunning ? 'bg-green-100 text-green-700 dark:bg-green-700 dark:text-green-100' : 
                      'bg-red-100 text-red-700 dark:bg-red-700 dark:text-red-100';
  
  const StatusIcon = isRunning ? PlayCircleIcon : StopCircleIcon;
  const cardStatusText = isRunning ? 'Running' : 'Stopped';

  return `
    <div class="bg-white dark:bg-dark-mode-card shadow-xl rounded-lg overflow-hidden transition-all duration-300 hover:shadow-2xl dark:hover:shadow-primary/20 flex flex-col w-full">
      <div class="p-5 border-b border-gray-200 dark:border-dark-mode-border bg-gray-50 dark:bg-dark-mode-hover-bg">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold text-primary dark:text-dark-mode-primary-accent uppercase flex items-center">
            ${CogIcon({ className: "h-6 w-6 mr-2" })}
            ${config.index_name} Scalper
          </h3>
          <button
            id="scalper-toggle-button"
            class="px-3 py-1 text-xs font-semibold rounded-full ${statusColor} flex items-center transition-transform transform hover:scale-105 cursor-pointer"
            aria-label="Toggle status for ${config.index_name} Scalper"
          >
            ${StatusIcon({ className: "h-4 w-4 mr-1.5" })}
            ${cardStatusText}
          </button>
        </div>
      </div>

      <div class="p-5 space-y-3 flex-grow">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-x-4 gap-y-1">
            ${DetailItem({ label: "Strike", value: config.strike })}
            ${DetailItem({ label: "Target Points", value: config.target })}
             ${BooleanDetailItemYN({ label: "On Candle Close", value: config.on_candle_close })}
            ${DetailItem({ label: "Lots", value: config.lots })}
        </div>
         <div class="border-t border-gray-200 dark:border-dark-mode-border pt-3 mt-3">
             ${BooleanDetailItem({ label: "Scalper Status", value: isRunning })}
        </div>
      </div>
       <div class="px-5 py-3 bg-gray-50 dark:bg-dark-mode-hover-bg border-t border-gray-200 dark:border-dark-mode-border text-right">
        <button 
          id="scalper-edit-button"
          class="text-xs text-primary dark:text-dark-mode-primary-accent hover:text-primary-dark dark:hover:text-blue-300 font-medium hover:underline"
          aria-label="Edit configuration for ${config.index_name} Scalper"
        >
          Edit Config
        </button>
      </div>
    </div>
  `;
};

export default ScalperConfigCard;