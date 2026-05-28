import { CogIcon } from './icons.js';
import { makeApiCall } from '../utils/api.js';
import Toast from './Toast.js';

let state = {
    chatId: '',
    notifyOnError: false,
    loading: true,
    saving: false,
    toast: null,
};

function showToast(message, type) {
    state.toast = { message, type };
    render();
    setTimeout(() => {
        state.toast = null;
        const el = document.querySelector('.settings-toast');
        if (el) el.remove();
    }, 5000);
}

async function loadSettings() {
    state.loading = true;
    render();
    try {
        const response = await makeApiCall('/get_telegram_settings');
        if (response.status === 'success') {
            state.chatId = response.chat_id || '';
            state.notifyOnError = response.notify_on_error || false;
        }
    } catch (err) {
        state.chatId = '';
        state.notifyOnError = false;
    } finally {
        state.loading = false;
        render();
    }
}

async function saveSettings(event) {
    event.preventDefault();
    state.saving = true;
    render();
    try {
        const form = event.target;
        const formData = new FormData(form);
        const response = await makeApiCall('/update_telegram_settings', {
            method: 'POST',
            body: {
                chat_id: formData.get('chat_id') || '',
                notify_on_error: form.elements.notify_on_error.checked,
            },
        });
        if (response.status === 'success') {
            state.chatId = response.chat_id || '';
            state.notifyOnError = response.notify_on_error || false;
            showToast('Telegram settings saved successfully!', 'success');
        } else {
            showToast('Failed to save settings.', 'error');
        }
    } catch (err) {
        showToast('Failed to save settings: ' + err.message, 'error');
    } finally {
        state.saving = false;
        render();
    }
}

function render() {
    const container = document.getElementById('settings-page-container');
    if (!container) return;

    if (state.loading) {
        container.innerHTML = `
            <div class="flex items-center justify-center min-h-[200px]">
                <div class="animate-spin rounded-full h-10 w-10 border-t-4 border-b-4 border-primary-500"></div>
                <p class="ml-4 text-surface-50">Loading settings...</p>
            </div>
        `;
        return;
    }

    const toastHtml = state.toast ? `<div class="settings-toast fixed top-20 right-5 z-50">${Toast(state.toast)}</div>` : '';

    container.innerHTML = `
        ${toastHtml}
        <div class="space-y-6">
            <div class="flex items-center gap-3 mb-2">
                <h2 class="text-xl lg:text-2xl font-bold text-surface-50 flex items-center gap-3">
                    ${CogIcon({ className: "h-6 w-6 text-primary-400" })}
                    Settings
                </h2>
            </div>
            <p class="text-surface-400 -mt-4">Configure your notification preferences.</p>

            <div class="max-w-2xl">
                <div class="card p-4 lg:p-5">
                    <h3 class="text-sm font-semibold text-surface-50 mb-6">Telegram Notifications</h3>

                    <form id="telegram-settings-form">
                        <div class="mb-5">
                            <label for="chat_id" class="block text-sm font-medium text-surface-50 mb-2">
                                Telegram Chat ID
                            </label>
                            <input
                                type="text"
                                id="chat_id"
                                name="chat_id"
                                value="${state.chatId}"
                                placeholder="Enter Telegram chat ID(s) (e.g. 123456789, 987654321)"
                                class="w-full px-4 py-2.5 bg-surface-800 border border-surface-700 text-surface-50 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-colors placeholder-surface-500"
                            />
                            <p class="mt-1.5 text-xs text-surface-400">
                                You can enter multiple chat IDs separated by commas. To get your chat ID, send a message to <a href="https://t.me/userinfobot" target="_blank" class="text-primary-400 underline">@userinfobot</a> on Telegram.
                            </p>
                        </div>

                        <div class="mb-6">
                            <label class="relative inline-flex items-center cursor-pointer">
                                <input
                                    type="checkbox"
                                    name="notify_on_error"
                                    class="sr-only peer"
                                    ${state.notifyOnError ? 'checked' : ''}
                                />
                                <div class="w-11 h-6 bg-surface-700 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-400/30 rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-surface-800 after:border-surface-600 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-500"></div>
                                <span class="ml-3 text-sm font-medium text-surface-50">
                                    Notify when error occurs
                                </span>
                            </label>
                        </div>

                        <button
                            type="submit"
                            class="px-6 py-2.5 bg-primary-500 hover:bg-primary-600 text-surface-50 font-medium rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-primary-400/50 disabled:opacity-50 disabled:cursor-not-allowed"
                            ${state.saving ? 'disabled' : ''}
                        >
                            ${state.saving ? 'Saving...' : 'Save Settings'}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    `;

    document.getElementById('telegram-settings-form')?.addEventListener('submit', saveSettings);
}

export function initSettingsPage() {
    loadSettings();
}

const TelegramSettingsPage = () => {
    return '<div id="settings-page-container"></div>';
};

export default TelegramSettingsPage;
