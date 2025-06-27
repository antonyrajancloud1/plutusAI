

import {
    HomeIcon, BookOpenIcon, MagnifyingGlassIcon, PencilSquareIcon, BoltIcon, BuildingLibraryIcon,
    ChartBarIcon, CheckCircleIcon, XCircleIcon, WalletIcon
} from './components/icons.js';
import { makeApiCall } from './utils/api.js';
import NavigationBar from './components/NavigationBar.js';
import DashboardHeader from './components/DashboardHeader.js';
import SummaryCard from './components/SummaryCard.js';
import StrategyTable from './components/StrategyTable.js';
import OpenOrdersTable from './components/OpenOrdersTable.js';
import OrderBookTable from './components/OrderBookTable.js';
import HunterConfigCard from './components/HunterConfigCard.js';
import EditHunterConfigModal from './components/EditHunterConfigModal.js';
import ManualOrdersPageContent from './components/ManualOrdersPageContent.js';
import ScalperConfigCard from './components/ScalperConfigCard.js';
import EditScalperConfigModal from './components/EditScalperConfigModal.js';
import BrokerInfoTable from './components/BrokerInfoTable.js';
import EditBrokerInfoModal from './components/EditBrokerInfoModal.js';
import Toast from './components/Toast.js';

// Application state
const state = {
    activePage: 'Dashboard',
    dashboardData: null,
    openOrdersData: [],
    orderBookData: [],
    hunterConfigs: [],
    scalperConfig: null,
    brokerInfoData: [],
    loading: true,
    error: null,
    theme: 'light',
    toast: null,
    isEditHunterModalOpen: false,
    editingHunterConfig: null,
    isEditScalperModalOpen: false,
    editingScalperConfig: null,
    isEditBrokerModalOpen: false,
    editingBrokerItem: null,
};

export const NAV_ITEMS = [
  { name: 'Dashboard', icon: HomeIcon },
  { name: 'Order Book', icon: BookOpenIcon },
  { name: 'Hunter', icon: MagnifyingGlassIcon },
  { name: 'Manual Orders', icon: PencilSquareIcon },
  { name: 'Scalper', icon: BoltIcon },
  { name: 'Broker Info', icon: BuildingLibraryIcon },
];

// --- Render Functions ---

const LoadingSpinner = () => `
  <div class="flex items-center justify-center min-h-screen bg-light-bg dark:bg-dark-mode-bg">
    <div class="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-primary dark:border-dark-mode-primary-accent"></div>
    <p class="ml-4 text-xl text-dark-text dark:text-dark-mode-text-primary">Loading Data...</p>
  </div>
`;

const ErrorMessage = ({ message }) => `
  <div class="flex flex-col items-center justify-center min-h-screen bg-red-50 dark:bg-red-900 dark:bg-opacity-20 p-4">
    ${XCircleIcon({ className: "h-16 w-16 text-danger mb-4" })}
    <h2 class="text-2xl font-semibold text-danger dark:text-red-400 mb-2">Oops! Something went wrong.</h2>
    <p class="text-medium-text dark:text-dark-mode-text-secondary">${message}</p>
  </div>
`;

const PagePlaceholder = ({ pageName, icon }) => `
  <div class="p-8 bg-white dark:bg-dark-mode-card shadow-lg rounded-lg text-center mt-8">
    <div class="flex justify-center items-center mb-4">
        ${icon ? icon({ className: "h-16 w-16 text-primary dark:text-dark-mode-primary-accent opacity-50" }) : ChartBarIcon({ className: "h-16 w-16 text-primary dark:text-dark-mode-primary-accent mx-auto opacity-50" })}
    </div>
    <h2 class="text-3xl font-semibold text-dark-text dark:text-dark-mode-text-primary">${pageName}</h2>
    <p class="mt-4 text-medium-text dark:text-dark-mode-text-secondary">Content for this page is coming soon or data is not available!</p>
  </div>
`;

// --- Event Handlers & State Changers ---

function handleNavigate(page) {
    state.activePage = page;
    render();
}

function toggleTheme() {
    state.theme = state.theme === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', state.theme);
    render();
}

function handleLogout() {
    console.log("Logout button clicked. Implement actual logout logic here.");
    showToast('Logged out successfully!', 'info');
}

function showToast(message, type) {
    state.toast = { message, type };
    render();
    setTimeout(() => {
        state.toast = null;
        const toastElement = document.querySelector('.fixed.top-20.right-5');
        if (toastElement) toastElement.remove();
    }, 5000);
}

function handleHunterStatusToggle(index_name) {
    state.hunterConfigs = state.hunterConfigs.map(c => {
        if (c.index_name === index_name) {
            const newStatus = c.status === 'running' ? 'stopped' : 'running';
            showToast(`Hunter for ${c.index_name} has been set to '${newStatus}'.`, 'success');
            return { ...c, status: newStatus };
        }
        return c;
    });
    render();
}

function handleScalperStatusToggle() {
    if (!state.scalperConfig) return;
    const currentStatus = state.scalperConfig.status?.toLowerCase();
    const newStatus = (currentStatus === 'running' || currentStatus === 'active') ? 'Stopped' : 'Running';
    const newIsActive = newStatus === 'Running';
    showToast(`Scalper for ${state.scalperConfig.index_name} has been set to '${newStatus}'.`, 'success');
    state.scalperConfig = { ...state.scalperConfig, is_active: newIsActive, status: newStatus };
    render();
}

// Modal Handlers
const handleOpenEditHunterModal = (config) => { state.editingHunterConfig = config; state.isEditHunterModalOpen = true; render(); };
const handleCloseEditHunterModal = () => { state.editingHunterConfig = null; state.isEditHunterModalOpen = false; render(); };
const handleSaveHunterConfig = (event) => {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const originalIndexName = formData.get('original_index_name');

    const configToUpdate = { ...state.hunterConfigs.find(c => c.index_name === originalIndexName) };

    for (let [key, value] of formData.entries()) {
        if (key in configToUpdate) {
             configToUpdate[key] = value;
        }
    }
    configToUpdate.start_scheduler = form.elements.start_scheduler.checked;
    configToUpdate.is_place_sl_required = form.elements.is_place_sl_required.checked;

    state.hunterConfigs = state.hunterConfigs.map(c => c.index_name === originalIndexName ? configToUpdate : c);
    showToast(`Hunter config for ${originalIndexName} updated.`, 'success');
    handleCloseEditHunterModal();
};

const handleOpenEditScalperModal = (config) => { state.editingScalperConfig = config; state.isEditScalperModalOpen = true; render(); };
const handleCloseEditScalperModal = () => { state.editingScalperConfig = null; state.isEditScalperModalOpen = false; render(); };
const handleSaveScalperConfig = (event) => {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    const updatedConfig = { ...state.scalperConfig };
     for (let [key, value] of formData.entries()) {
        if (key in updatedConfig) {
            updatedConfig[key] = value;
        }
    }
    updatedConfig.is_active = form.elements.is_active_scalper.checked;

    state.scalperConfig = updatedConfig;
    showToast(`Scalper config updated.`, 'success');
    handleCloseEditScalperModal();
};

const handleOpenEditBrokerModal = (item) => { state.editingBrokerItem = item; state.isEditBrokerModalOpen = true; render(); };
const handleCloseEditBrokerModal = () => { state.editingBrokerItem = null; state.isEditBrokerModalOpen = false; render(); };
const handleSaveBrokerInfo = (event) => {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const id = formData.get('id');

    const updatedItem = { ...state.brokerInfoData.find(i => i.id === id) };
    for (let [key, value] of formData.entries()) {
        if (key in updatedItem) {
            updatedItem[key] = value;
        }
    }
    updatedItem.is_demo_trading_enabled = form.elements.is_demo_trading_enabled.checked;

    state.brokerInfoData = state.brokerInfoData.map(item => item.id === id ? updatedItem : item);
    showToast(`Broker info for ${updatedItem.broker_name} updated.`, 'success');
    handleCloseEditBrokerModal();
};

// Data Fetching
async function fetchAllData() {
    state.loading = true;
    state.error = null;
    render();
    try {
        const [
            dashboardResponse,
            openOrdersResponse,
            orderBookResponse,
            hunterConfigsResponse,
            scalperConfigResponse,
            brokerInfoResponse,
            manualOrderResponse
        ] = await Promise.all([
              makeApiCall('/get_strategy_summary'),
            makeApiCall('/get_order_book_details'),
            makeApiCall('/get_order_book_details'),
            makeApiCall('/get_config_values'),
            makeApiCall('/get_scalper_details'),
            makeApiCall('/get_broker_details'),
            makeApiCall('/manual_details')
        ]);

        // Safely parse API responses with fallbacks to prevent crashes
        state.dashboardData = dashboardResponse?.summary ?? null;

        // Handle open orders, which might be a direct array or nested in an object like { data: [...] }
        state.openOrdersData = Array.isArray(openOrdersResponse) ? openOrdersResponse : openOrdersResponse?.data ?? [];

        state.orderBookData = orderBookResponse?.order_book_details ?? [];
        state.hunterConfigs = hunterConfigsResponse?.all_config_values ?? [];
        state.scalperConfig = scalperConfigResponse?.all_config_values[0] ?? [];
        state.brokerInfoData = brokerInfoResponse?.broker_details ?? [];
        state.manualOrdersData = manualOrderResponse?.message ?? [];

    } catch (err) {
        console.error("Failed to fetch data:", err);
        state.error = err instanceof Error ? err.message : "An unknown error occurred loading data.";
    } finally {
        state.loading = false;
        render();
    }
}


// --- Page Content Renderers ---

const renderDashboardContent = () => {
    if (!state.dashboardData) return ErrorMessage({ message: "Dashboard data is unavailable." });

    const { total_orders_today, task_status, full_summary, current_day_summary } = state.dashboardData;
    const totalProfitToday = current_day_summary.reduce((acc, curr) => acc + curr.total_profit, 0);
    const overallTotalProfit = full_summary.reduce((acc, curr) => acc + curr.total_profit, 0);

    return `
        ${DashboardHeader()}
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            ${SummaryCard({ title: "Total Orders Today", value: total_orders_today, icon: ChartBarIcon({ className: "h-6 w-6" }), iconBgColor: "bg-blue-100 dark:bg-blue-900", iconTextColor: "text-blue-600 dark:text-blue-300" })}
            ${SummaryCard({ title: "Task Status", value: task_status ? 'Active' : 'Inactive', icon: task_status ? CheckCircleIcon({ className: "h-6 w-6" }) : XCircleIcon({ className: "h-6 w-6" }), iconBgColor: task_status ? "bg-green-100 dark:bg-green-900" : "bg-red-100 dark:bg-red-900", iconTextColor: task_status ? "text-green-600 dark:text-green-300" : "text-red-600 dark:text-red-300" })}
            ${SummaryCard({ title: "Profit Today", value: new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(totalProfitToday), icon: WalletIcon({ className: "h-6 w-6" }), iconBgColor: totalProfitToday >= 0 ? "bg-emerald-100 dark:bg-emerald-900" : "bg-rose-100 dark:bg-rose-900", iconTextColor: totalProfitToday >= 0 ? "text-emerald-600 dark:text-emerald-300" : "text-rose-600 dark:text-rose-300" })}
            ${SummaryCard({ title: "Overall Profit", value: new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(overallTotalProfit), icon: WalletIcon({ className: "h-6 w-6" }), iconBgColor: overallTotalProfit >= 0 ? "bg-sky-100 dark:bg-sky-900" : "bg-orange-100 dark:bg-orange-900", iconTextColor: overallTotalProfit >= 0 ? "text-sky-600 dark:text-sky-300" : "text-orange-600 dark:text-orange-300" })}
        </div>
        <div class="grid grid-cols-1 xl:grid-cols-2 gap-8 mb-8">
            ${StrategyTable({ title: "Full Strategy Performance", data: full_summary })}
            ${StrategyTable({ title: "Today's Strategy Performance", data: current_day_summary })}
        </div>
        <div class="grid grid-cols-1 xl:grid-cols-2 gap-8">
            ${OpenOrdersTable({ title: "Open Orders", data: state.openOrdersData })}
            ${StrategyTable({ title: "Today's Order Details", data: current_day_summary })}
        </div>
    `;
};

function renderPageContent() {
    switch (state.activePage) {
        case 'Dashboard': return renderDashboardContent();
        case 'Order Book':
            if (!state.orderBookData || state.orderBookData.length === 0) {
                return PagePlaceholder({ pageName: "Order Book Details", icon: BookOpenIcon });
            }
            return OrderBookTable({ title: "Order Book Details", data: state.orderBookData });
        case 'Hunter':
            if (!state.hunterConfigs || state.hunterConfigs.length === 0) {
                return PagePlaceholder({ pageName: "Hunter Configurations", icon: MagnifyingGlassIcon });
            }
            return `
                <div class="mt-8">
                    <h2 class="text-3xl font-bold text-dark-text dark:text-dark-mode-text-primary mb-2 flex items-center">
                        ${MagnifyingGlassIcon({ className: "h-8 w-8 mr-3 text-primary dark:text-dark-mode-primary-accent" })}
                        Hunter Strategy Configurations
                    </h2>
                    <p class="text-medium-text dark:text-dark-mode-text-secondary mb-8">Manage and review your automated hunter strategy parameters.</p>
                    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                        ${state.hunterConfigs.map(config => HunterConfigCard({ config })).join('')}
                    </div>
                </div>
            `;
        case 'Manual Orders':
            return ManualOrdersPageContent({
                orders: state.manualOrdersData,
                webhookToken: state.webhookToken,
                strategyName: state.strategyName
            });
        case 'Scalper':
            if (!state.scalperConfig) {
                return PagePlaceholder({ pageName: "Scalper Configuration (BankNifty)", icon: BoltIcon });
            }
            return `
                 <div class="mt-8">
                    <h2 class="text-3xl font-bold text-dark-text dark:text-dark-mode-text-primary mb-2 flex items-center">
                        ${BoltIcon({ className: "h-8 w-8 mr-3 text-primary dark:text-dark-mode-primary-accent" })}
                        Scalper Configuration (BankNifty)
                    </h2>
                    <p class="text-medium-text dark:text-dark-mode-text-secondary mb-8">Manage your BankNifty scalping strategy parameters.</p>
                    <div class="flex justify-center">
                        <div class="w-full max-w-xl">
                            ${ScalperConfigCard({ config: state.scalperConfig })}
                        </div>
                    </div>
                </div>
            `;
        case 'Broker Info':
            const displayedBroker = state.brokerInfoData.length > 0 ? state.brokerInfoData[0] : null;
            if (!displayedBroker) {
                return PagePlaceholder({ pageName: "Broker Information", icon: BuildingLibraryIcon });
            }
            return BrokerInfoTable({ title: "Broker Information", data: displayedBroker });
        default:
            const navItem = NAV_ITEMS.find(item => item.name === state.activePage);
            return PagePlaceholder({ pageName: state.activePage, icon: navItem?.icon });
    }
}

// --- Main Render & Event Listener Attachment ---

function render() {
    const root = document.getElementById('root');
    if (!root) return;

    // Apply theme class to <html> element
    if (state.theme === 'dark') {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }

    let pageHtml;
    if (state.loading) {
        pageHtml = LoadingSpinner();
    } else if (state.error) {
        pageHtml = ErrorMessage({ message: state.error });
    } else {
        const mainContent = `
            <main class="container mx-auto px-4 sm:px-6 lg:px-8 py-4 md:py-8">
                ${renderPageContent()}
            </main>
        `;
        const modals = `
            ${state.isEditHunterModalOpen ? EditHunterConfigModal({ config: state.editingHunterConfig }) : ''}
            ${state.isEditScalperModalOpen ? EditScalperConfigModal({ config: state.editingScalperConfig }) : ''}
            ${state.isEditBrokerModalOpen ? EditBrokerInfoModal({ config: state.editingBrokerItem }) : ''}
        `;
        const toastHtml = state.toast ? Toast(state.toast) : '';

        pageHtml = `
            <div id="app-container" class="min-h-screen bg-light-bg dark:bg-dark-mode-bg selection:bg-primary selection:text-white dark:selection:bg-dark-mode-primary-accent dark:selection:text-dark-mode-card">
                ${NavigationBar({ activePage: state.activePage, userName: state.dashboardData?.user_name, theme: state.theme })}
                ${mainContent}
                <div id="modal-container">${modals}</div>
                <div id="toast-container">${toastHtml}</div>
            </div>
        `;
    }

    root.innerHTML = pageHtml;
    attachEventListeners();
}

function attachEventListeners() {
    // Navigation
    document.querySelectorAll('.nav-button').forEach(button => {
        button.addEventListener('click', () => handleNavigate(button.dataset.page));
    });
    const mobileNav = document.getElementById('mobile-nav-select');
    if (mobileNav) {
        mobileNav.value = state.activePage;
        mobileNav.addEventListener('change', (e) => handleNavigate(e.target.value));
    }

    // Theme Toggle & Logout
    document.getElementById('theme-toggle-button')?.addEventListener('click', toggleTheme);
    document.getElementById('logout-button')?.addEventListener('click', handleLogout);

    // Toast
    document.querySelector('.toast-close-button')?.addEventListener('click', () => {
        state.toast = null;
        document.getElementById('toast-container').innerHTML = '';
    });

    // Modals
    document.querySelectorAll('.modal-close-button').forEach(btn => {
        const modalId = btn.dataset.modal;
        const closeHandler = {
            hunter: handleCloseEditHunterModal,
            scalper: handleCloseEditScalperModal,
            broker: handleCloseEditBrokerModal,
        }[modalId];
        if(closeHandler) btn.addEventListener('click', closeHandler);
    });
    document.getElementById('edit-hunter-form')?.addEventListener('submit', handleSaveHunterConfig);
    document.getElementById('edit-scalper-form')?.addEventListener('submit', handleSaveScalperConfig);
    document.getElementById('edit-broker-form')?.addEventListener('submit', handleSaveBrokerInfo);

    // Page-specific listeners
    if (state.activePage === 'Hunter') {
        document.querySelectorAll('.hunter-edit-button').forEach(btn => {
            btn.addEventListener('click', () => {
                const config = state.hunterConfigs.find(c => c.index_name === btn.dataset.index);
                if (config) handleOpenEditHunterModal(config);
            });
        });
        document.querySelectorAll('.hunter-toggle-button').forEach(btn => {
            btn.addEventListener('click', () => handleHunterStatusToggle(btn.dataset.index));
        });
    }

    if (state.activePage === 'Scalper') {
        document.getElementById('scalper-edit-button')?.addEventListener('click', () => handleOpenEditScalperModal(state.scalperConfig));
        document.getElementById('scalper-toggle-button')?.addEventListener('click', handleScalperStatusToggle);
    }

    if (state.activePage === 'Broker Info') {
        document.getElementById('broker-edit-button')?.addEventListener('click', () => {
             if (state.brokerInfoData.length > 0) handleOpenEditBrokerModal(state.brokerInfoData[0]);
        });
    }
}

// Initializer
export function init() {
    state.theme = localStorage.getItem('theme') || 'light';
    fetchAllData();
}