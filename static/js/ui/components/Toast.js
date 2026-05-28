import { CheckCircleIcon, XCircleIcon, InformationCircleIcon, XMarkIcon } from './icons.js';

const toastConfig = {
  success: {
    icon: CheckCircleIcon({ className: "h-5 w-5 text-emerald-400" }),
    bg: 'bg-emerald-500/10',
    border: 'border-emerald-500/30',
    text: 'text-emerald-300'
  },
  error: {
    icon: XCircleIcon({ className: "h-5 w-5 text-red-400" }),
    bg: 'bg-red-500/10',
    border: 'border-red-500/30',
    text: 'text-red-300'
  },
  info: {
    icon: InformationCircleIcon({ className: "h-5 w-5 text-blue-400" }),
    bg: 'bg-blue-500/10',
    border: 'border-blue-500/30',
    text: 'text-blue-300'
  }
};

const Toast = ({ message, type }) => {
  const config = toastConfig[type];

  return `
    <div 
      class="fixed top-20 right-5 max-w-sm w-full ${config.bg} backdrop-blur-sm shadow-lg rounded-lg pointer-events-auto border-l-4 ${config.border} z-[200] animate-fade-in-right"
      role="alert"
    >
      <div class="p-4">
        <div class="flex items-start">
          <div class="flex-shrink-0">
            ${config.icon}
          </div>
          <div class="ml-3 w-0 flex-1 pt-0.5">
            <p class="text-sm font-medium ${config.text}">
              ${message}
            </p>
          </div>
          <div class="ml-4 flex-shrink-0 flex">
            <button
              class="toast-close-button inline-flex rounded-md text-surface-500 hover:text-surface-300 focus:outline-none"
              aria-label="Close toast"
            >
              ${XMarkIcon({ className: "h-4 w-4" })}
            </button>
          </div>
        </div>
      </div>
    </div>
  `;
};

export default Toast;