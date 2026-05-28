import { ListBulletIcon, ArrowPathIcon, InformationCircleIcon, XCircleIcon, CheckCircleIcon, ExclamationTriangleIcon, MagnifyingGlassIcon } from './icons.js';
import { makeApiCall } from '../utils/api.js';

function todayStr() {
    const d = new Date();
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
}

let state = {
    loading: true,
    logs: [],
    filterIndex: '',
    filterType: '',
    searchText: '',
    startDate: todayStr(),
    endDate: todayStr(),
    toast: null,
};

function render() {
    const container = document.getElementById('log-viewer-container');
    if (!container) return;

    if (state.loading) {
        container.innerHTML = `
            <div class="flex items-center justify-center min-h-[200px]">
                <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary-400"></div>
                <p class="ml-3 text-sm text-surface-400">Loading logs...</p>
            </div>`;
        return;
    }

    const logTypeIcon = (type) => {
        const t = (type || '').toLowerCase();
        if (t === 'error') return XCircleIcon({ className: 'h-4 w-4 text-red-400' });
        if (t === 'success') return CheckCircleIcon({ className: 'h-4 w-4 text-emerald-400' });
        if (t === 'warning') return ExclamationTriangleIcon({ className: 'h-4 w-4 text-amber-400' });
        return InformationCircleIcon({ className: 'h-4 w-4 text-blue-400' });
    };

    const logTypeBadge = (type) => {
        const t = (type || '').toLowerCase();
        if (t === 'error') return 'bg-red-500/10 text-red-400';
        if (t === 'success') return 'bg-emerald-500/10 text-emerald-400';
        if (t === 'warning') return 'bg-amber-500/10 text-amber-400';
        return 'bg-blue-500/10 text-blue-400';
    };

    const indexNames = [...new Set(state.logs.map(l => l.index_name).filter(Boolean))];
    const logTypes = [...new Set(state.logs.map(l => l.log_type).filter(Boolean))];
    const searchLower = state.searchText.toLowerCase();

    const filtered = state.logs.filter(l => {
        if (state.filterIndex && l.index_name !== state.filterIndex) return false;
        if (state.filterType && l.log_type !== state.filterType) return false;
        if (searchLower && !(l.log || '').toLowerCase().includes(searchLower) && !(l.index_name || '').toLowerCase().includes(searchLower)) return false;
        return true;
    });

    container.innerHTML = `
        <div class="space-y-6">
            <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                    ${ListBulletIcon({ className: 'h-6 w-6 text-primary-400' })}
                    <div>
                        <h1 class="text-xl lg:text-2xl font-bold text-surface-50">Log Viewer</h1>
                        <p class="text-sm text-surface-400">System activity and error logs</p>
                    </div>
                </div>
                <button onclick="window.refreshLogs()" class="px-3 py-1.5 bg-surface-800 hover:bg-surface-700 text-surface-300 rounded-lg text-xs font-medium transition-colors flex items-center gap-1.5 border border-surface-700">
                    ${ArrowPathIcon({ className: 'h-3.5 w-3.5' })} Refresh
                </button>
            </div>

            <div class="flex flex-wrap gap-3 items-end">
                <input id="log-search" type="text" placeholder="Search logs..." value="${state.searchText}"
                    class="px-3 py-1.5 bg-surface-800 border border-surface-700 text-surface-50 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-400 placeholder-surface-500 w-48" />

                <select id="log-filter-index" class="px-3 py-1.5 bg-surface-800 border border-surface-700 text-surface-50 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-400">
                    <option value="">All Indices</option>
                    ${indexNames.map(name => `
                        <option value="${name}" ${state.filterIndex === name ? 'selected' : ''}>${name}</option>
                    `).join('')}
                </select>
                <select id="log-filter-type" class="px-3 py-1.5 bg-surface-800 border border-surface-700 text-surface-50 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-400">
                    <option value="">All Types</option>
                    ${logTypes.map(type => `
                        <option value="${type}" ${state.filterType === type ? 'selected' : ''}>${type}</option>
                    `).join('')}
                </select>

                <div class="flex items-center gap-2">
                    <label class="text-xs text-surface-400">From</label>
                    <input id="log-start-date" type="date" value="${state.startDate}"
                        class="px-2 py-1.5 bg-surface-800 border border-surface-700 text-surface-50 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-400" />
                </div>
                <div class="flex items-center gap-2">
                    <label class="text-xs text-surface-400">To</label>
                    <input id="log-end-date" type="date" value="${state.endDate}"
                        class="px-2 py-1.5 bg-surface-800 border border-surface-700 text-surface-50 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-400" />
                </div>
                <button id="log-apply-dates" class="px-3 py-1.5 bg-primary-500 hover:bg-primary-600 text-surface-50 rounded-lg text-xs font-medium transition-colors">
                    Apply
                </button>

                <span class="text-sm text-surface-400 self-center ml-auto">${filtered.length} log entries</span>
            </div>

            <div class="card p-4 lg:p-5">
                ${filtered.length === 0 ? `
                    <div class="text-center py-10">
                        ${InformationCircleIcon({ className: 'h-12 w-12 text-surface-500 mx-auto mb-3' })}
                        <p class="text-surface-400">No log entries found.</p>
                    </div>
                ` : `
                    <div class="overflow-x-auto -mx-4 lg:-mx-5">
                        <table class="w-full text-sm">
                            <thead>
                                <tr class="text-surface-400 text-xs uppercase tracking-wider border-b border-surface-700">
                                    <th class="text-left py-3 px-4 lg:px-5 font-medium">Time</th>
                                    <th class="text-left py-3 px-4 lg:px-5 font-medium">Index</th>
                                    <th class="text-left py-3 px-4 lg:px-5 font-medium">Type</th>
                                    <th class="text-left py-3 px-4 lg:px-5 font-medium">Log</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-surface-700/50">
                                ${filtered.map(item => {
                                    const ts = item.time ? new Date(parseFloat(item.time) * 1000).toLocaleString() : '-';
                                    return `
                                    <tr class="hover:bg-surface-700/30 transition-colors">
                                        <td class="py-3 px-4 lg:px-5 text-surface-400 whitespace-nowrap text-xs">${ts}</td>
                                        <td class="py-3 px-4 lg:px-5 text-surface-50">${item.index_name || '-'}</td>
                                        <td class="py-3 px-4 lg:px-5">
                                            <span class="inline-flex items-center gap-1 px-2 py-0.5 text-xs font-medium rounded-full ${logTypeBadge(item.log_type)}">
                                                ${logTypeIcon(item.log_type)}
                                                ${item.log_type || 'info'}
                                            </span>
                                        </td>
                                        <td class="py-3 px-4 lg:px-5 text-surface-300 text-xs max-w-md break-words">${item.log || '-'}</td>
                                    </tr>`;
                                }).join('')}
                            </tbody>
                        </table>
                    </div>
                `}
            </div>
        </div>`;

    document.getElementById('log-search')?.addEventListener('input', (e) => {
        state.searchText = e.target.value;
        render();
    });
    document.getElementById('log-filter-index')?.addEventListener('change', (e) => {
        state.filterIndex = e.target.value;
        render();
    });
    document.getElementById('log-filter-type')?.addEventListener('change', (e) => {
        state.filterType = e.target.value;
        render();
    });
    document.getElementById('log-apply-dates')?.addEventListener('click', () => {
        state.startDate = document.getElementById('log-start-date').value;
        state.endDate = document.getElementById('log-end-date').value;
        fetchLogs();
    });
}

async function fetchLogs() {
    state.loading = true;
    render();
    try {
        const resp = await makeApiCall('/get_log_details', {
            method: 'POST',
            body: { start_date: state.startDate, end_date: state.endDate },
        });
        if (resp?.status === 'success') {
            state.logs = resp.data || [];
        }
    } catch (e) {
        state.logs = [];
    } finally {
        state.loading = false;
        render();
    }
}

export function initLogViewer() {
    window.refreshLogs = fetchLogs;
    state.startDate = todayStr();
    state.endDate = todayStr();
    fetchLogs();
}

const LogViewerPage = () => '<div id="log-viewer-container"></div>';
export default LogViewerPage;
