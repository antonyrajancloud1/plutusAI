import { NAV_ITEMS } from '../App.js'; 
import { UserCircleIcon, ArrowRightOnRectangleIcon } from './icons.js';
import ThemeToggleButton from './ThemeToggleButton.js';

const NavigationBar = ({ activePage, userName, theme }) => {
  return `
    <nav class="bg-white dark:bg-dark-mode-card shadow-md sticky top-0 z-50">
      <div class="container mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center">
            <span class="font-bold text-xl text-primary dark:text-dark-mode-primary-accent">Plutuz</span>
          </div>
          
          <div class="hidden md:flex flex-grow items-center justify-center space-x-2 lg:space-x-4">
            ${NAV_ITEMS.map((item) => {
              const isActive = activePage === item.name;
              return `
                <button
                  data-page="${item.name}"
                  aria-current="${isActive ? 'page' : 'false'}"
                  class="nav-button flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors duration-150 ease-in-out
                    ${isActive
                      ? 'bg-primary text-white dark:bg-dark-mode-primary-accent dark:text-dark-mode-card'
                      : 'text-dark-text dark:text-dark-mode-text-secondary hover:bg-gray-100 dark:hover:bg-dark-mode-hover-bg hover:text-primary-dark dark:hover:text-dark-mode-primary-accent'
                    }"
                >
                  ${item.icon({ className: `h-5 w-5 mr-2 ${isActive ? 'text-white dark:text-dark-mode-card': 'text-medium-text dark:text-dark-mode-text-secondary group-hover:text-dark-mode-primary-accent'}` })}
                  ${item.name}
                </button>
              `;
            }).join('')}
          </div>

          <div class="flex items-center space-x-2">
            ${ThemeToggleButton({ theme })}
            <button
              id="logout-button"
              class="p-2 rounded-full text-medium-text dark:text-dark-mode-text-secondary hover:bg-gray-200 dark:hover:bg-dark-mode-hover-bg focus:outline-none focus:ring-2 focus:ring-primary dark:focus:ring-dark-mode-primary-accent transition-colors duration-200"
              aria-label="Logout"
            >
              ${ArrowRightOnRectangleIcon({ className: "h-5 w-5" })}
            </button>
            ${userName ? `
              <div class="flex items-center text-sm text-medium-text dark:text-dark-mode-text-secondary ml-1 md:ml-2">
                ${UserCircleIcon({ className: "h-6 w-6 mr-2 text-primary dark:text-dark-mode-primary-accent" })}
                <span class="hidden sm:inline">${userName}</span>
              </div>
            `: ''}
          </div>

          <div class="md:hidden ml-2">
            <select
              id="mobile-nav-select"
              class="block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-dark-mode-border bg-white dark:bg-dark-mode-input-bg text-dark-text dark:text-dark-mode-text-primary focus:outline-none focus:ring-primary dark:focus:ring-dark-mode-primary-accent focus:border-primary dark:focus:border-dark-mode-primary-accent sm:text-sm rounded-md"
              aria-label="Select Page"
            >
              ${NAV_ITEMS.map(item => `
                <option value="${item.name}" ${activePage === item.name ? 'selected' : ''}>${item.name}</option>
              `).join('')}
            </select>
          </div>
        </div>
      </div>
    </nav>
  `;
};

export default NavigationBar;