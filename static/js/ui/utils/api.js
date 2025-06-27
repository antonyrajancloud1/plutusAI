/**
 * A common method to make API calls, handling different methods, body, and response parsing.
 * @param {string} url The endpoint URL to call.
 * @param {object} [options={ method: 'GET' }] Configuration for the fetch request, including method, body, etc.
 * @returns {Promise<any>} The JSON response from the API.
 * @throws An error if the network response is not OK, including status text.
 */
export const makeApiCall = async (url, options = { method: 'GET' }) => {
  try {
    const fetchOptions = {
      method: options.method,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    if (options.body) {
      fetchOptions.body = JSON.stringify(options.body);
    }

    const response = await fetch(url, fetchOptions);

    if (!response.ok) {
      // Try to get more info from the error response body
      let errorBody = 'Could not retrieve error details.';
      try {
        errorBody = await response.text();
      } catch (e) {
        // Ignore if body can't be read
      }
      throw new Error(`API request failed: ${response.status} ${response.statusText}. Details: ${errorBody}`);
    }

    // Handle responses with no content
    if (response.status === 204) {
      return null;
    }
    
    return await response.json();

  } catch (error) {
    console.error(`API call to ${url} failed:`, error);
    // Re-throw the error so the calling component's catch block can handle it
    throw error;
  }
};
