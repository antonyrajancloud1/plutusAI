// Formatting helpers shared by every page.

const inrFormatters = {};

export function formatINR(value, decimals = 2) {
    const n = typeof value === 'string' ? parseFloat(value) : value;
    if (!inrFormatters[decimals]) {
        inrFormatters[decimals] = new Intl.NumberFormat('en-IN', {
            style: 'currency', currency: 'INR',
            minimumFractionDigits: decimals, maximumFractionDigits: decimals,
        });
    }
    return inrFormatters[decimals].format(Number.isFinite(n) ? n : 0);
}

// Backend timestamps are epoch seconds (as numbers or strings).
export function formatTime(epochSeconds) {
    const ms = parseFloat(epochSeconds) * 1000;
    if (!Number.isFinite(ms) || ms === 0) return '-';
    return new Date(ms).toLocaleString('en-IN', {
        year: '2-digit', month: 'short', day: 'numeric',
        hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true,
    });
}

const HTML_ESCAPES = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };

// Escape anything that came from the server or a user before putting it in HTML.
export function esc(value) {
    if (value === null || value === undefined) return '';
    return String(value).replace(/[&<>"']/g, ch => HTML_ESCAPES[ch]);
}

// "bank_nifty" -> "Bank Nifty"
export function displayName(key) {
    return String(key || '').replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

export const pnlClass = (n) => (n >= 0 ? 'text-emerald-400' : 'text-red-400');

export const sum = (rows, field) => (rows || []).reduce((acc, r) => acc + (parseFloat(r[field]) || 0), 0);
