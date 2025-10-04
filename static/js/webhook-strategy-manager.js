// Fix: Declare jQuery's global `$` to resolve TypeScript errors.
const StrategyType = {
  DEFAULT: 'default',
  CUSTOM: 'custom',
};

const TOKEN = 'dc43c8dd7ac43be69c19139a8b0ff1530f85c9ef';
const indices = [
    { key: 'nifty', name: 'Nifty' },
    { key: 'bank_nifty', name: 'BankNifty' },
    { key: 'fin_nifty', name: 'FinNifty' },
    { key: 'sensex', name: 'Sensex' }
];
const productTypes = [
    { key: 'MIS', name: 'MIS (Intraday)' },
    { key: 'NRML', name: 'NRML (Overnight)' },
];
const timeframes = [
    { key: 'ONE_MINUTE', name: '1 Minute' },
    { key: 'THREE_MINUTE', name: '3 Minutes' },
    { key: 'FIVE_MINUTE', name: '5 Minutes' },
    { key: 'FIFTEEN_MINUTE', name: '15 Minutes' },
    { key: 'ONE_HOUR', name: '1 Hour' },
    { key: 'ONE_DAY', name: '1 Day' },
];

// App State
let strategies = [];
let expandedStrategyId = null;

// Helper functions to generate HTML components

function showNotification(message, type = 'success', duration = 3000) {
    const container = $('#notification-container');
    const bannerId = `notification-${Date.now()}`;
    const bgColor = type === 'success' ? 'bg-green-600' : 'bg-red-600';
    
    const bannerHTML = `
        <div id="${bannerId}" class="${bgColor} text-white py-2 px-5 rounded-lg shadow-lg text-sm font-semibold animate-fade-in-down" style="display: none;">
            ${message}
        </div>
    `;

    const banner = $(bannerHTML).appendTo(container);
    banner.fadeIn(200);

    setTimeout(() => {
        banner.fadeOut(500, function() {
            $(this).remove();
        });
    }, duration);
};

function createToggleSwitchHTML(id, enabled) {
  const bgColor = enabled ? 'toggle-bg-enabled' : 'toggle-bg-disabled';
  const translation = enabled ? 'translate-x-6' : 'translate-x-1';
  return `
    <button
      type="button"
      data-id="${id}"
      class="toggle-switch relative inline-flex items-center h-6 rounded-full w-11 transition-colors duration-300 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-indigo-500 focus-visible:ring-offset-gray-900 ${bgColor}"
      aria-pressed="${enabled}"
    >
      <span class="sr-only">Toggle</span>
      <span
        class="inline-block w-4 h-4 transform bg-white rounded-full transition-transform duration-300 ${translation}"
      />
    </button>
  `;
};

function createStrategyDetailsHTML(strategy) {
    const rows = indices.map(index => {
        let inputDataObject;

        if (strategy.type === StrategyType.CUSTOM) {
            inputDataObject = {
                strategy_name: strategy.name,
                index_name: index.name.toUpperCase(),
                strike: strategy.strike,
                lots: strategy.lots,
                on_candle_close: strategy.on_candle_close,
                producttype: strategy.producttype,
                timeframe: strategy.timeframe,
                index_group: strategy.index_group,
            };
        } else { // StrategyType.DEFAULT from API
            inputDataObject = {
                strategy_name: strategy.name,
                index_name: index.name.toUpperCase(),
                target: strategy.target,
                stop_loss: strategy.stop_loss,
                strike: strategy.strike,
                lots: strategy.lots,
                on_candle_close: strategy.on_candle_close,
                producttype: strategy.producttype,
                timeframe: strategy.timeframe,
                index_group: strategy.index_group,
            };
        }
        const inputData = JSON.stringify(inputDataObject, null, 2);

        return `
            <tr class="border-b border-theme last:border-b-0">
                <td class="p-2 align-top font-medium">${index.name}</td>
                <td class="p-2 align-top font-mono text-xs break-all text-theme-secondary webhook-url cursor-pointer" title="Copy URL">
                    http://plutuz.in/trigger_buy?token=${TOKEN}
                </td>
                <td class="p-2 align-top font-mono text-xs break-all text-theme-secondary webhook-url cursor-pointer" title="Copy URL">
                    http://plutuz.in/trigger_sell?token=${TOKEN}
                </td>
                <td class="p-2 align-top font-mono text-xs break-all text-theme-secondary webhook-url cursor-pointer" title="Copy URL">
                    http://plutuz.in/trigger_exit?token=${TOKEN}
                </td>
                <td class="p-2 align-top">
                    <pre class="details-code-bg p-2 rounded whitespace-pre-wrap break-all text-theme-secondary font-mono text-xs"><code>${inputData}</code></pre>
                </td>
            </tr>
        `;
    }).join('');

    return `
        <div class="details-bg p-4 animate-fade-in-down">
            <table class="w-full text-sm">
                <thead>
                    <tr class="border-b border-theme">
                        <th class="p-2 w-[10%] text-left font-semibold table-header-text text-xs">Index Name</th>
                        <th class="p-2 w-[25%] text-left font-semibold table-header-text text-xs">Buy URL</th>
                        <th class="p-2 w-[25%] text-left font-semibold table-header-text text-xs">Sell URL</th>
                        <th class="p-2 w-[25%] text-left font-semibold table-header-text text-xs">Exit URL</th>
                        <th class="p-2 w-[15%] text-left font-semibold table-header-text text-xs">Input Data</th>
                    </tr>
                </thead>
                <tbody>${rows}</tbody>
            </table>
        </div>
    `;
}

function createWebhookTableHTML(strategies) {
  if (strategies.length === 0) {
    return `
      <div class="text-center py-10 px-6 modal-bg rounded-lg border border-theme">
        <h3 class="text-lg font-medium">No Strategies Found</h3>
        <p class="mt-1 text-sm text-theme-secondary">Create a custom strategy to get started.</p>
      </div>
    `;
  }
  
  const tableRows = strategies.map(strategy => {
    const typeClass = strategy.strategy_type === StrategyType.DEFAULT ? 'badge badge-default' : 'badge badge-custom';
    
    const statusHTML = strategy.enabled 
        ? `<span class="flex items-center status-positive"><div class="status-dot status-dot-positive"></div>Enabled</span>`
        : `<span class="flex items-center status-negative"><div class="status-dot status-dot-negative"></div>Disabled</span>`;

    const toggleHTML = createToggleSwitchHTML(strategy.id, strategy.enabled);
    let actionHTML;

    if (strategy.strategy_type === StrategyType.DEFAULT) {
        actionHTML = toggleHTML;
    } else { // CUSTOM
        actionHTML = `
            <div class="flex items-center justify-center gap-4">
                ${toggleHTML}
                <div class="flex items-center gap-2">
                    <button class="btn-icon btn-edit" data-id="${strategy.id}" aria-label="Edit Strategy">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"><path d="M13.586 3.586a2 2 0 1 1 2.828 2.828l-.793.793-2.828-2.828.793-.793ZM11.379 5.793l2.828 2.828L5.657 17.172a1 1 0 0 1-.707.293H3.75a1 1 0 0 1-1-1v-1.207a1 1 0 0 1 .293-.707l8.485-8.485Z" /></svg>
                    </button>
                    <button class="btn-icon btn-delete" data-id="${strategy.id}" aria-label="Delete Strategy">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M8.75 1A2.75 2.75 0 0 0 6 3.75v.443c-.795.077-1.58.22-2.365.468a.75.75 0 1 0 .23 1.482l.149-.022.841 10.518A2.75 2.75 0 0 0 7.596 19h4.807a2.75 2.75 0 0 0 2.742-2.53l.841-10.52.149.023a.75.75 0 0 0 .23-1.482A41.03 41.03 0 0 0 14 4.193V3.75A2.75 2.75 0 0 0 11.25 1h-2.5ZM10 4c.84 0 1.673.025 2.5.075V3.75c0-.69-.56-1.25-1.25-1.25h-2.5c-.69 0-1.25.56-1.25 1.25v.325C8.327 4.025 9.16 4 10 4ZM8.58 7.72a.75.75 0 0 0-1.5.06l.3 7.5a.75.75 0 1 0 1.5-.06l-.3-7.5Zm4.34.06a.75.75 0 1 0-1.5-.06l-.3 7.5a.75.75 0 1 0 1.5.06l.3-7.5Z" clip-rule="evenodd"></path></svg>
                    </button>
                </div>
            </div>
        `;
    }

    const rowClass = 'cursor-pointer';
    
    let expandedRowHTML = '';
    if (expandedStrategyId === strategy.id) {
        const detailsContent = createStrategyDetailsHTML(strategy);
        expandedRowHTML = `
            <tr class="details-bg">
                <td colSpan="4" class="p-0">${detailsContent}</td>
            </tr>
        `;
    }
    
    return `
      <tr data-id="${strategy.id}" class="strategy-row table-row-hover transition-colors duration-150 ${rowClass}">
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">${strategy.strategy_name ? strategy.strategy_name : strategy.name}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm">
          <span class="${typeClass}">
            ${strategy.strategy_type ? strategy.strategy_type : StrategyType.CUSTOM}
          </span>
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm">${statusHTML}</td>
        <td class="px-6 py-4 whitespace-nowrap text-center text-sm font-medium">${actionHTML}</td>
      </tr>
      ${expandedRowHTML}
    `;
  }).join('');
  
  return `
    <div class="table-container">
      <table class="min-w-full divide-y border-theme">
        <thead class="table-header">
          <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium table-header-text">Strategy Name</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium table-header-text">Type</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium table-header-text">Status</th>
            <th scope="col" class="px-6 py-3 text-center text-xs font-medium table-header-text">Action</th>
          </tr>
        </thead>
        <tbody class="divide-y border-theme">${tableRows}</tbody>
      </table>
    </div>
  `;
}

function createAddStrategyModalHTML(strategyToEdit = null) {
    const isEditing = strategyToEdit !== null;
    const title = isEditing ? 'Edit Custom Strategy' : 'Create Custom Strategy';
    const submitButtonText = isEditing ? 'Save Changes' : 'Add Strategy';
    const strategyId = isEditing ? strategyToEdit.id : '';

    const name = isEditing ? strategyToEdit.strategy_name : '';
    const lots = isEditing ? strategyToEdit.lots : '1';
    const strike = isEditing ? strategyToEdit.strike : '100';
    const index_name = isEditing ? strategyToEdit.index_name : 'nifty';
    const producttype = isEditing ? strategyToEdit.producttype : 'MIS';
    const timeframe = isEditing ? strategyToEdit.timeframe : 'FIVE_MINUTE';
    const index_group = isEditing ? strategyToEdit.index_group : 'indian_index';
    const on_candle_close = isEditing ? strategyToEdit.on_candle_close : true;

    const indexOptions = indices.map(i => `<option value="${i.key}" ${i.key === index_name ? 'selected' : ''}>${i.name}</option>`).join('');
    const productOptions = productTypes.map(p => `<option value="${p.key}" ${p.key === producttype ? 'selected' : ''}>${p.name}</option>`).join('');
    const timeframeOptions = timeframes.map(t => `<option value="${t.key}" ${t.key === timeframe ? 'selected' : ''}>${t.name}</option>`).join('');

    const disabledAttr = isEditing ? 'disabled' : '';
    const disabledClass = isEditing ? 'opacity-70 cursor-not-allowed' : '';
    
    return `
        <div id="strategy-modal-overlay" class="fixed inset-0 modal-overlay-bg flex items-center justify-center p-4 animate-fade-in z-50">
            <div class="modal-bg rounded-lg border border-theme shadow-xl w-full max-w-lg animate-fade-in-down">
                <div class="flex justify-between items-center p-5 border-b border-theme">
                    <h3 class="text-lg font-semibold">${title}</h3>
                    <button type="button" id="close-modal-btn" class="text-theme-secondary hover:text-theme-default transition-colors duration-200 focus:outline-none">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                    </button>
                </div>
                <form id="add-strategy-form" autocomplete="off" data-editing-id="${strategyId}">
                    <div class="p-6">
                        <div class="space-y-4">
                            <div>
                                <label for="strategy-name" class="form-label">Strategy Name</label>
                                <input id="strategy-name" type="text" placeholder="e.g. 'My Custom MACD'" class="form-input ${disabledClass}" required autofocus autocomplete="off" value="${name}" ${disabledAttr} />
                            </div>
                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                <div>
                                    <label for="lots" class="form-label">Lots</label>
                                    <input id="lots" type="number" placeholder="1" value="${lots}" class="form-input" required autocomplete="off" />
                                </div>
                                <div>
                                    <label for="strike" class="form-label">Strike</label>
                                    <input id="strike" type="text" placeholder="e.g. '100'" value="${strike}" class="form-input" required autocomplete="off" />
                                </div>
                            </div>
                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                <div>
                                    <label for="index_name" class="form-label">Index Name</label>
                                   <select id="index_name" class="form-select ${disabledClass}" ${disabledAttr}>${indexOptions}</select>
                                </div>
                                <div>
                                    <label for="producttype" class="form-label">Product Type</label>
                                    <select id="producttype" class="form-select">${productOptions}</select>
                                </div>
                            </div>
                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                <div>
                                    <label for="timeframe" class="form-label">Timeframe</label>
                                    <select id="timeframe" class="form-select">${timeframeOptions}</select>
                                </div>
                                <div>
                                    <label for="index_group" class="form-label">Index Group</label>
                                    <input id="index_group" type="text" placeholder="e.g. 'indian_index'" value="${index_group}" class="form-input" required autocomplete="off" />
                                </div>
                            </div>
                            <div class="pt-2">
                                <label for="on_candle_close" class="flex items-center cursor-pointer">
                                    <input id="on_candle_close" type="checkbox" class="form-checkbox" ${on_candle_close ? 'checked' : ''} />
                                    <span class="ml-3 text-sm font-medium text-theme-secondary">On Candle Close</span>
                                </label>
                            </div>
                        </div>
                    </div>
                    <div class="px-6 py-4 flex justify-end gap-3 rounded-b-lg">
                        <button type="button" id="cancel-add-strategy" class="btn btn-secondary">
                            Cancel
                        </button>
                        <button type="submit" class="btn btn-positive flex items-center justify-center min-w-[140px]">
                            <span class="button-text">${submitButtonText}</span>
                            <svg class="animate-spin h-5 w-5 text-white hidden loader" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                        </button>
                    </div>
                </form>
            </div>
        </div>
    `;
}


// Main render function
function render() {
  const tableHTML = createWebhookTableHTML(strategies);
  $('#webhook-table-container').html(tableHTML);
}

function closeModal() {
    $('#modal-container').empty();
}

function fetchAjax(url, data, additionalAjaxOptions) {
    data = data || {};
    if( additionalAjaxOptions.type === "GET") {
        if( typeof data === "object" && Object.keys(data).length !== 0) {
            url += this.serialize(data);
        }
    } else {
        data = JSON.stringify(data);
    }
	let options = {
		url 		: url,
        contentType : 'application/json',
		headers		: { 
            Accept          :   "*/*"
        }
	};
    if(additionalAjaxOptions.type !== "GET") {
        options.data = data;
    }
	options = $.extend( {}, (additionalAjaxOptions || {}), options );
	return $.ajax(options);
};

function fallbackCopyTextToClipboard(text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.top = "0";
    textArea.style.left = "0";
    textArea.style.position = "fixed";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    try {
        if (document.execCommand('copy')) {
            showNotification('Webhook URL Copied!', 'success');
        }
    } catch (err) {
        console.error('Fallback: Unable to copy', err);
        showNotification('Failed to copy URL', 'error');
    }
    document.body.removeChild(textArea);
}

// Event Handlers
function bindEventsForStrategyManager() {
    async function loadStrategies() {
        try {
            $('#webhook-table-container').html('<p class="text-center p-8 text-theme-secondary">Loading strategies...</p>');
            const responseFromApi = await fetchAjax("/get_strategy_details", {}, { type: "GET" });

            if (responseFromApi.status === 'success' && Array.isArray(responseFromApi.data)) {
                const defaultStrategiesFromAPI = responseFromApi.data.filter(s => s.strategy_type === 'default');

                const transformedDefaults = defaultStrategiesFromAPI.map(apiStrategy => {
                    const name = `${(indices.find(i => i.key === apiStrategy.index_name)?.name || (apiStrategy.index_name.charAt(0).toUpperCase() + apiStrategy.index_name.slice(1)))}`;
                    return {
                        ...apiStrategy,
                        id: String(apiStrategy.id),
                        name: name,
                        type: StrategyType.DEFAULT,
                        enabled: apiStrategy.order_status === 'order_placed',
                    };
                });
                
                const customStrategies = strategies.filter(s => s.type === StrategyType.CUSTOM);
                strategies = [...transformedDefaults, ...customStrategies];
            } else {
                throw new Error('Invalid API response structure');
            }
        } catch (error) {
            console.error("Failed to load strategies : ", error);
            $('#webhook-table-container').html(`
                <div class="text-center py-10 px-6 error-box rounded-lg">
                    <h3 class="text-lg font-medium">Failed to Load Strategies</h3>
                    <p class="mt-1 text-sm">There was an error fetching the strategy data. Please try again later.</p>
                </div>
            `);
            strategies = strategies.filter(s => s.type === StrategyType.CUSTOM);
        } finally {
            render();
        }
    }

    loadStrategies();

    // Show add form modal
    $('#create-strategy-btn').on('click', function() {
        $('#modal-container').html(createAddStrategyModalHTML());
        $('#strategy-name').focus();
    });

    // Close/Cancel add form modal
    $('#modal-container').on('click', '#cancel-add-strategy, #strategy-modal-overlay, #close-modal-btn', function(e) {
        if (e.target.id === 'strategy-modal-overlay' || $(e.target).closest('#cancel-add-strategy').length || $(e.target).closest('#close-modal-btn').length) {
             closeModal();
        }
    });

    // Submit add/edit form
    $('#modal-container').on('submit', '#add-strategy-form', async function(e) {
        e.preventDefault();
        const form = $(this);
        const submitButton = form.find('button[type="submit"]');
        const cancelButton = form.find('#cancel-add-strategy');
        const editingId = form.attr('data-editing-id');

        submitButton.prop('disabled', true);
        cancelButton.prop('disabled', true);
        submitButton.find('.button-text').addClass('hidden');
        submitButton.find('.loader').removeClass('hidden');

       const strategyDataFromForm = {
            strategy_name: $('#strategy-name').val().trim(),
            lots: $('#lots').val(),
            strike: $('#strike').val(),
            index_name: $('#index_name').val(),
            producttype: $('#producttype').val(),
            timeframe: $('#timeframe').val(),
            index_group: $('#index_group').val(),
            on_candle_close: $('#on_candle_close').is(':checked'),
        };

        if (!strategyDataFromForm.strategy_name) {
            // Re-enable form
            submitButton.prop('disabled', false);
            cancelButton.prop('disabled', false);
            submitButton.find('.button-text').removeClass('hidden');
            submitButton.find('.loader').addClass('hidden');
            return;
        }

        const isEditing = !!editingId;
        let url;
        let body;
        const method = isEditing ? 'PUT' : 'POST';

        if( isEditing ) {
            const strategyToEdit = strategies.find(s => s.id === editingId);
            if (!strategyToEdit) {
                showNotification('Error: Strategy to edit not found.', 'error');
                submitButton.prop('disabled', false);
                cancelButton.prop('disabled', false);
                submitButton.find('.button-text').removeClass('hidden');
                submitButton.find('.loader').addClass('hidden');
                return;
            }

            url = '/update_strategy_details';
            const { strategy_name, index_name, ...fields } = strategyDataFromForm;
            const editPayload = {
                strategy_name: strategyToEdit.strategy_name, // Original name as identifier
                fields: {
                   strike: fields.strike,
                   lots: fields.lots,
                   on_candle_close: fields.on_candle_close,
                   producttype: fields.producttype,
                   timeframe: fields.timeframe,
                   index_group: fields.index_group
                }
            };
            body = editPayload;
        } else {
            url = '/add_strategy_details';
            const { name, ...rest } = strategyDataFromForm;
            const addPayload = {
                strategy_name: name,
                ...rest
            };
            body = addPayload;
        }

        try {
            const response = await fetchAjax(url, body, { type : method });
            if (isEditing) {
                const strategyIndex = strategies.findIndex(s => s.id === editingId);
                if (strategyIndex > -1) {
                    strategies[strategyIndex] = { ...strategies[strategyIndex], ...strategyDataFromForm };
                }
                 showNotification('Strategy updated successfully!', 'success');
            } else {
                const newStrategy = {
                    id: String(Date.now()),                             // Use backend ID, fallback to timestamp
                    type: StrategyType.CUSTOM,
                    strategy_type : StrategyType.CUSTOM,
                    ...strategyDataFromForm,
                    enabled: true,
                };
                strategies.push(newStrategy);
                expandedStrategyId = newStrategy.id;
                showNotification('Strategy created successfully!', 'success');
            }
            closeModal();
            render();
        } catch (error) {
            console.error(`Failed to ${isEditing ? 'update' : 'create'} strategy : `, error);
            showNotification(error.message, 'error');
            
            // Re-enable form on error
            submitButton.prop('disabled', false);
            cancelButton.prop('disabled', false);
            submitButton.find('.button-text').removeClass('hidden');
            submitButton.find('.loader').addClass('hidden');
        }
    });

    // Toggle default strategy
    $('#webhook-table-container').on('click', '.toggle-switch', async function(e) {
        e.stopPropagation();
        const id = $(this).attr('data-id');
        const strategy = strategies.find(s => s.id === id);
        if (strategy) {
            const originalEnabledState = strategy.enabled;
            // Optimistic UI update
            strategy.enabled = !strategy.enabled;

            try {
                const response = await fetchAjax("/toggle_strategy_details", { strategy_name : strategy.strategy_name }, { type : "POST" });
                render();
            } catch (error) {
                 console.error("Failed to toggle strategy:", error);
                 showNotification(error.message, 'error');
                 // Revert on error
                 strategy.enabled = originalEnabledState;
                 render();
            }
        }
    });
    
    // Edit custom strategy
    $('#webhook-table-container').on('click', '.btn-edit', function(e) {
        e.stopPropagation();
        const id = $(this).attr('data-id');
        const strategyToEdit = strategies.find(s => s.id === id);
        if (strategyToEdit) {
            $('#modal-container').html(createAddStrategyModalHTML(strategyToEdit));
            $('#strategy-name').focus();
        }
    });

    // Delete custom strategy
    $('#webhook-table-container').on('click', '.btn-delete', async function(e) {
        e.stopPropagation();
        const id = $(this).attr('data-id');
        const strategyToDelete = strategies.find(s => s.id === id);

        if (strategyToDelete && window.confirm(`Are you sure you want to delete the "${strategyToDelete.strategy_name}" strategy?`)) {
            const rowActions = $(this).closest('td');
            rowActions.find('button').prop('disabled', true);

            try {
                const response = await fetchAjax("/delete_strategy_details", { strategy_name : strategyToDelete.strategy_name }, { type : "POST" });

                strategies = strategies.filter(s => s.id !== id);
                if (expandedStrategyId === id) {
                    expandedStrategyId = null;
                }
                render();
                showNotification('Strategy deleted successfully!', 'success');

            } catch (error) {
                console.error("Failed to delete strategy : ", error);
                showNotification(error.message, 'error');
                rowActions.find('button').prop('disabled', false);
            }
        }
    });

    // Expand strategy details
    $('#webhook-table-container').on('click', '.strategy-row', function() {
        const id = $(this).attr('data-id');
        const strategy = strategies.find(s => s.id === id);
        
        if (strategy) {
            expandedStrategyId = (expandedStrategyId === id) ? null : id;
            render();
        }
    });

     // Copy webhook URL to clipboard
    $('#webhook-table-container').on('click', '.webhook-url', function() {
        const urlToCopy = $(this).text().trim();
        if (navigator.clipboard && window.isSecureContext) {
            navigator.clipboard.writeText(urlToCopy).then(() => {
                showNotification('Webhook URL Copied!', 'success');
            }).catch(() => {
                fallbackCopyTextToClipboard(urlToCopy);
            });
        } else {
            fallbackCopyTextToClipboard(urlToCopy);
        }
    });
};