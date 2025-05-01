function generateTable(data, headers, displayHeaders, enableEdit = false) {
    const tableContainer = document.createElement('div');
    tableContainer.className = 'table-container';

    const table = document.createElement('table');
    table.style.width = '100%';

    // Create table headers
    const headerRow = table.insertRow();
    displayHeaders.forEach(headerText => { // Use displayHeaders here
        const header = document.createElement('th');
        header.textContent = headerText;
        header.className = 'order-book-header-cell';
        headerRow.appendChild(header);
    });

    // Add an extra header for the edit column if enableEdit is true
    if (enableEdit) {
        const editHeader = document.createElement('th');
        editHeader.textContent = 'Edit';
        editHeader.className = 'order-book-header-cell edit-header';
        headerRow.appendChild(editHeader);
    }

    // Create table rows from data
    data.forEach(item => {
        const row = table.insertRow();
        headers.forEach(header => { // Iterate through the actual data headers
            const cell = row.insertCell();
            let cellValue = item[header];

            // Format specific columns if needed
            if (header === 'entry_time' || header === 'exit_time') {
                cellValue = convertToIST(cellValue);
            } else if (header === 'status') {
                if (cellValue === 'NO') {
                    cell.className = 'status-no';
                } else if (cellValue === 'YES') {
                    cell.className = 'status-yes';
                }
            } else if (header === 'total') {
                cellValue = cellValue || 0;
            } else if (header === 'strategy') {
                cellValue = cellValue || 'N/A';
            }

            cell.textContent = cellValue || '';
            cell.className = 'order-book-cell';
        });

        // Add an edit icon cell if enableEdit is true
        if (enableEdit) {
            const editCell = row.insertCell();
            const editIcon = document.createElement('span');
            editIcon.textContent = '✏️'; // You can use an actual icon or image here
            editIcon.className = 'edit-icon';
            editCell.appendChild(editIcon);

            // You can add an event listener to the edit icon to handle edit functionality
            editIcon.addEventListener('click', () => {
                // Implement your edit logic here, e.g., open a modal, populate a form
                console.log('Edit clicked for:', item);
            });
             editCell.className = 'order-book-cell edit-cell';
        }
    });

    tableContainer.appendChild(table);
    return tableContainer;
}

function displayOrderBook(orderBookDetails) {

    const mainElement = document.querySelector('main');

    const tableHeaders = ['entry_time', 'script_name', 'qty', 'entry_price', 'status', 'exit_price', 'exit_time', 'total', 'strategy']; // Correct order of headers
    const displayHeaders = ['Entry Time', 'Script Name', 'Quantity', 'Entry Price', 'Status', 'Exit Price', 'Exit Time', 'Total', 'Strategy'];

    const orderBookTable = generateTable(orderBookDetails, tableHeaders, displayHeaders, true); // Pass displayHeaders
    mainElement.appendChild(orderBookTable);
}

// Example Usage for other data:
function displayOtherData(data, title, headers, displayHeaders) { // Added displayHeaders
    const mainElement = document.querySelector('main');
    const section = document.createElement('section');
    section.innerHTML = `<h2>${title}</h2>`;

    const otherTable = generateTable(data, headers, displayHeaders, true); // Pass displayHeaders
    section.appendChild(otherTable);
    mainElement.appendChild(section);
}

function fetchData() {

    const mainElement = document.querySelector('main');
    mainElement.innerHTML = `
      <section class="pnl">
        <h2>Today's PNL</h2>
        <div class="pnl-chart">
            <canvas id="pnlChart"></canvas>
        </div>
            <div id="pnlInfo"></div>
      </section>
      <section class="positions">
        <h2>Live Positions</h2>
        <div class="positions-header">
          <div class="position-name-header">Strategy (Index)</div>
          <div class="position-value-header">Total Profit</div>
        </div>
        </section>
      <section class="orders">
        <h2>Orders</h2>
        <div class="orders-header">
          <div class="order-name-header">Strategy (Index)</div>
          <div class="order-count-header">Order Count</div>
        </div>
        </section>
    `;
    fetch('get_strategy_summary')
        .then(response => response.json())
        .then(data => {
            const positionsData = data.summary.current_day_summary;
            let userName = data.summary.user_name;
            userName = userName.charAt(0).toUpperCase() + userName.slice(1);
            document.getElementById("userName").innerHTML = "Welcome,  " + userName;
            document.getElementById("today_orders").innerHTML = "Today's Orders: " + data.summary.total_orders_today;


            displayAllData(positionsData);
        })
        .catch(error => console.error('Error fetching data:', error));
}

function displayAllData(positions) {

    const mainElement = document.querySelector('main');
    mainElement.innerHTML = `
      <section class="pnl">
        <h2>Today's PNL</h2>
        <div class="pnl-chart">
            <canvas id="pnlChart"></canvas>
        </div>
            <div id="pnlInfo"></div>
      </section>
      <section class="positions">
        <h2>Live Positions</h2>
        <div class="positions-header">
          <div class="position-name-header">Strategy (Index)</div>
          <div class="position-value-header">Total Profit</div>
        </div>
        </section>
      <section class="orders">
        <h2>Orders</h2>
        <div class="orders-header">
          <div class="order-name-header">Strategy (Index)</div>
          <div class="order-count-header">Order Count</div>
        </div>
        </section>
    `;
    displayChart(positions);
    displayPositions(positions);
    displayOrders(positions);
}



function displayChart(positions) {
    const mainElement = document.querySelector('main');
    const pnlChartContainer = mainElement.querySelector('.pnl-chart');



    // Filter out invalid entries
    const validPositions = positions.filter(pos =>
        typeof pos.total_profit === "number" && !isNaN(pos.total_profit)
    );

    // Use Month labels or fallback to strategy names
    const labels = validPositions.map((pos, index) => pos.month || pos.strategy || `Item ${index + 1}`);
    const data = validPositions.map(pos => pos.total_profit || 0);
    const backgroundColors = data.map(value => value >= 0 ? 'green' : 'red');

    const canvas = document.getElementById('pnlChart');
    const ctx = canvas.getContext('2d');

    // Destroy previous chart
    if (canvas.chartInstance) {
        canvas.chartInstance.destroy();
    }

    // Create Bar Chart
    try {
        canvas.chartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Monthly PNL',
                    data: data,
                    backgroundColor: backgroundColors,
                    barPercentage: 0.3,
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        labels: {
                            generateLabels: () => [{
                                text: 'Negative Liquidity',
                                fillStyle: 'red',
                                fontColor: '#FFFFFF'
                            },
                            {
                                text: 'Positive Liquidity',
                                fillStyle: 'green',
                                fontColor: '#FFFFFF'
                            }
                            ],
                            fontColor: '#FFFFFF',
                            boxWidth: 15,
                            padding: 15
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: '#FFFFFF' // Y-axis labels
                        }
                    },
                    x: {
                        ticks: {
                            color: '#FFFFFF' // X-axis labels
                        }
                    }
                }
            }

        });
    } catch (e) {
        console.log(e)
    }

    // Display overall PNL
    const totalPNL = calculateTotalPNL(positions);
    document.getElementById("pnlInfo").innerHTML = `
      <h3 style="text-align:center; margin-bottom:10px; font-size:18px;">
          Overall PNL: <span style="color: ${totalPNL >= 0 ? 'green' : 'red'};">
          ₹${totalPNL.toLocaleString('en-IN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    })}
          </span>
      </h3>
  `;
}

const predefinedColors = [
    "#00bcd4",
    "#9c27b0",
    "#ffc107",
    "#2196f3",
    "#ff5722",
    "#4CAF50",
    "#e91e63",
    "#607d8b",
    "#ff9800",
    "#3f51b5"
];

const strategyColors = {};

function getColorForStrategy(strategy) {
    if (!strategyColors[strategy]) {
        const colorIndex = Object.keys(strategyColors).length % predefinedColors.length;
        strategyColors[strategy] = predefinedColors[colorIndex];
    }
    return strategyColors[strategy];
}

function calculateTotalPNL(positions) {
    let totalPNL = 0;

    for (let i = 0; i < positions.length; i++) {
        let profit = positions[i].total_profit;

        // Ensure total_profit is a valid number before adding
        if (typeof profit === "number" && !isNaN(profit)) {
            totalPNL += profit;
        }
    }

    return totalPNL;
}




function displayPositions(positions) {
    const positionsContainer = document.querySelector('.positions');
    // positionsContainer.innerHTML = ''; // Keep the header
    if (!positionsContainer) return;

    positions.forEach(position => {
        const positionItem = document.createElement('div');
        positionItem.classList.add('position-item');

        const positionName = document.createElement('div');
        positionName.classList.add('position-name');
        positionName.textContent = `${position.strategy} (${position.index_name.toUpperCase()})`;

        const positionValue = document.createElement('div');
        positionValue.classList.add('position-value');
        positionValue.textContent = position.total_profit.toLocaleString('en-IN', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });

        positionItem.appendChild(positionName);
        positionItem.appendChild(positionValue);
        positionsContainer.appendChild(positionItem);

        if (position.total_profit > 0) {
            positionValue.classList.add('positive');
        } else if (position.total_profit < 0) {
            positionValue.classList.add('negative');
        }
    });
}

function displayOrders(positions) {
    const ordersContainer = document.querySelector('.orders');
    // ordersContainer.innerHTML = ''; // Keep the header
    if (!ordersContainer) return;

    positions.forEach(position => {
        const orderItem = document.createElement('div');
        orderItem.classList.add('order-item');

        const orderName = document.createElement('div');
        orderName.classList.add('order-name');
        orderName.textContent = `${position.strategy} (${position.index_name.toUpperCase()})`;

        const orderCount = document.createElement('div');
        orderCount.classList.add('order-count');
        orderCount.textContent = position.order_count;

        orderItem.appendChild(orderName);
        orderItem.appendChild(orderCount);
        ordersContainer.appendChild(orderItem);

        if (position.order_count > 0) {
            orderCount.classList.add('positive');
        } else if (position.order_count < 0) {
            orderCount.classList.add('negative');
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    fetchData();

    // Add event listeners to nav items
    document.getElementById("dashboard").addEventListener("click", function () {
        setActive(this);
        fetchData();
    });
    document.getElementById("order").addEventListener("click", function () {
        setActive(this);
        fetch('get_order_book_details')
            .then(response => response.json())
            .then(data => {
                const orderBookData = data.order_book_details;
                displayOrderBook(orderBookData);
            })
            .catch(error => console.error('Error fetching order book details:', error));
    });

    // Function to set active class

});
function setActive(element) {

    const mainElements = document.querySelectorAll('main');  // Use querySelectorAll in case there are multiple main tags
    mainElements.forEach(mainElement => {
        mainElement.innerHTML = ''; // Remove all children of each main element.
    });

    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => item.classList.remove('active'));
    element.classList.add('active');
}
document.getElementById("webhook").addEventListener("click", function () {
    setActive(this);
    //fetchData();
    fetchWebhookData();
});


function convertToIST(timestamp) {
    if (!timestamp) return "N/A";

    const utcDate = new Date(timestamp * 1000);
    const istOffset = 5.5 * 60 * 60 * 1000;
    const istTime = new Date(utcDate.getTime() + istOffset);

    const day = istTime.getDate();
    const month = istTime.toLocaleString('default', {
        month: 'short'
    }).toUpperCase();
    const year = istTime.getFullYear();
    const hours = istTime.getHours();
    const minutes = istTime.getMinutes();
    const seconds = istTime.getSeconds();
    const ampm = hours >= 12 ? 'pm' : 'am';

    const formattedHours = hours % 12 || 12;

    return `${day} ${month} ${year}, ${formattedHours}:${minutes}:${seconds} ${ampm}`;
}

async function fetchWebhookData() {
    try {
        const response = await fetch('manual_details');
        const data = await response.json();

        if (data.status === 'success') {
             const mainElement = document.querySelector('main');

    const tableHeaders = ['index_name', 'lots', 'trigger', 'stop_loss', 'target', 'strike', 'current_premium']; // Correct order of headers
    const displayHeaders = ['Index' ,'Lots','Trigger',     'SL',  'Target' , 'Strike',  'CurrentOrder'];

    const orderBookTable = generateTable(data.message, tableHeaders, displayHeaders, true); // Pass displayHeaders
    mainElement.appendChild(orderBookTable);
//            $('#tkn_btn').addEventListener('click', reGenTokenData);
//            getTokenData();
//            fetchFlashData();
        }

    } catch (error) {
       // showResult(`Error fetching data: ${error.message}`, false);
       console.log("error")
       console.log(error)

    }
}
