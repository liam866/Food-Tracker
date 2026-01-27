export async function apiRequest(endpoint, method = 'GET', body = null) {
    console.log(`[API] Request: ${method} ${endpoint}`, body || '');
    try {
        const options = {
            method,
            headers: { 'Content-Type': 'application/json' },
        };
        if (body) {
            options.body = JSON.stringify(body);
        }
        const response = await fetch(endpoint, options);
        if (!response.ok) {
            console.error(`[API] Error ${response.status} for ${method} ${endpoint}`);
            if (response.status === 204) return null;
            throw new Error('API request failed');
        }
         if (response.status === 204) return null;
        const data = await response.json();
        console.log(`[API] Response for ${method} ${endpoint}:`, data);
        return data;
    } catch (error) {
        console.error(`[API] Network or fatal error for ${method} ${endpoint}:`, error);
        throw error;
    }
}
