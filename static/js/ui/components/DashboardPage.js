// Overview: today's and overall P&L plus per-strategy performance.
import { HomeIcon, ChartBarIcon, CheckCircleIcon, XCircleIcon, WalletIcon, ArrowPathIcon } from './icons.js';
import { makeApiCall } from '../utils/api.js';
import { toast } from '../utils/notify.js';
import { esc, formatINR, displayName, pnlClass, sum } from '../utils/format.js';
import { Button, Card, CardTitle, DataTable, PageHeader, withBusy } from './ui.js';
import SummaryCard from './SummaryCard.js';

let summary;
const listeners = new Set();

/** Other parts of the app (top bar P&L, user name) subscribe to summary updates. */
export function onSummary(fn) { listeners.add(fn); if (summary) fn(summary); }

export async function loadSummary() {
    try {
        summary = (await makeApiCall('/get_strategy_summary'))?.summary ?? {};
    } catch (err) {
        summary = summary || {};
        toast(`Could not load dashboard: ${err.message}`, 'error');
    }
    listeners.forEach(fn => fn(summary));
    render();
    return summary;
}

const strategyTable = (title, rows) => Card(`
    ${CardTitle(title, `<span class="text-sm font-semibold ${pnlClass(sum(rows, 'total_profit'))}">${formatINR(sum(rows, 'total_profit'))}</span>`)}
    ${DataTable({
        rows,
        empty: 'No data for this period',
        columns: [
            { label: 'Strategy', primary: true, render: r => esc(r.strategy) },
            { label: 'P&L', primary: true, align: 'right', render: r => `<span class="font-semibold ${pnlClass(r.total_profit)}">${formatINR(r.total_profit)}</span>` },
            { label: 'Index', render: r => esc(displayName(r.index_name)) },
            { label: 'Orders', align: 'center', render: r => esc(r.order_count) },
        ],
    })}`);

function render() {
    const el = document.getElementById('dashboard-page');
    if (!el) return;
    const refresh = Button({ label: `${ArrowPathIcon({ className: 'h-4 w-4' })}Refresh`, variant: 'ghost', size: 'sm', attrs: 'id="dashboard-refresh"' });
    if (!summary) {
        el.innerHTML = `${PageHeader({ title: 'Dashboard', icon: HomeIcon, subtitle: 'Trading performance overview' })}
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 lg:gap-4">${'<div class="skeleton h-28"></div>'.repeat(4)}</div>`;
        return;
    }
    const today = summary.current_day_summary || [];
    const full = summary.full_summary || [];
    const todayPnl = sum(today, 'total_profit');
    const overall = sum(full, 'total_profit');
    const icon = (I) => I({ className: 'h-5 w-5' });
    el.innerHTML = `
      ${PageHeader({ title: 'Dashboard', icon: HomeIcon, subtitle: 'Trading performance overview', actions: refresh })}
      <div class="space-y-5">
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 lg:gap-4">
          ${SummaryCard({ title: 'Orders Today', value: summary.total_orders_today || 0, icon: icon(ChartBarIcon), accent: 'indigo' })}
          ${SummaryCard({ title: 'Strategies Today', value: today.length, icon: icon(today.length ? CheckCircleIcon : XCircleIcon), accent: today.length ? 'green' : 'amber' })}
          ${SummaryCard({ title: "Today's P&L", value: formatINR(todayPnl, 0), icon: icon(WalletIcon), accent: todayPnl >= 0 ? 'green' : 'red' })}
          ${SummaryCard({ title: 'Overall P&L', value: formatINR(overall, 0), icon: icon(WalletIcon), accent: overall >= 0 ? 'green' : 'red' })}
        </div>
        <div class="grid grid-cols-1 xl:grid-cols-2 gap-5">
          ${strategyTable("Today's Performance", today)}
          ${strategyTable('Full Performance', full)}
        </div>
      </div>`;
    const btn = document.getElementById('dashboard-refresh');
    btn?.addEventListener('click', () => withBusy(btn, loadSummary));
}

export function initDashboard() { render(); }

export default () => '<div id="dashboard-page"></div>';
