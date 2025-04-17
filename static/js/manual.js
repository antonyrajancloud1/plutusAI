// ====== Utility DOM Selectors ======
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);

// ====== Dynamic Table Rendering ======
function populateTable(data) {
    const tableBody = $('#tradeTableBody');
    tableBody.innerHTML = '';

    data.message.forEach((item, index) => {
        tableBody.innerHTML += `
            <tr>
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
            </tr>
        `;
    });
}

function populateFlashTable(data) {
    const tableBody = $('#flashTableBody');
    tableBody.innerHTML = '';

    data.message.forEach((item, index) => {
        tableBody.innerHTML += `
            <tr>
                <td>
                    <button class="start-button" data-index="${index}">Start</button>
                    <button class="stop-button" data-index="${index}">Stop</button>
                    <button class="edit-button" data-index="${index}">Edit</button>
                </td>
                <td>${item.index_name}</td>
                <td><input type="text" value="${item.lots}" id="lots-${index}"></td>
                <td><input type="text" value="${item.strike}" id="strike-${index}"></td>
                <td><input type="text" value="${item.max_profit}" id="max_profit-${index}"></td>
                <td><input type="text" value="${item.max_loss}" id="max_loss-${index}"></td>
                <td><input type="text" value="${item.trend_check_points}" id="trend_check_points-${index}"></td>
                <td>${item.status}</td>
            </tr>
        `;
    });
}

// ====== Event Delegation for Buttons ======
$('#tradeTableBody').addEventListener('click', (event) => {
    const target = event.target;
    const index = target.dataset.index;

    if (target.classList.contains('buy-button')) handleOrder('place_order_buy', index);
    else if (target.classList.contains('sell-button')) handleOrder('place_order_sell', index);
    else if (target.classList.contains('edit-button')) editOrder(index);
});

$('#flashTableBody').addEventListener('click', (event) => {
    const target = event.target;
    const index = target.dataset.index;
    const flash_data = { index_name: 'nifty', strategy: 'flash' };

    if (target.classList.contains('start-button')) stopFlash('start_flash', flash_data);
    else if (target.classList.contains('stop-button')) stopFlash('stop_index', flash_data);
    else if (target.classList.contains('edit-button')) editFlash(index);
});

// ====== Order Management ======
async function handleOrder(url, index) {
    const orderDetails = getOrderDetails(index);
    await placeOrder(url, orderDetails);
}

async function placeOrder(url, orderDetails) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(orderDetails)
        });

        const result = await response.json();
        showResult(result.message, result.status === 'success');
    } catch (error) {
        showResult(`Error placing order: ${error.message}`, false);
    }
}

function getOrderDetails(index) {
    return {
        index_name: $(`#tradeTableBody tr:nth-child(${+index + 1}) td:nth-child(2)`).textContent.trim(),
        lots: $(`#lots-${index}`).value,
        trigger: $(`#trigger-${index}`).value,
        stop_loss: $(`#sl-${index}`).value,
        target: $(`#target-${index}`).value,
        strike: $(`#strike-${index}`).value
    };
}

// ====== Edit Functionality ======
function editOrder(index) {
    const index_name = $(`#tradeTableBody tr:nth-child(${+index + 1}) td:nth-child(2)`).textContent.trim();
    fetchEditOrderDetails(index_name);
}

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

function createEditForm(order) {
    const modal = $('#editModal');
    const form = $('#editOrderForm');

    form.innerHTML = `
        <h3>Edit Order for ${order.index_name}</h3>
        ${['lots', 'trigger', 'stop_loss', 'target', 'strike'].map(field => `
            <label for="edit-${field}">${field.replace('_', ' ')}:</label>
            <input type="text" id="edit-${field}" value="${order[field]}" name="${field}"><br><br>
        `).join('')}
        <button type="button" id="saveChanges">Save Changes</button>
        <button type="button" id="cancelEdit">Cancel</button>
    `;

    modal.style.display = 'block';

    $('#saveChanges').onclick = () => saveOrderChanges(order.index_name);
    $('#cancelEdit').onclick = () => modal.style.display = 'none';
}

async function saveOrderChanges(index_name) {
    const fields = ['lots', 'trigger', 'stop_loss', 'target', 'strike'];
    const orderDetails = { index_name };

    fields.forEach(field => {
        orderDetails[field] = $(`#edit-${field}`).value;
    });

    if (!validateForm(orderDetails)) {
        showResult('Please fill in all fields correctly.', false);
        return;
    }

    try {
        const response = await fetch('update_manual_details', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(orderDetails)
        });

        const result = await response.json();
        showResult(result.status === 'success' ? 'Index updated successfully.' : `Failed to update: ${result.message}`, result.status === 'success');

        if (result.status === 'success') {
            $('#editModal').style.display = 'none';
            fetchData();
        }
    } catch (error) {
        showResult(`Error updating order: ${error.message}`, false);
    }
}

function validateForm(orderDetails) {
    return Object.values(orderDetails).every(val => val.toString().trim() !== '');
}

// ====== Flash Order Handling ======
async function stopFlash(url, orderDetails) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(orderDetails)
        });

        const result = await response.json();
        showResult(result.status === 'success' ? result.message : `Failed: ${result.message}`, result.status === 'success');
    } catch (error) {
        showResult(`Error: ${error.message}`, false);
    }
}

// ====== Strategy Summary ======
async function fetchStrategySummary() {
    try {
        const response = await fetch("get_strategy_summary", {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        const data = await response.json();
        if (data.status === "success" && data.summary) {
            renderTable(data.summary.full_summary, "fullSummaryTable");
            renderTable(data.summary.current_day_summary, "currentDaySummaryTable");
        }
    } catch (error) {
        console.error("Error fetching strategy summary:", error);
    }
}

function renderTable(data, tableId) {
    const tableBody = $(`#${tableId} tbody`);
    tableBody.innerHTML = data.length
        ? data.map(item => `
            <tr>
                <td>${item.strategy}</td>
                <td>${item.index_name}</td>
                <td>${item.order_count}</td>
                <td style="color: ${item.total_profit >= 0 ? 'green' : 'red'};">
                    ${item.total_profit != null ? item.total_profit.toFixed(2) : "N/A"}
                </td>
            </tr>`).join('')
        : "<tr><td colspan='4' style='text-align:center;'>No data available</td></tr>";
}

// ====== Token Management ======
async function getTokenData() {
    try {
        const response = await fetch("get_auth_token", {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        const data = await response.json();
        $('#token_details').innerHTML = data.status === 'success' ? data.message : "No Token Present";
    } catch (error) {
        $('#token_details').innerHTML = error;
    }
}

async function reGenTokenData() {
    try {
        const response = await fetch("generate_auth_token", {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        const data = await response.json();
        $('#token_details').innerHTML = data.status === 'success' ? data.message : "No Token Present";
    } catch (error) {
        $('#token_details').innerHTML = error;
    }
}

// ====== UI Feedback ======
function showResult(message, isSuccess = true) {
    const resultDiv = $('#result');
    resultDiv.textContent = message;
    resultDiv.className = isSuccess ? 'success' : 'error';
    resultDiv.style.display = 'block';
}

// ====== Fetch All Data ======
async function fetchData() {
    try {
        const response = await fetch('manual_details');
        const data = await response.json();

        if (data.status === 'success') {
            populateTable(data);
            $('#tkn_btn').addEventListener('click', reGenTokenData);
            getTokenData();
            fetchFlashData();
        } else {
            showResult('Failed to fetch data', false);
        }
    } catch (error) {
        showResult(`Error fetching data: ${error.message}`, false);
    }
}

async function fetchFlashData() {
    try {
        const response = await fetch('get_flash_details');
        const data = await response.json();

        if (data.status === 'success') {
            populateFlashTable(data);
        } else {
            showResult('Failed to fetch flash data', false);
        }
    } catch (error) {
        showResult(`Error fetching flash data: ${error.message}`, false);
    }
}

// ====== On Load Initialization ======
window.onload = () => {
    fetchData();
    fetchStrategySummary();
};
