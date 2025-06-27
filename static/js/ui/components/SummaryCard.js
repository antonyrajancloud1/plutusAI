const SummaryCard = ({ title, value, icon, iconBgColor = 'bg-primary-dark dark:bg-dark-mode-primary-accent-dark', iconTextColor = 'text-light-text dark:text-dark-mode-text-primary', trend = null, trendText }) => {
  return `
    <div class="bg-white dark:bg-dark-mode-card p-6 rounded-xl shadow-lg hover:shadow-xl dark:hover:shadow-primary/20 transition-shadow duration-300 flex flex-col justify-between">
      <div class="flex items-start justify-between">
        <div class="p-3 rounded-lg ${iconBgColor} ${iconTextColor}">
          ${icon}
        </div>
      </div>
      <div class="mt-4">
        <p class="text-sm font-medium text-medium-text dark:text-dark-mode-text-secondary">${title}</p>
        <p class="text-2xl font-semibold text-dark-text dark:text-dark-mode-text-primary mt-1">${value}</p>
      </div>
      ${trend && trendText ? `
        <div class="mt-2 text-xs flex items-center ${trend === 'up' ? 'text-secondary dark:text-green-400' : 'text-danger dark:text-red-400'}">
          <span>${trendText}</span>
        </div>
      ` : ''}
    </div>
  `;
};

export default SummaryCard;