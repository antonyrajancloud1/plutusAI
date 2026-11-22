// Shared building blocks: page header, buttons, status pill, form fields, modal,
// and a table that turns into stacked cards on phones.
import { XMarkIcon, CheckCircleIcon, XCircleIcon, PlayCircleIcon, StopCircleIcon, InformationCircleIcon } from './icons.js';
import { esc } from '../utils/format.js';

export const inputClass = 'mt-1 block w-full px-3 py-2.5 sm:py-2 bg-surface-900 text-surface-50 border border-surface-700 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-primary-400 text-base sm:text-sm placeholder-surface-500';
export const labelClass = 'block text-sm font-medium text-surface-400';

const BUTTON_VARIANTS = {
    primary: 'bg-primary-500 hover:bg-primary-600 text-white',
    success: 'bg-emerald-600 hover:bg-emerald-700 text-white',
    danger: 'bg-red-600 hover:bg-red-700 text-white',
    warning: 'bg-amber-500 hover:bg-amber-600 text-white',
    ghost: 'bg-surface-800 hover:bg-surface-700 text-surface-200 border border-surface-700',
};

/** attrs: extra HTML attributes as a string, e.g. 'data-action="start" data-index="nifty"'. */
export function Button({ label, variant = 'primary', attrs = '', size = 'md', type = 'button' }) {
    const sizing = size === 'sm' ? 'text-xs px-3 py-2 sm:py-1.5' : 'text-sm px-4 py-2.5 sm:py-2';
    return `<button type="${type}" ${attrs} class="inline-flex items-center justify-center gap-1.5 font-medium rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${sizing} ${BUTTON_VARIANTS[variant]}">${label}</button>`;
}

/** Disables a button and shows "…" while `work` runs, then restores it. */
export async function withBusy(button, work) {
    const html = button.innerHTML;
    button.disabled = true;
    button.innerHTML = '<span class="animate-pulse">…</span>';
    try { return await work(); } finally {
        if (button.isConnected) { button.disabled = false; button.innerHTML = html; }
    }
}

export function PageHeader({ title, icon, subtitle, actions = '' }) {
    return `
    <div class="flex flex-wrap items-center justify-between gap-3 mb-5">
      <div class="flex items-center gap-3 min-w-0">
        ${icon ? icon({ className: 'h-6 w-6 text-primary-400 flex-shrink-0' }) : ''}
        <div class="min-w-0">
          <h1 class="text-lg sm:text-xl lg:text-2xl font-bold text-surface-50 truncate">${esc(title)}</h1>
          ${subtitle ? `<p class="text-xs sm:text-sm text-surface-400 mt-0.5">${esc(subtitle)}</p>` : ''}
        </div>
      </div>
      ${actions ? `<div class="flex flex-wrap gap-2">${actions}</div>` : ''}
    </div>`;
}

export function EmptyState({ title, message = 'No data available', icon = InformationCircleIcon }) {
    return `
    <div class="flex flex-col items-center justify-center py-12 text-surface-400 text-center">
      ${icon({ className: 'h-12 w-12 mb-3 opacity-40' })}
      <p class="font-medium">${esc(title)}</p>
      <p class="text-sm mt-1">${esc(message)}</p>
    </div>`;
}

const RUNNING = ['running', 'active', 'started', 'initiated', 'long_placed', 'short_placed', 'order_placed'];

export function isRunning(status) {
    return RUNNING.includes(String(status || '').toLowerCase());
}

export function StatusPill(status) {
    const s = String(status || 'stopped').toLowerCase();
    const running = isRunning(s);
    const stopped = s === 'stopped' || s === '';
    const cls = running ? 'bg-emerald-500/10 text-emerald-400' : stopped ? 'bg-red-500/10 text-red-400' : 'bg-amber-500/10 text-amber-400';
    const Icon = running ? PlayCircleIcon : stopped ? StopCircleIcon : InformationCircleIcon;
    return `<span class="inline-flex items-center gap-1 px-2.5 py-1 text-xs font-semibold rounded-full whitespace-nowrap ${cls}">${Icon({ className: 'h-3.5 w-3.5' })}${esc(String(status || 'stopped').replace(/_/g, ' '))}</span>`;
}

export function YesNo(value) {
    return value
        ? `<span class="inline-flex items-center gap-1 text-emerald-400">${CheckCircleIcon({ className: 'h-4 w-4' })}Yes</span>`
        : `<span class="inline-flex items-center gap-1 text-red-400">${XCircleIcon({ className: 'h-4 w-4' })}No</span>`;
}

// ------------------------------------------------------------------ forms

/**
 * field: { name, label, type: 'text'|'number'|'textarea'|'checkbox'|'select', options, readonly, full }
 */
export function FormField(field, value) {
    const id = `f-${field.name}`;
    if (field.type === 'checkbox') {
        return `
        <label for="${id}" class="flex items-center gap-3 py-1.5 ${field.full ? 'sm:col-span-2' : ''}">
          <input id="${id}" name="${field.name}" type="checkbox" ${value ? 'checked' : ''} class="h-5 w-5 sm:h-4 sm:w-4 accent-primary-500" />
          <span class="text-sm text-surface-300">${esc(field.label)}</span>
        </label>`;
    }
    const ro = field.readonly ? 'readonly' : '';
    const roClass = field.readonly ? 'opacity-60 cursor-not-allowed' : '';
    let control;
    if (field.type === 'textarea') {
        control = `<textarea id="${id}" name="${field.name}" rows="3" ${ro} class="${inputClass} ${roClass}">${esc(value)}</textarea>`;
    } else if (field.type === 'select') {
        control = `<select id="${id}" name="${field.name}" ${ro} class="${inputClass} ${roClass}">
            ${field.options.map(o => `<option value="${esc(o.value)}" ${String(o.value) === String(value) ? 'selected' : ''}>${esc(o.label)}</option>`).join('')}
          </select>`;
    } else {
        const inputMode = field.type === 'number' ? 'inputmode="decimal"' : '';
        control = `<input id="${id}" name="${field.name}" type="text" ${inputMode} value="${esc(value)}" ${ro} class="${inputClass} ${roClass}" />`;
    }
    return `<div class="${field.full || field.type === 'textarea' ? 'sm:col-span-2' : ''}"><label for="${id}" class="${labelClass}">${esc(field.label)}</label>${control}</div>`;
}

/** Reads a form built from `fields` back into an object (checkboxes as booleans). */
export function readForm(form, fields) {
    const out = {};
    for (const f of fields) {
        const el = form.elements[f.name];
        if (!el) continue;
        out[f.name] = f.type === 'checkbox' ? el.checked : el.value.trim();
    }
    return out;
}

// ------------------------------------------------------------------ modal

const modalRoot = () => document.getElementById('modal-container');

export function closeModal() {
    const root = modalRoot();
    if (root) root.innerHTML = '';
    document.body.classList.remove('overflow-hidden');
}

/**
 * Opens a form modal. `onSubmit(values, form)` returns true to close it.
 * Full-screen sheet on phones, centred dialog from `sm` up.
 */
export function openFormModal({ title, icon, fields, values = {}, submitLabel = 'Save Changes', onSubmit }) {
    const root = modalRoot();
    if (!root) return;
    root.innerHTML = `
    <div class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-end sm:items-center justify-center sm:p-4" data-modal-backdrop>
      <div role="dialog" aria-modal="true" class="bg-surface-800 border border-surface-700 w-full sm:max-w-2xl rounded-t-2xl sm:rounded-xl shadow-xl max-h-[92vh] flex flex-col page-enter">
        <div class="flex items-center justify-between px-5 py-4 border-b border-surface-700">
          <h2 class="text-base sm:text-lg font-semibold text-surface-50 flex items-center gap-2 min-w-0">
            ${icon ? icon({ className: 'h-5 w-5 text-primary-400 flex-shrink-0' }) : ''}<span class="truncate">${esc(title)}</span>
          </h2>
          <button type="button" data-modal-close class="p-2 -m-2 text-surface-500 hover:text-surface-300" aria-label="Close">${XMarkIcon({ className: 'h-5 w-5' })}</button>
        </div>
        <form class="flex flex-col min-h-0 flex-1" novalidate>
          <div class="overflow-y-auto px-5 py-4 grid grid-cols-1 sm:grid-cols-2 gap-4">
            ${fields.map(f => FormField(f, values[f.name])).join('')}
          </div>
          <div class="px-5 py-3 border-t border-surface-700 flex gap-3 justify-end pb-[max(0.75rem,env(safe-area-inset-bottom))]">
            ${Button({ label: 'Cancel', variant: 'ghost', attrs: 'data-modal-close' })}
            ${Button({ label: esc(submitLabel), type: 'submit' })}
          </div>
        </form>
      </div>
    </div>`;
    document.body.classList.add('overflow-hidden');

    root.querySelectorAll('[data-modal-close]').forEach(b => b.addEventListener('click', closeModal));
    root.querySelector('[data-modal-backdrop]').addEventListener('click', (e) => {
        if (e.target.hasAttribute('data-modal-backdrop')) closeModal();
    });
    const form = root.querySelector('form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submit = form.querySelector('[type="submit"]');
        const done = await withBusy(submit, () => onSubmit(readForm(form, fields), form));
        if (done) closeModal();
    });
}

document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeModal(); });

// ------------------------------------------------------------------ responsive table

/**
 * columns: [{ label, render(row) -> html, align: 'left'|'right'|'center', primary: bool, hideOnMobile: bool }]
 * Rendered as a table from `md` up and as one card per row below that.
 * `primary` columns form the card's title line; the rest become label/value pairs.
 */
export function DataTable({ columns, rows, empty = 'No data available', rowKey }) {
    if (!rows?.length) return `<p class="text-sm text-surface-400 text-center py-8">${esc(empty)}</p>`;
    const align = (c) => (c.align === 'right' ? 'text-right' : c.align === 'center' ? 'text-center' : 'text-left');
    const primary = columns.filter(c => c.primary);
    const rest = columns.filter(c => !c.primary && !c.hideOnMobile);

    const table = `
    <div class="hidden md:block overflow-x-auto -mx-4 lg:-mx-5">
      <table class="w-full text-sm">
        <thead><tr class="text-surface-400 text-xs uppercase tracking-wider border-b border-surface-700">
          ${columns.map(c => `<th class="${align(c)} py-3 px-4 lg:px-5 font-medium whitespace-nowrap">${esc(c.label)}</th>`).join('')}
        </tr></thead>
        <tbody class="divide-y divide-surface-700/50">
          ${rows.map((r, i) => `<tr ${rowKey ? `data-row="${esc(rowKey(r, i))}"` : ''} class="hover:bg-surface-700/30 transition-colors">
            ${columns.map(c => `<td class="${align(c)} py-3 px-4 lg:px-5 text-surface-300">${c.render(r)}</td>`).join('')}
          </tr>`).join('')}
        </tbody>
      </table>
    </div>`;

    const cards = `
    <div class="md:hidden space-y-3">
      ${rows.map((r, i) => `
        <div ${rowKey ? `data-row="${esc(rowKey(r, i))}"` : ''} class="rounded-lg border border-surface-700 bg-surface-900/40 p-3">
          ${primary.length ? `<div class="flex items-start justify-between gap-2 mb-2">${primary.map(c => `<div class="min-w-0 text-surface-50 font-medium break-words">${c.render(r)}</div>`).join('')}</div>` : ''}
          <dl class="grid grid-cols-2 gap-x-3 gap-y-2 text-sm">
            ${rest.map(c => `<div class="${c.wide ? 'col-span-2' : ''} min-w-0"><dt class="text-[11px] uppercase tracking-wider text-surface-500">${esc(c.label)}</dt><dd class="text-surface-200 break-words">${c.render(r)}</dd></div>`).join('')}
          </dl>
        </div>`).join('')}
    </div>`;
    return table + cards;
}

export const Card = (inner, extra = '') => `<div class="card p-4 lg:p-5 ${extra}">${inner}</div>`;

export const CardTitle = (title, right = '') => `
    <div class="flex flex-wrap items-center justify-between gap-2 mb-4">
      <h2 class="text-sm font-semibold text-surface-50">${esc(title)}</h2>${right}
    </div>`;
