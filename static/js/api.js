/**
 * Helper function for API calls
 */
async function fetchAPI(endpoint, options = {}) {
    try {
        const response = await fetch(endpoint, options);
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`API error (${response.status}): ${errorText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error(`API call failed: ${error.message}`);
        throw error;
    }
}
