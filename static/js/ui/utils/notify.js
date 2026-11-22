// One toast + clipboard implementation for the whole app. Toasts live in their own
// container outside #root, so a page re-render never wipes them.
import { CheckCircleIcon, XCircleIcon, InformationCircleIcon, XMarkIcon } from '../components/icons.js';
import { esc } from './format.js';

const STYLES = {
    success: { icon: CheckCircleIcon, iconClass: 'text-emerald-400', border: 'border-emerald-500/40', text: 'text-emerald-200' },
    error: { icon: XCircleIcon, iconClass: 'text-red-400', border: 'border-red-500/40', text: 'text-red-200' },
    info: { icon: InformationCircleIcon, iconClass: 'text-blue-400', border: 'border-blue-500/40', text: 'text-blue-200' },
};

function container() {
    let el = document.getElementById('toast-root');
    if (!el) {
        el = document.createElement('div');
        el.id = 'toast-root';
        el.className = 'fixed z-[200] top-14 inset-x-3 sm:inset-x-auto sm:right-5 sm:w-96 flex flex-col gap-2 pointer-events-none';
        document.body.appendChild(el);
    }
    return el;
}

export function toast(message, type = 'success', ms = 4500) {
    const s = STYLES[type] || STYLES.info;
    const el = document.createElement('div');
    el.setAttribute('role', 'alert');
    el.className = `pointer-events-auto bg-surface-800/95 backdrop-blur-sm border-l-4 ${s.border} rounded-lg shadow-lg p-3 flex items-start gap-3 page-enter`;
    el.innerHTML = `
        ${s.icon({ className: `h-5 w-5 flex-shrink-0 ${s.iconClass}` })}
        <p class="flex-1 text-sm font-medium ${s.text} break-words">${esc(message)}</p>
        <button class="p-1 -m-1 text-surface-500 hover:text-surface-300" aria-label="Close">${XMarkIcon({ className: 'h-4 w-4' })}</button>`;
    const close = () => el.remove();
    el.querySelector('button').addEventListener('click', close);
    container().appendChild(el);
    setTimeout(close, ms);
}

export async function copyText(text, label = 'Copied to clipboard') {
    try {
        if (navigator.clipboard && window.isSecureContext) {
            await navigator.clipboard.writeText(text);
        } else {
            const ta = document.createElement('textarea');
            ta.value = text;
            ta.style.cssText = 'position:fixed;opacity:0';
            document.body.appendChild(ta);
            ta.select();
            const copied = document.execCommand('copy');
            ta.remove();
            if (!copied) throw new Error('copy failed');
        }
        toast(label, 'success', 2500);
    } catch {
        toast('Failed to copy', 'error');
    }
}

// Clicking any element with data-copy="text" copies that text.
document.addEventListener('click', (e) => {
    const el = e.target.closest('[data-copy]');
    if (el) copyText(el.dataset.copy, el.dataset.copyLabel || undefined);
});
