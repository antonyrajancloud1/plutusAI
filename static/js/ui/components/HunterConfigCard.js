import { CogIcon, ListBulletIcon, PlayCircleIcon, StopCircleIcon, InformationCircleIcon, CheckCircleIcon, XCircleIcon } from './icons.js';

const DetailItem = ({ label, value }) => `
  <div class="flex items-start py-2">
    <div class="flex-shrink-0 w-6 h-6 mr-2"></div> <!-- Placeholder for alignment -->
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
            <span class="${value ? 'text-secondary dark:text-green-400' : 'text-danger dark:text-red-400'}">${value ? 'Yes' : 'No'}</span>
        </dd>
    </div>
`;


const HunterConfigCard = ({ config }) => {
  const statusColor = config.status.toLowerCase() === 'stopped' ? 'bg-red-100 text-red-700 dark:bg-red-700 dark:text-red-100' : 
                      config.status.toLowerCase() === 'running' || config.status.toLowerCase() === 'active' ? 'bg-green-100 text-green-700 dark:bg-green-700 dark:text-green-100' : 
                      'bg-yellow-100 text-yellow-700 dark:bg-yellow-600 dark:text-yellow-100';
  
  const StatusIcon = config.status.toLowerCase() === 'stopped' ? StopCircleIcon : 
                     config.status.toLowerCase() === 'running' || config.status.toLowerCase() === 'active' ? PlayCircleIcon : 
                     InformationCircleIcon;

  return `
    <div class="bg-white dark:bg-dark-mode-card shadow-xl rounded-lg overflow-hidden transition-all duration-300 hover:shadow-2xl dark:hover:shadow-primary/20 flex flex-col">
      <div class="p-5 border-b border-gray-200 dark:border-dark-mode-border bg-gray-50 dark:bg-dark-mode-hover-bg">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold text-primary dark:text-dark-mode-primary-accent uppercase flex items-center">
            ${CogIcon({ className: "h-6 w-6 mr-2" })}
            ${config.index_name}
          </h3>
          <button
            data-index="${config.index_name}"
            class="hunter-toggle-button px-3 py-1 text-xs font-semibold rounded-full ${statusColor} flex items-center transition-transform transform hover:scale-105 cursor-pointer"
            aria-label="Toggle status for ${config.index_name}"
          >
            ${StatusIcon({ className: "h-4 w-4 mr-1.5" })}
            ${config.status}
          </button>
        </div>
      </div>

      <div class="p-5 space-y-4 flex-grow">
        <div>
          <h4 class="text-xs font-semibold text-medium-text dark:text-dark-mode-text-secondary uppercase mb-2 flex items-center">
            ${ListBulletIcon({ className: "h-4 w-4 mr-1.5 text-primary dark:text-dark-mode-primary-accent" })}Levels
          </h4>
          <p class="text-xs text-dark-text dark:text-dark-mode-text-primary bg-gray-100 dark:bg-dark-mode-input-bg p-2 rounded break-all max-h-36 overflow-y-auto">${config.levels || 'N/A'}</p>
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
         <div class="border-t border-gray-200 dark:border-dark-mode-border pt-3 mt-3">
             ${BooleanDetailItem({ label: "Scheduler Active", value: config.start_scheduler })}
             ${BooleanDetailItem({ label: "Place SL Required", value: config.is_place_sl_required })}
        </div>
      </div>
       <div class="px-5 py-3 bg-gray-50 dark:bg-dark-mode-hover-bg border-t border-gray-200 dark:border-dark-mode-border text-right">
        <button 
          data-index="${config.index_name}"
          class="hunter-edit-button text-xs text-primary dark:text-dark-mode-primary-accent hover:text-primary-dark dark:hover:text-blue-300 font-medium hover:underline"
          aria-label="Edit configuration for ${config.index_name}"
        >
          Edit Config
        </button>
      </div>
    </div>
  `;
};

export default HunterConfigCard;