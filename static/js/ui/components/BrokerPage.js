// Broker accounts: view, edit, check token, regenerate the broker session.
import { BuildingLibraryIcon, PencilSquareIcon, ArrowPathIcon, CheckCircleIcon } from './icons.js';
import { makeApiCall, runAction } from '../utils/api.js';
import { toast } from '../utils/notify.js';
import { esc, displayName } from '../utils/format.js';
import { Button, Card, PageHeader, EmptyState, YesNo, openFormModal, withBusy } from './ui.js';

const TOKEN_STATUS_OPTIONS = ['added', 'generated', 'active', 'expired', 'pending', 'error', 'revoked']
    .map(s => ({ value: s, label: displayName(s) }));

const ANGEL_FIELDS = [
    { name: 'broker_user_id', label: 'User ID' },
    { name: 'broker_user_name', label: 'User Name' },
    { name: 'broker_mpin', label: 'MPIN' },
    { name: 'broker_api_token', label: 'API Token' },
    { name: 'broker_qr', label: 'QR Code (TOTP secret)', full: true },
    { name: 'token_status', label: 'Token Status', type: 'select', options: TOKEN_STATUS_OPTIONS },
    { name: 'is_demo_trading_enabled', label: 'Demo trading', type: 'checkbox' },
];
const FOREX_FIELDS = [
    { name: 'broker_user_id', label: 'User ID' },
    { name: 'broker_password', label: 'Password' },
    { name: 'broker_forex_server', label: 'Server', full: true },
    { name: 'is_demo_trading_enabled', label: 'Demo trading', type: 'checkbox' },
];

const fieldsFor = (row) => (row.index_group === 'forex' ? FOREX_FIELDS : ANGEL_FIELDS);
let brokers;

const tokenPill = (status) => {
    const s = String(status || '').toLowerCase();
    const cls = ['generated', 'active'].includes(s) ? 'bg-emerald-500/10 text-emerald-400'
        : ['expired', 'revoked', 'error'].includes(s) ? 'bg-red-500/10 text-red-400'
        : 'bg-amber-500/10 text-amber-400';
    return `<span class="px-2 py-0.5 text-xs font-semibold rounded-full ${cls}">${esc(status || '-')}</span>`;
};

function BrokerCard(row, i) {
    const fields = fieldsFor(row).filter(f => f.type !== 'checkbox' && f.name !== 'token_status');
    const isAngel = row.index_group !== 'forex';
    return Card(`
      <div class="flex flex-wrap items-center justify-between gap-2 mb-4">
        <h2 class="text-base font-semibold text-surface-50 flex items-center gap-2">
          ${BuildingLibraryIcon({ className: 'h-5 w-5 text-primary-400' })}${esc(displayName(row.broker_name))}
          <span class="text-xs font-normal text-surface-500">${esc(displayName(row.index_group))}</span>
        </h2>
        ${tokenPill(row.token_status)}
      </div>
      <dl class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-3 text-sm">
        ${fields.map(f => `<div class="min-w-0"><dt class="text-[11px] uppercase tracking-wider text-surface-500">${esc(f.label)}</dt><dd class="text-surface-200 break-all font-mono text-xs mt-0.5">${esc(row[f.name]) || '<span class="text-surface-500">Not set</span>'}</dd></div>`).join('')}
        <div><dt class="text-[11px] uppercase tracking-wider text-surface-500">Demo Trading</dt><dd class="mt-0.5">${YesNo(row.is_demo_trading_enabled)}</dd></div>
      </dl>
      <div class="grid grid-cols-1 sm:flex gap-2 mt-5">
        ${Button({ label: `${PencilSquareIcon({ className: 'h-4 w-4' })}Edit`, variant: 'ghost', attrs: `data-broker-action="edit" data-i="${i}"` })}
        ${isAngel ? Button({ label: `${CheckCircleIcon({ className: 'h-4 w-4' })}Check Token`, variant: 'ghost', attrs: 'data-broker-action="check"' }) : ''}
        ${isAngel ? Button({ label: `${ArrowPathIcon({ className: 'h-4 w-4' })}Regenerate Session`, variant: 'primary', attrs: 'data-broker-action="regenerate"' }) : ''}
      </div>`);
}

function render() {
    const el = document.getElementById('broker-page');
    if (!el) return;
    el.innerHTML = `
      ${PageHeader({ title: 'Broker Info', icon: BuildingLibraryIcon, subtitle: 'Broker accounts linked to your login' })}
      ${brokers === undefined ? '<div class="skeleton h-64"></div>'
        : brokers.length ? `<div class="grid grid-cols-1 xl:grid-cols-2 gap-4">${brokers.map(BrokerCard).join('')}</div>`
        : `<div class="card">${EmptyState({ title: 'No broker linked', message: 'Ask the admin to add your broker details.', icon: BuildingLibraryIcon })}</div>`}`;
}

async function load() {
    try {
        brokers = (await makeApiCall('/get_broker_details'))?.broker_details ?? [];
    } catch (err) {
        brokers = [];
        toast(`Could not load broker info: ${err.message}`, 'error');
    }
    render();
}

function openEdit(row) {
    const fields = fieldsFor(row);
    openFormModal({
        title: `Edit Broker: ${displayName(row.broker_name)}`,
        icon: BuildingLibraryIcon,
        fields,
        values: row,
        onSubmit: async (values) => {
            const body = { ...values, broker_name: row.broker_name, index_group: row.index_group };
            const res = await runAction('/edit_broker_details', { method: 'PUT', body });
            toast(res.message, res.ok ? 'success' : 'error');
            if (!res.ok) return false;
            await load();
            return true;
        },
    });
}

async function onClick(e) {
    const btn = e.target.closest('[data-broker-action]');
    if (!btn) return;
    const action = btn.dataset.brokerAction;
    if (action === 'edit') return openEdit(brokers[Number(btn.dataset.i)]);
    const url = action === 'check' ? '/check_broker_status' : '/regenerate_token';
    const options = action === 'check' ? {} : { method: 'POST' };
    await withBusy(btn, async () => {
        const res = await runAction(url, options);
        toast(res.message, res.ok ? 'success' : 'error');
        if (action === 'regenerate' && res.ok) await load();
    });
}

let listening = false;
export function initBrokerPage() {
    if (!listening) { document.addEventListener('click', onClick); listening = true; }
    render();
    if (brokers === undefined) load();
}

export default () => '<div id="broker-page"></div>';
