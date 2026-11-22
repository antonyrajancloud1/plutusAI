// Positions (open orders), Order Book and Manual Orders pages.
import { BookOpenIcon, PencilSquareIcon, ChartBarIcon, ArrowPathIcon, ClipboardIcon } from './icons.js';
import { makeApiCall, runAction } from '../utils/api.js';
import { toast } from '../utils/notify.js';
import { esc, formatINR, formatTime, displayName, pnlClass, sum } from '../utils/format.js';
import { Button, Card, CardTitle, DataTable, PageHeader, StatusPill, openFormModal, withBusy, inputClass, labelClass } from './ui.js';

const data = { open: undefined, book: undefined, manual: undefined, token: '' };

const pnlHtml = (n) => `<span class="font-semibold ${pnlClass(n)}">${formatINR(n)}</span>`;
const refreshBtn = (target) => Button({ label: `${ArrowPathIcon({ className: 'h-4 w-4' })}Refresh`, variant: 'ghost', size: 'sm', attrs: `data-orders-action="refresh" data-target="${target}"` });
const skeleton = '<div class="skeleton h-48"></div>';

function mount(id, html) {
    const el = document.getElementById(id);
    if (el) el.innerHTML = html;
}

// ------------------------------------------------------------------ positions

const openPnl = (o) => ((parseFloat(o.ltp) || 0) - (parseFloat(o.entry_price) || 0)) * (parseFloat(o.qty) || 0);

function renderOpen() {
    const rows = data.open;
    const total = (rows || []).reduce((a, o) => a + openPnl(o), 0);
    const actions = `${refreshBtn('open')}${rows?.length ? Button({ label: 'Exit All', variant: 'danger', size: 'sm', attrs: 'data-orders-action="exit-all"' }) : ''}`;
    mount('open-orders-page', `
      ${PageHeader({ title: 'Positions', icon: ChartBarIcon, subtitle: 'Open orders with live LTP', actions })}
      ${rows === undefined ? skeleton : Card(`
        ${CardTitle(`${rows.length} open`, `<span class="text-sm text-surface-400">Unrealised P&amp;L: ${pnlHtml(total)}</span>`)}
        ${DataTable({
            rows,
            empty: 'No open orders',
            columns: [
                { label: 'Script', primary: true, render: o => esc(o.script_name) },
                { label: 'Strategy', render: o => esc(o.strategy) },
                { label: 'Index', render: o => esc(displayName(o.index_name)) },
                { label: 'Entry Time', render: o => formatTime(o.entry_time) },
                { label: 'Qty', align: 'right', render: o => esc(o.qty) },
                { label: 'Entry', align: 'right', render: o => formatINR(o.entry_price) },
                { label: 'LTP', align: 'right', render: o => formatINR(o.ltp) },
                { label: 'P&L', align: 'right', render: o => pnlHtml(openPnl(o)) },
                { label: 'Action', align: 'right', wide: true, render: (o) => Button({ label: 'Exit', variant: 'warning', size: 'sm', attrs: `data-orders-action="exit-one" data-index="${esc(o.index_name)}" data-strategy="${esc(o.strategy)}"` }) },
            ],
        })}`)}`);
}

async function loadOpen() {
    try {
        data.open = (await makeApiCall('/all_open_orders'))?.open_orders ?? [];
    } catch (err) {
        data.open = [];
        toast(`Could not load positions: ${err.message}`, 'error');
    }
    renderOpen();
}

const exitPosition = (index_name, strategy) => runAction('/place_order_exit', { method: 'POST', body: { index_name, strategy } });

// ------------------------------------------------------------------ order book

function renderBook() {
    const rows = data.book;
    const query = (document.getElementById('book-filter')?.value || '').toLowerCase();
    const shown = (rows || []).filter(r => !query || [r.script_name, r.strategy, r.index_name, r.status].some(v => String(v || '').toLowerCase().includes(query)));
    const total = sum(shown, 'total');
    mount('order-book-list', rows === undefined ? skeleton : `
        ${CardTitle(`${shown.length} orders`, `<span class="text-sm text-surface-400">Total P&amp;L: ${pnlHtml(total)}</span>`)}
        ${DataTable({
            rows: shown,
            empty: 'No orders found',
            columns: [
                { label: 'Script', primary: true, render: r => esc(r.script_name) },
                { label: 'Status', primary: true, render: r => StatusPill(r.status) },
                { label: 'Entry Time', render: r => formatTime(r.entry_time) },
                { label: 'Exit Time', render: r => formatTime(r.exit_time) },
                { label: 'Qty', align: 'right', render: r => esc(r.qty) },
                { label: 'Entry', align: 'right', render: r => formatINR(r.entry_price) },
                { label: 'Exit', align: 'right', render: r => (r.exit_price === '' ? '-' : formatINR(r.exit_price)) },
                { label: 'P&L', align: 'right', render: r => pnlHtml(parseFloat(r.total) || 0) },
                { label: 'Strategy', render: r => esc(r.strategy || '-') },
                { label: 'Index', render: r => esc(displayName(r.index_name) || '-') },
            ],
        })}`);
}

function renderBookShell() {
    mount('order-book-page', `
      ${PageHeader({ title: 'Order Book', icon: BookOpenIcon, subtitle: 'All your orders, newest first', actions: refreshBtn('book') })}
      ${Card(`
        <input id="book-filter" type="search" placeholder="Filter by script, strategy, index or status" class="${inputClass} mt-0 mb-4" />
        <div id="order-book-list"></div>`)}`);
    document.getElementById('book-filter')?.addEventListener('input', renderBook);
    renderBook();
}

async function loadBook() {
    try {
        data.book = (await makeApiCall('/get_order_book_details'))?.order_book_details ?? [];
    } catch (err) {
        data.book = [];
        toast(`Could not load order book: ${err.message}`, 'error');
    }
    renderBook();
}

// ------------------------------------------------------------------ manual orders + webhooks

const STRATEGY_KEY = 'manualStrategyName';
const DEFAULT_STRATEGY = 'default_strategy';

function strategyName() {
    try { return localStorage.getItem(STRATEGY_KEY) || DEFAULT_STRATEGY; } catch { return DEFAULT_STRATEGY; }
}

const MANUAL_FIELDS = [
    { name: 'lots', label: 'Lots', type: 'number' },
    { name: 'trigger', label: 'Trigger', type: 'number' },
    { name: 'stop_loss', label: 'Stop Loss', type: 'number' },
    { name: 'target', label: 'Target', type: 'number' },
    { name: 'strike', label: 'Strike', type: 'number' },
];

function webhookUrl(path) {
    return `${window.location.origin}/${path}?token=${encodeURIComponent(data.token)}`;
}

function CopyBlock(text, label) {
    return `<button type="button" data-copy="${esc(text)}" data-copy-label="${esc(label)} copied" class="group w-full flex items-start gap-2 text-left font-mono text-xs text-surface-300 bg-surface-900/60 hover:bg-surface-900 rounded p-2 break-all">
        <span class="flex-1 whitespace-pre-wrap">${esc(text)}</span>${ClipboardIcon({ className: 'h-4 w-4 flex-shrink-0 text-surface-500 group-hover:text-surface-200' })}</button>`;
}

function renderManual() {
    const rows = data.manual;
    const name = strategyName();
    const webhookRows = (rows || []).map(r => ({
        index_name: r.index_name,
        input: JSON.stringify({ index_name: r.index_name, strategy: name === DEFAULT_STRATEGY ? `${r.index_name}_${DEFAULT_STRATEGY}` : `${r.index_name}_${name}` }),
    }));

    mount('manual-orders-page', `
      ${PageHeader({ title: 'Manual Orders', icon: PencilSquareIcon, subtitle: 'Place, exit and configure orders by hand', actions: refreshBtn('manual') })}
      <div class="space-y-5">
        ${Card(`
          <label for="strategy-name-input" class="${labelClass}">Strategy name used for these buttons</label>
          <input id="strategy-name-input" type="text" value="${esc(name)}" class="${inputClass} sm:max-w-xs" />
          <p class="text-xs text-surface-500 mt-1">Buy, Sell and Exit use this name, so Exit closes the position opened with the same name.</p>`)}
        ${rows === undefined ? skeleton : Card(DataTable({
            rows,
            empty: 'No manual orders configured',
            columns: [
                { label: 'Index', primary: true, render: r => esc(displayName(r.index_name)) },
                { label: 'Status', primary: true, render: r => StatusPill(r.order_status || 'none') },
                { label: 'Lots', align: 'right', render: r => esc(r.lots) },
                { label: 'Trigger', align: 'right', render: r => esc(r.trigger) },
                { label: 'Stop Loss', align: 'right', render: r => esc(r.stop_loss) },
                { label: 'Target', align: 'right', render: r => esc(r.target) },
                { label: 'Strike', align: 'right', render: r => esc(r.strike) },
                { label: 'Actions', wide: true, render: r => `<div class="grid grid-cols-4 md:flex gap-1.5">
                    ${Button({ label: 'Buy', variant: 'success', size: 'sm', attrs: `data-orders-action="buy" data-index="${esc(r.index_name)}"` })}
                    ${Button({ label: 'Sell', variant: 'danger', size: 'sm', attrs: `data-orders-action="sell" data-index="${esc(r.index_name)}"` })}
                    ${Button({ label: 'Exit', variant: 'warning', size: 'sm', attrs: `data-orders-action="exit" data-index="${esc(r.index_name)}"` })}
                    ${Button({ label: 'Edit', variant: 'ghost', size: 'sm', attrs: `data-orders-action="edit" data-index="${esc(r.index_name)}"` })}
                  </div>` },
            ],
        }))}
        ${Card(`
          ${CardTitle('Webhook Details')}
          <div class="flex flex-col sm:flex-row gap-2 mb-4">
            <input id="webhook-token-input" type="text" readonly value="${esc(data.token)}" class="${inputClass} mt-0 font-mono flex-1" aria-label="Webhook token" />
            <div class="grid grid-cols-2 sm:flex gap-2">
              ${Button({ label: 'Copy', variant: 'ghost', attrs: `data-copy="${esc(data.token)}" data-copy-label="Token copied"` })}
              ${Button({ label: 'Regenerate', variant: 'primary', attrs: 'data-orders-action="regenerate-token"' })}
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-4">
            ${['trigger_buy', 'trigger_sell', 'trigger_exit'].map(p => `<div><p class="text-[11px] uppercase tracking-wider text-surface-500 mb-1">${esc(displayName(p.replace('trigger_', '')))} URL</p>${CopyBlock(webhookUrl(p), 'URL')}</div>`).join('')}
          </div>
          ${DataTable({
              rows: webhookRows,
              empty: 'Configure manual orders to see webhook payloads',
              columns: [
                  { label: 'Index', primary: true, render: r => esc(displayName(r.index_name)) },
                  { label: 'Input Data (alert message)', wide: true, render: r => CopyBlock(r.input, 'Input data') },
              ],
          })}`)}
      </div>`);

    document.getElementById('strategy-name-input')?.addEventListener('change', (e) => {
        try { localStorage.setItem(STRATEGY_KEY, e.target.value.trim() || DEFAULT_STRATEGY); } catch { /* private mode */ }
        renderManual();
    });
}

async function loadManual() {
    const [manual, token] = await Promise.all([
        makeApiCall('/manual_details').catch(() => null),
        makeApiCall('/get_auth_token', { method: 'POST' }).catch(() => null),
    ]);
    data.manual = Array.isArray(manual?.message) ? manual.message : [];
    data.token = token?.message || '';
    renderManual();
}

function openManualEdit(row) {
    openFormModal({
        title: `Edit Order: ${displayName(row.index_name)}`,
        icon: PencilSquareIcon,
        fields: MANUAL_FIELDS,
        values: row,
        onSubmit: async (values) => {
            if (Object.values(values).some(v => v === '')) { toast('Please fill all the fields', 'error'); return false; }
            const res = await runAction('/update_manual_details', { method: 'PUT', body: { index_name: row.index_name, ...values } });
            toast(res.message, res.ok ? 'success' : 'error');
            if (!res.ok) return false;
            await loadManual();
            return true;
        },
    });
}

// ------------------------------------------------------------------ events

const loaders = { open: loadOpen, book: loadBook, manual: loadManual };

async function onClick(e) {
    const btn = e.target.closest('[data-orders-action]');
    if (!btn) return;
    const { ordersAction: action, index, strategy } = btn.dataset;

    switch (action) {
        case 'refresh':
            return withBusy(btn, loaders[btn.dataset.target]);
        case 'exit-one':
            if (!confirm(`Exit ${strategy} (${displayName(index)})?`)) return;
            return withBusy(btn, async () => {
                const res = await exitPosition(index, strategy);
                toast(res.message, res.ok ? 'success' : 'error');
                await loadOpen();
            });
        case 'exit-all':
            if (!confirm(`Exit all ${data.open.length} open positions?`)) return;
            return withBusy(btn, async () => {
                const failed = [];
                for (const o of data.open) {
                    const res = await exitPosition(o.index_name, o.strategy);
                    if (!res.ok) failed.push(`${o.strategy}: ${res.message}`);
                }
                toast(failed.length ? `Some exits failed - ${failed.join('; ')}` : 'All open orders exited', failed.length ? 'error' : 'success', 8000);
                await loadOpen();
            });
        case 'buy':
        case 'sell':
        case 'exit': {
            if (action === 'exit' && !confirm(`Exit ${displayName(index)} (${strategyName()})?`)) return;
            const url = { buy: '/place_order_buy', sell: '/place_order_sell', exit: '/place_order_exit' }[action];
            return withBusy(btn, async () => {
                const res = await runAction(url, { method: 'POST', body: { index_name: index, strategy: strategyName() } });
                toast(`${displayName(action)} ${displayName(index)}: ${res.message}`, res.ok ? 'success' : 'error');
                await loadManual();
            });
        }
        case 'edit': {
            const row = data.manual?.find(r => r.index_name === index);
            if (row) openManualEdit(row);
            return;
        }
        case 'regenerate-token':
            if (!confirm('Regenerate the webhook token? Existing TradingView alerts will stop working until you update them.')) return;
            return withBusy(btn, async () => {
                const res = await runAction('/generate_auth_token', { method: 'POST' });
                if (res.ok) { data.token = res.data.message; renderManual(); toast('Token regenerated', 'success'); } else toast(res.message, 'error');
            });
    }
}

let listening = false;
function listen() {
    if (!listening) { document.addEventListener('click', onClick); listening = true; }
}

export function initOpenOrders() { listen(); renderOpen(); loadOpen(); }
export function initOrderBook() { listen(); renderBookShell(); if (data.book === undefined) loadBook(); }
export function initManualOrders() { listen(); renderManual(); if (data.manual === undefined) loadManual(); }

export const OpenOrdersPage = () => '<div id="open-orders-page"></div>';
export const OrderBookPage = () => '<div id="order-book-page"></div>';
export const ManualOrdersPage = () => '<div id="manual-orders-page"></div>';
