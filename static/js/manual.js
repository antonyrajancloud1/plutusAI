// Function to dynamically populate the table based on the data
function populateTable(data) {
    const tableBody = document.getElementById('tradeTableBody');
    tableBody.innerHTML = ''; // Clear existing content

    data.message.forEach((item, index) => {
        const row = document.createElement('tr');

        row.innerHTML = `
            <td>
                <button class="buy-button" data-index="${index}">Buy</button>
                <button class="sell-button" data-index="${index}" ${item.order_status !== 'order_placed' ? 'disabled' : ''}>Sell</button>
                <button class="exit-button" data-index="${index}" disabled>Exit</button>
                <button class="edit-button" data-index="${index}" ${item.order_status !== 'order_placed' ? 'disabled' : ''}>Edit</button>
                <button class="add-button" data-index="${index}" disabled>Add</button>
            </td>
            <td>${item.index_name}</td>
            <td><input type="text" value="${item.lots}" id="lots-${index}"></td>
            <td><input type="text" value="${item.trigger}" id="trigger-${index}"></td>
            <td><input type="text" value="${item.stop_loss}" id="sl-${index}"></td>
            <td><input type="text" value="${item.target}" id="target-${index}"></td>
            <td><input type="text" value="${item.strike}" id="strike-${index}"></td>
            <td>${item.current_premium}</td>
        `;
        tableBody.appendChild(row);
    });
}

// Delegate event listeners for Buy, Sell, and Edit buttons
document.getElementById('tradeTableBody').addEventListener('click', function (event) {
    const target = event.target;
    const index = target.getAttribute('data-index');

    if (target.classList.contains('buy-button')) {
        handleOrder('place_order_buy', index);
    } else if (target.classList.contains('sell-button')) {
        handleOrder('place_order_sell', index);
    } else if (target.classList.contains('edit-button')) {
        editOrder(index);
    }
});

async function handleOrder(url, index) {
    const orderDetails = getOrderDetails(index);
    await placeOrder(url, orderDetails);
}

// Function to handle Edit button click
function editOrder(index) {
    const index_name = document.querySelector(`#tradeTableBody tr:nth-child(${parseInt(index) + 1}) td:nth-child(2)`).textContent.trim();
    fetchEditOrderDetails(index_name);
}

// Fetch edit details from API
async function fetchEditOrderDetails(index_name) {
    try {
        const response = await fetch(`manual_details?index_name=${index_name}`);
        const data = await response.json();

        if (data.status === 'success' && data.message.length > 0) {
            createEditForm(data.message[0]);
        } else {
            showResult('Failed to fetch details for editing.', false);
        }
    } catch (error) {
        showResult('Error fetching details: ' + error.message, false);
    }
}

// Create and show the edit form in a modal popup
function createEditForm(order) {
    const modal = document.getElementById('editModal');
    const form = document.getElementById('editOrderForm');

    // Clear previous form content
    form.innerHTML = `
        <h3>Edit Order for ${order.index_name}</h3>
        <label for="edit-lots">Lots:</label>
        <input type="text" id="edit-lots" value="${order.lots}" name="lots"><br><br>

        <label for="edit-trigger">Trigger:</label>
        <input type="text" id="edit-trigger" value="${order.trigger}" name="trigger"><br><br>

        <label for="edit-stop_loss">Stop Loss:</label>
        <input type="text" id="edit-stop_loss" value="${order.stop_loss}" name="stop_loss"><br><br>

        <label for="edit-target">Target:</label>
        <input type="text" id="edit-target" value="${order.target}" name="target"><br><br>

        <label for="edit-strike">Strike:</label>
        <input type="text" id="edit-strike" value="${order.strike}" name="strike"><br><br>

        <button type="button" id="saveChanges">Save Changes</button>
        <button type="button" id="cancelEdit">Cancel</button>
    `;

    // Show the modal
    modal.style.display = 'block';

    document.getElementById('saveChanges').addEventListener('click', function () {
        saveOrderChanges(order.index_name);
    });

    document.getElementById('cancelEdit').addEventListener('click', function () {
        modal.style.display = 'none';
    });



}

// Save changes
async function saveOrderChanges(index_name) {
    const orderDetails = {
        index_name: index_name,
        lots: document.getElementById('edit-lots').value,
        trigger: document.getElementById('edit-trigger').value,
        stop_loss: document.getElementById('edit-stop_loss').value,
        target: document.getElementById('edit-target').value,
        strike: document.getElementById('edit-strike').value
    };

    if (!validateForm(orderDetails)) {
        showResult('Please fill in all fields correctly.', false);
        return;
    }

    try {
        const response = await fetch('update_manual_details', { // Replace with actual save URL
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(orderDetails)
        });

        const result = await response.json();
        if (result.status === 'success') {
            showResult('Index updated successfully.', true);
            document.getElementById('editModal').style.display = 'none';
            fetchData(); // Refresh table after changes
        } else {
            showResult(`Failed to update: ${result.message}`, false);
        }
    } catch (error) {
        showResult(`Error updating order: ${error.message}`, false);
    }
}

// Validate form fields
function validateForm(orderDetails) {
    return Object.values(orderDetails).every(value => value.trim() !== '');
}

// Function to get order details from the row based on index
function getOrderDetails(index) {
    return {
        index_name: document.querySelector(`#tradeTableBody tr:nth-child(${parseInt(index) + 1}) td:nth-child(2)`).textContent.trim(),
        lots: document.getElementById(`lots-${index}`).value,
        trigger: document.getElementById(`trigger-${index}`).value,
        stop_loss: document.getElementById(`sl-${index}`).value,
        target: document.getElementById(`target-${index}`).value,
        strike: document.getElementById(`strike-${index}`).value
    };
}

// Function to make API call to place_order
async function placeOrder(url, orderDetails) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(orderDetails)
        });
        const result = await response.json();

        if (result.status === 'success') {
            showResult(result.message, true);
        } else {
            showResult(`Failed to place order: ${result.message}`, false);
        }
    } catch (error) {
        showResult(`Error placing order: ${error.message}`, false);
    }
}

// Fetch data from the API to populate the table
async function fetchData() {
    try {
        const response = await fetch('manual_details'); // Replace with actual API endpoint URL
        const data = await response.json();

        if (data.status === 'success') {
            populateTable(data);
            document.getElementById('tkn_btn').addEventListener('click', function () {
            reGenTokenData();
            });
            getTokenData();
        } else {
            showResult('Failed to fetch data', false);
        }
    } catch (error) {
        showResult(`Error fetching data: ${error.message}`, false);
    }
}

// Function to show a result (can be tied to specific button actions)
function showResult(message, isSuccess = true) {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = message;
    resultDiv.className = isSuccess ? 'success' : 'error';  // Toggle between success and error styles
    resultDiv.style.display = 'block';  // Show the div
}

// Fetch data from the API to populate the table
async function getTokenData() {
    try {
        const response = await fetch("get_auth_token", {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        const data = await response.json(); // ✅ Parse JSON once and store it

        const token_details = document.getElementById('token_details');

        if (data.status === 'success') {
            token_details.innerHTML = data.message;
        } else {
            token_details.innerHTML = "No Token Present";
        }

//        console.log(data); // ✅ Log the parsed JSON object, NOT response.json()

    } catch (error) {
        document.getElementById('token_details').innerHTML = error;
    }
}


async function reGenTokenData() {
    try {
        const response = await fetch("generate_auth_token", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }

        });
        const token_details = document.getElementById('token_details');
        const data = await response.json();
        if (data.status === 'success') {
            token_details.innerHTML = data.message
        } else {
           token_details.innerHTML = "No Token Present"
        }
console.log(response.json())
    } catch (error) {
        token_details.innerHTML =error
    }
}


// Fetch and populate the table on page load
//window.onload = fetchData;




// Call the function when the page loads
window.onload = function () {
    fetchData();  // Existing function to fetch table data
    fetchStrategySummary();  // Fetch and display the chart
};






//document.addEventListener("DOMContentLoaded", function () {
//    fetchStrategySummary();  // Fetch and display the strategy chart
//
//    fetchData();  // Ensure trade table data is fetched
//});

// Function to fetch strategy summary and display in a Chart.js bar chart
async function fetchStrategySummary() {
    try {
//        const response = await fetch("http://localhost:8000/get_strategy_summary");
        const response = await fetch("get_strategy_summary", {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }

        });
        const data = await response.json();

        // Check if API response contains the expected structure
        if (!data || data.status !== "success" || !data.summary) {
            console.error("Unexpected API response:", data);
            return;
        }

//        renderChart(data.summary.full_summary); // ✅ Pass correct data structure
        renderTable(data.summary.full_summary, "fullSummaryTable");
        renderTable(data.summary.current_day_summary, "currentDaySummaryTable");
    } catch (error) {
        console.error("Error fetching strategy summary:", error);
    }
}


// Function to render the chart using Chart.js
function renderChart(summaryData) {
    const canvas = document.getElementById("strategyChart");

    if (!canvas) {
        console.error("Error: 'strategyChart' canvas element not found in HTML.");
        return;
    }

    const ctx = canvas.getContext("2d"); // ✅ This line won't break if canvas is missing

    // Destroy existing chart if it exists (prevents duplication)
    if (window.strategyChartInstance) {
        window.strategyChartInstance.destroy();
    }

    window.strategyChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: summaryData.map(item => item.strategy),
            datasets: [{
                label: "Total Profit (After Brokerage)",
                data: summaryData.map(item => item.total_profit ?? 0),
                backgroundColor: summaryData.map(value => value.total_profit >= 0 ? "green" : "red"),
                borderColor: "black",
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true } }
        }
    });
}
function renderTable(data, tableId) {
    const tableBody = document.querySelector(`#${tableId} tbody`);
    tableBody.innerHTML = "";

    if (data.length === 0) {
        tableBody.innerHTML = "<tr><td colspan='4' style='text-align:center;'>No data available</td></tr>";
        return;
    }

    data.forEach(item => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${item.strategy}</td>
            <td>${item.index_name}</td>
            <td>${item.order_count}</td>
            <td style="color: ${item.total_profit >= 0 ? 'green' : 'red'};">
                ${item.total_profit !== null ? item.total_profit.toFixed(2) : "N/A"}
            </td>
        `;
        tableBody.appendChild(row);
    });
}