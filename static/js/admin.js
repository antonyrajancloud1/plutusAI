const startWSButton = document.getElementById("startWS");
const stopWSButton = document.getElementById("stopWS");
const reGenerateTokenButton = document.getElementById("regenerateToken");
const updateExpiryButton = document.getElementById("updateExpiry");
const wsTypeInput = document.getElementById("ws-input");
//const statusDiv = document.getElementById('ws-status');

// Celery Elements
const statusDot = document.getElementById("celery-status-dot");
const statusText = document.getElementById("celery-status-text");
const restartCeleryBtn = document.getElementById("restartCelery");
const stopCeleryBtn = document.getElementById("stopCelery");
const apiBanner = document.getElementById('apiBanner');

////////////
 // Banner element
    const bannerMessageDiv = document.getElementById('bannerMessage');
    let bannerTimeout; // To store the timeout ID for clearing
const showBanner = (message, type = 'info', duration = 3000) => {
        // Clear any existing banner timeout
        if (bannerTimeout) {
            clearTimeout(bannerTimeout);
        }

        bannerMessageDiv.textContent = message;
        bannerMessageDiv.className = 'banner'; // Reset classes to just 'banner'
        bannerMessageDiv.classList.add('show');

        // Add type-specific class for styling
        if (type === 'success') {
            bannerMessageDiv.classList.add('success');
        } else if (type === 'error') {
            bannerMessageDiv.classList.add('error');
        } else if (type === 'info') {
            bannerMessageDiv.classList.add('info');
        } else {
            bannerMessageDiv.classList.add('info'); // Default to info if type is unknown
        }


        // Hide the banner after the specified duration
        bannerTimeout = setTimeout(() => {
            bannerMessageDiv.classList.remove('show');
            // Optionally clear text after transition to prevent flicker
            setTimeout(() => {
                bannerMessageDiv.textContent = '';
                bannerMessageDiv.className = 'banner'; // Reset classes completely
            }, 3000); // Match CSS transition duration
        }, duration);
    };
/////////

// Function to make an API call and update status
function makeAPICall(method, api_url, payload_data) {
    const options = {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: payload_data ? JSON.stringify(payload_data) : null
    };
    fetch(api_url, options)
        .then(response => response.json())
        .then(data => {
//            statusDiv.textContent = data.message || 'Action completed successfully!';
//            statusDiv.className = data.task_status ? 'status true' : 'status false';
//        alert(data.message || 'Action completed successfully!');
        showBanner(data.message || 'Action completed successfully!', 'success');

        })
        .catch(error => {
            console.error('Error making API call:', error);
            showBanner(error, 'error');
        });
}

// WebSocket Button Actions
startWSButton.addEventListener("click", () => {
    makeAPICall('POST', 'start_ws', { ws_type: wsTypeInput.value });
});
stopWSButton.addEventListener("click", () => {
    makeAPICall('POST', 'stop_ws', { ws_type: wsTypeInput.value });
});
reGenerateTokenButton.addEventListener("click", () => {
    makeAPICall('POST', 'regenerate_token', null);
});
updateExpiryButton.addEventListener("click", () => {
showBanner('Updating Expiry Details', 'info',5000);
    const expiryDetails = {
        expiry_date: "2025-12-31",
        next_expiry_date: "2026-12-31"
    };
    makeAPICall('POST', 'update_expiry_details', expiryDetails);
});

// Add User
document.querySelector(".add-btn").addEventListener("click", () => {
    const email = document.getElementById("email").value;
    const name = document.getElementById("name").value;
    const password = document.getElementById("password").value;
    const userData = { email, name, password };
    makeAPICall('POST', 'add_user', userData);
});

//// Fetch Index Data
//async function fetchIndexData() {
//    try {
//        const response = await fetch('get_index_data');
//        const data = await response.json();
//        if (data.status === "success") {
//            populateTable(data.message.index_data);
//            loadingMessage.style.display = 'none';
//        }
//    } catch (error) {
//        console.error("Error fetching index data:", error);
//    }
//}
//
//// Populate Index Table
//function populateTable(indexData) {
//    const tableBody = document.getElementById("indexTable").querySelector("tbody");
//    tableBody.innerHTML = "";
//    indexData.forEach(item => {
//        const row = `<tr>
//            <td>${item.id}</td>
//            <td>${item.index_name}</td>
//            <td>${item.index_group}</td>
//            <td>${item.index_token}</td>
//            <td>${item.ltp}</td>
//            <td>${item.last_updated_time}</td>
//            <td>${item.qty}</td>
//            <td>${item.current_expiry}</td>
//            <td>${item.next_expiry}</td>
//        </tr>`;
//        tableBody.innerHTML += row;
//    });
//}
// Assume this is at the top of your script.js or within your DOMContentLoaded listener

// Helper for parsing DD-Mon-YYYY format reliably
// This function needs to be accessible within populateTable
const parseDDMonYYYY = (dateString) => {
    if (!dateString) return null; // Handle cases where dateString might be empty or null
    const parts = dateString.split('-');
    if (parts.length !== 3) return null; // Basic validation

    const day = parseInt(parts[0], 10);
    const monthNames = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"];
    const month = monthNames.indexOf(parts[1]);
    const year = parseInt(parts[2], 10);

    // Basic validation for parsed values
    if (isNaN(day) || isNaN(month) || isNaN(year) || month === -1) {
        return null;
    }

    const date = new Date(year, month, day);
    date.setHours(0, 0, 0, 0); // Normalize to start of day
    return date;
};


// Fetch Index Data
async function fetchIndexData() {
    // Assuming loadingMessage is defined globally or passed into this scope
    const loadingMessage = document.getElementById('loadingMessage'); // Ensure this element exists in your HTML
    if (loadingMessage) {
        loadingMessage.style.display = 'block'; // Show loading message before fetch
        loadingMessage.textContent = 'Loading Index Data...'; // Reset text
        loadingMessage.style.color = '#bb86fc'; // Reset color
    }

    try {
        const response = await fetch('get_index_data'); // This will hit your Flask/backend endpoint
        const data = await response.json();

        if (data.status === "success") {
            populateTable(data.message.index_data);
            if (loadingMessage) {
                loadingMessage.style.display = 'none'; // Hide loading message on success
            }
            // Assuming showBanner is defined globally or accessible here
            //showBanner('Index data loaded successfully!', 'success');
        } else {
            console.error("Error fetching index data:", data.message);
            if (loadingMessage) {
                loadingMessage.textContent = `Failed to load data: ${data.message}`;
                loadingMessage.style.color = '#f44336';
            }
            showBanner(`Failed to load index data: ${data.message}`, 'error');
        }
    } catch (error) {
        console.error("Error fetching index data:", error);
        if (loadingMessage) {
            loadingMessage.textContent = 'Failed to load data. Please check network.';
            loadingMessage.style.color = '#f44336';
        }
        // Assuming showBanner is defined globally or accessible here
        showBanner('Failed to load index data!', 'error');
    }
}

// Populate Index Table
function populateTable(indexData) {
    const tableBody = document.getElementById("indexDataTableBody"); // Ensure this ID matches your HTML
    if (!tableBody) {
        console.error("Error: Table body element with ID 'indexDataTableBody' not found.");
        return;
    }
    tableBody.innerHTML = ""; // Clear existing rows

    const currentDate = new Date();
    currentDate.setHours(0, 0, 0, 0); // Normalize current date to the start of the day

    indexData.forEach(item => {
        const currentExpiryDate = parseDDMonYYYY(item.current_expiry.toLowerCase());
        const nextExpiryDate = parseDDMonYYYY(item.next_expiry.toLowerCase());

        let rowClass = '';
        let currentExpiryClass = '';
        let nextExpiryClass = '';

        if (currentExpiryDate && currentExpiryDate < currentDate) {
            rowClass = 'expired-row'; // Apply to the whole row
            currentExpiryClass = 'expired-text'; // Apply to current expiry cell
        } else if (currentExpiryDate) { // If not expired and date is valid
            currentExpiryClass = 'current-text'; // Apply green to current expiry cell
        }

        // Check next expiry independently for its text color
        if (nextExpiryDate && nextExpiryDate < currentDate) {
            nextExpiryClass = 'expired-text';
        } else if (nextExpiryDate) { // If not expired and date is valid
            nextExpiryClass = 'current-text';
        }


        const row = `<tr class="${rowClass}">
            <td>${item.id}</td>
            <td>${item.index_name}</td>
            <td>${item.index_group}</td>
            <td>${item.index_token}</td>
            <td>${item.ltp}</td>
            <td>${item.last_updated_time}</td>
            <td>${item.qty}</td>
            <td class="${currentExpiryClass}">${item.current_expiry}</td>
            <td class="${nextExpiryClass}">${item.next_expiry}</td>
        </tr>`;
        tableBody.innerHTML += row;
    });
}

// You would call fetchIndexData when your page loads, e.g., in DOMContentLoaded
// document.addEventListener('DOMContentLoaded', () => {
//     fetchIndexData();
//     // ... other event listeners and setup
// });
// Celery Status Monitoring
async function fetchCeleryStatus() {
    try {
        const response = await fetch('/get_celery_status');
        const data = await response.json();
        if (data.celery_running) {
            statusDot.classList.remove("disconnected");
            statusDot.classList.add("connected");
            statusText.textContent = "Running";
        } else {
            statusDot.classList.remove("connected");
            statusDot.classList.add("disconnected");
            statusText.textContent = "Stopped";
        }
    } catch (error) {
        statusText.textContent = "Error checking status";
        statusDot.classList.remove("connected");
        statusDot.classList.add("disconnected");
    }
}

restartCeleryBtn.addEventListener("click", async () => {
    await makeAPICall('POST', '/restart_celery');
    fetchCeleryStatus();
});
stopCeleryBtn.addEventListener("click", async () => {
    await makeAPICall('POST', '/stop_celery');
    fetchCeleryStatus();
});


// Initial data fetch
fetchIndexData();
fetchCeleryStatus();
// setInterval(fetchCeleryStatus, 10000);
