import { SunIcon, MoonIcon } from './icons.js';

const ThemeToggleButton = ({ theme }) => {
  return `
    <button
      id="theme-toggle-button"
      class="p-2 rounded-full text-medium-text dark:text-dark-mode-text-secondary hover:bg-gray-200 dark:hover:bg-dark-mode-hover-bg focus:outline-none focus:ring-2 focus:ring-primary dark:focus:ring-dark-mode-primary-accent transition-colors duration-200"
      aria-label="${theme === 'light' ? 'Switch to dark mode' : 'Switch to light mode'}"
    >
      ${theme === 'light' ? MoonIcon({ className: "h-5 w-5" }) : SunIcon({ className: "h-5 w-5" })}
    </button>
  `;
};

export default ThemeToggleButton;