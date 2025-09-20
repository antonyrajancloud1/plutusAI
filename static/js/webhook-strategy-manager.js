import { GoogleGenAI, Type } from "@google/genai";

const StrategyType = {
  DEFAULT: 'default',
  CUSTOM: 'custom',
};

const TOKEN = 'dc43c8dd7ac43be69c19139a8b0ff1530f85c9ef';
const indices = [
    { key: 'nifty', name: 'Nifty' },
    { key: 'bank_nifty', name: 'BankNifty' },
    { key: 'fin_nifty', name: 'FinNifty' }
];

const initialStrategies = [
  { id: '1', name: 'UTBOT', type: StrategyType.DEFAULT, enabled: true },
  { id: '2', name: 'SuperTrend', type: StrategyType.DEFAULT, enabled: true },
  { id: '3', name: 'EMACROSS', type: StrategyType.DEFAULT, enabled: false },
];

// App State
let strategies = [...initialStrategies];
let expandedStrategyId = null;

// Helper functions to generate HTML components

function createToggleSwitchHTML(id, enabled) {
  const bgColor = enabled ? 'bg-indigo-600' : 'bg-gray-600';
  const translation = enabled ? 'translate-x-6' : 'translate-x-1';
  return `
    <button
      type="button"
      data-id="${id}"
      class="toggle-switch relative inline-flex items-center h-6 rounded-full w-11 transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 focus:ring-offset-gray-900 ${bgColor}"
      aria-pressed="${enabled}"
    >
      <span class="sr-only">Toggle</span>
      <span
        class="inline-block w-4 h-4 transform bg-white rounded-full transition-transform duration-300 ${translation}"
      />
    </button>
  `;
}

function createStrategyDetailsHTML(strategy) {
    const strategySlug = strategy.name.replace(/ /g, '_').toUpperCase();
    const rows = indices.map(index => {
        const inputData = `{"index_name":"${index.key}","strategy":"${index.key}_${strategySlug}"}`;
        return `
            <tr class="border-b border-gray-700/50 last:border-b-0">
                <td class="p-2 align-top text-white font-medium">${index.name}</td>
                <td class="p-2 align-top text-gray-300 font-mono text-xs break-all">
                    http://plutuz.in/trigger_buy?token=${TOKEN}
                </td>
                <td class="p-2 align-top text-gray-300 font-mono text-xs break-all">
                    http://plutuz.in/trigger_sell?token=${TOKEN}
                </td>
                <td class="p-2 align-top text-gray-300 font-mono text-xs break-all">
                    http://plutuz.in/trigger_exit?token=${TOKEN}
                </td>
                <td class="p-2 align-top">
                    <pre class="bg-gray-900/50 p-2 rounded whitespace-pre-wrap break-all text-gray-300 font-mono text-xs"><code>${inputData}</code></pre>
                </td>
            </tr>
        `;
    }).join('');

    return `
        <div class="bg-gray-800/40 p-4 animate-fade-in-down">
            <table class="w-full text-sm">
                <thead>
                    <tr class="border-b border-gray-700">
                        <th class="p-2 w-[10%] text-left font-semibold text-blue-400 uppercase tracking-wider text-xs">Index Name</th>
                        <th class="p-2 w-[25%] text-left font-semibold text-blue-400 uppercase tracking-wider text-xs">Buy URL</th>
                        <th class="p-2 w-[25%] text-left font-semibold text-blue-400 uppercase tracking-wider text-xs">Sell URL</th>
                        <th class="p-2 w-[25%] text-left font-semibold text-blue-400 uppercase tracking-wider text-xs">Exit URL</th>
                        <th class="p-2 w-[15%] text-left font-semibold text-blue-400 uppercase tracking-wider text-xs">Input Data</th>
                    </tr>
                </thead>
                <tbody>${rows}</tbody>
            </table>
        </div>
    `;
}

function createSuperTrendDetailsHTML() {
    return `
        <div id="supertrend-container" class="p-4 sm:p-6 bg-gray-900/10 animate-fade-in-down">
             <div class="p-6 text-center text-gray-400 animate-pulse">
                Generating SuperTrend Parameters...
            </div>
        </div>
    `;
}

async function fetchAndRenderSuperTrendParameters() {
    const container = $('#supertrend-container');
    try {
        if (!process.env.API_KEY) {
            throw new Error("API_KEY environment variable not set");
        }
        const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
        const prompt = 'Generate a list of configurable parameters for a SuperTrend trading strategy. For each parameter, provide a name, a common default value, and a brief description.';
        const response = await ai.models.generateContent({
            model: "gemini-2.5-flash",
            contents: prompt,
            config: {
                responseMimeType: "application/json",
                responseSchema: {
                    type: Type.OBJECT,
                    properties: {
                        parameters: {
                            type: Type.ARRAY,
                            description: "An array of parameters for the SuperTrend strategy.",
                            items: {
                                type: Type.OBJECT,
                                properties: {
                                    name: { type: Type.STRING, description: "The name of the parameter." },
                                    defaultValue: { type: Type.STRING, description: "A common default value for the parameter, as a string." },
                                    description: { type: Type.STRING, description: "A brief explanation of what the parameter does." }
                                },
                                required: ["name", "defaultValue", "description"]
                            }
                        }
                    },
                    required: ["parameters"]
                },
            }
        });
        const jsonText = response.text.trim();
        const data = JSON.parse(jsonText);
        
        if (!data || !data.parameters) {
            throw new Error("Invalid data format received from API.");
        }
        
        const params = data.parameters;
        const rows = params.map(param => `
            <tr>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-white">${param.name}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-300 font-mono">${param.defaultValue}</td>
                <td class="px-6 py-4 text-sm text-gray-400">${param.description}</td>
            </tr>
        `).join('');

        const tableHTML = `
            <h4 class="text-lg font-semibold text-white mb-4">Generated SuperTrend Parameters</h4>
            <div class="overflow-x-auto rounded-lg border border-gray-700">
                <table class="min-w-full divide-y divide-gray-600">
                    <thead class="bg-gray-800">
                        <tr>
                            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Parameter</th>
                            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Default Value</th>
                            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Description</th>
                        </tr>
                    </thead>
                    <tbody class="bg-gray-800/50 divide-y divide-gray-700">
                        ${rows}
                    </tbody>
                </table>
            </div>
        `;
        container.html(tableHTML);
    } catch (err) {
        console.error("Error fetching SuperTrend parameters:", err);
        const errorMessage = err instanceof Error ? err.message : "An unknown error occurred.";
        const errorHTML = `
             <div class="p-6 text-center text-red-400 bg-red-900/20 border border-red-800 rounded-b-lg">
                <p class="font-semibold">Error</p>
                <p class="text-sm">Failed to generate strategy details. ${errorMessage}</p>
            </div>
        `;
        container.html(errorHTML);
    }
}

function createWebhookTableHTML(strategies) {
    if (strategies.length === 0) {
        return `
        <div class="text-center py-10 px-6 bg-gray-800 rounded-lg border border-gray-700">
            <h3 class="text-lg font-medium text-white">No Strategies Found</h3>
            <p class="mt-1 text-sm text-gray-400">Create a custom strategy to get started.</p>
        </div>
        `;
    }
  
    const tableRows = strategies.map(strategy => {
        const typeClass = strategy.type === StrategyType.DEFAULT ? 'bg-blue-900 text-blue-200' : 'bg-green-900 text-green-200';
        let statusHTML;
        let actionHTML;
        
        if (strategy.type === StrategyType.DEFAULT) {
        statusHTML = strategy.enabled 
            ? `<span class="flex items-center text-green-400"><div class="h-2 w-2 rounded-full bg-green-400 mr-2"></div>Enabled</span>`
            : `<span class="flex items-center text-red-400"><div class="h-2 w-2 rounded-full bg-red-400 mr-2"></div>Disabled</span>`;
        actionHTML = createToggleSwitchHTML(strategy.id, strategy.enabled);
        } else {
        statusHTML = `<span class="text-gray-500">-</span>`;
        actionHTML = `<span class="text-gray-500">-</span>`;
        }

        const canExpand = strategy.type === StrategyType.CUSTOM || strategy.name === 'SuperTrend';
        const rowClass = canExpand ? 'cursor-pointer' : 'cursor-default';
        
        let expandedRowHTML = '';
        if (expandedStrategyId === strategy.id) {
            let detailsContent = '';
            if (strategy.name === 'SuperTrend') {
                detailsContent = createSuperTrendDetailsHTML();
            } else {
                detailsContent = createStrategyDetailsHTML(strategy);
            }
            expandedRowHTML = `
                <tr class="bg-gray-800/40">
                    <td colSpan="4" class="p-0">${detailsContent}</td>
                </tr>
            `;
        }
        
        return `
        <tr data-id="${strategy.id}" class="strategy-row hover:bg-gray-800/50 transition-colors duration-150 ${rowClass}">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-white">${strategy.name}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
            <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full capitalize ${typeClass}">
                ${strategy.type}
            </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">${statusHTML}</td>
            <td class="px-6 py-4 whitespace-nowrap text-center text-sm font-medium">${actionHTML}</td>
        </tr>
        ${expandedRowHTML}
        `;
    }).join('');
  
  return `
    <div class="overflow-x-auto rounded-lg border border-gray-700 shadow-lg">
      <table class="min-w-full divide-y divide-gray-700">
        <thead class="bg-gray-800">
          <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Strategy Name</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Type</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Status</th>
            <th scope="col" class="px-6 py-3 text-center text-xs font-medium text-gray-300 uppercase tracking-wider">Action</th>
          </tr>
        </thead>
        <tbody id="webhook-table-body">${tableRows}</tbody>
      </table>
    </div>
  `;
}

function createAddStrategyFormHTML() {
    return `
        <div class="mt-6 mb-6 p-6 bg-gray-800 rounded-lg border border-gray-700 animate-fade-in">
            <h3 class="text-lg font-semibold text-white mb-4">Create Custom Strategy</h3>
            <form id="add-strategy-form">
                <div class="flex flex-col sm:flex-row gap-4">
                    <label for="strategy-name" class="sr-only">Strategy Name</label>
                    <input
                        id="strategy-name"
                        type="text"
                        placeholder="Enter new strategy name, e.g. 'My Custom MACD'"
                        class="flex-grow bg-gray-900 text-white border border-gray-600 rounded-md px-4 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-shadow duration-200"
                        required
                        autofocus
                    />
                    <div class="flex gap-3 justify-end flex-shrink-0">
                        <button
                        type="button"
                        id="cancel-add-strategy"
                        class="px-5 py-2 bg-gray-600 text-white font-semibold rounded-md hover:bg-gray-500 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 focus:ring-offset-gray-800"
                        >
                        Cancel
                        </button>
                        <button
                        type="submit"
                        class="px-5 py-2 bg-indigo-600 text-white font-semibold rounded-md hover:bg-indigo-700 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 focus:ring-offset-gray-800"
                        >
                        Add Strategy
                        </button>
                    </div>
                </div>
            </form>
        </div>
    `;
}

// Main render function
function render() {
    const tableHTML = createWebhookTableHTML(strategies);
    $('#webhook-table-container').html(tableHTML);
    
    const expandedStrategy = strategies.find(s => s.id === expandedStrategyId);
    if (expandedStrategy && expandedStrategy.name === 'SuperTrend') {
        fetchAndRenderSuperTrendParameters();
    }
}

// Event Handlers
$(function() {
    // Initial render
    render();

    // Show add form
    $('#create-strategy-btn').on('click', function() {
        $('#add-strategy-form-container').html(createAddStrategyFormHTML()).find('input').focus();
        $(this).hide();
    });

    // Cancel add form
    $('#add-strategy-form-container').on('click', '#cancel-add-strategy', function() {
        $('#add-strategy-form-container').empty();
        $('#create-strategy-btn').show();
    });

    // Submit add form
    $('#add-strategy-form-container').on('submit', '#add-strategy-form', function(e) {
        e.preventDefault();
        const name = $('#strategy-name').val().trim();
        if (name) {
            const newStrategy = {
                id: `${Date.now()}`,
                name,
                type: StrategyType.CUSTOM,
                enabled: true,
            };
            strategies.push(newStrategy);
            expandedStrategyId = newStrategy.id;
            $('#add-strategy-form-container').empty();
            $('#create-strategy-btn').show();
            render();
        }
    });

    // Toggle default strategy
    $('#webhook-table-container').on('click', '.toggle-switch', function(e) {
        e.stopPropagation();
        const id = $(this).data('id').toString();
        const strategy = strategies.find(s => s.id === id);
        if (strategy) {
            strategy.enabled = !strategy.enabled;
            render();
        }
    });

    // Expand strategy details
    $('#webhook-table-container').on('click', '.strategy-row', function() {
        const id = $(this).data('id').toString();
        const strategy = strategies.find(s => s.id === id);
        
        if (strategy && (strategy.type === StrategyType.CUSTOM || strategy.name === 'SuperTrend')) {
            expandedStrategyId = (expandedStrategyId === id) ? null : id;
            render();
        }
    });
});