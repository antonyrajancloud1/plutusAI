/**
 * Calls a backend endpoint and returns the parsed JSON body.
 * Throws on network errors and non-2xx responses; the error message is the
 * server's own `message` when it sent one (validation errors come back as 400).
 */
export const makeApiCall = async (url, options = {}) => {
    const fetchOptions = {
        method: options.method || 'GET',
        headers: { 'Content-Type': 'application/json', ...options.headers },
    };
    if (options.body) fetchOptions.body = JSON.stringify(options.body);

    const response = await fetch(url, fetchOptions);
    if (response.status === 204) return null;

    let data = null;
    try { data = await response.json(); } catch { /* non-JSON body */ }

    if (!response.ok) {
        throw new Error(data?.message || `${response.status} ${response.statusText}`);
    }
    // A session that expired mid-use gets {"status":"failed","message":"unauthorised"}.
    if (data?.status === 'failed' && /unauthori[sz]ed/i.test(data?.message || '')) {
        window.location.href = '/login';
    }
    return data;
};

// Backend messages are often keys ("config_values_updated"); turn them into text.
const MESSAGES = {
    internal_error: 'Something went wrong on the server. Check the logs.',
    unauthorised: 'You are not allowed to do that.',
    index_details_not_found: 'No settings found for this index.',
    fill_mandatory: 'Please fill all the fields.',
    token_is_valid: 'Broker token is valid',
    token_is_invalid: 'Broker token is invalid',
};

export function humanize(message) {
    if (typeof message !== 'string') return message;
    if (MESSAGES[message]) return MESSAGES[message];
    if (/^[a-z]+(_[a-z]+)+$/.test(message)) {
        const text = message.replace(/_/g, ' ');
        return text.charAt(0).toUpperCase() + text.slice(1);
    }
    return message;
}

/** For actions (start/stop/save/order): resolves to { ok, message, data } and never throws. */
export async function runAction(url, options = {}) {
    try {
        const data = await makeApiCall(url, options);
        const failed = data?.status === 'failed' || data?.success === false;
        const message = data?.message ?? data?.details ?? (failed ? 'Request failed' : 'Done');
        return { ok: !failed, message: humanize(typeof message === 'string' ? message : (failed ? 'Request failed' : 'Done')), data };
    } catch (err) {
        return { ok: false, message: humanize(err.message) || 'Network error', data: null };
    }
}
