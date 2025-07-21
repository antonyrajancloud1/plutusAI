import { CalendarDaysIcon } from './icons.js';

const DashboardHeader = () => {
  const formatDate = (date) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString(undefined, options);
  };

  return `
    <div class="mb-8 p-6 bg-white dark:bg-dark-mode-card shadow-lg rounded-lg">
      <div class="flex flex-col sm:flex-row justify-between items-center">
        <h1 class="text-3xl font-bold text-dark-text dark:text-dark-mode-text-primary mb-4 sm:mb-0">Plutuz Dashboard</h1>
        <div class="flex flex-col sm:flex-row items-center space-y-2 sm:space-y-0 sm:space-x-6 text-medium-text dark:text-dark-mode-text-secondary">
          <div class="flex items-center">
            ${CalendarDaysIcon({ className: "h-6 w-6 mr-2 text-primary dark:text-dark-mode-primary-accent" })}
            <span>${formatDate(new Date())}</span>
          </div>
        </div>
      </div>
    </div>
  `;
};

export default DashboardHeader;