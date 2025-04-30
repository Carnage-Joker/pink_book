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

        console.warn("⚠️ CSRF token not found in cookies! Requests may fail.");
        return '';  // Return empty string if CSRF token is missing
    }

    async function fetchWithCSRF(url, options = {}) {
        const headers = options.headers || {};
        headers['X-CSRFToken'] = getCSRFToken();
        headers['Content-Type'] = headers['Content-Type'] || 'application/json';

        try {
            const response = await fetch(url, { ...options, headers });

            if (!response.ok) {
                // Try to parse error response
                const errorData = await response.json().catch(() => ({ message: "Unknown error occurred" }));
                throw new Error(errorData.message || `HTTP Error ${response.status}`);
            }

            return response.json();
        } catch (error) {
            console.error("❌ Fetch request failed:", error.message);
            throw error; // Rethrow so calling functions can handle it
        }
    }

    return { getCSRFToken, fetchWithCSRF };
})();
