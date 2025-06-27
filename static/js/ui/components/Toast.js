import { CheckCircleIcon, XCircleIcon, InformationCircleIcon, XMarkIcon } from './icons.js';

const toastConfig = {
  success: {
    icon: CheckCircleIcon({ className: "h-6 w-6 text-green-500" }),
    bg: 'bg-green-50 dark:bg-green-900 dark:bg-opacity-50',
    border: 'border-green-400 dark:border-green-600',
    text: 'text-green-800 dark:text-green-200'
  },
  error: {
    icon: XCircleIcon({ className: "h-6 w-6 text-red-500" }),
    bg: 'bg-red-50 dark:bg-red-900 dark:bg-opacity-50',
    border: 'border-red-400 dark:border-red-600',
    text: 'text-red-800 dark:text-red-200'
  },
  info: {
    icon: InformationCircleIcon({ className: "h-6 w-6 text-blue-500" }),
    bg: 'bg-blue-50 dark:bg-blue-900 dark:bg-opacity-50',
    border: 'border-blue-400 dark:border-blue-600',
    text: 'text-blue-800 dark:text-blue-200'
  }
};

const Toast = ({ message, type }) => {
  const config = toastConfig[type];

  return `
    <div 
      class="fixed top-20 right-5 max-w-sm w-full ${config.bg} shadow-lg rounded-lg pointer-events-auto ring-1 ring-black ring-opacity-5 border-l-4 ${config.border} z-[200] animate-fade-in-right"
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
              class="toast-close-button inline-flex rounded-md ${config.bg} text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              aria-label="Close toast"
            >
              <span class="sr-only">Close</span>
              ${XMarkIcon({ className: "h-5 w-5" })}
            </button>
          </div>
        </div>
      </div>
      <style>
        @keyframes fade-in-right {
          from { opacity: 0; transform: translateX(100%); }
          to { opacity: 1; transform: translateX(0); }
        }
        .animate-fade-in-right { animation: fade-in-right 0.3s ease-out forwards; }
      </style>
    </div>
  `;
};

export default Toast;