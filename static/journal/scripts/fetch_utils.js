// ==============================
// Module: Fetch Utilities
// ==============================
export const fetchUtils = (() => {
    function getCSRFToken() {
        const name = 'csrftoken=';
        const decodedCookie = decodeURIComponent(document.cookie);
        const cookies = decodedCookie.split(';').map(cookie => cookie.trim());
        for (let cookie of cookies) {
            if (cookie.startsWith(name)) {
                return cookie.substring(name.length);
            }
        }
        return '';
    }

    function fetchWithCSRF(url, options = {}) {
        const headers = options.headers || {};
        headers['X-CSRFToken'] = getCSRFToken();
        headers['Content-Type'] = headers['Content-Type'] || 'application/json';

        return fetch(url, { ...options, headers });
    }

    return { getCSRFToken, fetchWithCSRF };
})();
