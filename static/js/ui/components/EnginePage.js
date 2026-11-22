// Hunter, Scalper and Flash are the same shape: one config row per index with
// start / stop / edit. This page renders any of them from the ENGINES definition.
import { MagnifyingGlassIcon, BoltIcon, ArrowTrendingUpIcon, CogIcon, PlayCircleIcon, StopCircleIcon, PencilSquareIcon, ArrowPathIcon } from './icons.js';
import { makeApiCall, runAction } from '../utils/api.js';
import { toast } from '../utils/notify.js';
import { esc, displayName } from '../utils/format.js';
import { Button, PageHeader, EmptyState, StatusPill, YesNo, openFormModal, withBusy } from './ui.js';

const num = (name, label) => ({ name, label, type: 'number' });
const check = (name, label) => ({ name, label, type: 'checkbox' });

export const ENGINES = {
    hunter: {
        title: 'Hunter',
        subtitle: 'Level-based option buying, one config per index',
        icon: MagnifyingGlassIcon,
        load: async () => (await makeApiCall('/get_config_values'))?.all_config_values ?? [],
        update: '/update_config_values',
        start: (index) => ['/start_index', { index_name: index }],
        stop: (index) => ['/stop_index', { index_name: index, strategy: 'hunter' }],
        fields: [
            { name: 'levels', label: 'Levels (comma-separated)', type: 'textarea' },
            num('strike', 'Strike'), num('lots', 'Lots'),
            num('trend_check_points', 'Trend Check Points'), num('trailing_points', 'Trailing Points'),
            num('initial_sl', 'Initial SL'), num('safe_sl', 'Safe SL'),
            num('target_for_safe_sl', 'Target for Safe SL'),
            check('start_scheduler', 'Start scheduler'), check('is_place_sl_required', 'Place SL required'),
        ],
    },
    scalper: {
        title: 'Scalper',
        subtitle: 'Scalping strategy parameters',
        icon: BoltIcon,
        load: async () => (await makeApiCall('/get_scalper_details'))?.all_config_values ?? [],
        update: '/update_scalper_details',
        start: (index) => ['/start_scalper', { index_name: index, strategy: 'scalper' }],
        stop: (index) => ['/stop_index', { index_name: index, strategy: 'scalper' }],
        fields: [
            num('strike', 'Strike'), num('target', 'Target Points'), num('lots', 'Lots'),
            check('on_candle_close', 'On candle close'), check('use_full_capital', 'Use full capital'),
            check('is_demo_trading_enabled', 'Demo trading'),
        ],
    },
    flash: {
        title: 'Flash',
        subtitle: 'Flash trade parameters',
        icon: ArrowTrendingUpIcon,
        load: async () => {
            const resp = await makeApiCall('/get_flash_details');
            return Array.isArray(resp?.message) ? resp.message : [];
        },
        update: '/update_flash_details',
        start: (index) => ['/start_flash', { index_name: index, strategy: 'flash' }],
        stop: (index) => ['/stop_index', { index_name: index, strategy: 'flash' }],
        fields: [
            num('strike', 'Strike'), num('lots', 'Lots'),
            num('max_profit', 'Max Profit'), num('max_loss', 'Max Loss'),
            num('trend_check_points', 'Trend Check Points'), num('trailing_points', 'Trailing Points'),
            num('average_points', 'Average Points'),
            check('is_demo_trading_enabled', 'Demo trading'),
        ],
    },
};

const cache = {};   // engine key -> rows, so re-renders don't refetch

function valueHtml(field, value) {
    if (field.type === 'checkbox') return YesNo(value);
    if (value === null || value === undefined || value === '') return '<span class="text-surface-500">-</span>';
    return esc(value);
}

function EngineCard(engine, row) {
    const index = esc(row.index_name);
    const details = engine.fields.filter(f => f.type !== 'textarea');
    const long = engine.fields.filter(f => f.type === 'textarea');
    return `
    <div class="card flex flex-col">
      <div class="flex items-center justify-between gap-2 p-4 border-b border-surface-700">
        <h3 class="text-sm font-semibold text-surface-50 uppercase flex items-center gap-2 min-w-0">
          ${CogIcon({ className: 'h-5 w-5 text-primary-400 flex-shrink-0' })}<span class="truncate">${esc(displayName(row.index_name))}</span>
        </h3>
        ${StatusPill(row.status)}
      </div>
      <div class="p-4 space-y-3 flex-1">
        ${long.map(f => `
          <div>
            <p class="text-[11px] uppercase tracking-wider text-surface-500 mb-1">${esc(f.label)}</p>
            <p class="text-xs text-surface-200 bg-surface-900/60 p-2 rounded break-all max-h-32 overflow-y-auto font-mono">${esc(row[f.name]) || '-'}</p>
          </div>`).join('')}
        <dl class="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
          ${details.map(f => `<div class="min-w-0"><dt class="text-[11px] uppercase tracking-wider text-surface-500">${esc(f.label)}</dt><dd class="text-surface-100 break-words">${valueHtml(f, row[f.name])}</dd></div>`).join('')}
        </dl>
      </div>
      <div class="grid grid-cols-3 gap-2 p-3 border-t border-surface-700">
        ${Button({ label: `${PlayCircleIcon({ className: 'h-4 w-4' })}Start`, variant: 'success', size: 'sm', attrs: `data-engine-action="start" data-index="${index}"` })}
        ${Button({ label: `${StopCircleIcon({ className: 'h-4 w-4' })}Stop`, variant: 'danger', size: 'sm', attrs: `data-engine-action="stop" data-index="${index}"` })}
        ${Button({ label: `${PencilSquareIcon({ className: 'h-4 w-4' })}Edit`, variant: 'ghost', size: 'sm', attrs: `data-engine-action="edit" data-index="${index}"` })}
      </div>
    </div>`;
}

function renderInto(key) {
    const el = document.getElementById('engine-page');
    if (!el || el.dataset.engine !== key) return;
    const engine = ENGINES[key];
    const rows = cache[key];
    const refresh = Button({ label: `${ArrowPathIcon({ className: 'h-4 w-4' })}Refresh`, variant: 'ghost', size: 'sm', attrs: 'data-engine-action="refresh"' });
    el.innerHTML = `
      ${PageHeader({ title: engine.title, icon: engine.icon, subtitle: engine.subtitle, actions: refresh })}
      ${rows === undefined
        ? '<div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">' + '<div class="skeleton h-64"></div>'.repeat(3) + '</div>'
        : rows.length
            ? `<div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">${rows.map(r => EngineCard(engine, r)).join('')}</div>`
            : `<div class="card">${EmptyState({ title: `No ${engine.title} configuration`, message: 'Nothing is configured for your account yet.', icon: engine.icon })}</div>`}`;
}

async function load(key) {
    try {
        cache[key] = await ENGINES[key].load();
    } catch (err) {
        cache[key] = [];
        toast(`Could not load ${ENGINES[key].title}: ${err.message}`, 'error');
    }
    renderInto(key);
}

function openEdit(key, row) {
    const engine = ENGINES[key];
    openFormModal({
        title: `Edit ${engine.title}: ${displayName(row.index_name)}`,
        icon: engine.icon,
        fields: [{ name: 'index_name', label: 'Index', readonly: true, full: true }, ...engine.fields],
        values: row,
        onSubmit: async (values) => {
            const missing = engine.fields.find(f => f.type !== 'checkbox' && values[f.name] === '');
            if (missing) { toast(`${missing.label} is required`, 'error'); return false; }
            const res = await runAction(engine.update, { method: 'PUT', body: values });
            toast(res.message, res.ok ? 'success' : 'error');
            if (!res.ok) return false;
            await load(key);
            return true;
        },
    });
}

async function onClick(e) {
    const btn = e.target.closest('[data-engine-action]');
    const page = document.getElementById('engine-page');
    if (!btn || !page?.contains(btn)) return;
    const key = page.dataset.engine;
    const engine = ENGINES[key];
    const action = btn.dataset.engineAction;
    const index = btn.dataset.index;

    if (action === 'refresh') return withBusy(btn, () => load(key));
    if (action === 'edit') {
        const row = cache[key]?.find(r => r.index_name === index);
        if (row) openEdit(key, row);
        return;
    }
    if (action === 'stop' && !confirm(`Stop ${engine.title} for ${displayName(index)}?`)) return;
    await withBusy(btn, async () => {
        const [url, body] = engine[action](index);
        const res = await runAction(url, { method: 'POST', body });
        toast(res.message, res.ok ? 'success' : 'error');
        await load(key);
    });
}

let listening = false;

export function initEnginePage(key) {
    if (!listening) { document.addEventListener('click', onClick); listening = true; }
    renderInto(key);
    if (cache[key] === undefined) load(key);
}

export default function EnginePage(key) {
    return `<div id="engine-page" data-engine="${key}"></div>`;
}
