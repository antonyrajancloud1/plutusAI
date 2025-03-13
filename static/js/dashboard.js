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
       console.log(data)
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

  function displayChart(positions) {
    const pnlChartContainer = document.querySelector('.pnl-chart');
    pnlChartContainer.innerHTML = ''; // Clear existing content

    // Calculate total profit for percentage calculation
    const totalProfit = positions.reduce((sum, pos) => sum + pos.total_profit, 0);
    let conicGradientValue = '';

    // Create chart elements
    const chartCircle = document.createElement('div');
    chartCircle.classList.add('chart-circle');

    const chartValue = document.createElement('div');
    chartValue.classList.add('chart-value');
    chartValue.textContent = totalProfit.toLocaleString('en-IN', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });

    const chartLegend = document.createElement('div');
    chartLegend.classList.add('chart-legend');

    let startAngle = 0;

    positions.forEach((position, index) => {
      const percentage = (position.total_profit / totalProfit) * 100;
      const angle = percentage * 3.6; // 360 degrees / 100%
      const color = getColorForStrategy(position.strategy);

      conicGradientValue += `${color} ${startAngle}deg ${startAngle + angle}deg, `;
      startAngle += angle;

      // Create legend item
      const legendItem = document.createElement('div');
      legendItem.classList.add('legend-item');
      legendItem.classList.add(position.strategy.replace(/_/g, '-'));

      const legendLabel = document.createElement('span');
      legendLabel.classList.add('legend-label');
      legendLabel.textContent = position.strategy;

      const legendPercentage = document.createElement('span');
      legendPercentage.classList.add('legend-percentage');
      legendPercentage.textContent = percentage.toFixed(2) + '%';

      legendItem.appendChild(legendLabel);
      legendItem.appendChild(legendPercentage);
      chartLegend.appendChild(legendItem);
    });

    // Remove trailing comma and space from conicGradientValue
    conicGradientValue = conicGradientValue.slice(0, -2);

    // Create the ::before pseudo-element using JavaScript
    const chartCircleBefore = document.createElement('div');
    chartCircleBefore.style.position = 'absolute';
    chartCircleBefore.style.top = '0';
    chartCircleBefore.style.left = '0';
    chartCircleBefore.style.width = '100%';
    chartCircleBefore.style.height = '100%';
    chartCircleBefore.style.borderRadius = '50%';
    chartCircleBefore.style.background = `conic-gradient(${conicGradientValue})`;
    chartCircleBefore.style.opacity = '0.8';

    chartCircle.appendChild(chartValue);
    chartCircle.appendChild(chartCircleBefore); // Append the pseudo-element
    pnlChartContainer.appendChild(chartCircle);
    pnlChartContainer.appendChild(chartLegend);
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