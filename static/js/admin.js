 const startWSButton = document.getElementById("startWS");
        const stopWSButton = document.getElementById("stopWS");
        const reGenerateTokenButton = document.getElementById("regenerateToken");
        const updateExpiryButton = document.getElementById("updateExpiry");
        const wsTypeInput = document.getElementById("ws-input");
        const statusDiv = document.getElementById('ws-status');

        // Function to make an API call and update the status message
        function makeAPICall(method, api_url, payload_data) {
            const options = {
                method: method,
                headers: {'Content-Type': 'application/json'},
                body: payload_data ? JSON.stringify(payload_data) : null
            };
            fetch(api_url, options)
                .then(response => response.json())
                .then(data => {
                    statusDiv.textContent = data.message || 'Action completed successfully!';
                    statusDiv.className = data.task_status ? 'status true' : 'status false';
                })
                .catch(error => {
                    console.error('Error making API call:', error);
                    statusDiv.textContent = 'Error: ' + error.message;
                    statusDiv.className = 'status false';
                });
        }

        // WebSocket Button Actions
        startWSButton.addEventListener("click", function() {
            makeAPICall('POST', 'start_ws', { ws_type: wsTypeInput.value });
        });

        stopWSButton.addEventListener("click", function() {
            makeAPICall('POST', 'stop_ws', { ws_type: wsTypeInput.value });
        });

        reGenerateTokenButton.addEventListener("click", function() {
            makeAPICall('POST', 'regenrate_token', null);
        });

        // Update Expiry Button Action
        updateExpiryButton.addEventListener("click", function() {
            const expiryDetails = {
                expiry_date: "2025-12-31",
                next_expiry_date: "2026-12-31"
            };
            makeAPICall('POST', 'update_expiry_details', expiryDetails);
        });

        // Add User Button Action
        document.querySelector(".add-btn").addEventListener("click", function() {
            const email = document.getElementById("email").value;
            const name = document.getElementById("name").value;
            const password = document.getElementById("password").value;
            const userData = { email, name, password };
            makeAPICall('POST', 'add_user', userData); // API endpoint to add user
        });

        // Fetch Index Data Functionality
        async function fetchIndexData() {
            try {
                const response = await fetch('get_index_data');
                const data = await response.json();
                if (data.status === "success") {
                    populateTable(data.message.index_data);
                }
            } catch (error) {
                console.error("Error fetching index data:", error);
            }
        }

        // Populate Index Data Table
        function populateTable(indexData) {
            const tableBody = document.getElementById("indexTable").querySelector("tbody");
            tableBody.innerHTML = ""; // Clear existing table content
            indexData.forEach(item => {
                const row = `<tr>
                    <td>${item.id}</td>
                    <td>${item.index_name}</td>
                    <td>${item.index_group}</td>
                    <td>${item.index_token}</td>
                    <td>${item.ltp}</td>
                    <td>${item.last_updated_time}</td>
                    <td>${item.qty}</td>
                    <td>${item.current_expiry}</td>
                    <td>${item.next_expiry}</td>
                </tr>`;
                tableBody.innerHTML += row;
            });
        }

        // Initial index data fetch
        fetchIndexData();