export async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(`${url}`, options);
        const responseText = await response.text();

        let data;

        try {
            data = responseText ? JSON.parse(responseText) : null;
        } catch {
            data = responseText;
        }

        if (!response.ok) {
            throw new Error(
                data?.detail ||
                `API request failed with status ${response.status}`
            );
        }

        return data
    } catch (err) {
        console.error("API request failed: ", err);
        throw err;
    }
}
