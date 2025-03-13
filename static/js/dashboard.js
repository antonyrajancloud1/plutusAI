document.addEventListener('DOMContentLoaded', () => {
  // Fetch and display data
  fetchData();

  function fetchData() {
    // Simulated JSON Fetch (Replace with your actual fetch)
//    const jsonData = {
//      "status": "success",
//      "summary": {
//        "status": "success",
//        "current_day_summary": [
//          {
//            "strategy": "c_3m_tripleEMA_ADX",
//            "index_name": "nifty",
//            "order_count": 6,
//            "total_profit": 3577.5000000000023
//          },
//          {
//            "strategy": "c_5m_supertrend",
//            "index_name": "nifty",
//            "order_count": 7,
//            "total_profit": 2746.249999999999
//          },
//          {
//            "strategy": "ha_1m_supertrend",
//            "index_name": "nifty",
//            "order_count": 28,
//            "total_profit": 2296.2500000000036
//          },
//          {
//            "strategy": "c_5m_tripleEMA_ADX",
//            "index_name": "nifty",
//            "order_count": 2,
//            "total_profit": 1862.499999999999
//          },
//          {
//            "strategy": "ha_5m_tripleEMA_ADX",
//            "index_name": "nifty",
//            "order_count": 2,
//            "total_profit": 1269.9999999999998
//          }
//        ],
//        "current_date": "2025-03-13",
//        "task_status": true
//      },
//      "task_status": true
//    };

     //Replace this with your actual fetch code:
     fetch('get_strategy_summary')
       .then(response => response.json())
       .then(data => {
         const positionsData = data.summary.current_day_summary;
         displayAllData(positionsData);
       })
       .catch(error => console.error('Error fetching data:', error));

    // Simulate asynchronous fetch with setTimeout
//    setTimeout(() => {
//      const positionsData = jsonData.summary.current_day_summary;
//      displayAllData(positionsData);
//    }, 500); // Simulate a 500ms delay
  }

  function displayAllData(positions) {
  console.log(positions);
    displayChart(positions);
    displayPositions(positions);
    displayOrders(positions);
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


  function displayChart(positions) {
    console.log("Raw Positions Data:", positions);
    console.log("Positions with total_profit:", positions.map(pos => pos.total_profit)); // Debugging


    const pnlChartContainer = document.querySelector('.pnl-chart');

    // **Filter out null total_profit values**
const validPositions = positions.filter(pos =>
    typeof pos.total_profit === "number" && !isNaN(pos.total_profit)
);


    // **Chart Data Extraction**
    const labels = validPositions.map(pos => pos.strategy);
    const data = validPositions.map(pos => pos.total_profit || 0);

    const canvas = document.getElementById('pnlChart');
    const ctx = canvas.getContext('2d');

    // **Destroy Previous Chart If Exists**
    if (canvas.chartInstance) {
        canvas.chartInstance.destroy();
    }

    // **Create New Chart**
    canvas.chartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
                hoverBackgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

    let totalPNL = calculateTotalPNL(positions);
    console.log("Overall PNL:", totalPNL);

    document.getElementById("pnlInfo").innerHTML =`<h3 style="text-align:center; margin-bottom:10px; font-size:18px;">
            Overall PNL: <span style="color: ${totalPNL >= 0 ? 'green' : 'red'};">
            ₹${totalPNL.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
            </span>
        </h3>
    `;;
}


  function displayPositions(positions) {
    const positionsContainer = document.querySelector('.positions');
    // positionsContainer.innerHTML = ''; // Keep the header

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
});