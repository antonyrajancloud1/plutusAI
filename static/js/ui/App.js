// App shell: sidebar (desktop) / bottom bar + "More" sheet (mobile), top bar, and
// hash routing (#/hunter) so refresh, bookmarks and the phone's back button work.
// Each page owns its data and renders into its own container.
import {
    HomeIcon, BookOpenIcon, MagnifyingGlassIcon, PencilSquareIcon, BoltIcon, BuildingLibraryIcon,
    CogIcon, ChartBarIcon, SunIcon, MoonIcon, UserCircleIcon, ArrowRightOnRectangleIcon, Bars3Icon,
    XMarkIcon, ShieldCheckIcon, ListBulletIcon, ClockIcon, ActivityIcon, ArrowTrendingUpIcon,
} from './components/icons.js';
import { makeApiCall } from './utils/api.js';
import { esc, formatINR, pnlClass, sum } from './utils/format.js';
import { closeModal } from './components/ui.js';
import DashboardPage, { initDashboard, loadSummary, onSummary } from './components/DashboardPage.js';
import EnginePage, { initEnginePage } from './components/EnginePage.js';
import { OpenOrdersPage, OrderBookPage, ManualOrdersPage, initOpenOrders, initOrderBook, initManualOrders } from './components/OrdersPages.js';
import BrokerPage, { initBrokerPage } from './components/BrokerPage.js';
import StrategiesPage, { initStrategiesPage } from './components/StrategiesPage.js';
import LogViewerPage, { initLogViewer } from './components/LogViewerPage.js';
import AdminConsolePage, { initAdminConsole } from './components/AdminConsolePage.js';
import TelegramSettingsPage, { initSettingsPage } from './components/TelegramSettingsPage.js';

const PAGES = [
    { slug: 'dashboard', name: 'Dashboard', icon: HomeIcon, view: DashboardPage, init: initDashboard },
    { slug: 'positions', name: 'Positions', icon: ChartBarIcon, view: OpenOrdersPage, init: initOpenOrders },
    { slug: 'order-book', name: 'Order Book', icon: BookOpenIcon, view: OrderBookPage, init: initOrderBook },
    { slug: 'manual', name: 'Manual Orders', short: 'Manual', icon: PencilSquareIcon, view: ManualOrdersPage, init: initManualOrders },
    { slug: 'strategies', name: 'Strategies', icon: ShieldCheckIcon, view: StrategiesPage, init: initStrategiesPage },
    { slug: 'hunter', name: 'Hunter', icon: MagnifyingGlassIcon, view: () => EnginePage('hunter'), init: () => initEnginePage('hunter') },
    { slug: 'scalper', name: 'Scalper', icon: BoltIcon, view: () => EnginePage('scalper'), init: () => initEnginePage('scalper') },
    { slug: 'flash', name: 'Flash', icon: ArrowTrendingUpIcon, view: () => EnginePage('flash'), init: () => initEnginePage('flash') },
    { slug: 'broker', name: 'Broker Info', icon: BuildingLibraryIcon, view: BrokerPage, init: initBrokerPage },
    { slug: 'logs', name: 'Log Viewer', short: 'Logs', icon: ListBulletIcon, view: LogViewerPage, init: initLogViewer },
    { slug: 'admin', name: 'Admin Console', short: 'Admin', icon: ShieldCheckIcon, view: AdminConsolePage, init: initAdminConsole, admin: true },
    { slug: 'settings', name: 'Settings', icon: CogIcon, view: TelegramSettingsPage, init: initSettingsPage },
];
const BOTTOM_NAV = ['dashboard', 'positions', 'manual', 'strategies'];

const state = { isAdmin: false, page: 'dashboard', menuOpen: false, theme: 'dark', liveFeed: null };

const visiblePages = () => PAGES.filter(p => !p.admin || state.isAdmin);
const pageFor = (slug) => visiblePages().find(p => p.slug === slug) || PAGES[0];

// ------------------------------------------------------------------ shell

function navButton(p, extra = '') {
    return `
      <a href="#/${p.slug}" data-nav="${p.slug}" class="nav-item w-full flex items-center gap-3 px-3 py-3 lg:py-2.5 rounded-lg text-sm font-medium text-surface-400 hover:text-surface-50 ${extra}">
        ${p.icon({ className: 'h-5 w-5 flex-shrink-0' })}<span>${p.name}</span>
        ${p.admin ? '<span class="ml-auto px-1.5 py-0.5 text-[10px] font-semibold bg-primary-500/20 text-primary-300 rounded">ADMIN</span>' : ''}
      </a>`;
}

function shellHtml() {
    const bottom = BOTTOM_NAV.map(pageFor);
    return `
    <div class="min-h-screen bg-surface-900">
      <div id="menu-overlay" class="fixed inset-0 bg-black/50 z-30 lg:hidden hidden"></div>
      <aside id="sidebar" class="sidebar-panel fixed top-0 left-0 z-40 h-full w-72 lg:w-64 max-w-[85vw] bg-surface-800 border-r border-surface-700 -translate-x-full lg:translate-x-0 flex flex-col">
        <div class="flex items-center justify-between h-14 px-5 border-b border-surface-700 pt-[env(safe-area-inset-top)]">
          <span class="text-lg font-bold text-surface-50 tracking-tight">Plutu<span class="text-primary-400">Z</span></span>
          <button id="menu-close" class="lg:hidden p-2 -mr-2 rounded-lg hover:bg-surface-700 text-surface-400" aria-label="Close menu">${XMarkIcon({ className: 'h-5 w-5' })}</button>
        </div>
        <nav id="side-nav" class="flex-1 overflow-y-auto py-3 px-2 space-y-0.5">${visiblePages().map(p => navButton(p)).join('')}</nav>
        <div class="p-3 border-t border-surface-700 pb-[max(0.75rem,env(safe-area-inset-bottom))]">
          <div class="flex items-center gap-3 px-3 py-2 text-sm">
            ${UserCircleIcon({ className: 'h-5 w-5 text-surface-500' })}<span id="user-name" class="truncate text-surface-50">User</span>
          </div>
        </div>
      </aside>

      <div class="flex flex-col min-w-0 lg:pl-64">
        <header class="sticky top-0 z-20 bg-surface-900/90 backdrop-blur-md border-b border-surface-700/50 pt-[env(safe-area-inset-top)]">
          <div class="flex items-center justify-between h-12 px-3 sm:px-4 lg:px-6 gap-2">
            <div class="flex items-center gap-2 min-w-0">
              <button id="menu-open" class="lg:hidden p-2 -ml-1 rounded-lg hover:bg-surface-800 text-surface-400" aria-label="Open menu">${Bars3Icon({ className: 'h-5 w-5' })}</button>
              <span class="text-surface-500 font-mono text-xs font-semibold uppercase tracking-wider hidden sm:inline">PlutuZ</span>
              <span class="text-surface-600 hidden sm:inline">/</span>
              <span id="page-title" class="text-surface-50 font-medium text-sm truncate"></span>
            </div>
            <div class="flex items-center gap-3 sm:gap-4 text-xs">
              <span class="flex items-center gap-1.5 text-surface-400" title="Market data feed">
                ${ActivityIcon({ className: 'h-3.5 w-3.5 hidden sm:block' })}<span id="live-dot" class="live-dot bg-surface-500"></span><span id="live-text" class="hidden md:inline">Feed</span>
              </span>
              <span class="hidden md:flex items-center gap-1.5 text-surface-400">${ClockIcon({ className: 'h-3.5 w-3.5' })}<span class="font-mono" id="header-clock">--:--:--</span></span>
              <span class="flex items-center gap-1"><span class="text-surface-400 hidden sm:inline">P&amp;L:</span><span id="top-pnl" class="font-mono font-semibold stat-value">-</span></span>
              <button id="theme-toggle" class="p-2 rounded-lg hover:bg-surface-800 text-surface-400 hover:text-surface-50" title="Toggle theme"></button>
              <button id="logout" class="p-2 -mr-1 rounded-lg hover:bg-surface-800 text-surface-400 hover:text-red-400" title="Logout">${ArrowRightOnRectangleIcon({ className: 'h-4 w-4' })}</button>
            </div>
          </div>
        </header>

        <main id="page" class="flex-1 p-3 sm:p-4 lg:p-6 pb-24 lg:pb-6"></main>
      </div>

      <nav class="lg:hidden fixed bottom-0 inset-x-0 z-30 bg-surface-800/95 backdrop-blur-md border-t border-surface-700 grid grid-cols-5 pb-[env(safe-area-inset-bottom)]">
        ${bottom.map(p => `
          <a href="#/${p.slug}" data-nav="${p.slug}" class="mobile-nav-btn flex flex-col items-center justify-center gap-0.5 h-14 text-surface-500">
            ${p.icon({ className: 'h-5 w-5' })}<span class="text-[10px] font-medium">${p.short || p.name}</span>
          </a>`).join('')}
        <button id="menu-more" class="mobile-nav-btn flex flex-col items-center justify-center gap-0.5 h-14 text-surface-500">
          ${Bars3Icon({ className: 'h-5 w-5' })}<span class="text-[10px] font-medium">More</span>
        </button>
      </nav>
    </div>
    <div id="modal-container"></div>`;
}

function setMenu(open) {
    state.menuOpen = open;
    document.getElementById('sidebar')?.classList.toggle('-translate-x-full', !open);
    document.getElementById('menu-overlay')?.classList.toggle('hidden', !open);
}

function paintTheme() {
    document.documentElement.setAttribute('data-theme', state.theme);
    const btn = document.getElementById('theme-toggle');
    if (btn) btn.innerHTML = (state.theme === 'dark' ? SunIcon : MoonIcon)({ className: 'h-4 w-4' });
}

function paintLiveFeed() {
    const dot = document.getElementById('live-dot');
    const text = document.getElementById('live-text');
    if (!dot) return;
    const on = state.liveFeed;
    dot.className = `live-dot ${on === null ? 'bg-surface-500' : on ? 'bg-emerald-400' : 'bg-red-400'}`;
    if (text) text.textContent = on === null ? 'Feed' : on ? 'Feed live' : 'Feed off';
}

function paintSummary(s) {
    const pnl = sum(s.current_day_summary, 'total_profit');
    const el = document.getElementById('top-pnl');
    if (el) { el.textContent = formatINR(pnl, 0); el.className = `font-mono font-semibold stat-value ${pnlClass(pnl)}`; }
    const name = document.getElementById('user-name');
    if (name && s.user_name) name.innerHTML = esc(s.user_name);
}

// ------------------------------------------------------------------ routing

function route() {
    const slug = (window.location.hash.match(/^#\/([\w-]+)/) || [])[1] || 'dashboard';
    const page = pageFor(slug);
    if (`#/${page.slug}` !== window.location.hash) history.replaceState(null, '', `#/${page.slug}`);
    state.page = page.slug;

    closeModal();
    setMenu(false);
    document.querySelectorAll('[data-nav]').forEach(a => {
        const active = a.dataset.nav === page.slug;
        a.classList.toggle('active', active);
        a.classList.toggle('text-primary-300', active);
        a.classList.toggle('text-surface-400', !active && a.classList.contains('nav-item'));
        if (a.classList.contains('mobile-nav-btn')) {
            a.classList.toggle('text-primary-400', active);
            a.classList.toggle('text-surface-500', !active);
        }
    });
    document.getElementById('page-title').textContent = page.name;
    document.title = `${page.name} · PlutuZ`;

    const main = document.getElementById('page');
    main.innerHTML = `<div class="page-enter">${page.view()}</div>`;
    window.scrollTo(0, 0);
    page.init();
}

// ------------------------------------------------------------------ start

async function checkLiveFeed() {
    try {
        state.liveFeed = !!(await makeApiCall('/check_task_status'))?.task_status;
    } catch { state.liveFeed = false; }
    paintLiveFeed();
}

function bindShell() {
    document.getElementById('menu-open').addEventListener('click', () => setMenu(true));
    document.getElementById('menu-more').addEventListener('click', () => setMenu(true));
    document.getElementById('menu-close').addEventListener('click', () => setMenu(false));
    document.getElementById('menu-overlay').addEventListener('click', () => setMenu(false));
    document.getElementById('theme-toggle').addEventListener('click', () => {
        state.theme = state.theme === 'light' ? 'dark' : 'light';
        try { localStorage.setItem('theme', state.theme); } catch { /* private mode */ }
        paintTheme();
    });
    document.getElementById('logout').addEventListener('click', async () => {
        try { await makeApiCall('/logout'); } catch { /* going to login anyway */ }
        window.location.href = '/login';
    });
}

export async function init() {
    try { state.theme = localStorage.getItem('theme') || 'dark'; } catch { state.theme = 'dark'; }
    document.documentElement.setAttribute('data-theme', state.theme);

    const root = document.getElementById('root');
    root.innerHTML = '<div class="min-h-screen flex items-center justify-center"><div class="skeleton h-10 w-40"></div></div>';

    // Admin decides which pages exist, so it's needed before the shell is drawn.
    state.isAdmin = !!(await makeApiCall('/check_admin').catch(() => null))?.is_admin;

    root.innerHTML = shellHtml();
    bindShell();
    paintTheme();
    paintLiveFeed();
    onSummary(paintSummary);
    window.addEventListener('hashchange', route);
    route();

    loadSummary();
    checkLiveFeed();
    setInterval(checkLiveFeed, 60000);
    setInterval(() => {
        const el = document.getElementById('header-clock');
        if (el) el.textContent = new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false });
    }, 1000);
}
