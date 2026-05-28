import {
    HomeIcon, BookOpenIcon, MagnifyingGlassIcon, PencilSquareIcon, BoltIcon,
    BuildingLibraryIcon, CogIcon, ChartBarIcon, CheckCircleIcon, XCircleIcon,
    WalletIcon, SunIcon, MoonIcon, UserCircleIcon, ArrowRightOnRectangleIcon,
    Bars3Icon, XMarkIcon, ShieldCheckIcon, ListBulletIcon, ClockIcon, ActivityIcon
} from './components/icons.js';
import { makeApiCall } from './utils/api.js';
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
import TelegramSettingsPage, { initSettingsPage } from './components/TelegramSettingsPage.js';
import AdminConsolePage, { initAdminConsole } from './components/AdminConsolePage.js';
import LogViewerPage, { initLogViewer } from './components/LogViewerPage.js';
import StrategiesPage, { initStrategiesPage } from './components/StrategiesPage.js';

const state = {
    activePage: 'Dashboard',
    isAdmin: false,
    sidebarOpen: false,
    dashboardData: null,
    openOrdersData: [],
    orderBookData: [],
    hunterConfigs: [],
    scalperConfig: null,
    brokerInfoData: [],
    loading: true,
    error: null,
    theme: 'dark',
    toast: null,
    isEditHunterModalOpen: false,
    editingHunterConfig: null,
    isEditScalperModalOpen: false,
    editingScalperConfig: null,
    isEditBrokerModalOpen: false,
    editingBrokerItem: null,
    todayPnl: 0,
    systemOk: false,
    manualOrdersData: [],
    webhookToken: '',
    strategyName: 'DefaultStrategy',
};

const USER_NAV = [
    { name: 'Dashboard', icon: HomeIcon },
    { name: 'Order Book', icon: BookOpenIcon },
    { name: 'Hunter', icon: MagnifyingGlassIcon },
    { name: 'Manual Orders', icon: PencilSquareIcon },
    { name: 'Scalper', icon: BoltIcon },
    { name: 'Strategies', icon: ShieldCheckIcon },
    { name: 'Broker Info', icon: BuildingLibraryIcon },
    { name: 'Settings', icon: CogIcon },
];

const ADMIN_NAV = [
    { name: 'Dashboard', icon: HomeIcon },
    { name: 'Admin Console', icon: ShieldCheckIcon },
    { name: 'Order Book', icon: BookOpenIcon },
    { name: 'Hunter', icon: MagnifyingGlassIcon },
    { name: 'Manual Orders', icon: PencilSquareIcon },
    { name: 'Scalper', icon: BoltIcon },
    { name: 'Strategies', icon: ShieldCheckIcon },
    { name: 'Broker Info', icon: BuildingLibraryIcon },
    { name: 'Log Viewer', icon: ListBulletIcon },
    { name: 'Settings', icon: CogIcon },
];

const MOBILE_NAV = [
    { name: 'Dashboard', icon: HomeIcon },
    { name: 'Hunter', icon: MagnifyingGlassIcon },
    { name: 'Manual Orders', icon: PencilSquareIcon },
    { name: 'Scalper', icon: BoltIcon },
    { name: 'Strategies', icon: ShieldCheckIcon },
    { name: 'Settings', icon: CogIcon },
];

function getNav() { return state.isAdmin ? ADMIN_NAV : USER_NAV; }

function handleNavigate(page) {
    state.activePage = page;
    state.sidebarOpen = false;
    render();
}

function toggleTheme() {
    state.theme = state.theme === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', state.theme);
    document.documentElement.setAttribute('data-theme', state.theme);
    render();
}

function toggleSidebar() {
    state.sidebarOpen = !state.sidebarOpen;
    render();
}

async function handleLogout() {
    try { await makeApiCall('/logout'); } catch (e) {}
    window.location.href = '/login';
}

function showToast(message, type) {
    state.toast = { message, type };
    render();
    setTimeout(() => {
        state.toast = null;
        const el = document.querySelector('.toast-fixed');
        if (el) el.remove();
    }, 4500);
}

function handleHunterStatusToggle(index_name) {
    state.hunterConfigs = state.hunterConfigs.map(c => {
        if (c.index_name === index_name) {
            showToast(`Hunter for ${c.index_name} toggled`, 'success');
            return { ...c, status: c.status === 'running' ? 'stopped' : 'running' };
        }
        return c;
    });
    render();
}

function handleScalperStatusToggle() {
    if (!state.scalperConfig) return;
    const newStatus = state.scalperConfig.status?.toLowerCase() === 'running' ? 'Stopped' : 'Running';
    showToast(`Scalper set to ${newStatus}`, 'success');
    state.scalperConfig = { ...state.scalperConfig, status: newStatus };
    render();
}

const handleOpenEditHunterModal = (config) => { state.editingHunterConfig = config; state.isEditHunterModalOpen = true; render(); };
const handleCloseEditHunterModal = () => { state.editingHunterConfig = null; state.isEditHunterModalOpen = false; render(); };
const handleSaveHunterConfig = (event) => {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const originalIndexName = formData.get('original_index_name');
    const configToUpdate = { ...state.hunterConfigs.find(c => c.index_name === originalIndexName) };
    for (let [key, value] of formData.entries()) {
        if (key in configToUpdate) configToUpdate[key] = value;
    }
    configToUpdate.start_scheduler = form.elements.start_scheduler.checked;
    configToUpdate.is_place_sl_required = form.elements.is_place_sl_required.checked;
    state.hunterConfigs = state.hunterConfigs.map(c => c.index_name === originalIndexName ? configToUpdate : c);
    showToast(`Hunter config for ${originalIndexName} updated`, 'success');
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
        if (key in updatedConfig) updatedConfig[key] = value;
    }
    updatedConfig.is_active = form.elements.is_active_scalper.checked;
    state.scalperConfig = updatedConfig;
    showToast('Scalper config updated', 'success');
    handleCloseEditScalperModal();
};

const handleOpenEditBrokerModal = (item) => { state.editingBrokerItem = item; state.isEditBrokerModalOpen = true; render(); };
const handleCloseEditBrokerModal = () => { state.editingBrokerItem = null; state.isEditBrokerModalOpen = false; render(); };
const handleSaveBrokerInfo = async (event) => {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const id = formData.get('id');
    const payload = {};
    for (let [key, value] of formData.entries()) {
        if (key !== 'id') payload[key] = value;
    }
    payload.is_demo_trading_enabled = form.elements.is_demo_trading_enabled.checked;
    try {
        const resp = await makeApiCall('/edit_broker_details', {
            method: 'PUT',
            body: payload,
        });
        if (resp?.status === 'success') {
            const brokerResp = await makeApiCall('/get_broker_details');
            state.brokerInfoData = brokerResp?.broker_details ?? [];
            showToast('Broker info updated', 'success');
            handleCloseEditBrokerModal();
        } else {
            showToast(resp?.message || 'Failed to update broker info', 'error');
        }
    } catch (err) {
        showToast('Network error updating broker info', 'error');
    }
};

async function fetchAllData() {
    state.loading = true;
    state.error = null;
    render();
    try {
        const [dashResp, orderBookResp, hunterResp, scalperResp, brokerResp, manualResp, tokenResp, adminResp] = await Promise.all([
            makeApiCall('/get_strategy_summary'),
            makeApiCall('/get_order_book_details'),
            makeApiCall('/get_config_values'),
            makeApiCall('/get_scalper_details'),
            makeApiCall('/get_broker_details'),
            makeApiCall('/manual_details'),
            makeApiCall('/get_auth_token', { method: 'POST' }).catch(() => null),
            makeApiCall('/check_admin').catch(() => null),
        ]);
        state.dashboardData = dashResp?.summary ?? null;
        state.orderBookData = orderBookResp?.order_book_details ?? [];
        state.hunterConfigs = hunterResp?.all_config_values ?? [];
        state.scalperConfig = scalperResp?.all_config_values?.[0] ?? null;
        state.brokerInfoData = brokerResp?.broker_details ?? [];
        state.manualOrdersData = Array.isArray(manualResp?.message) ? manualResp.message : [];
        state.webhookToken = tokenResp?.message || '';
        state.isAdmin = adminResp?.is_admin ?? false;

        const todayPnl = state.dashboardData?.current_day_summary?.reduce((a, c) => a + (c.total_profit || 0), 0) || 0;
        state.todayPnl = todayPnl;
        state.systemOk = state.dashboardData?.task_status ?? false;
    } catch (err) {
        state.error = err.message || 'Failed to load data';
    } finally {
        state.loading = false;
        render();
    }
}

const SkeletonDashboard = () => `
<div class="p-4 lg:p-6 space-y-6">
  <div class="skeleton h-8 w-48 mb-6"></div>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
    ${Array(4).fill(0).map(() => '<div class="skeleton h-28 rounded-xl"></div>').join('')}
  </div>
  <div class="grid grid-cols-1 xl:grid-cols-2 gap-6">
    ${Array(2).fill(0).map(() => '<div class="skeleton h-64 rounded-xl"></div>').join('')}
  </div>
</div>`;

const ErrorMessage = ({ message }) => `
<div class="flex flex-col items-center justify-center min-h-[60vh] p-8">
  ${XCircleIcon({ className: "h-16 w-16 text-red-400 mb-4" })}
  <h2 class="text-xl font-semibold text-surface-50 mb-2">Something went wrong</h2>
  <p class="text-surface-400 text-center max-w-md">${message}</p>
  <button onclick="location.reload()" class="mt-6 px-5 py-2.5 bg-primary-500 hover:bg-primary-600 text-surface-50 rounded-lg text-sm font-medium transition-colors">Retry</button>
</div>`;

const PageHeader = ({ title, icon, subtitle }) => `
<div class="flex items-center justify-between mb-6 page-enter">
  <div class="flex items-center gap-3">
    ${icon ? icon({ className: "h-6 w-6 text-primary-400" }) : ''}
    <div>
      <h1 class="text-xl lg:text-2xl font-bold text-surface-50">${title}</h1>
      ${subtitle ? `<p class="text-sm text-surface-400 mt-0.5">${subtitle}</p>` : ''}
    </div>
  </div>
</div>`;

const PagePlaceholder = ({ pageName, icon }) => `
<div class="flex flex-col items-center justify-center min-h-[40vh] text-surface-400">
  ${icon ? icon({ className: "h-16 w-16 mb-4 opacity-40" }) : ''}
  <p class="text-lg font-medium">${pageName}</p>
  <p class="text-sm mt-1">No data available</p>
</div>`;

function renderPageContent() {
    switch (state.activePage) {
        case 'Dashboard': return renderDashboardContent();
        case 'Admin Console': return AdminConsolePage();
        case 'Order Book':
            if (!state.orderBookData?.length) return PagePlaceholder({ pageName: 'Order Book', icon: BookOpenIcon });
            return OrderBookTable({ title: 'Order History', data: state.orderBookData });
        case 'Hunter':
            if (!state.hunterConfigs?.length) return PagePlaceholder({ pageName: 'Hunter Configurations', icon: MagnifyingGlassIcon });
            return `
                <div class="page-enter">
                    ${PageHeader({ title: 'Hunter Strategies', icon: MagnifyingGlassIcon, subtitle: 'Manage automated hunter strategy parameters' })}
                    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                        ${state.hunterConfigs.map(c => HunterConfigCard({ config: c })).join('')}
                    </div>
                </div>`;
        case 'Manual Orders':
            return `<div class="page-enter">${ManualOrdersPageContent({ orders: state.manualOrdersData, webhookToken: state.webhookToken, strategyName: state.strategyName })}</div>`;
        case 'Scalper':
            if (!state.scalperConfig) return PagePlaceholder({ pageName: 'Scalper Configuration', icon: BoltIcon });
            return `
                <div class="page-enter">
                    ${PageHeader({ title: 'Scalper (BankNifty)', icon: BoltIcon, subtitle: 'BankNifty scalping strategy parameters' })}
                    <div class="max-w-xl mx-auto">${ScalperConfigCard({ config: state.scalperConfig })}</div>
                </div>`;
        case 'Broker Info':
            if (!state.brokerInfoData?.length) return PagePlaceholder({ pageName: 'Broker Information', icon: BuildingLibraryIcon });
            return `<div class="page-enter">${BrokerInfoTable({ title: 'Broker Information', data: state.brokerInfoData[0] })}</div>`;
        case 'Strategies':
            return `<div class="page-enter">${StrategiesPage()}</div>`;
        case 'Log Viewer':
            return `<div class="page-enter">${LogViewerPage()}</div>`;
        case 'Settings':
            return `<div class="page-enter">${TelegramSettingsPage()}</div>`;
        default:
            return PagePlaceholder({ pageName: state.activePage });
    }
}

const renderDashboardContent = () => {
    if (!state.dashboardData) return ErrorMessage({ message: 'Dashboard data unavailable' });
    const { total_orders_today, task_status, full_summary, current_day_summary } = state.dashboardData;
    const todayProfit = current_day_summary?.reduce((a, c) => a + (c.total_profit || 0), 0) || 0;
    const overallProfit = full_summary?.reduce((a, c) => a + (c.total_profit || 0), 0) || 0;
    return `
    <div class="page-enter space-y-6">
        ${PageHeader({ title: 'Dashboard', icon: HomeIcon, subtitle: 'Trading performance overview' })}
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 lg:gap-4">
            ${SummaryCard({ title: 'Orders Today', value: total_orders_today || 0, icon: ChartBarIcon({ className: 'h-5 w-5' }), accent: 'indigo' })}
            ${SummaryCard({ title: 'Task Status', value: task_status ? 'Active' : 'Inactive', icon: task_status ? CheckCircleIcon({ className: 'h-5 w-5' }) : XCircleIcon({ className: 'h-5 w-5' }), accent: task_status ? 'green' : 'red' })}
            ${SummaryCard({ title: "Today's P&L", value: formatINR(todayProfit), icon: WalletIcon({ className: 'h-5 w-5' }), accent: todayProfit >= 0 ? 'green' : 'red' })}
            ${SummaryCard({ title: 'Overall P&L', value: formatINR(overallProfit), icon: WalletIcon({ className: 'h-5 w-5' }), accent: overallProfit >= 0 ? 'green' : 'red' })}
        </div>
        <div class="grid grid-cols-1 xl:grid-cols-2 gap-6">
            ${StrategyTable({ title: 'Full Performance', data: full_summary || [] })}
            ${StrategyTable({ title: "Today's Performance", data: current_day_summary || [] })}
        </div>
    </div>`;
};

const formatINR = (n) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', minimumFractionDigits: 0 }).format(n || 0);

function renderSidebar() {
    const nav = getNav();
    return `
    <div class="sidebar-overlay fixed inset-0 bg-black/50 z-30 lg:hidden" onclick="handleSidebarToggle()"></div>
    <aside class="sidebar-panel fixed top-0 left-0 z-40 h-full w-64 bg-surface-800 border-r border-surface-700 transform -translate-x-full lg:translate-x-0 flex flex-col">
      <div class="flex items-center justify-between h-14 px-5 border-b border-surface-700">
        <span class="text-lg font-bold text-surface-50 tracking-tight">Plutu<span class="text-primary-400">Z</span></span>
        <button class="lg:hidden p-1.5 rounded-lg hover:bg-surface-700 text-surface-400" onclick="handleSidebarToggle()">
          ${XMarkIcon({ className: 'h-5 w-5' })}
        </button>
      </div>
      <nav class="flex-1 overflow-y-auto py-3 px-2 space-y-0.5">
        ${nav.map(item => {
            const isActive = state.activePage === item.name;
            return `
              <button data-page="${item.name}" class="nav-item w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${isActive ? 'active text-primary-300' : 'text-surface-400 hover:text-surface-50 hover:bg-surface-700/50'}">
                ${item.icon({ className: `h-5 w-5 flex-shrink-0 ${isActive ? 'text-primary-400' : ''}` })}
                <span>${item.name}</span>
                ${item.name === 'Admin Console' ? `<span class="ml-auto px-1.5 py-0.5 text-[10px] font-semibold bg-primary-500/20 text-primary-300 rounded">ADMIN</span>` : ''}
              </button>`;
        }).join('')}
      </nav>
      <div class="p-3 border-t border-surface-700">
        <div class="flex items-center gap-3 px-3 py-2 text-sm text-surface-400">
          ${UserCircleIcon({ className: 'h-5 w-5 text-surface-500' })}
          <span class="truncate text-surface-50">${state.dashboardData?.user_name || 'User'}</span>
        </div>
      </div>
    </aside>`;
}

function renderTopBar() {
    const nav = getNav();
    const current = nav.find(n => n.name === state.activePage);
    const pnlClass = state.todayPnl >= 0 ? 'text-emerald-400' : 'text-red-400';
    return `
    <header class="sticky top-0 z-20 bg-surface-900/90 backdrop-blur-md border-b border-surface-700/50">
      <div class="flex items-center justify-between h-12 px-4 lg:px-6">
        <div class="flex items-center gap-3">
          <button class="lg:hidden p-1.5 rounded-lg hover:bg-surface-800 text-surface-400" onclick="handleSidebarToggle()">
            ${Bars3Icon({ className: 'h-5 w-5' })}
          </button>
          <div class="hidden sm:flex items-center gap-2 text-sm">
            <span class="text-surface-500 font-mono text-xs font-semibold uppercase tracking-wider">PlutuZ</span>
            <span class="text-surface-600">/</span>
            <span class="text-surface-50 font-medium">${current?.name || 'Dashboard'}</span>
          </div>
        </div>
        <div class="flex items-center gap-4">
          <div class="hidden md:flex items-center gap-4 text-xs">
            <div class="flex items-center gap-1.5 text-surface-400">
              ${ActivityIcon({ className: 'h-3.5 w-3.5' })}
              <span class="flex items-center gap-1">
                <span class="live-dot ${state.systemOk ? 'bg-emerald-400' : 'bg-red-400'}"></span>
                ${state.systemOk ? 'System OK' : 'Check System'}
              </span>
            </div>
            <div class="flex items-center gap-1.5 text-surface-400">
              ${ClockIcon({ className: 'h-3.5 w-3.5' })}
              <span class="font-mono" id="header-clock">--:--:--</span>
            </div>
            <div class="flex items-center gap-1.5">
              <span class="text-surface-400">P&L:</span>
              <span class="font-mono font-semibold stat-value ${pnlClass}">${formatINR(state.todayPnl)}</span>
            </div>
          </div>
          <button onclick="window.${toggleTheme.name}()" class="p-1.5 rounded-lg hover:bg-surface-800 text-surface-400 hover:text-surface-50 transition-colors" title="Toggle theme">
            ${state.theme === 'dark' ? SunIcon({ className: 'h-4 w-4' }) : MoonIcon({ className: 'h-4 w-4' })}
          </button>
          <button onclick="window.${handleLogout.name}()" class="p-1.5 rounded-lg hover:bg-surface-800 text-surface-400 hover:text-red-400 transition-colors" title="Logout">
            ${ArrowRightOnRectangleIcon({ className: 'h-4 w-4' })}
          </button>
        </div>
      </div>
    </header>`;
}

function renderMobileNav() {
    return `
    <nav class="lg:hidden fixed bottom-0 left-0 right-0 z-30 bg-surface-800/95 backdrop-blur-md border-t border-surface-700 flex items-center justify-around h-14 px-1">
      ${MOBILE_NAV.map(item => {
          const isActive = state.activePage === item.name;
          return `
            <button data-page="${item.name}" class="mobile-nav-btn flex flex-col items-center gap-0.5 py-1 px-2 min-w-0 ${isActive ? 'active text-primary-400' : 'text-surface-500'}">
              ${item.icon({ className: 'h-5 w-5' })}
              <span class="text-[10px] font-medium truncate max-w-full">${item.name}</span>
            </button>`;
      }).join('')}
    </nav>`;
}

function render() {
    const root = document.getElementById('root');
    if (!root) return;
    window.toggleTheme = toggleTheme;
    window.handleLogout = handleLogout;
    window.handleSidebarToggle = () => { state.sidebarOpen = !state.sidebarOpen; render(); };

    if (state.loading) {
        root.innerHTML = `
        <div class="flex h-screen bg-surface-900">
          <div class="hidden lg:block w-64 bg-surface-800 border-r border-surface-700">
            <div class="skeleton h-14 m-5"></div>
            ${Array(6).fill(0).map(() => '<div class="skeleton h-10 mx-3 my-2"></div>').join('')}
          </div>
          <div class="flex-1 overflow-hidden">${SkeletonDashboard()}</div>
        </div>`;
        return;
    }

    if (state.error) {
        root.innerHTML = `<div class="min-h-screen bg-surface-900 flex items-center justify-center">${ErrorMessage({ message: state.error })}</div>`;
        return;
    }

    const modals = `
        ${state.isEditHunterModalOpen ? EditHunterConfigModal({ config: state.editingHunterConfig }) : ''}
        ${state.isEditScalperModalOpen ? EditScalperConfigModal({ config: state.editingScalperConfig }) : ''}
        ${state.isEditBrokerModalOpen ? EditBrokerInfoModal({ config: state.editingBrokerItem }) : ''}`;

    const toastHtml = state.toast ? `<div class="toast-fixed">${Toast(state.toast)}</div>` : '';

    root.innerHTML = `
    <div class="min-h-screen bg-surface-900 flex ${state.sidebarOpen ? 'sidebar-open' : ''}">
      ${renderSidebar()}
      <div class="flex-1 flex flex-col min-w-0 lg:pl-64">
        ${renderTopBar()}
        <main class="flex-1 overflow-auto p-4 lg:p-6 pb-16 lg:pb-6">
          ${renderPageContent()}
        </main>
        ${renderMobileNav()}
      </div>
    </div>
    <div id="modal-container">${modals}</div>
    <div id="toast-container">${toastHtml}</div>`;

    attachEventListeners();
}

function attachEventListeners() {
    document.querySelectorAll('.nav-item').forEach(btn => {
        btn.addEventListener('click', () => handleNavigate(btn.dataset.page));
    });
    document.querySelectorAll('.mobile-nav-btn').forEach(btn => {
        btn.addEventListener('click', () => handleNavigate(btn.dataset.page));
    });
    document.querySelector('.toast-close-button')?.addEventListener('click', () => {
        state.toast = null;
        document.getElementById('toast-container').innerHTML = '';
    });
    document.querySelectorAll('.modal-close-button').forEach(btn => {
        const map = { hunter: handleCloseEditHunterModal, scalper: handleCloseEditScalperModal, broker: handleCloseEditBrokerModal };
        const fn = map[btn.dataset.modal];
        if (fn) btn.addEventListener('click', fn);
    });
    document.getElementById('edit-hunter-form')?.addEventListener('submit', handleSaveHunterConfig);
    document.getElementById('edit-scalper-form')?.addEventListener('submit', handleSaveScalperConfig);
    document.getElementById('edit-broker-form')?.addEventListener('submit', handleSaveBrokerInfo);

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
    if (state.activePage === 'Settings') initSettingsPage();
    if (state.activePage === 'Admin Console') initAdminConsole();
    if (state.activePage === 'Log Viewer') initLogViewer();
    if (state.activePage === 'Manual Orders') attachManualOrdersListeners();
    if (state.activePage === 'Strategies') initStrategiesPage();
}

function attachManualOrdersListeners() {
    document.querySelectorAll('.manual-order-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const index = btn.dataset.index;
            const action = btn.dataset.action;
            const endpoint = action === 'buy' ? '/place_order_buy'
                : action === 'sell' ? '/place_order_sell'
                : '/place_order_exit';
            btn.disabled = true;
            btn.innerHTML = '<span class="animate-pulse">...</span>';
            try {
                const resp = await makeApiCall(endpoint, {
                    method: 'POST',
                    body: { index_name: index },
                });
                showToast(`${action} order for ${index}: ${resp?.message || 'sent'}`, 'success');
            } catch (err) {
                showToast(`${action} failed: ${err.message}`, 'error');
            } finally {
                btn.disabled = false;
                btn.innerHTML = action.charAt(0).toUpperCase() + action.slice(1);
            }
        });
    });

    function copyToClipboard(text, successMsg, failMsg) {
        if (navigator.clipboard && window.isSecureContext) {
            navigator.clipboard.writeText(text).then(() => showToast(successMsg, 'success')).catch(() => showToast(failMsg, 'error'));
        } else {
            const ta = document.createElement('textarea');
            ta.value = text;
            ta.style.position = 'fixed';
            ta.style.opacity = '0';
            document.body.appendChild(ta);
            ta.select();
            try { document.execCommand('copy'); showToast(successMsg, 'success'); } catch { showToast(failMsg, 'error'); }
            document.body.removeChild(ta);
        }
    }

    document.querySelectorAll('.copy-btn, .copy-content').forEach(el => {
        el.addEventListener('click', () => {
            const text = el.closest('td')?.querySelector('code, pre')?.textContent
                || el.previousElementSibling?.textContent
                || el.textContent;
            copyToClipboard(text.trim(), 'Copied to clipboard', 'Failed to copy');
        });
    });

    document.getElementById('copy-token-btn')?.addEventListener('click', () => {
        const input = document.getElementById('webhook-token-input');
        if (!input) return;
        copyToClipboard(input.value, 'Token copied to clipboard', 'Failed to copy token');
    });

    document.getElementById('regenerate-token-button')?.addEventListener('click', async () => {
        const btn = document.getElementById('regenerate-token-button');
        btn.disabled = true;
        btn.textContent = 'Regenerating...';
        try {
            const resp = await makeApiCall('/generate_auth_token', { method: 'POST' });
            if (resp?.status === 'success') {
                state.webhookToken = resp.message;
                document.getElementById('webhook-token-input').value = resp.message;
                showToast('Token regenerated successfully', 'success');
            } else {
                showToast('Failed to regenerate token', 'error');
            }
        } catch (err) {
            showToast(`Error: ${err.message}`, 'error');
        } finally {
            btn.disabled = false;
            btn.textContent = 'Regenerate Token';
        }
    });
}

export function init() {
    state.theme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', state.theme);
    setInterval(() => {
        const el = document.getElementById('header-clock');
        if (el) el.textContent = new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false });
    }, 1000);
    fetchAllData();
}
