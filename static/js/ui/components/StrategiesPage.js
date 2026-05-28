import { makeApiCall } from '../utils/api.js';
import { PlusIcon } from './icons.js';

const indices = [
    { key: 'nifty', name: 'Nifty' },
    { key: 'bank_nifty', name: 'BankNifty' },
    { key: 'fin_nifty', name: 'FinNifty' },
    { key: 'sensex', name: 'Sensex' },
];
const productTypes = [
    { key: 'MIS', name: 'MIS (Intraday)' },
    { key: 'NRML', name: 'NRML (Overnight)' },
];
const timeframes = [
    { key: 'ONE_MINUTE', name: '1 Minute' },
    { key: 'THREE_MINUTE', name: '3 Minutes' },
    { key: 'FIVE_MINUTE', name: '5 Minutes' },
    { key: 'FIFTEEN_MINUTE', name: '15 Minutes' },
    { key: 'ONE_HOUR', name: '1 Hour' },
    { key: 'ONE_DAY', name: '1 Day' },
];

let strategies = [];
let expandedStrategyId = null;
let TOKEN = '';
let modalListenersAttached = false;

function formatName(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function showNotification(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const id = `notif-${Date.now()}`;
    const bg = type === 'success' ? 'bg-emerald-500' : 'bg-red-500';
    const html = `
        <div id="${id}" class="fixed top-4 right-4 z-[100] ${bg} text-white py-2 px-5 rounded-lg shadow-lg text-sm font-semibold animate-fade-in-down">
            ${message}
        </div>`;
    const el = document.createElement('div');
    el.innerHTML = html;
    container.appendChild(el.firstElementChild);
    setTimeout(() => {
        const e = document.getElementById(id);
        if (e) { e.style.opacity = '0'; e.style.transition = 'opacity 0.3s'; setTimeout(() => e.remove(), 300); }
    }, 3000);
}

function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(() => showNotification('URL Copied!', 'success'))
            .catch(() => fallbackCopy(text));
    } else {
        fallbackCopy(text);
    }
}

function fallbackCopy(text) {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); showNotification('URL Copied!', 'success'); } catch { showNotification('Failed to copy', 'error'); }
    document.body.removeChild(ta);
}

function createToggleHTML(id, enabled) {
    const bg = enabled ? 'bg-emerald-500' : 'bg-surface-600';
    const tx = enabled ? 'translate-x-5' : 'translate-x-0.5';
    return `
        <button type="button" data-id="${id}" class="toggle-switch relative inline-flex items-center h-5 rounded-full w-9 transition-colors duration-300 focus:outline-none ${bg}" aria-pressed="${enabled}">
            <span class="inline-block w-4 h-4 transform bg-white rounded-full transition-transform duration-300 ${tx}" />
        </button>`;
}

function createDetailsHTML(strategy) {
    const rows = indices.map(index => {
        const inputObj = {
            strategy_name: strategy.strategy_name || strategy.name,
            index_name: index.name.toUpperCase(),
            target: strategy.target,
            stop_loss: strategy.stop_loss,
            strike: strategy.strike,
            lots: strategy.lots,
            on_candle_close: strategy.on_candle_close,
            producttype: strategy.producttype,
            timeframe: strategy.timeframe,
            index_group: strategy.index_group,
        };
        const inputData = JSON.stringify(inputObj, null, 2);
        return `
            <tr class="border-b border-surface-700 last:border-b-0">
                <td class="p-3 align-top font-medium text-surface-50">${index.name}</td>
                <td class="p-3 align-top font-mono text-xs break-all text-surface-400 webhook-url cursor-pointer hover:text-surface-50" title="Copy URL">/trigger_buy?token=${TOKEN}</td>
                <td class="p-3 align-top font-mono text-xs break-all text-surface-400 webhook-url cursor-pointer hover:text-surface-50" title="Copy URL">/trigger_sell?token=${TOKEN}</td>
                <td class="p-3 align-top font-mono text-xs break-all text-surface-400 webhook-url cursor-pointer hover:text-surface-50" title="Copy URL">/trigger_exit?token=${TOKEN}</td>
                <td class="p-3 align-top max-w-[200px]">
                    <pre class="bg-surface-900 p-2 rounded whitespace-pre-wrap break-all text-surface-400 font-mono text-xs">${inputData}</pre>
                </td>
            </tr>`;
    }).join('');

    return `
        <div class="bg-surface-800/50 p-4 animate-fade-in-down">
            <table class="w-full text-sm">
                <thead>
                    <tr class="border-b border-surface-700">
                        <th class="p-3 w-[10%] text-left font-semibold text-surface-400 text-xs uppercase tracking-wider">Index</th>
                        <th class="p-3 w-[22%] text-left font-semibold text-surface-400 text-xs uppercase tracking-wider">Buy URL</th>
                        <th class="p-3 w-[22%] text-left font-semibold text-surface-400 text-xs uppercase tracking-wider">Sell URL</th>
                        <th class="p-3 w-[22%] text-left font-semibold text-surface-400 text-xs uppercase tracking-wider">Exit URL</th>
                        <th class="p-3 w-[24%] text-left font-semibold text-surface-400 text-xs uppercase tracking-wider">Input Data</th>
                    </tr>
                </thead>
                <tbody>${rows}</tbody>
            </table>
        </div>`;
}

function createTableHTML() {
    if (strategies.length === 0) {
        return `<div class="text-center py-12 text-surface-400"><p class="text-lg font-medium">No Strategies Found</p><p class="mt-1 text-sm">Create a custom strategy to get started.</p></div>`;
    }

    const rows = strategies.map(s => {
        const typeClass = s.strategy_type === 'default' ? 'bg-surface-700 text-surface-300' : 'bg-emerald-500/20 text-emerald-400';
        const statusDot = s.enabled ? 'bg-emerald-400' : 'bg-red-400';
        const statusText = s.enabled ? 'Enabled' : 'Disabled';
        const toggleHTML = createToggleHTML(s.id, s.enabled);

        let actions;
        if (s.strategy_type === 'default') {
            actions = `<div class="flex items-center justify-center gap-3">${toggleHTML}<button class="btn-edit p-1.5 rounded-lg hover:bg-surface-700 text-blue-400 hover:text-blue-300 transition-colors" data-id="${s.id}" title="Edit">${PencilIcon}</button></div>`;
        } else {
            actions = `<div class="flex items-center justify-center gap-3">${toggleHTML}<button class="btn-edit p-1.5 rounded-lg hover:bg-surface-700 text-blue-400 hover:text-blue-300 transition-colors" data-id="${s.id}" title="Edit">${PencilIcon}</button><button class="btn-delete p-1.5 rounded-lg hover:bg-surface-700 text-red-400 hover:text-red-300 transition-colors" data-id="${s.id}" title="Delete">${TrashIcon}</button></div>`;
        }

        const expanded = expandedStrategyId === s.id ? `
            <tr class="bg-surface-800/30">
                <td colspan="4" class="p-0">${createDetailsHTML(s)}</td>
            </tr>` : '';

        return `
            <tr data-id="${s.id}" class="strategy-row border-b border-surface-700/50 hover:bg-surface-700/30 cursor-pointer transition-colors duration-150">
                <td class="px-4 py-3.5 whitespace-nowrap text-sm font-medium text-surface-50">${s.strategy_name || s.name}</td>
                <td class="px-4 py-3.5 whitespace-nowrap text-sm"><span class="px-2.5 py-0.5 text-xs font-semibold rounded-full ${typeClass}">${s.strategy_type || 'custom'}</span></td>
                <td class="px-4 py-3.5 whitespace-nowrap text-sm"><span class="flex items-center gap-1.5 ${s.enabled ? 'text-emerald-400' : 'text-red-400'}"><span class="h-2 w-2 rounded-full ${statusDot}"></span>${statusText}</span></td>
                <td class="px-4 py-3.5 whitespace-nowrap text-center text-sm">${actions}</td>
            </tr>
            ${expanded}`;
    }).join('');

    return `
        <div class="card overflow-hidden">
            <table class="min-w-full divide-y divide-surface-700">
                <thead class="bg-surface-800">
                    <tr>
                        <th scope="col" class="px-4 py-3 text-left text-xs font-semibold text-surface-400 uppercase tracking-wider">Strategy Name</th>
                        <th scope="col" class="px-4 py-3 text-left text-xs font-semibold text-surface-400 uppercase tracking-wider">Type</th>
                        <th scope="col" class="px-4 py-3 text-left text-xs font-semibold text-surface-400 uppercase tracking-wider">Status</th>
                        <th scope="col" class="px-4 py-3 text-center text-xs font-semibold text-surface-400 uppercase tracking-wider">Action</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-surface-700/50 bg-surface-800">${rows}</tbody>
            </table>
        </div>`;
}

function createModalHTML(strategyToEdit = null) {
    const isEditing = strategyToEdit !== null;
    const title = isEditing ? 'Edit Custom Strategy' : 'Create Custom Strategy';
    const submitText = isEditing ? 'Save Changes' : 'Add Strategy';
    const sid = isEditing ? strategyToEdit.id : '';
    const name = isEditing ? (strategyToEdit.strategy_name || '') : '';
    const lots = isEditing ? strategyToEdit.lots : '1';
    const strike = isEditing ? strategyToEdit.strike : '100';
    const index_name = isEditing ? strategyToEdit.index_name : 'nifty';
    const producttype = isEditing ? strategyToEdit.producttype : 'MIS';
    const timeframe = isEditing ? strategyToEdit.timeframe : 'FIVE_MINUTE';
    const index_group = isEditing ? strategyToEdit.index_group : 'indian_index';
    const on_candle_close = isEditing ? strategyToEdit.on_candle_close : true;
    const disabled = isEditing ? 'disabled' : '';
    const dClass = isEditing ? 'opacity-60 cursor-not-allowed' : '';

    const indexOpts = indices.map(i => `<option value="${i.key}" ${i.key === index_name ? 'selected' : ''}>${i.name}</option>`).join('');
    const prodOpts = productTypes.map(p => `<option value="${p.key}" ${p.key === producttype ? 'selected' : ''}>${p.name}</option>`).join('');
    const timeOpts = timeframes.map(t => `<option value="${t.key}" ${t.key === timeframe ? 'selected' : ''}>${t.name}</option>`).join('');

    return `
        <div id="strategy-modal-overlay" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
            <div class="bg-surface-800 rounded-xl border border-surface-700 shadow-2xl w-full max-w-lg animate-fade-in-down">
                <div class="flex justify-between items-center p-5 border-b border-surface-700">
                    <h3 class="text-lg font-semibold text-surface-50">${title}</h3>
                    <button type="button" id="close-modal-btn" class="text-surface-400 hover:text-surface-50 transition-colors">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                    </button>
                </div>
                <form id="add-strategy-form" autocomplete="off" data-editing-id="${sid}">
                    <div class="p-6 space-y-4">
                        <div>
                            <label for="strategy-name" class="block text-sm font-medium text-surface-400 mb-1">Strategy Name</label>
                            <input id="strategy-name" type="text" placeholder="e.g. 'My Custom MACD'" class="w-full px-3 py-2 bg-surface-700 border border-surface-600 rounded-md text-surface-50 placeholder-surface-500 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-primary-400 text-sm ${dClass}" required value="${name}" ${disabled} />
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div>
                                <label for="lots" class="block text-sm font-medium text-surface-400 mb-1">Lots</label>
                                <input id="lots" type="number" value="${lots}" class="w-full px-3 py-2 bg-surface-700 border border-surface-600 rounded-md text-surface-50 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-primary-400 text-sm" required />
                            </div>
                            <div>
                                <label for="strike" class="block text-sm font-medium text-surface-400 mb-1">Strike</label>
                                <input id="strike" type="text" placeholder="e.g. 100" value="${strike}" class="w-full px-3 py-2 bg-surface-700 border border-surface-600 rounded-md text-surface-50 placeholder-surface-500 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-primary-400 text-sm" required />
                            </div>
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div>
                                <label for="index_name" class="block text-sm font-medium text-surface-400 mb-1">Index Name</label>
                                <select id="index_name" class="w-full px-3 py-2 bg-surface-700 border border-surface-600 rounded-md text-surface-50 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-primary-400 text-sm ${dClass}" ${disabled}>${indexOpts}</select>
                            </div>
                            <div>
                                <label for="producttype" class="block text-sm font-medium text-surface-400 mb-1">Product Type</label>
                                <select id="producttype" class="w-full px-3 py-2 bg-surface-700 border border-surface-600 rounded-md text-surface-50 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-primary-400 text-sm">${prodOpts}</select>
                            </div>
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div>
                                <label for="timeframe" class="block text-sm font-medium text-surface-400 mb-1">Timeframe</label>
                                <select id="timeframe" class="w-full px-3 py-2 bg-surface-700 border border-surface-600 rounded-md text-surface-50 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-primary-400 text-sm">${timeOpts}</select>
                            </div>
                            <div>
                                <label for="index_group" class="block text-sm font-medium text-surface-400 mb-1">Index Group</label>
                                <input id="index_group" type="text" placeholder="indian_index" value="${index_group}" class="w-full px-3 py-2 bg-surface-700 border border-surface-600 rounded-md text-surface-50 placeholder-surface-500 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-primary-400 text-sm" required />
                            </div>
                        </div>
                        <div>
                            <label class="flex items-center gap-2 cursor-pointer">
                                <input id="on_candle_close" type="checkbox" class="w-4 h-4 rounded bg-surface-700 border-surface-600 text-primary-400 focus:ring-primary-400" ${on_candle_close ? 'checked' : ''} />
                                <span class="text-sm font-medium text-surface-400">On Candle Close</span>
                            </label>
                        </div>
                    </div>
                    <div class="px-6 py-4 flex justify-end gap-3 border-t border-surface-700">
                        <button type="button" id="cancel-add-strategy" class="px-4 py-2 text-sm font-medium text-surface-300 bg-surface-700 hover:bg-surface-600 rounded-lg transition-colors">Cancel</button>
                        <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-primary-500 hover:bg-primary-600 rounded-lg transition-colors flex items-center gap-2 min-w-[130px] justify-center">
                            <span class="button-text">${submitText}</span>
                            <svg class="animate-spin h-4 w-4 text-white hidden loader" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                        </button>
                    </div>
                </form>
            </div>
        </div>`;
}

const PencilIcon = `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>`;
const TrashIcon = `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>`;

async function loadStrategies() {
    const container = document.getElementById('strategy-table-container');
    if (!container) return;
    container.innerHTML = '<p class="text-center py-8 text-surface-400">Loading strategies...</p>';
    try {
        const [stratResp, tokenResp] = await Promise.all([
            makeApiCall('/get_strategy_details'),
            makeApiCall('/get_auth_token', { method: 'POST' }),
        ]);
        if (tokenResp?.status === 'success' && tokenResp.message) {
            TOKEN = tokenResp.message;
        }
        if (stratResp?.status === 'success' && Array.isArray(stratResp.data)) {
            const defaults = stratResp.data.filter(s => s.strategy_type === 'default');
            const transformed = defaults.map(s => ({
                ...s,
                id: String(s.id),
                name: indices.find(i => i.key === s.index_name)?.name || formatName(s.index_name),
                type: 'default',
                enabled: s.order_status === 'order_placed',
            }));
            const customs = stratResp.data.filter(s => s.strategy_type === 'custom');
            strategies = [...transformed, ...customs];
        } else {
            throw new Error('Invalid API response');
        }
    } catch (err) {
        console.error('Failed to load strategies:', err);
        container.innerHTML = `<div class="text-center py-10 px-6 bg-red-500/10 border border-red-500/30 rounded-lg"><h3 class="text-lg font-medium text-surface-50">Failed to Load Strategies</h3><p class="mt-1 text-sm text-surface-400">${err.message}</p></div>`;
        strategies = strategies.filter(s => s.type === 'custom');
    }
    renderStrategies();
}

function renderStrategies() {
    const container = document.getElementById('strategy-table-container');
    if (!container) return;
    container.innerHTML = createTableHTML();
}

function closeModal() {
    const overlay = document.getElementById('strategy-modal-overlay');
    if (overlay) overlay.remove();
}

async function handleStrategyFormSubmit(form) {
    const submitBtn = form.querySelector('button[type="submit"]');
    const cancelBtn = form.querySelector('#cancel-add-strategy');
    const editingId = form.dataset.editingId;

    const data = {
        strategy_name: document.getElementById('strategy-name').value.trim(),
        lots: document.getElementById('lots').value,
        strike: document.getElementById('strike').value,
        index_name: document.getElementById('index_name').value,
        producttype: document.getElementById('producttype').value,
        timeframe: document.getElementById('timeframe').value,
        index_group: document.getElementById('index_group').value,
        on_candle_close: document.getElementById('on_candle_close').checked,
    };

    if (!data.strategy_name) return;

    const isEditing = !!editingId;
    submitBtn.disabled = true;
    cancelBtn.disabled = true;
    const bt = submitBtn.querySelector('.button-text');
    const ld = submitBtn.querySelector('.loader');
    if (bt) bt.classList.add('hidden');
    if (ld) ld.classList.remove('hidden');

    try {
        if (isEditing) {
            const orig = strategies.find(s => s.id === editingId);
            if (!orig) throw new Error('Strategy not found');
            await makeApiCall('/update_strategy_details', {
                method: 'PUT',
                body: { strategy_name: orig.strategy_name, fields: { strike: data.strike, lots: data.lots, on_candle_close: data.on_candle_close, producttype: data.producttype, timeframe: data.timeframe, index_group: data.index_group } },
            });
            const idx = strategies.findIndex(s => s.id === editingId);
            if (idx > -1) strategies[idx] = { ...strategies[idx], ...data };
            showNotification('Strategy updated!', 'success');
        } else {
            await makeApiCall('/add_strategy_details', { method: 'POST', body: data });
            strategies.push({ id: String(Date.now()), type: 'custom', strategy_type: 'custom', ...data, enabled: true });
            expandedStrategyId = strategies[strategies.length - 1].id;
            showNotification('Strategy created!', 'success');
        }
        closeModal();
        renderStrategies();
    } catch (err) {
        console.error('Failed to save strategy:', err);
        showNotification(err.message, 'error');
        submitBtn.disabled = false;
        cancelBtn.disabled = false;
        if (bt) bt.classList.remove('hidden');
        if (ld) ld.classList.add('hidden');
    }
}

function openCreateModal() {
    const mc = document.getElementById('modal-container');
    if (mc) mc.innerHTML = createModalHTML();
    const form = document.getElementById('add-strategy-form');
    if (form) form.addEventListener('submit', (e) => { e.preventDefault(); handleStrategyFormSubmit(form); });
    const nameInput = document.getElementById('strategy-name');
    if (nameInput) nameInput.focus();
}

function openEditModal(strategy) {
    const mc = document.getElementById('modal-container');
    if (mc) mc.innerHTML = createModalHTML(strategy);
    const form = document.getElementById('add-strategy-form');
    if (form) form.addEventListener('submit', (e) => { e.preventDefault(); handleStrategyFormSubmit(form); });
}

export function initStrategiesPage() {
    loadStrategies();

    document.getElementById('create-strategy-btn')?.addEventListener('click', openCreateModal);

    if (!modalListenersAttached) {
        modalListenersAttached = true;

        document.getElementById('modal-container')?.addEventListener('click', (e) => {
            if (e.target.id === 'strategy-modal-overlay' || e.target.closest('#cancel-add-strategy') || e.target.closest('#close-modal-btn')) {
                closeModal();
            }
        });
    }

    document.getElementById('strategy-table-container')?.addEventListener('click', async (e) => {
        const toggle = e.target.closest('.toggle-switch');
        if (toggle) {
            e.stopPropagation();
            const id = toggle.dataset.id;
            const s = strategies.find(x => x.id === id);
            if (!s) return;
            const prev = s.enabled;
            s.enabled = !s.enabled;
            renderStrategies();
            try {
                await makeApiCall('/toggle_strategy_details', { method: 'POST', body: { strategy_name: s.strategy_name } });
            } catch (err) {
                console.error('Toggle failed:', err);
                s.enabled = prev;
                renderStrategies();
                showNotification('Toggle API not available', 'error');
            }
        }

        const editBtn = e.target.closest('.btn-edit');
        if (editBtn) {
            e.stopPropagation();
            const id = editBtn.dataset.id;
            const s = strategies.find(x => x.id === id);
            if (s) openEditModal(s);
        }

        const deleteBtn = e.target.closest('.btn-delete');
        if (deleteBtn) {
            e.stopPropagation();
            const id = deleteBtn.dataset.id;
            const s = strategies.find(x => x.id === id);
            if (s && confirm(`Delete "${s.strategy_name || s.name}"?`)) {
                try {
                    await makeApiCall('/delete_strategy_details', { method: 'POST', body: { strategy_name: s.strategy_name } });
                    strategies = strategies.filter(x => x.id !== id);
                    if (expandedStrategyId === id) expandedStrategyId = null;
                    renderStrategies();
                    showNotification('Strategy deleted!', 'success');
                } catch (err) {
                    console.error('Delete failed:', err);
                    showNotification(err.message, 'error');
                }
            }
        }

        const row = e.target.closest('.strategy-row');
        if (row && !e.target.closest('button')) {
            const id = row.dataset.id;
            expandedStrategyId = expandedStrategyId === id ? null : id;
            renderStrategies();
        }

        const urlEl = e.target.closest('.webhook-url');
        if (urlEl) {
            copyText(urlEl.textContent.trim());
        }
    });
}

const StrategiesPage = () => {
    return `
        <div class="space-y-6 mt-2">
            <div class="flex items-center justify-between">
                <h1 class="text-xl lg:text-2xl font-bold text-surface-50">Strategies</h1>
                <button id="create-strategy-btn" class="px-4 py-2 text-sm font-medium text-white bg-primary-500 hover:bg-primary-600 rounded-lg transition-colors flex items-center gap-2">
                    ${PlusIcon({ className: 'h-4 w-4' })}
                    New Strategy
                </button>
            </div>
            <div id="strategy-table-container">
                <p class="text-center py-8 text-surface-400">Loading strategies...</p>
            </div>
        </div>`;
};

export default StrategiesPage;
