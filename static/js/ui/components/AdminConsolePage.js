import { ShieldCheckIcon, PlayCircleIcon, StopCircleIcon, ArrowPathIcon, PlusIcon, EyeIcon, CogIcon } from './icons.js';
import { makeApiCall } from '../utils/api.js';
import Toast from './Toast.js';


let state = {
    loading: true,
    celeryStatus: null,
    socketStatus: null,
    indexData: [],
    toast: null,
    botConfig: null,
    savingBotConfig: false,
};

function showToast(message, type) {
    state.toast = { message, type };
    render();
    setTimeout(() => {
        state.toast = null;
        const el = document.querySelector('.admin-toast');
        if (el) el.remove();
    }, 4000);
}

async function fetchAdminData() {
    state.loading = true;
    render();
    try {
        const [celeryResp, socketResp, indexResp, botResp] = await Promise.all([
            makeApiCall('/get_celery_status').catch(() => null),
            makeApiCall('/check_task_status').catch(() => null),
            makeApiCall('/get_index_data').catch(() => null),
            makeApiCall('/get_telegram_bot_config').catch(() => null),
        ]);
        state.celeryStatus = celeryResp?.celery_running ?? null;
        state.socketStatus = socketResp?.task_status ?? null;
        state.indexData = indexResp?.message?.index_data ?? [];
        state.botConfig = botResp?.status === 'success' ? botResp : null;
    } catch (e) {
        showToast('Failed to load admin data', 'error');
    } finally {
        state.loading = false;
        render();
    }
}

async function handleAction(endpoint, successMsg, body = {}) {
    try {
        const resp = await makeApiCall(endpoint, { method: 'POST', body });
        if (resp?.status === 'success' || resp?.task_status) {
            showToast(successMsg, 'success');
        } else {
            showToast(resp?.message || 'Action failed', 'error');
        }
    } catch (e) {
        showToast('Request failed: ' + e.message, 'error');
    }
    fetchAdminData();
}

async function handleUpdateExpiry() {
    try {
        const tokenResponse = await makeApiCall('/get_auth_token', { method: 'POST' });
        const token = tokenResponse?.status === 'success' ? tokenResponse.message : null;

        if (!token) {
            throw new Error('Could not retrieve authentication token');
        }

        await handleAction(
            `/update_expiry_details?token=${encodeURIComponent(token)}`,
            'Expiry updated'
        );
    } catch (e) {
        showToast('Request failed: ' + e.message, 'error');
    }
}

async function handleAddUser() {
    const email = document.getElementById('new-user-email')?.value;
    const name = document.getElementById('new-user-name')?.value;
    const password = document.getElementById('new-user-password')?.value;
    if (!email || !name || !password) {
        showToast('Please fill all fields', 'error');
        return;
    }
    try {
        const resp = await makeApiCall('/add_user', { method: 'POST', body: { user_id: email, user_name: name, password } });
        if (resp?.status === 'success') {
            showToast('User added successfully', 'success');
            document.getElementById('new-user-email').value = '';
            document.getElementById('new-user-name').value = '';
            document.getElementById('new-user-password').value = '';
        } else {
            showToast(resp?.message || 'Failed to add user', 'error');
        }
    } catch (e) {
        showToast('Error: ' + e.message, 'error');
    }
}

async function handleSaveBotConfig() {
    const botId = document.getElementById('bot-id-input')?.value.trim();
    const adminBotId = document.getElementById('admin-bot-id-input')?.value.trim();
    const adminIds = document.getElementById('admin-chat-ids-input')?.value.trim();
    state.savingBotConfig = true;
    render();
    try {
        const resp = await makeApiCall('/update_telegram_bot_config', {
            method: 'POST',
            body: { bot_id: botId, admin_bot_id: adminBotId, admin_chat_ids: adminIds },
        });
        if (resp?.status === 'success') {
            state.botConfig = resp;
            showToast('Bot configuration saved', 'success');
        } else {
            showToast(resp?.message || 'Failed to save', 'error');
        }
    } catch (e) {
        showToast('Error: ' + e.message, 'error');
    } finally {
        state.savingBotConfig = false;
        render();
    }
}

function getExpiryClass(dateStr) {
    if (!dateStr) return 'text-surface-500';
    try {
        const date = new Date(dateStr);
        if (isNaN(date.getTime())) return 'text-surface-500';
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const diffDays = (date - today) / (1000 * 60 * 60 * 24);
        if (diffDays < 0) return 'text-red-400 font-semibold';
        if (diffDays <= 7) return 'text-amber-400 font-semibold';
        return 'text-emerald-400';
    } catch {
        return 'text-surface-500';
    }
}

function getExpiryBadge(dateStr) {
    if (!dateStr) return '';
    try {
        const date = new Date(dateStr);
        if (isNaN(date.getTime())) return '';
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const diffDays = (date - today) / (1000 * 60 * 60 * 24);
        if (diffDays < 0) return '<span class="ml-1.5 px-1.5 py-0.5 text-[10px] font-bold rounded bg-red-500/20 text-red-400">EXPIRED</span>';
        if (diffDays <= 7) return '<span class="ml-1.5 px-1.5 py-0.5 text-[10px] font-bold rounded bg-amber-500/20 text-amber-400">SOON</span>';
        return '';
    } catch {
        return '';
    }
}

function render() {
    const container = document.getElementById('admin-console-container');
    if (!container) return;

    const toastHtml = state.toast ? `<div class="admin-toast fixed top-20 right-5 z-50">${Toast(state.toast)}</div>` : '';

    if (state.loading) {
        container.innerHTML = `
            ${toastHtml}
            <div class="flex items-center justify-center min-h-[200px]">
                <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary-400"></div>
                <p class="ml-3 text-sm text-surface-400">Loading admin panel...</p>
            </div>`;
        return;
    }

    container.innerHTML = `
        ${toastHtml}
        <div class="page-enter space-y-6">
            <div class="flex items-center gap-3 mb-6">
                ${ShieldCheckIcon({ className: 'h-6 w-6 text-primary-400' })}
                <div>
                    <h1 class="text-xl lg:text-2xl font-bold text-surface-50">Admin Console</h1>
                    <p class="text-sm text-surface-400">System controls and user management</p>
                </div>
            </div>

            <div class="card p-5 border border-cyan-500/20">
                <h3 class="text-sm font-semibold text-surface-50 mb-4 flex items-center gap-2">
                    ${CogIcon({ className: 'h-4 w-4 text-cyan-400' })} Default Telegram Bot
                </h3>
                <p class="text-xs text-surface-400 mb-4">Bot ID is used for user error notifications. Admin Bot ID is used for admin/fallback messages.</p>
                <div class="space-y-3 max-w-2xl">
                    <div>
                        <label class="block text-xs text-surface-400 mb-1">Bot ID</label>
                        <input id="bot-id-input" type="text" value="${state.botConfig?.bot_id || ''}" placeholder="Bot token for user notifications" class="w-full px-3 py-2 bg-surface-700 border border-surface-600 rounded-lg text-sm text-surface-50 placeholder-surface-400 focus:outline-none focus:border-primary-500/50 font-mono">
                    </div>
                    <div>
                        <label class="block text-xs text-surface-400 mb-1">Admin Bot ID</label>
                        <input id="admin-bot-id-input" type="text" value="${state.botConfig?.admin_bot_id || ''}" placeholder="Bot token for admin notifications (optional)" class="w-full px-3 py-2 bg-surface-700 border border-surface-600 rounded-lg text-sm text-surface-50 placeholder-surface-400 focus:outline-none focus:border-primary-500/50 font-mono">
                    </div>
                    <div>
                        <label class="block text-xs text-surface-400 mb-1">Admin Chat IDs <span class="text-surface-500">(comma-separated)</span></label>
                        <input id="admin-chat-ids-input" type="text" value="${state.botConfig?.admin_chat_ids || ''}" placeholder="e.g. 710817544, 648567264" class="w-full px-3 py-2 bg-surface-700 border border-surface-600 rounded-lg text-sm text-surface-50 placeholder-surface-400 focus:outline-none focus:border-primary-500/50">
                    </div>
                    <button onclick="window.saveBotConfig()" class="px-4 py-2 bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-400 rounded-lg text-xs font-medium transition-colors" ${state.savingBotConfig ? 'disabled' : ''}>
                        ${state.savingBotConfig ? 'Saving...' : 'Save Bot Config'}
                    </button>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="card p-5">
                    <h3 class="text-sm font-semibold text-surface-50 mb-4 flex items-center gap-2">
                        ${PlayCircleIcon({ className: 'h-4 w-4 text-emerald-400' })} WebSocket
                    </h3>
                    <div class="flex items-center gap-3 mb-4">
                        <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${state.socketStatus ? 'bg-emerald-500/10 text-emerald-400' : 'bg-red-500/10 text-red-400'}">
                            <span class="w-1.5 h-1.5 rounded-full ${state.socketStatus ? 'bg-emerald-400' : 'bg-red-400'}"></span>
                            ${state.socketStatus ? 'Running' : 'Stopped'}
                        </span>
                    </div>
                    <div class="flex flex-wrap gap-2">
                        <button onclick="window.wsAction('start_ws', {ws_type: '1'})" class="px-3 py-1.5 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 rounded-lg text-xs font-medium transition-colors flex items-center gap-1">${PlayCircleIcon({className:'h-3.5 w-3.5'})} Start Candle WS</button>
                        <button onclick="window.wsAction('start_ws', {ws_type: '2'})" class="px-3 py-1.5 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 rounded-lg text-xs font-medium transition-colors flex items-center gap-1">${PlayCircleIcon({className:'h-3.5 w-3.5'})} Start HTTP WS</button>
                        <button onclick="window.wsAction('stop_ws', {ws_type: '1'})" class="px-3 py-1.5 bg-red-500/10 hover:bg-red-500/20 text-red-400 rounded-lg text-xs font-medium transition-colors flex items-center gap-1">${StopCircleIcon({className:'h-3.5 w-3.5'})} Stop</button>
                    </div>
                </div>

                <div class="card p-5">
                    <h3 class="text-sm font-semibold text-surface-50 mb-4 flex items-center gap-2">
                        ${ArrowPathIcon({ className: 'h-4 w-4 text-indigo-400' })} Celery Worker
                    </h3>
                    <div class="flex items-center gap-3 mb-4">
                        <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${state.celeryStatus ? 'bg-emerald-500/10 text-emerald-400' : 'bg-red-500/10 text-red-400'}">
                            <span class="w-1.5 h-1.5 rounded-full ${state.celeryStatus ? 'bg-emerald-400' : 'bg-red-400'}"></span>
                            ${state.celeryStatus ? 'Running' : 'Stopped'}
                        </span>
                    </div>
                    <div class="flex flex-wrap gap-2">
                        <button onclick="window.restartCelery()" class="px-3 py-1.5 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 rounded-lg text-xs font-medium transition-colors">Restart</button>
                        <button onclick="window.stopCelery()" class="px-3 py-1.5 bg-red-500/10 hover:bg-red-500/20 text-red-400 rounded-lg text-xs font-medium transition-colors">Stop</button>
                    </div>
                </div>
            </div>

            <div class="card p-5">
                <h3 class="text-sm font-semibold text-surface-50 mb-4 flex items-center gap-2">
                    ${PlusIcon({ className: 'h-4 w-4 text-primary-400' })} Add New User
                </h3>
                <div class="flex flex-wrap gap-3">
                    <input id="new-user-email" type="email" placeholder="Email" class="flex-1 min-w-[200px] px-3 py-2 bg-surface-700 border border-surface-600 rounded-lg text-sm text-surface-50 placeholder-surface-400 focus:outline-none focus:border-primary-500/50">
                    <input id="new-user-name" type="text" placeholder="Name" class="flex-1 min-w-[150px] px-3 py-2 bg-surface-700 border border-surface-600 rounded-lg text-sm text-surface-50 placeholder-surface-400 focus:outline-none focus:border-primary-500/50">
                    <input id="new-user-password" type="password" placeholder="Password" class="flex-1 min-w-[150px] px-3 py-2 bg-surface-700 border border-surface-600 rounded-lg text-sm text-surface-50 placeholder-surface-400 focus:outline-none focus:border-primary-500/50">
                    <button onclick="window.addUser()" class="px-4 py-2 bg-primary-500 hover:bg-primary-600 text-surface-50 rounded-lg text-sm font-medium transition-colors whitespace-nowrap">Add User</button>
                </div>
            </div>

            <div class="card p-5">
                <div class="flex items-center justify-between mb-4 flex-wrap gap-3">
                    <h3 class="text-sm font-semibold text-surface-50 flex items-center gap-2">
                        ${EyeIcon({ className: 'h-4 w-4 text-primary-400' })} Index Data
                    </h3>
                    <div class="flex flex-wrap gap-2">
                        <button onclick="window.regenerateToken()" class="px-3 py-1.5 bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 rounded-lg text-xs font-medium transition-colors flex items-center gap-1">${ArrowPathIcon({className:'h-3.5 w-3.5'})} Regenerate Token</button>
                        <button onclick="window.updateExpiry()" class="px-3 py-1.5 bg-blue-500/10 hover:bg-blue-500/20 text-blue-400 rounded-lg text-xs font-medium transition-colors flex items-center gap-1">${ArrowPathIcon({className:'h-3.5 w-3.5'})} Update Expiry</button>
                    </div>
                </div>
                ${state.indexData.length === 0 ? '<p class="text-sm text-surface-400">No index data available.</p>' : `
                <div class="overflow-x-auto">
                    <table class="w-full text-sm">
                        <thead>
                            <tr class="text-surface-400 text-xs uppercase tracking-wider border-b border-surface-700">
                                <th class="text-left py-3 px-3 font-medium">Name</th>
                                <th class="text-left py-3 px-3 font-medium">Token</th>
                                <th class="text-right py-3 px-3 font-medium">LTP</th>
                                <th class="text-right py-3 px-3 font-medium">Qty</th>
                                <th class="text-right py-3 px-3 font-medium">Current Expiry</th>
                                <th class="text-right py-3 px-3 font-medium">Next Expiry</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-surface-700/50">
                            ${state.indexData.map(item => `
                                <tr class="hover:bg-surface-700/30">
                                    <td class="py-3 px-3 text-surface-50 font-medium">${item.index_name || '-'}</td>
                                    <td class="py-3 px-3 text-surface-400 font-mono text-xs">${item.index_token || '-'}</td>
                                    <td class="py-3 px-3 text-right text-surface-200">${item.ltp || '-'}</td>
                                    <td class="py-3 px-3 text-right text-surface-200">${item.qty || '-'}</td>
                                    <td class="py-3 px-3 text-right ${getExpiryClass(item.current_expiry)}">${item.current_expiry || '-'}${getExpiryBadge(item.current_expiry)}</td>
                                    <td class="py-3 px-3 text-right ${getExpiryClass(item.next_expiry)}">${item.next_expiry || '-'}${getExpiryBadge(item.next_expiry)}</td>
                                </tr>`).join('')}
                        </tbody>
                    </table>
                </div>`}
            </div>
        </div>`;

    window.wsAction = (endpoint, body) => handleAction(endpoint, 'WebSocket action completed', body);
    window.regenerateToken = () => handleAction('/regenerate_token', 'Token regenerated');
    window.updateExpiry = handleUpdateExpiry;
    window.restartCelery = () => handleAction('/restart_celery', 'Celery restarted');
    window.stopCelery = () => handleAction('/stop_celery', 'Celery stopped');
    window.addUser = handleAddUser;
    window.saveBotConfig = handleSaveBotConfig;
}

export function initAdminConsole() {
    fetchAdminData();
}

export default function AdminConsolePage() {
    return '<div id="admin-console-container"></div>';
}
