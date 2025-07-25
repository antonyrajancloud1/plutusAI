let MadaraConstructor = function() {
    this.DOM_SELECTORS = {
        main_container          :   "#main-container",
        login_main_container    :   "#login-main-container",
        home_container          :   "#home-container",
        lhs_container           :   "#lhs-container",
        lhs_module_container    :   "#lhs-module-container",
        rhs_container           :   "#rhs-container",
        footer_container        :   "#footer-container",
        profile_name            :   "#profile-name"
    };
    this.project_name   =   "Madara";
    this.EVENT_AND_DOM_CACHE = {};
    this.default_strategy = "default_strategy";
    this.tokenData = null;
    this.currentStrategy = null;
    this.whiteListedProperties = {
        getConfigurations   : [ "actions", "index_name", "levels", "trend_check_points", "strike", "safe_sl", "status" ],
        getScalperDetails   : [ "actions", "index_name", "strike", "target", "is_demo_trading_enabled", "use_full_capital", "lots" ,"status", "on_candle_close" ],
        getManualDetails    : [ "actions", "index_name", "lots", "trigger", "stop_loss", "target", "strike", "current_premium" ],
        getWebhookDetails   : [ "index_name", "buy_url", "sell_url", "exit_url", "input_data" ],
        getOrderBook        : [ "entry_time", "script_name", "qty", "entry_price", "exit_price", "status", "exit_time", "strategy", "total" ],
        getBrokerInfo       : [ "actions", "broker_name", "broker_user_id", "broker_user_name", "broker_mpin", "broker_api_token" ]
    };
    this.statusVsColorCodeClass = {
        initiated   :   "clrB",
        started     :   "clrY",
        running     :   "clrG",
        stopped     :   "clrR"
    }
};

MadaraConstructor.prototype.templates = {
    mainHtml : 
                `<div id="home-container" class="wh100 home-bg-container">
                    <div id="banner-container"></div>
                    <div id="header-container" class="flexC header-container pL15 pT5 pB5 pR20">
                        <div class="flexG font1_5 fontB">{project_name}</div>
                        <div id="today-orders" class="primary-button today-orders flexM bdrR5 pT10 pB10 pL15 pR15"></div>
                        {logout}
                        {profile_html}
                    </div>
                    <div id="body-container" class="flex w100 flexG body-container">
                        <div id="lhs-container" class="ovrflwH lhs-container-main p15">
                            <div id="lhs-module-container" class="flex-col lhs-container h100 posrel ovrflwA gap10">
                                {modules_html}
                            </div>
                        </div>
                        <div id="rhs-container" class="flex h100 flexG ovrflwH rhs-bg-container p20"></div>
                    </div>
                    </div>
                </div>`,

    eachModuleHtml :
                    `<div id="module-{module_id}" class="font18 lhs-module curP bdrR5" home-page-buttons purpose="view{purpose}">
                        {module}
                    </div>`,

    loaderHtml : 
                `<div id="rhs-center-loader" class="h100 w100 flexM fdirC">
                    <div class="rloader posrel"></div>
                </div>`,

    dataTableHtml : 
                    `<div id="{module}-container" class="wh100 flexG {module}-container ovrflwAuto data-table-container" home-page-buttons purpose="{purpose}">
                        <div class="tbl tblHead fshrink">   
                            {table_head_row}
                        </div>
                        <div class="flexG">
                            <div class="tbl tblMain">
                                {table_body}
                            </div>
                        </div>
                    </div>`,

    tableRow : `<div class="tblRow">{table_row_contents}</div>`,

    tableCell : `<div class="tblCel {disable_status} ellips" title="{tooltip_content}">{table_cell_content}</div>`,

    actionsHtml : `<div id="actions-container" class="flexM gap10">
                        {start_button}
                        {stop_button}
                        {exit_button}
                        {edit_button}
                  </div>`,

    startButton : `<div id="start-index" purpose="startIndex" trigger-source="{trigger_source}" home-page-buttons index="{index}" class="action-button xs fa fa-play curP clrG start-index-button p5 bdrR4" title="{start_index_title}"></div>`,

    stopButton : `<div id="stop-index" purpose="stopIndex" trigger-source="{trigger_source}" home-page-buttons index="{index}" class="action-button xs fa fa-stop curP clrR stop-index-button p5 bdrR4" title="{stop_index_title}"></div>`,

    editButton : `<div id="edit-{module}" purpose="{purpose_of_edit}" home-page-buttons index="{index}" class="action-button fa xs fa-pencil curP clrB edit-config-button p5 bdrR4" title="{edit_module_title}"></div>`,

    buyButton : `<div id="buy-{module}" purpose="buyManualOrders" home-page-buttons index="{index}" class="action-button xs curP clrG exit-config-button p5 bdrR4 fontB font10" title="{buy_title}">{buy_title}</div>`,

    sellButton : `<div id="sell-{module}" purpose="sellManualOrders" home-page-buttons index="{index}" class="action-button xs curP clrR exit-config-button p5 bdrR4 fontB font10" title="{sell_title}">{sell_title}</div>`,

    exitButton : `<div id="exit-{module}" purpose="exitManualOrders" home-page-buttons index="{index}" class="action-button xs curP clrY exit-config-button p5 bdrR4 fontB font10" title="{exit_title}">{exit_title}</div>`,

    editButtonForManualOrders : `<div id="edit-{module}" purpose="editManualOrders" home-page-buttons index="{index}" class="action-button xs curP clrB exit-config-button p5 bdrR4 fontB font10" title="{edit_title}">{edit_title}</div>`,

    logoutHtml : 
                `<div id="logout-button" home-page-buttons class="primary-button logout-button curP flexM bdrR5 sm mL20" purpose="logoutUser" userId>
                    {logout_text}
                </div>`,

    profileHtml :   `<div id="profile-region" class="profile-region flex-col gap5 flexM mL20">
                        <div id="profile-container" class="profile-container bdrR100">
                            <div class="profile-wrapper wh100">
                                <img id="profile-image" src="{profile_image}" class="profile-image wh100 bdrR100" alt="Profile Image">
                            </div>
                        </div>
                        <div id="profile-name" class="profile-name font16 ellips"></div>
                    </div>`,

    bannerHtml : 
                `<div id="banner-wrapper" class="{banner_type} banner-wrapper dN textC">
                    <div class="font16 clrW">{banner_content}</div>
                </div>`,

    formHtml : 
                `<div id="index-edit-configuration-form" class="index-edit-configuration-form mask-bg">
                    <div id="form-main-container" class="form-main-container flex-col flexG">
                        <div id="form-header" class="flexM pB15 pL15 pR15 fontB fontItalic form-header justifySB">
                            <div class="font24">{index_configuration}</div>
                            <div class="fa fa-close close-icon font14 curP clrW flexM" purpose="closeEditConfigurationForm" home-page-buttons title="{close}"></div>
                        </div>
                        <div id="form-body" class="flexM">
                            <div id="form-input-elements" class="form-input-elements flex-col flexG gap20 p15" {main_key}="{index_name}">
                                {input_elements}
                            </div>
                        </div>
                        <div id="form-footer" class="flexM pT15 pL15 pR15">
                            <div id="sumbit-form" class="submit-button bdrR10 flexM curP sm primary-button" purpose="{purpose_of_submit}" home-page-buttons>{update_config}</div>
                        </div>
                    </div>
                </div>`,

    textInputHtml : 
                    `<div class="flexC gap10" property="{configuration_key}">
                        <div id="{configuration_key}-label" class="label-container ellips" title="{configuration_key_text}">{configuration_key_text}</div>
                        <div id="{configuration_key}-input-container" class="input-container">
                            <input id="{configuration_key}-input-element" type="text" class="edit-config-input-elements" autocomplete="off" value="{value}">
                        </div>
                    </div>`,

    booleanInputHtml : 
                    `<div class="flexC gap10" property="{configuration_key}" boolean-input>
                        <div id="{configuration_key}-label" class="label-container ellips" title="{configuration_key_text}">{configuration_key_text}</div>
                        <div id="{configuration_key}-input-container" class="input-container flexC">
                            <input id="{configuration_key}-input-element" type="checkbox" class="edit-config-boolean-input-elements" {checked}>
                        </div>
                    </div>`,

    noDataFoundHtml : 
                    `<div id="no-data-found-container" class="wh100 flexG pL35 pR35 pT20 pB20 flexM gap10 font24 no-data-found-container">  
                        <div class="fa fa-close clrR flex"></div>
                        <div class="fontItalic">{no_data_text}</div>
                    </div>`,

    dashboardHtml : 
                    `<div id="dashboard-container" class="dashboard-container wh100">
                        <div class="item-1 pnl flex-col">
                            <div class="font18 fontB">{pnl_header}</div>
                            {chart_html}
                        </div>
                        <div class="item-2 positions ovrflwH flex-col gap10">
                            <div class="font18 fontB">{positions_header}</div>
                            {positions_html}
                        </div>
                        <div class="item-3 orders ovrflwH flex-col gap10">
                            <div class="font18 fontB">{orders_header}</div>
                            {orders_html}
                        </div>
                        <div class="item-4 open-orders">
                            <div class="font18 fontB">{open_orders_header}</div>
                            {open_orders_html}
                        </div>
                    </div>`,

    htmlForCellContentHightlighter : `<span class="{class_for_highlighting}">{cell_content}</span>`,

    pnlInfoHtml :   `<div class="textC font18 fontB">
                        {pnl_info_header}
                        <span class="{class_for_total_pnl}">{total_pnl_cost_in_rupees}</span>
                    </div>`,

    manualOrdersHtml :
                    `<div id="manual-order-container" class="manual-order-container flex-col">
                        {strategy_search_html}
                        {manual_orders_table}
                        {webhook_details}
                    </div>`,

    strategySearchHtml :    
                    `<div id="strategy-search-container" class="flexC strategy-search-container pB20 gap15">
                        <div>{strategy_name_text}</div>
                        <input id="strategy-name-input" type="text" placeholder="{strategy_search_placeholder}" value="{strategy_search_value}" class="strategy-name-input edit-config-input-elements" home-page-buttons purpose="updateWebhookDataTableWithThisStrategy" autocomplete="off" value="{strategy_name}" />
                    </div>`,

    webhookDetailsHtml : 
                    `<div id="webhook-details-container" class="webhook-details-container flex-col ovrflwH">
                        <div class="mT30 mB20 flexC justifySB">
                            <div class="font18 fontB">{webhook_details_header}</div>
                            <div id="token-details" class="token-details flexC gap10">
                                <div id="regenerate-token-button" class="regenerate-token-button bdrR5 flexC curP sm" home-page-buttons purpose="regenerateAuthToken">{regenerate_token}</div>
                                <div id="auth-token" class="auth-token pT10 pB10 pL15 pR15 bdrR5">{token}</div>
                            </div>
                        </div>
                        <div class="flex-col gap10 ovrflwA">
                            {webhook_details_table}
                        </div>
                    </div>`
};

MadaraConstructor.prototype.getWindowLocationOrigin = function() {
    return window.location.origin;
};

MadaraConstructor.prototype.API = {
    home                    :   "/home",
    login                   :   "/login",
    logout                  :   "/logout",
    getConfigValues         :   "/get_config_values",
    getSummary              :   "/get_strategy_summary",
    getManualDetails        :   "/manual_details",  
    updateManualDetails     :   "/update_manual_details",  
    updateConfigValues      :   "/update_config_values",
    addUser                 :   "/add_user",
    getBrokerDetails        :   "/get_broker_details",
    addBrokerDetails        :   "/add_broker_details",
    editBrokerDetails       :   "/edit_broker_details",
    getOrderBookDetails     :   "/get_order_book_details",
    getScalperDetails       :   "/get_scalper_details",
    updateScalperDetails    :   "/update_scalper_details",
    startIndex              :   "/start_index",
    stopIndex               :   "/stop_index",
    startScalper            :   "/start_scalper",
    placeManualOrder        :   "/place_order_buy",
    placeOrderViaWebhook    :   "/trigger_buy",
    sellManualOrder         :   "/place_order_sell",
    sellOrderViaWebhook     :   "/trigger_sell",
    exitManualOrder         :   "/place_order_exit",
    exitOrderViaWebhook     :   "/trigger_exit",
    getPlans                :   "/plans",
    editPlans               :   "/edit_plans",
    getTokenData            :   "/get_auth_token",
    generateAuthToken       :   "/generate_auth_token",
    brokerToken             :   "/regenrate_token"
};

MadaraConstructor.prototype.getLHSModulesList = function() {
    return [ "dashboard", "orderBook", "configurations", "manualOrders", "scalper", "brokerInfo" ];
};

MadaraConstructor.prototype.addLoaderForTheRHS = function() {
    $(this.DOM_SELECTORS.rhs_container).html(this.templates.loaderHtml);
};

MadaraConstructor.prototype.getResource = function(key) {
    let resourceValue = Resource[key];
    if(!resourceValue) {
        return key;
    }
    return resourceValue;
};

MadaraConstructor.prototype.getLHSModulesHtml = function() {
    let modules = this.getLHSModulesList();
    let allModulesHtml = "";
    modules.forEach(module => {
        allModulesHtml += this.templates.eachModuleHtml.replace(/{module}/g, this.getResource(module))
                                                        .replace(/{module_id}/g, module)
                                                        .replace(/{purpose}/g, module.charAt(0).toUpperCase() + module.slice(1));
    });
    return allModulesHtml;
};

MadaraConstructor.prototype.getLogoutButton = function() {
    return this.templates.logoutHtml.replace(/{logout_text}/g, this.getResource("logout"));
};

MadaraConstructor.prototype.getProfileHtml = function() {
    return this.templates.profileHtml.replace(/{profile_image}/g, "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Default_pfp.svg/1024px-Default_pfp.svg.png");
};

MadaraConstructor.prototype.getHomeHtml = function() {
    return this.templates.mainHtml.replace(/{modules_html}/g, this.getLHSModulesHtml())
                                    .replace(/{logout}/g, this.getLogoutButton())
                                    .replace(/{profile_html}/g, this.getProfileHtml())
                                    .replace(/{project_name}/g, this.project_name);
};

MadaraConstructor.prototype.setCurrentLHSModuleAsSelected = function(domId) {
    let lhsModuleContainer = $(this.DOM_SELECTORS.lhs_module_container);
    lhsModuleContainer.children().removeClass("selected");
    let domToBeSelected = (this.EVENT_AND_DOM_CACHE.currentTarget) ? (this.EVENT_AND_DOM_CACHE.currentTarget) : lhsModuleContainer.find(domId);
    domToBeSelected.addClass("selected");
};

MadaraConstructor.prototype.addLoaderInThisButton = function(element) {
    element.addClass("rloader");
};

MadaraConstructor.prototype.removeLoaderInThisButton = function(element) {
    element.removeClass("rloader");
};

MadaraConstructor.prototype.getStartIndexButton = function(index) {
    return this.templates.startButton.replace(/{start_index_title}/g, Resource.start_index);
};

MadaraConstructor.prototype.getStopIndexButton = function(index) {
    return this.templates.stopButton.replace(/{stop_index_title}/g, Resource.stop_index);
};

MadaraConstructor.prototype.getEditButton = function() {
    return this.templates.editButton.replace(/{edit_module_title}/g, Resource.edit_config);
};

MadaraConstructor.prototype.getBuyButton = function() {
    return this.templates.buyButton.replace(/{buy_title}/g, Resource.buy);
};

MadaraConstructor.prototype.getSellButton = function() {
    return this.templates.sellButton.replace(/{sell_title}/g, Resource.sell);
};

MadaraConstructor.prototype.getExitButton = function() {
    return this.templates.exitButton.replace(/{exit_title}/g, Resource.exit);
};

MadaraConstructor.prototype.getEditButtonForManualOrders = function() {
    return this.templates.editButtonForManualOrders.replace(/{edit_title}/g, Resource.edit);
};

MadaraConstructor.prototype.updateBanner = function(bannerObject) {
    if(!bannerObject || (bannerObject.content === "")) {
        return;
    }
    clearTimeout(this.bannertimer);
    let bannerHtml = this.templates.bannerHtml;
    bannerHtml = bannerHtml.replace(/{banner_type}/g, bannerObject.type)
                            .replace(/{banner_content}/g, bannerObject.content);
    let bannerContainer = $("#banner-container");
    bannerContainer.html(bannerHtml);					//NO I18N
    let bannerWrapper = bannerContainer.find("#banner-wrapper");
    bannerWrapper.slideDown();
    setTimeout( function() { 
        bannerWrapper.slideUp()
    }, "3000");
};

MadaraConstructor.prototype.getFormattedTime = function(time) {
    if(!time) {
        return "-";
    }

    if(!isNaN(time)) {
        time = time * 1000;
    }
    
    let dateObject = new Date(time);
    return dateObject.toDateString().split(' ').slice(1).join(' ') + ", " + dateObject.toLocaleTimeString(["en-US"], { hour12 : true, hour : '2-digit', minute : '2-digit', second : '2-digit' });
};

MadaraConstructor.prototype.populateNoDataFoundHTML = function() {
    let noDataFoundHtml = this.templates.noDataFoundHtml.replace(/{no_data_text}/g, Resource["no_data_found"]);
    $(this.DOM_SELECTORS.rhs_container).html(noDataFoundHtml);
};

MadaraConstructor.prototype.viewOrderBook = function() {
    let self = this;
    this.setCurrentLHSModuleAsSelected("#module-orderBook");
    this.addLoaderForTheRHS();
    let whiteListedProperties = this.whiteListedProperties.getOrderBook;
    let url = this.API.getOrderBookDetails;
    let additionalAjaxOptions = {
        type    :   "GET",
        success :   function(successResp) {
            let tableHeadCell = "";
            whiteListedProperties.forEach(property => {
                tableHeadCell +=  self.templates.tableCell.replace(/{table_cell_content}/g, Resource[property])
                                                            .replace(/{tooltip_content}/g, Resource[property])
                                                            .replace(/{disable_status}/, "");
            });
            let tableHeadRow = self.templates.tableRow.replace(/{table_row_contents}/g, tableHeadCell);
            let response = successResp.order_book_details;
            if(!response.length) {
                self.populateNoDataFoundHTML();
                return;
            }
            let eachConfigurationRow = "";
            response.forEach((key, index) => {
                let currentConfiguration = response[index];
                let configurationObject = currentConfiguration;
                let disableStatus = configurationObject["disable"];

                let eachConfigurationCell = "";
                whiteListedProperties.forEach(property => {
                    if(property !== "index_name") {
                        let tableCellContent = (property === "status") ? Resource[configurationObject[property]] : property.includes("time") ? self.getFormattedTime(configurationObject[property]) : configurationObject[property];
                        let tooltipContent = tableCellContent;
                        if(property === "total") {
                            let total = configurationObject[property] ? configurationObject[property] : 0;
                            total = parseFloat(total);
                            let totalInLocale = parseFloat(configurationObject[property]).toLocaleString('en-IN', { minimumFractionDigits : 2, maximumFractionDigits : 2 });
                            tooltipContent = totalInLocale;
                            tableCellContent = self.templates.htmlForCellContentHightlighter.replace(/{class_for_highlighting}/g, (total > 0) ? "positive" : ((total == 0) ? "neutral" : "negative"))
                                                                            .replace(/{cell_content}/g, totalInLocale);
                        }
                        eachConfigurationCell += self.templates.tableCell.replace(/{table_cell_content}/g, tableCellContent ? tableCellContent : "-")
                                                                            .replace(/{tooltip_content}/g, tooltipContent ? tooltipContent : "")
                                                                            .replace(/{disable_status}/g, disableStatus ? "disabled" : "");
                    }
                });
                eachConfigurationRow += self.templates.tableRow.replace(/{table_row_contents}/g, eachConfigurationCell);
            });

            let dataTableForConfiguration = self.templates.dataTableHtml.replace(/{module}/g, "orderBook")
                                                                        .replace(/{table_head_row}/g, tableHeadRow)
                                                                        .replace(/{table_body}/g, eachConfigurationRow);

            $(self.DOM_SELECTORS.rhs_container).html(dataTableForConfiguration);
        },
        error   :   function(errorResp) {
            let errorContent = (JSON.parse(errorResp.responseText).message) ? self.checkAndGetResponseMessageFromResourceObject(JSON.parse(errorResp.responseText).message) : errorResp.statusText;
            self.updateBanner({ type : "failure", content : errorContent });
        }
    }
    this.makeAjaxRequest(url, {}, additionalAjaxOptions);
};

MadaraConstructor.prototype.viewBrokerInfo = function() {
    let self = this;
    this.setCurrentLHSModuleAsSelected("#module-brokerInfo");
    this.addLoaderForTheRHS();
    let whiteListedProperties = this.whiteListedProperties.getBrokerInfo;
    let url = this.API.getBrokerDetails;
    let additionalAjaxOptions = {
        type    :   "GET",
        success :   function(successResp) {
            let tableHeadCell = "";
            whiteListedProperties.forEach((property, index) => {
                tableHeadCell +=  self.templates.tableCell.replace(/{table_cell_content}/g, Resource[property])
                                                            .replace(/{tooltip_content}/g, Resource[property])
                                                            .replace(/{disable_status}/, index === 0 ? "actions-table-cell" : "");
            });
            let tableHeadRow = self.templates.tableRow.replace(/{table_row_contents}/g, tableHeadCell);
            let response = successResp.broker_details;
            if(!response.length) {
                self.populateNoDataFoundHTML();
                return;
            }
            let eachConfigurationRow = "";
            response.forEach((key, index) => {
                let currentConfiguration = response[index];
                let configurationObject = currentConfiguration;
                let disableStatus = configurationObject["disable"];
                let actionsHtml = self.templates.actionsHtml.replace(/{start_button}/g, "")
                                                            .replace(/{stop_button}/g, "")
                                                            .replace(/{exit_button}/g, "")
                                                            .replace(/{edit_button}/g, self.getEditButton());
                
                actionsHtml = actionsHtml.replace(/{index}/g, configurationObject["broker_name"])
                                        .replace(/{module}/g, "broker")
                                        .replace(/{purpose_of_edit}/g, "editThisBrokerDetail");

                let eachConfigurationCell = self.templates.tableCell.replace(/{table_cell_content}/g, actionsHtml)
                                                                    .replace(/{tooltip_content}/g, "")
                                                                    .replace(/{disable_status}/g, disableStatus ? "disabled actions-table-cell" : "actions-table-cell");

                whiteListedProperties.forEach(property => {
                    if(property !== "index_name" && property !== "actions") {
                        let tableCellContent = (property === "broker_name" || property === "token_status" || property === "index_group") ? Resource[configurationObject[property]] : configurationObject[property];
                        eachConfigurationCell += self.templates.tableCell.replace(/{table_cell_content}/g, tableCellContent ? tableCellContent : "-")
                                                                            .replace(/{tooltip_content}/g, tableCellContent ? tableCellContent : "")
                                                                            .replace(/{disable_status}/g, disableStatus ? "disabled" : "");
                    }
                });
                eachConfigurationRow += self.templates.tableRow.replace(/{table_row_contents}/g, eachConfigurationCell);
            });

            let dataTableForConfiguration = self.templates.dataTableHtml.replace(/{module}/g, "brokerInfo")
                                                                        .replace(/{table_head_row}/g, tableHeadRow)
                                                                        .replace(/{table_body}/g, eachConfigurationRow);

            $(self.DOM_SELECTORS.rhs_container).html(dataTableForConfiguration);
        },
        error   :   function(errorResp) {
            let errorContent = (JSON.parse(errorResp.responseText).message) ? self.checkAndGetResponseMessageFromResourceObject(JSON.parse(errorResp.responseText).message) : errorResp.statusText;
            self.updateBanner({ type : "failure", content : errorContent });
        }
    }
    this.makeAjaxRequest(url, {}, additionalAjaxOptions);
};

MadaraConstructor.prototype.viewScalper = function() {
    let self = this;
    this.setCurrentLHSModuleAsSelected("#module-configurations");
    this.addLoaderForTheRHS();
    let whiteListedProperties = this.whiteListedProperties.getScalperDetails;
    let url = this.getWindowLocationOrigin() + this.API.getScalperDetails;
    let additionalAjaxOptions = {
        type    :   "GET",
        success :   function(successResp) {
            let tableHeadCell = "";
            whiteListedProperties.forEach((property, index) => {
                tableHeadCell +=  self.templates.tableCell.replace(/{table_cell_content}/g, Resource[property])
                                                            .replace(/{tooltip_content}/g, Resource[property])
                                                            .replace(/{disable_status}/, index === 0 ? "actions-table-cell" : "");
            });
            let tableHeadRow = self.templates.tableRow.replace(/{table_row_contents}/g, tableHeadCell);
            let response = successResp.all_config_values;
            if(!response.length) {
                self.populateNoDataFoundHTML();
                return;
            }
            let eachConfigurationRow = "";
            response.forEach((key, index) => {
                let currentConfiguration = response[index];
                let configuration = currentConfiguration.index_name;
                let configurationObject = currentConfiguration;
                let disableStatus = configurationObject["disable"];
                let actionsHtml = self.templates.actionsHtml.replace(/{start_button}/g, self.getStartIndexButton())
                                                            .replace(/{stop_button}/g, self.getStopIndexButton())
                                                            .replace(/{exit_button}/g, "")
                                                            .replace(/{edit_button}/g, self.getEditButton());
                                                            
                actionsHtml = actionsHtml.replace(/{index}/g, configuration)
                                        .replace(/{module}/g, "scalper")
                                        .replace(/{purpose_of_edit}/g, "editThisIndexScalper")
                                        .replace(/{trigger_source}/g, "scalper");

                let eachConfigurationCell = self.templates.tableCell.replace(/{table_cell_content}/g, actionsHtml)
                                                                    .replace(/{tooltip_content}/g, "")
                                                                    .replace(/{disable_status}/g, disableStatus ? "disabled actions-table-cell" : "actions-table-cell");

                eachConfigurationCell += self.templates.tableCell.replace(/{table_cell_content}/g, Resource[configuration])
                                                                    .replace(/{tooltip_content}/g, Resource[configuration])
                                                                    .replace(/{disable_status}/g, disableStatus ? "disabled" : "");

                whiteListedProperties.forEach(property => {
                    if(property !== "index_name" && property !== "actions") {
                        let valueFromResponse = configurationObject[property];
                        let tableCellContent = (property === "status") ? (Resource[valueFromResponse] ? Resource[valueFromResponse] : valueFromResponse) : valueFromResponse;
                        eachConfigurationCell += self.templates.tableCell.replace(/{table_cell_content}/g, (typeof tableCellContent !== "undefined") ? tableCellContent : "-")
                                                                         .replace(/{tooltip_content}/g, tableCellContent ? tableCellContent : "")
                                                                         .replace(/{disable_status}/g, disableStatus ? "disabled" : "");
                    }
                });
                eachConfigurationRow += self.templates.tableRow.replace(/{table_row_contents}/g, eachConfigurationCell);
            });

            let dataTableForConfiguration = self.templates.dataTableHtml.replace(/{module}/g, "scalper")
                                                                        .replace(/{table_head_row}/g, tableHeadRow)
                                                                        .replace(/{table_body}/g, eachConfigurationRow);

            $(self.DOM_SELECTORS.rhs_container).html(dataTableForConfiguration);
        },
        error   :   function(errorResp) {
            let errorContent = (JSON.parse(errorResp.responseText).message) ? self.checkAndGetResponseMessageFromResourceObject(JSON.parse(errorResp.responseText).message) : errorResp.statusText;
            self.updateBanner({ type : "failure", content : errorContent });
        }
    }
    this.makeAjaxRequest(url, {}, additionalAjaxOptions);
};

MadaraConstructor.prototype.viewPlans = function() {
    this.setCurrentLHSModuleAsSelected("#module-plans");
    this.addLoaderForTheRHS();
};

MadaraConstructor.prototype.viewNeedHelp = function() {
    this.setCurrentLHSModuleAsSelected("#module-needHelp");
    this.addLoaderForTheRHS();
};

MadaraConstructor.prototype.viewConfigurations = function() {
    let self = this;
    this.setCurrentLHSModuleAsSelected("#module-configurations");
    this.addLoaderForTheRHS();
    let whiteListedProperties = this.whiteListedProperties.getConfigurations;
    let url = this.getWindowLocationOrigin() + this.API.getConfigValues;
    let additionalAjaxOptions = {
        type    :   "GET",
        success :   function(successResp) {
            let tableHeadCell = "";
            whiteListedProperties.forEach((property, index) => {
                tableHeadCell +=  self.templates.tableCell.replace(/{table_cell_content}/g, Resource[property])
                                                            .replace(/{tooltip_content}/g, Resource[property])
                                                            .replace(/{disable_status}/, index === 0 ? "actions-table-cell" : "");
            });
            let tableHeadRow = self.templates.tableRow.replace(/{table_row_contents}/g, tableHeadCell);
            let response = successResp.all_config_values;
            if(!response.length) {
                self.populateNoDataFoundHTML();
                return;
            }
            let eachConfigurationRow = "";
            response.forEach((key, index) => {
                let currentConfiguration = response[index];
                let configuration = currentConfiguration.index_name;
                let configurationObject = currentConfiguration;
                let disableStatus = configurationObject["disable"];
                let actionsHtml = self.templates.actionsHtml.replace(/{start_button}/g, self.getStartIndexButton())
                                                            .replace(/{stop_button}/g, self.getStopIndexButton())
                                                            .replace(/{exit_button}/g, "")
                                                            .replace(/{edit_button}/g, self.getEditButton());
                                                            
                actionsHtml = actionsHtml.replace(/{index}/g, configuration)
                                        .replace(/{module}/g, "configurations")
                                        .replace(/{purpose_of_edit}/g, "editThisIndexConfiguration")
                                        .replace(/{trigger_source}/g, "configurations");

                let eachConfigurationCell = self.templates.tableCell.replace(/{table_cell_content}/g, actionsHtml)
                                                                    .replace(/{tooltip_content}/g, "")
                                                                    .replace(/{disable_status}/g, disableStatus ? "disabled actions-table-cell" : "actions-table-cell");

                eachConfigurationCell += self.templates.tableCell.replace(/{table_cell_content}/g, Resource[configuration])
                                                                    .replace(/{tooltip_content}/g, Resource[configuration])
                                                                    .replace(/{disable_status}/g, disableStatus ? "disabled" : "");

                whiteListedProperties.forEach(property => {
                    if(property !== "index_name" && property !== "actions") {
                        let valueFromResponse = configurationObject[property];
                        let tableCellContent = (property === "status") ? (Resource[valueFromResponse] ? Resource[valueFromResponse] : valueFromResponse) : valueFromResponse;
                        let tooltipContent = tableCellContent;
                        if(property === "status") {
                            tableCellContent = self.templates.htmlForCellContentHightlighter.replace(/{class_for_highlighting}/g, self.statusVsColorCodeClass[valueFromResponse] ? self.statusVsColorCodeClass[valueFromResponse] : "neutral")
                                                                            .replace(/{cell_content}/g, tooltipContent);
                        }
                        eachConfigurationCell += self.templates.tableCell.replace(/{table_cell_content}/g, tableCellContent ? tableCellContent : "-")
                                                                         .replace(/{tooltip_content}/g, tooltipContent ? tooltipContent : "")
                                                                         .replace(/{disable_status}/g, disableStatus ? "disabled" : "");
                    }
                });
                eachConfigurationRow += self.templates.tableRow.replace(/{table_row_contents}/g, eachConfigurationCell);
            });

            let dataTableForConfiguration = self.templates.dataTableHtml.replace(/{module}/g, "configurations")
                                                                        .replace(/{table_head_row}/g, tableHeadRow)
                                                                        .replace(/{table_body}/g, eachConfigurationRow);

            $(self.DOM_SELECTORS.rhs_container).html(dataTableForConfiguration);
        },
        error   :   function(errorResp) {
            let errorContent = (JSON.parse(errorResp.responseText).message) ? self.checkAndGetResponseMessageFromResourceObject(JSON.parse(errorResp.responseText).message) : errorResp.statusText;
            self.updateBanner({ type : "failure", content : errorContent });
        }
    }
    this.makeAjaxRequest(url, {}, additionalAjaxOptions);
};

MadaraConstructor.prototype.viewDashboard = function() {
    let self = this;
    this.setCurrentLHSModuleAsSelected("#module-dashboard");
    this.addLoaderForTheRHS();
    let url = this.getWindowLocationOrigin() + this.API.getSummary;
    let additionalAjaxOptions = {
        type    :   "GET",
        success :   function(successResp) {
            let summary = successResp.summary;
            let userName = summary.user_name;
            userName = userName.charAt(0).toUpperCase() + userName.slice(1);
            $(self.DOM_SELECTORS.profile_name).text(userName).attr("title", Resource.hello + " " + userName);
            
            let totalOrdersForToday = summary.total_orders_today;
            $(self.DOM_SELECTORS.main_container).find("#today-orders").text(Resource.total_orders_today + " : " + totalOrdersForToday);
            let currentDaySummary = summary.current_day_summary;
            let fullSummary = summary.full_summary;
            let dashBoardHtml = self.templates.dashboardHtml.replace(/{pnl_header}/g, Resource.todays_pandl)
                                                            .replace(/{positions_header}/g, Resource.live_positions)
                                                            .replace(/{orders_header}/g, Resource.orders)
                                                            .replace(/{open_orders_header}/g, Resource.open_orders)
                                                            .replace(/{chart_html}/g, self.getChartHTML())
                                                            .replace(/{positions_html}/g, self.getPositionsAndOrdersHTML(currentDaySummary, "needPositions"))
                                                            .replace(/{orders_html}/g, self.getPositionsAndOrdersHTML(currentDaySummary, "needOrders"))
                                                            .replace(/{open_orders_html}/g, self.getPositionsAndOrdersHTML(currentDaySummary, "needOpenOrders"))

            $(self.DOM_SELECTORS.rhs_container).html(dashBoardHtml);
            self.renderChartForPNL(currentDaySummary);
        },
        error   :   function(errorResp) {
            let errorContent = (JSON.parse(errorResp.responseText).message) ? self.checkAndGetResponseMessageFromResourceObject(JSON.parse(errorResp.responseText).message) : errorResp.statusText;
            self.updateBanner({ type : "failure", content : errorContent });
        }
    }
    this.makeAjaxRequest(url, {}, additionalAjaxOptions);
};

MadaraConstructor.prototype.viewManualOrders = function() {
    let self = this;
    this.setCurrentLHSModuleAsSelected("#module-dashboard");
    this.addLoaderForTheRHS();
    let whiteListedProperties = this.whiteListedProperties.getManualDetails;
    let url = this.getWindowLocationOrigin() + this.API.getManualDetails;
    let additionalAjaxOptions = {
        type    :   "GET",
        success :   async function(successResp) {
            let webhookData = successResp.message;
            if(!webhookData.length) {
                self.populateNoDataFoundHTML();
                return;
            }
            
            let tableHeadCell = "";
            whiteListedProperties.forEach((property, index) => {
                tableHeadCell +=  self.templates.tableCell.replace(/{table_cell_content}/g, Resource[property])
                                                            .replace(/{tooltip_content}/g, Resource[property])
                                                            .replace(/{disable_status}/, index === 0 ? "actions-table-cell" : "");
            });
            let tableHeadRow = self.templates.tableRow.replace(/{table_row_contents}/g, tableHeadCell);
            
            let eachConfigurationRow = "";
            webhookData.forEach((key, index) => {
                let currentConfiguration = webhookData[index];
                let configuration = currentConfiguration.index_name;
                let configurationObject = currentConfiguration;
                let disableStatus = configurationObject["disable"];
                let actionsHtml = self.templates.actionsHtml.replace(/{start_button}/g, self.getBuyButton())
                                                            .replace(/{stop_button}/g, self.getSellButton())
                                                            .replace(/{exit_button}/g, self.getExitButton())
                                                            .replace(/{edit_button}/g, self.getEditButtonForManualOrders());
                                                            
                actionsHtml = actionsHtml.replace(/{index}/g, configuration)
                                        .replace(/{module}/g, "manualOrders")
                                        .replace(/{purpose_of_edit}/g, "editThisManualOrder")
                                        .replace(/{trigger_source}/g, "manualOrders");

                let eachConfigurationCell = self.templates.tableCell.replace(/{table_cell_content}/g, actionsHtml)
                                                                    .replace(/{tooltip_content}/g, "")
                                                                    .replace(/{disable_status}/g, disableStatus ? "disabled actions-table-cell" : "actions-table-cell");

                eachConfigurationCell += self.templates.tableCell.replace(/{table_cell_content}/g, Resource[configuration])
                                                                    .replace(/{tooltip_content}/g, Resource[configuration])
                                                                    .replace(/{disable_status}/g, disableStatus ? "disabled" : "");

                whiteListedProperties.forEach(property => {
                    if(property !== "index_name" && property !== "actions") {
                        let valueFromResponse = configurationObject[property];
                        let tableCellContent = (property === "status") ? (Resource[valueFromResponse] ? Resource[valueFromResponse] : valueFromResponse) : valueFromResponse;
                        eachConfigurationCell += self.templates.tableCell.replace(/{table_cell_content}/g, tableCellContent ? tableCellContent : "-")
                                                                         .replace(/{tooltip_content}/g, tableCellContent ? tableCellContent : "")
                                                                         .replace(/{disable_status}/g, disableStatus ? "disabled" : "");
                    }
                });
                eachConfigurationRow += self.templates.tableRow.replace(/{table_row_contents}/g, eachConfigurationCell);
            });

            let dataTableForConfiguration = self.templates.dataTableHtml.replace(/{module}/g, "manualOrders")
                                                                        .replace(/{table_head_row}/g, tableHeadRow)
                                                                        .replace(/{table_body}/g, eachConfigurationRow);

            let manualOrdersHtml = self.templates.manualOrdersHtml.replace(/{manual_orders_table}/g, dataTableForConfiguration)
                                                                .replace(/{strategy_search_html}/g, self.getStrategySearchHTML())
                                                                .replace(/{webhook_details}/g, await self.getWebhookDetailsHTML(webhookData));

            self.webhookData = webhookData;

            $(self.DOM_SELECTORS.rhs_container).html(manualOrdersHtml);
            
        },
        error   :   function(errorResp) {
            let errorContent = (JSON.parse(errorResp.responseText).message) ? self.checkAndGetResponseMessageFromResourceObject(JSON.parse(errorResp.responseText).message) : errorResp.statusText;
            self.updateBanner({ type : "failure", content : errorContent });
        }
    }
    this.makeAjaxRequest(url, {}, additionalAjaxOptions);
};

MadaraConstructor.prototype.getStrategySearchHTML = function() {
    let strategySearchHtml = this.templates.strategySearchHtml.replace(/{strategy_name_text}/g, Resource.strategy_name_text)
                                                            .replace(/{strategy_search_placeholder}/g, Resource.default_strategy)
                                                            .replace(/{strategy_search_value}/g, this.default_strategy);

    return strategySearchHtml;
};

MadaraConstructor.prototype.getBuyUrl = function() {
    return this.getWindowLocationOrigin() + this.API.placeOrderViaWebhook + "?token=" + this.tokenData.message;
};

MadaraConstructor.prototype.getSellUrl = function() {
    return this.getWindowLocationOrigin() + this.API.sellOrderViaWebhook + "?token=" + this.tokenData.message;
};

MadaraConstructor.prototype.getExitUrl = function() {
    return this.getWindowLocationOrigin() + this.API.exitOrderViaWebhook + "?token=" + this.tokenData.message;
};

MadaraConstructor.prototype.getWebhookDetailsHTML = async function(webhookData, strategyName) {
    let self = this;
    let tokenData = "";
    try {
        if(!self.tokenData) {
            tokenData = await this.getTokenData();
            self.tokenData = tokenData;
        } else {
            tokenData = self.tokenData;
        }
        let whiteListedProperties = this.whiteListedProperties.getWebhookDetails;
        let tableHeadCell = "";
        whiteListedProperties.forEach((property, index) => {
            tableHeadCell +=  self.templates.tableCell.replace(/{table_cell_content}/g, Resource[property])
                                                        .replace(/{tooltip_content}/g, Resource[property])
                                                        .replace(/{disable_status}/, "");
        });
        let tableHeadRow = self.templates.tableRow.replace(/{table_row_contents}/g, tableHeadCell);
        
        let eachConfigurationRow = "";

        let neededDetailsObject = {
            buy_url         :   this.getBuyUrl(),
            sell_url        :   this.getSellUrl(),
            exit_url        :   this.getExitUrl(),
            input_data      :   { }
        };

        webhookData.forEach((key, index) => {
            let currentConfiguration = webhookData[index];
            let configurationObject = currentConfiguration;
            configurationObject = $.extend(configurationObject, neededDetailsObject);

            let indexName = configurationObject.index_name;
            configurationObject.input_data.index_name = indexName;
            let strategy = (indexName + "_" + self.default_strategy);
            self.currentStrategy = self.default_strategy;
            if(strategyName) {
                strategy = (strategyName === self.default_strategy) ? (indexName + "_" + self.default_strategy) : (indexName + "_" + strategyName);
                self.currentStrategy = (strategyName !== "") ? strategyName : self.currentStrategy;
            }
            self.currentStrategy = strategyName ? strategyName : self.default_strategy;
            configurationObject.input_data.strategy = strategy;
            let eachConfigurationCell = "";
            whiteListedProperties.forEach(property => {
                if(property !== "actions") {
                    let valueFromResponse = configurationObject[property];
                    let tableCellContent = (property === "index_name") ? (Resource[valueFromResponse] ? Resource[valueFromResponse] : valueFromResponse) : valueFromResponse;
                    if(property === "input_data") {
                        tableCellContent = JSON.stringify(configurationObject.input_data);
                    }
                    eachConfigurationCell += self.templates.tableCell.replace(/{table_cell_content}/g, tableCellContent ? tableCellContent : "-")
                                                                        .replace(/{tooltip_content}/g, "")
                                                                        .replace(/{disable_status}/g, "webhook-details-table-cell can-be-copied");
                } 
            });
            eachConfigurationRow += self.templates.tableRow.replace(/{table_row_contents}/g, eachConfigurationCell);
        });

        let dataTableForConfiguration = self.templates.dataTableHtml.replace(/{module}/g, "webhookDetails")
                                                                    .replace(/{purpose}/g, "copyTheContentOfTheWebhookDetails")
                                                                    .replace(/{table_head_row}/g, tableHeadRow)
                                                                    .replace(/{table_body}/g, eachConfigurationRow);

        
        
        let token = tokenData.message ? tokenData.message : "";
        let webhookDetailsHtml = this.templates.webhookDetailsHtml.replace(/{webhook_details_table}/g, dataTableForConfiguration)
                                                                .replace(/{webhook_details_header}/g, Resource.webhook_details_header)
                                                                .replace(/{token}/g, token)
                                                                .replace(/{regenerate_token}/g, Resource.regenerate_token);

        return webhookDetailsHtml;
    } catch(error) {
        console.log("Error in getting Auth Token --> ", error.statusText);
        let webhookDetailsHtml = this.templates.webhookDetailsHtml.replace(/{webhook_details_table}/g, self.templates.noDataFoundHtml.replace(/{no_data_text}/g, error.statusText))
                                                                .replace(/{webhook_details_header}/g, Resource.webhook_details_header)
                                                                .replace(/{token}/g, tokenData)
                                                                .replace(/{regenerate_token}/g, Resource.regenerate_token);
        return webhookDetailsHtml;
    }
};

MadaraConstructor.prototype.getTokenData = function() {
    let url = this.getWindowLocationOrigin() + this.API.getTokenData;
    return new Promise((resolve, reject) => {
        let additionalAjaxOptions = {
            type    :   "POST",
            success : function(response) {  
                resolve(response);                      // Resolving the promise on success
            }, 
            error   : function(errorResponse) {
                reject(errorResponse);                  //Rejecting the promise on error
            }
        };
        this.makeAjaxRequest(url, {}, additionalAjaxOptions);
    });
};

MadaraConstructor.prototype.updateWebhookDataTableWithThisStrategy = async function() {
    let currentTarget = this.getCurrentTarget();
    let val = currentTarget.val();
    let updatedWebhookDetailsHtml = await this.getWebhookDetailsHTML(this.webhookData, val);
    let webhookDetailsContainer = $(this.DOM_SELECTORS.rhs_container).find("#webhook-details-container");
    webhookDetailsContainer.replaceWith(updatedWebhookDetailsHtml);
};

MadaraConstructor.prototype.updateWebhookDataTableWithThisToken = async function(tokenResponse) {
    let val = this.currentStrategy;
    this.tokenData = tokenResponse;
    let updatedWebhookDetailsHtml = await this.getWebhookDetailsHTML(this.webhookData, val);
    let webhookDetailsContainer = $(this.DOM_SELECTORS.rhs_container).find("#webhook-details-container");
    webhookDetailsContainer.replaceWith(updatedWebhookDetailsHtml);
};

MadaraConstructor.prototype.regenerateAuthToken = function() {
    let self = this;
    let url = this.getWindowLocationOrigin() + this.API.generateAuthToken;
    let currentTarget = this.EVENT_AND_DOM_CACHE.currentTarget;
    this.addLoaderInThisButton(currentTarget);
    let additionalAjaxOptions = {
        type    :   "POST",
        success :   function(successResp) {
            // let tokenData = successResp.message ? successResp.message : "";
            // $(self.DOM_SELECTORS.rhs_container).find("#auth-token").text(tokenData);
            self.updateWebhookDataTableWithThisToken(successResp);
            self.updateBanner({ type : "success", content : Resource.token_regenerated });
        },
        error   :   function(errorResp) {
            let errorContent = (JSON.parse(errorResp.responseText).message) ? self.checkAndGetResponseMessageFromResourceObject(JSON.parse(errorResp.responseText).message) : errorResp.statusText;
            self.updateBanner({ type : "failure", content : errorContent });
        }
    }
    this.makeAjaxRequest(url, {}, additionalAjaxOptions);
};

MadaraConstructor.prototype.updateTheManualOrderContainerForThisIndex = function(data) {
    let indexName = data.index_name;
    let actionContainerWithThisIndex = $(this.DOM_SELECTORS.rhs_container).find("#buy-manualOrders[index='" + indexName + "']");
    let rowOfTheRequiredCell = actionContainerWithThisIndex.parents(".tblRow");
    let allCellsInRow = rowOfTheRequiredCell.children();
    let whiteListedProperties = this.whiteListedProperties.getManualDetails;
    for(let i = 0; i < allCellsInRow.length; i++) {
        let element = allCellsInRow[i];
        let valueFromResponse = data[whiteListedProperties[i]];
        let valueToBeUpdated = Resource[valueFromResponse] ? Resource[valueFromResponse] : valueFromResponse;
        if(element.classList.contains("actions-table-cell")) {
            continue;
        }
        element.innerText = valueToBeUpdated ? valueToBeUpdated : "-";
        element.setAttribute("title", valueToBeUpdated ? valueToBeUpdated : "-");
    };
};

MadaraConstructor.prototype.getManualOrderDetails = function() {
    let currentTarget = this.getCurrentTarget();
    let rowOfTheClickedButton = currentTarget.parents(".tblRow");
    let allCellsInRow = rowOfTheClickedButton.children();
    let payload = {};
    let whiteListedProperties = this.whiteListedProperties.getManualDetails;
    for(let i = 0; i < allCellsInRow.length; i++) {
        let element = allCellsInRow[i];
        let valueOfTheElement = "";
        if(whiteListedProperties[i] === "index_name") {
            valueOfTheElement = currentTarget.attr("index");
        } else {
            valueOfTheElement = element.textContent.trim();
        }
        if(element.classList.contains("actions-table-cell") || (whiteListedProperties[i] === "current_premium")) {
            continue;
        }
        payload[whiteListedProperties[i]] = valueOfTheElement;
    };
    return payload;
};

MadaraConstructor.prototype.buyManualOrders = function() {
    let self = this;
    let currentTarget = this.EVENT_AND_DOM_CACHE.currentTarget;
    this.addLoaderInThisButton(currentTarget);
    let data = this.getManualOrderDetails();
    let url = this.getWindowLocationOrigin() + this.API.placeManualOrder;
    if(self.currentStrategy !== this.default_strategy) {
        url = this.getWindowLocationOrigin() + this.API.placeOrderViaWebhook + "?token=" + this.tokenData.message;
        data.strategy = self.currentStrategy;
    }

    let additionalAjaxOptions = {
        type    :   "POST",
        success :   function(successResp) {
            self.removeLoaderInThisButton(currentTarget);
            self.updateBanner({ type : "success", content : self.checkAndGetResponseMessageFromResourceObject(successResp.message) });
        },
        error   :   function(errorResp) {
            self.removeLoaderInThisButton(currentTarget);
            let errorContent = (JSON.parse(errorResp.responseText).message) ? self.checkAndGetResponseMessageFromResourceObject(JSON.parse(errorResp.responseText).message) : errorResp.statusText;
            self.updateBanner({ type : "failure", content : errorContent });
        }
    }
    this.makeAjaxRequest(url, data, additionalAjaxOptions);
};

MadaraConstructor.prototype.sellManualOrders = function() {
    let self = this;
    let currentTarget = this.EVENT_AND_DOM_CACHE.currentTarget;
    this.addLoaderInThisButton(currentTarget);
    let data = this.getManualOrderDetails();
    let url = this.getWindowLocationOrigin() + this.API.sellManualOrder;
    if(self.currentStrategy !== this.default_strategy) {
        url = this.getWindowLocationOrigin() + this.API.sellOrderViaWebhook + "?token=" + this.tokenData.message;
        data.strategy = self.currentStrategy;
    }

    let additionalAjaxOptions = {
        type    :   "POST",
        success :   function(successResp) {
            self.removeLoaderInThisButton(currentTarget);
            self.updateBanner({ type : "success", content : self.checkAndGetResponseMessageFromResourceObject(successResp.message) });
        },
        error   :   function(errorResp) {
            self.removeLoaderInThisButton(currentTarget);
            let errorContent = (JSON.parse(errorResp.responseText).message) ? self.checkAndGetResponseMessageFromResourceObject(JSON.parse(errorResp.responseText).message) : errorResp.statusText;
            self.updateBanner({ type : "failure", content : errorContent });
        }
    }
    this.makeAjaxRequest(url, data, additionalAjaxOptions);
};

MadaraConstructor.prototype.exitManualOrders = function() {
    let self = this;
    let currentTarget = this.EVENT_AND_DOM_CACHE.currentTarget;
    this.addLoaderInThisButton(currentTarget);
    let data = this.getManualOrderDetails();
    let url = this.getWindowLocationOrigin() + this.API.exitManualOrder;
    if(self.currentStrategy !== this.default_strategy) {
        url = this.getWindowLocationOrigin() + this.API.exitOrderViaWebhook + "?token=" + this.tokenData.message;
        data.strategy = self.currentStrategy;
    }

    let additionalAjaxOptions = {
        type    :   "POST",
        success :   function(successResp) {
            self.removeLoaderInThisButton(currentTarget);
            self.updateBanner({ type : "success", content : self.checkAndGetResponseMessageFromResourceObject(successResp.message) });
        },
        error   :   function(errorResp) {
            self.removeLoaderInThisButton(currentTarget);
            let errorContent = (JSON.parse(errorResp.responseText).message) ? self.checkAndGetResponseMessageFromResourceObject(JSON.parse(errorResp.responseText).message) : errorResp.statusText;
            self.updateBanner({ type : "failure", content : errorContent });
        }
    }
    this.makeAjaxRequest(url, data, additionalAjaxOptions);
};

MadaraConstructor.prototype.editManualOrders = function() {
    let self = this;
    let currentTarget = this.EVENT_AND_DOM_CACHE.currentTarget;
    let data = {
        index_name : currentTarget.attr("index")
    };
    this.addLoaderInThisButton(currentTarget);
    let url = this.getWindowLocationOrigin() + this.API.getManualDetails;
    let additionalAjaxOptions = {
        type    :   "GET",
        success :   function(successResp) {
            self.removeLoaderInThisButton(currentTarget);
            self.populateFormForEditingIndexConfiguration(successResp.message[0], { isFromManualOrders : true });
        },
        error   :   function(errorResp) {
            self.removeLoaderInThisButton(currentTarget);
            self.updateBanner({ type : "failure", content : self.checkAndGetResponseMessageFromResourceObject(JSON.parse(errorResp.responseText).message) });
        }
    }
    this.makeAjaxRequest(url, data, additionalAjaxOptions);
};

MadaraConstructor.prototype.updateManualOrders = function() {
    let inputData = this.validateAndGetInputs();
    if(inputData) {
        let self = this;
        let currentTarget = this.EVENT_AND_DOM_CACHE.currentTarget;
        this.addLoaderInThisButton(currentTarget);
        let data = inputData;
        let url = this.getWindowLocationOrigin() + this.API.updateManualDetails;
        let additionalAjaxOptions = {
            type    :   "PUT",
            success :   function(successResp) {
                self.removeLoaderInThisButton(currentTarget);
                self.closeEditForm("#index-edit-configuration-form");
                self.updateBanner({ type : "success", content : self.checkAndGetResponseMessageFromResourceObject(successResp.message) });
                self.updateTheManualOrderContainerForThisIndex(successResp.data);
            },
            error   :   function(errorResp) {
                self.removeLoaderInThisButton(currentTarget);
                let errorContent = (JSON.parse(errorResp.responseText).message) ? self.checkAndGetResponseMessageFromResourceObject(JSON.parse(errorResp.responseText).message) : errorResp.statusText;
                self.updateBanner({ type : "failure", content : errorContent });
            }
        }
        this.makeAjaxRequest(url, data, additionalAjaxOptions);
    }
};

MadaraConstructor.prototype.copyTheContentOfTheWebhookDetails = function() {
    let self = this;
    let target = this.EVENT_AND_DOM_CACHE.event.target;
    let canBeCopied = target.classList.contains("can-be-copied");
    if(canBeCopied) {
        const text = $(target).text();
        const tempTextarea = $('<textarea>');
        $(this.DOM_SELECTORS.rhs_container).append(tempTextarea);
        tempTextarea.val(text).select();
        const successful = document.execCommand('copy');
        tempTextarea.remove();
        if (successful) {
            self.updateBanner({ type : "success", content : Resource.copy_success });

            //Highlight the copied text
            target.classList.add("highlight");
            setTimeout(() => {
                target.classList.remove("highlight");
                selection.removeAllRanges(); //Clear existing selections
            }, 500);
            const selection = window.getSelection();
            const range = document.createRange();
            range.selectNodeContents(target);
            selection.removeAllRanges(); //Clear existing selections
            selection.addRange(range);
        } else {
            self.updateBanner({ type : "failure", content : Resource.copy_failed });
        }
    }
};

MadaraConstructor.prototype.getChartHTML = function() {
    let chartHtml = `<div class="flex-col gap10 flexG">
                        <div id="pnl-chart" class="pnl-chart flex-col p10 flexG">
                            <canvas id="pnlChart"></canvas>
                        </div>
                        <div id="pnlInfo" class="flexM line24"></div>
                    </div>`;
    return chartHtml;
};

MadaraConstructor.prototype.renderChartForPNL = function(currentDaySummary) {
    // Filter out invalid entries
    const validPositions = currentDaySummary.filter(pos =>
        typeof pos.total_profit === "number" && !isNaN(pos.total_profit)
    );

    //Use Month labels or fallback to strategy names
    const labels = validPositions.map((pos, index) => pos.month || pos.strategy || `Item ${index + 1}`);
    const data = validPositions.map(pos => pos.total_profit || 0);
    const backgroundColors = data.map(value => value >= 0 ? '#4CAF50' : '#F44336');

    const canvas = document.getElementById('pnlChart');
    const ctx = canvas.getContext('2d');

    // Destroy previous chart
    if(canvas.chartInstance) {
        canvas.chartInstance.destroy();
    }

    // Create Bar Chart
    try {
        canvas.chartInstance = new Chart(ctx, {
            type    : 'bar',
            data    : {
                labels  : labels,
                datasets            : [{
                    label           : Resource.monthly_pandl,
                    data            : data,
                    backgroundColor : backgroundColors,
                    barPercentage   : 0.3,
                }]
            },
            options : {
                indexAxis           : 'y',
                responsive          : true,
                maintainAspectRatio : false,
                plugins : {
                    legend  : {
                        display : true,
                        labels  : {
                            generateLabels  : () => [
                                {
                                    text        : Resource.negative_liquidity,
                                    fillStyle   : '#F44336',
                                    fontColor   : '#FFFFFF'
                                },
                                {
                                    text        : Resource.positive_liquidity,
                                    fillStyle   : '#4CAF50',
                                    fontColor   : '#FFFFFF'
                                }
                            ],
                            fontColor   : '#FFFFFF',
                            boxWidth    : 15,
                            padding     : 15
                        }
                    }
                },
                scales  : {
                    y   : {
                        beginAtZero : true,
                        ticks   : {
                            color   : '#FFFFFF'        //Y-axis labels
                        }
                    },
                    x   : {
                        ticks   : {
                            color   : '#FFFFFF'        //X-axis labels
                        }
                    }
                }
            }
        });
    } catch(error) {
        console.log(error);
    }

    // Display overall PNL
    const totalPNL = this.calculateTotalPNL(currentDaySummary);

    let pnlInfoHtml = this.templates.pnlInfoHtml.replace(/{pnl_info_header}/g, Resource.overall_pandl)
                            .replace(/{class_for_total_pnl}/g, (totalPNL > 0) ? "positive" : ((totalPNL == 0) ? "neutral" : "negative"))
                            .replace(/{total_pnl_cost_in_rupees}/g, "₹" + totalPNL.toLocaleString('en-IN', { minimumFractionDigits : 2, maximumFractionDigits : 2 }));

    document.getElementById("pnlInfo").innerHTML = pnlInfoHtml;
}

MadaraConstructor.prototype.calculateTotalPNL = function(currentDaySummary) {
    let totalPNL = 0;
    for (let i = 0; i < currentDaySummary.length; i++) {
        let profit = currentDaySummary[i].total_profit;

        //Ensure total_profit is a valid number before adding
        if (typeof profit === "number" && !isNaN(profit)) {
            totalPNL += profit;
        }
    }

    return totalPNL;
}
MadaraConstructor.prototype.getPositionsAndOrdersHTML = function(currentDaySummary, need) {
    let positionsHtml = "";
    let self = this;
    if(!currentDaySummary.length) {
        positionsHtml = this.templates.noDataFoundHtml.replace(/{no_data_text}/g, (need === "needOpenOrders") ? Resource.no_open_orders : Resource.no_live_positions);
        return positionsHtml;
    }

    let headerPropeties = ["strategy_header", "profit_header"];
    if(need === "needOrders") {
        headerPropeties = ["strategy_header", "order_count_header"];
    } else if(need === "needPositions"){
        headerPropeties = ["strategy_header", "profit_header"];
    } else if(need === "needOpenOrders") {
        return this.templates.noDataFoundHtml.replace(/{no_data_text}/g, Resource.no_open_orders);
    }

    let tableHeadCell = "";
    headerPropeties.forEach((property, index) => {
        tableHeadCell +=  self.templates.tableCell.replace(/{table_cell_content}/g, Resource[property])
                                                    .replace(/{tooltip_content}/g, Resource[property])
                                                    .replace(/{disable_status}/, "");
    });
    let tableHeadRow = self.templates.tableRow.replace(/{table_row_contents}/g, tableHeadCell);
    let eachConfigurationRow = "";
    currentDaySummary.forEach((position, index) => {
        let indexName = position.index_name;
        indexName = indexName.toUpperCase();
        let orderCount = position.order_count;
        let totalProfit = position.total_profit;
        totalProfit = parseFloat(totalProfit);
        totalProfitInLocale = totalProfit ? totalProfit.toLocaleString('en-IN', { minimumFractionDigits : 2, maximumFractionDigits : 2 }) : 0;
        let strategy = position.strategy;

        let totalProfitHtml = self.templates.htmlForCellContentHightlighter.replace(/{class_for_highlighting}/g, (totalProfit > 0) ? "positive" : ((totalProfit == 0) ? "neutral" : "negative"))
                                                                            .replace(/{cell_content}/g, totalProfitInLocale);
        let totalOrderHtml = self.templates.htmlForCellContentHightlighter.replace(/{class_for_highlighting}/g, (orderCount > 0) ? "positive" : ((orderCount == 0) ? "neutral" : "negative"))
                                                                            .replace(/{cell_content}/g, orderCount);
                                                                            
        let eachConfigurationCell = "";
        headerPropeties.forEach(property => {
            let tableCellContent = (property === "strategy_header") ? (strategy + " (" + indexName + ")") : (property === "profit_header" && (need === "needPositions")) ? totalProfitHtml : totalOrderHtml;
            let contentForTooltip = (property === "strategy_header") ? (strategy + " (" + indexName + ")") : (property === "profit_header" && (need === "needPositions")) ? totalProfitInLocale : orderCount;
            eachConfigurationCell += self.templates.tableCell.replace(/{table_cell_content}/g, tableCellContent ? tableCellContent : "-")
                                                                .replace(/{tooltip_content}/g, contentForTooltip ? contentForTooltip : "")
                                                                .replace(/{disable_status}/g, "");
        });
        eachConfigurationRow += self.templates.tableRow.replace(/{table_row_contents}/g, eachConfigurationCell);
    });

    let dataTable = self.templates.dataTableHtml.replace(/{module}/g, (need === "needOrders") ? "orders" : "positions")
                                                .replace(/{table_head_row}/g, tableHeadRow)
                                                .replace(/{table_body}/g, eachConfigurationRow);

    return dataTable;
};

MadaraConstructor.prototype.checkAndGetResponseMessageFromResourceObject = function(key) {
    return Resource[key] ? Resource[key] : key;
};

MadaraConstructor.prototype.startIndex = function() {
    let self = this;
    let currentTarget = this.EVENT_AND_DOM_CACHE.currentTarget;
    this.addLoaderInThisButton(currentTarget);
    let data = {
        index_name  :   currentTarget.attr("index")
    };
    let url = this.getWindowLocationOrigin() + this.API.startIndex;
    let triggerSource = currentTarget.attr("trigger-source");
    if(triggerSource === "scalper") {
        data.strategy = triggerSource;
        url = this.getWindowLocationOrigin() + this.API.startScalper;
    } 

    let additionalAjaxOptions = {
        type    :   "POST",
        success :   function(successResp) {
            self.removeLoaderInThisButton(currentTarget);
            self.updateBanner({ type : "success", content : self.checkAndGetResponseMessageFromResourceObject(successResp.message) });
        },
        error   :   function(errorResp) {
            self.removeLoaderInThisButton(currentTarget);
            let errorContent = (JSON.parse(errorResp.responseText).message) ? self.checkAndGetResponseMessageFromResourceObject(JSON.parse(errorResp.responseText).message) : errorResp.statusText;
            self.updateBanner({ type : "failure", content : errorContent });
        }
    }
    this.makeAjaxRequest(url, data, additionalAjaxOptions);
};

MadaraConstructor.prototype.stopIndex = function() {
    let self = this;
    let currentTarget = this.EVENT_AND_DOM_CACHE.currentTarget;
    this.addLoaderInThisButton(currentTarget);
    let data = {
        index_name  :   currentTarget.attr("index"),
        strategy    :   "hunter"
    };

    let triggerSource = currentTarget.attr("trigger-source");
    if(triggerSource === "scalper") {
        data.strategy = triggerSource;
    }

    let url = this.getWindowLocationOrigin() + this.API.stopIndex;
    let additionalAjaxOptions = {
        type    :   "POST",
        success :   function(successResp) {
            self.removeLoaderInThisButton(currentTarget);
            self.updateBanner({ type : "success", content : self.checkAndGetResponseMessageFromResourceObject(successResp.message) });
        },
        error   :   function(errorResp) {
            self.removeLoaderInThisButton(currentTarget);
            let errorContent = (JSON.parse(errorResp.responseText).message) ? self.checkAndGetResponseMessageFromResourceObject(JSON.parse(errorResp.responseText).message) : errorResp.statusText;
            self.updateBanner({ type : "failure", content : errorContent });
        }
    }
    this.makeAjaxRequest(url, data, additionalAjaxOptions);
};

MadaraConstructor.prototype.validateAndGetInputs = function() {
    let formInputElements = $("#form-input-elements");
    let formData = {};
    if(formInputElements.attr("index_name")) {
        formData.index_name = formInputElements.attr("index_name");
    }
    if(formInputElements.attr("broker_name")) {
        formData.broker_name = formInputElements.attr("broker_name");
    }
    let allInputElementsContainer = formInputElements.children();
    for(let i = 0; i < allInputElementsContainer.length; i++) {
        let element = formInputElements.find(allInputElementsContainer[i]);
        let property = element.attr("property");
        let isBooleanType = (typeof element.attr("boolean-input") !== "undefined") ? true : false;
        let input = element.find("input");
        let inputValue = isBooleanType ? input.prop("checked") : input.val();
        if(inputValue === "" || inputValue === "null") {
            this.updateBanner({ type : "failure", content : Resource["fill_mandatory"] });
            return;
        }
        formData[property] = inputValue;
    }
    return formData;
};

MadaraConstructor.prototype.updateBrokerDetails = function() {
    let inputData = this.validateAndGetInputs();
    if(inputData) {
        let self = this;
        let currentTarget = this.EVENT_AND_DOM_CACHE.currentTarget;
        this.addLoaderInThisButton(currentTarget);
        let data = inputData;
        let url = this.getWindowLocationOrigin() + this.API.editBrokerDetails;
        let additionalAjaxOptions = {
            type    :   "PUT",
            success :   function(successResp) {
                self.removeLoaderInThisButton(currentTarget);
                self.closeEditForm("#index-edit-configuration-form");
                self.updateBanner({ type : "success", content : self.checkAndGetResponseMessageFromResourceObject(successResp.message) });
                self.viewBrokerInfo();
            },
            error   :   function(errorResp) {
                self.removeLoaderInThisButton(currentTarget);
                let errorContent = (JSON.parse(errorResp.responseText).message) ? self.checkAndGetResponseMessageFromResourceObject(JSON.parse(errorResp.responseText).message) : errorResp.statusText;
                self.updateBanner({ type : "failure", content : errorContent });
            }
        }
        this.makeAjaxRequest(url, data, additionalAjaxOptions);
    }
};

MadaraConstructor.prototype.updateConfigurations = function() {
    let inputData = this.validateAndGetInputs();
    if(inputData) {
        let self = this;
        let currentTarget = this.EVENT_AND_DOM_CACHE.currentTarget;
        this.addLoaderInThisButton(currentTarget);
        let data = inputData;
        let url = this.getWindowLocationOrigin() + this.API.updateConfigValues;
        let additionalAjaxOptions = {
            type    :   "PUT",
            success :   function(successResp) {
                self.removeLoaderInThisButton(currentTarget);
                self.closeEditForm("#index-edit-configuration-form");
                self.updateBanner({ type : "success", content : self.checkAndGetResponseMessageFromResourceObject(successResp.message) });
                self.viewConfigurations();
            },
            error   :   function(errorResp) {
                self.removeLoaderInThisButton(currentTarget);
                let errorContent = (JSON.parse(errorResp.responseText).message) ? self.checkAndGetResponseMessageFromResourceObject(JSON.parse(errorResp.responseText).message) : errorResp.statusText;
                self.updateBanner({ type : "failure", content : errorContent });
            }
        }
        this.makeAjaxRequest(url, data, additionalAjaxOptions);
    }
};

MadaraConstructor.prototype.updateScalperDetails = function() {
    let inputData = this.validateAndGetInputs();
    if(inputData) {
        let self = this;
        let currentTarget = this.EVENT_AND_DOM_CACHE.currentTarget;
        this.addLoaderInThisButton(currentTarget);
        let data = inputData;
        let url = this.getWindowLocationOrigin() + this.API.updateScalperDetails;
        let additionalAjaxOptions = {
            type    :   "PUT",
            success :   function(successResp) {
                self.removeLoaderInThisButton(currentTarget);
                self.closeEditForm("#index-edit-configuration-form");
                self.updateBanner({ type : "success", content : self.checkAndGetResponseMessageFromResourceObject(successResp.message) });
                self.viewConfigurations();
            },
            error   :   function(errorResp) {
                self.removeLoaderInThisButton(currentTarget);
                let errorContent = (JSON.parse(errorResp.responseText).message) ? self.checkAndGetResponseMessageFromResourceObject(JSON.parse(errorResp.responseText).message) : errorResp.statusText;
                self.updateBanner({ type : "failure", content : errorContent });
            }
        }
        this.makeAjaxRequest(url, data, additionalAjaxOptions);
    }
};

MadaraConstructor.prototype.closeEditConfigurationForm = function() {
    this.closeEditForm("#index-edit-configuration-form");
};

MadaraConstructor.prototype.closeEditForm = function(domId) {               // Common method to close forms
    $(domId).remove();
};

MadaraConstructor.prototype.populateFormForEditingBrokerDetail = function(brokerDetails) {
    let inputHtml = "";
    let blackListedProperties = [ "token_status"];
    Object.keys(brokerDetails).forEach(property => {
        if(!blackListedProperties.includes(property)) {
            if(typeof brokerDetails[property] === "boolean") {
                inputHtml += this.templates.booleanInputHtml.replace(/{configuration_key}/g, property)
                                                            .replace(/{configuration_key_text}/g, Resource[property])
                                                            .replace(/{checked}/g, brokerDetails[property] ? "checked" : "");
            } else {
                inputHtml += this.templates.textInputHtml.replace(/{configuration_key}/g, property)
                                                        .replace(/{configuration_key_text}/g, Resource[property])
                                                        .replace(/{value}/g, brokerDetails[property]);
            }
        }
    });
    let formHtml = this.templates.formHtml.replace(/{input_elements}/g, inputHtml)
                                            .replace(/{index_configuration}/g, Resource["broker_detail"] + Resource[brokerDetails.broker_name])
                                            .replace(/{index_name}/g, brokerDetails.broker_name)
                                            .replace(/{main_key}/g, "broker_name")
                                            .replace(/{update_config}/g, Resource["update_broker"])
                                            .replace(/{purpose_of_submit}/g, "updateBrokerDetails")
                                            .replace(/{close}/g, Resource["close"]);

    $(this.DOM_SELECTORS.home_container).prepend(formHtml);
};

MadaraConstructor.prototype.populateFormForEditingIndexConfiguration = function(indexData, additionalData) {
    let inputHtml = "";
    let blackListedProperties = ["index_name", "status", "current_premium", "id", "order_id", "order_status", "time", "unique_order_id", "user_id"];            //These properties (properties from the response of respective edit request) are not needed in the form
    Object.keys(indexData).forEach(property => {
        if(!blackListedProperties.includes(property)) {
            if(typeof indexData[property] === "boolean") {
                inputHtml += this.templates.booleanInputHtml.replace(/{configuration_key}/g, property)
                                                            .replace(/{configuration_key_text}/g, Resource[property])
                                                            .replace(/{checked}/g, indexData[property] ? "checked" : "");
            } else {
                inputHtml += this.templates.textInputHtml.replace(/{configuration_key}/g, property)
                                                        .replace(/{configuration_key_text}/g, Resource[property])
                                                        .replace(/{value}/g, indexData[property]);
            }
        }
    });

    let updateConfigLabel = Resource.update_config;
    if(additionalData && additionalData.isFromScalper) {
        updateConfigLabel = Resource.update_scalper_details;
    } else if(additionalData && additionalData.isFromManualOrders) {
        updateConfigLabel = Resource.update_manual_orders;
    }

    let purposeOfSubmit = "updateConfigurations";
    if(additionalData && additionalData.isFromScalper) {
        purposeOfSubmit = "updateScalperDetails";
    } else if(additionalData && additionalData.isFromManualOrders) {
        purposeOfSubmit = "updateManualOrders";
    }

    let configText = Resource.index_configuration;
    if(additionalData && additionalData.isFromManualOrders) {
        configText = Resource.manual_order_config;
    }

    let formHtml = this.templates.formHtml.replace(/{input_elements}/g, inputHtml)
                                            .replace(/{index_configuration}/g, configText + Resource[indexData.index_name])
                                            .replace(/{index_name}/g, indexData.index_name)
                                            .replace(/{main_key}/g, "index_name")
                                            .replace(/{update_config}/g, updateConfigLabel)
                                            .replace(/{purpose_of_submit}/g, purposeOfSubmit)
                                            .replace(/{close}/g, Resource["close"]);

    $(this.DOM_SELECTORS.home_container).prepend(formHtml);
};

MadaraConstructor.prototype.editThisBrokerDetail = function() {
    let self = this;
    let currentTarget = this.EVENT_AND_DOM_CACHE.currentTarget;
    let data = {
        broker_name : currentTarget.attr("index")
    };
    this.addLoaderInThisButton(currentTarget);
    let url = this.getWindowLocationOrigin() + this.API.getBrokerDetails;
    let additionalAjaxOptions = {
        type    :   "GET",
        success :   function(successResp) {
            self.removeLoaderInThisButton(currentTarget);
            self.populateFormForEditingBrokerDetail(successResp.broker_details);
        },
        error   :   function(errorResp) {
            self.removeLoaderInThisButton(currentTarget);
            self.updateBanner({ type : "failure", content : self.checkAndGetResponseMessageFromResourceObject(JSON.parse(errorResp.responseText).message) });
        }
    }
    this.makeAjaxRequest(url, data, additionalAjaxOptions);
};

MadaraConstructor.prototype.editThisIndexConfiguration = function() {
    let self = this;
    let currentTarget = this.EVENT_AND_DOM_CACHE.currentTarget;
    let data = {
        index_name : currentTarget.attr("index")
    };
    this.addLoaderInThisButton(currentTarget);
    let url = this.getWindowLocationOrigin() + this.API.getConfigValues;
    let additionalAjaxOptions = {
        type    :   "GET",
        success :   function(successResp) {
            self.removeLoaderInThisButton(currentTarget);
            self.populateFormForEditingIndexConfiguration(successResp);
        },
        error   :   function(errorResp) {
            self.removeLoaderInThisButton(currentTarget);
            self.updateBanner({ type : "failure", content : self.checkAndGetResponseMessageFromResourceObject(JSON.parse(errorResp.responseText).message) });
        }
    }
    this.makeAjaxRequest(url, data, additionalAjaxOptions);
};

MadaraConstructor.prototype.editThisIndexScalper = function() {
    let self = this;
    let currentTarget = this.EVENT_AND_DOM_CACHE.currentTarget;
    let data = {
        index_name : currentTarget.attr("index")
    };
    this.addLoaderInThisButton(currentTarget);
    let url = this.getWindowLocationOrigin() + this.API.getScalperDetails;
    let additionalAjaxOptions = {
        type    :   "GET",
        success :   function(successResp) {
            self.removeLoaderInThisButton(currentTarget);
            self.populateFormForEditingIndexConfiguration(successResp, { isFromScalper : true });
        },
        error   :   function(errorResp) {
            self.removeLoaderInThisButton(currentTarget);
            self.updateBanner({ type : "failure", content : self.checkAndGetResponseMessageFromResourceObject(JSON.parse(errorResp.responseText).message) });
        }
    }
    this.makeAjaxRequest(url, data, additionalAjaxOptions);
};

MadaraConstructor.prototype.editThisManualOrder = function() {
    let self = this;
    let currentTarget = this.EVENT_AND_DOM_CACHE.currentTarget;
    let data = {
        index_name : currentTarget.attr("index")
    };
    this.addLoaderInThisButton(currentTarget);
    let url = this.getWindowLocationOrigin() + this.API.getManualDetails;
    let additionalAjaxOptions = {
        type    :   "GET",
        success :   function(successResp) {
            self.removeLoaderInThisButton(currentTarget);
            self.populateFormForEditingIndexConfiguration(successResp, { isFromScalper : true });
        },
        error   :   function(errorResp) {
            self.removeLoaderInThisButton(currentTarget);
            self.updateBanner({ type : "failure", content : self.checkAndGetResponseMessageFromResourceObject(JSON.parse(errorResp.responseText).message) });
        }
    }
    this.makeAjaxRequest(url, data, additionalAjaxOptions);
};

MadaraConstructor.prototype.bindEvents = function() {
    this.bindClickEvent();
    this.bindKeyUpEvent();
};

MadaraConstructor.prototype.bindClickEvent = function() {
    let self = this;
    let mainContainer = $(this.DOM_SELECTORS.main_container);
    mainContainer.on("click", "[home-page-buttons]", function(event) {
        event.stopPropagation();
        event.stopImmediatePropagation();
        let purpose = mainContainer.find(event.currentTarget).attr("purpose");
        if(typeof self[purpose] === "function") {
            self.addEventAndDomCache(event);
            self[purpose]();
            self.removeEventCache();
        }
    });
};

MadaraConstructor.prototype.bindKeyUpEvent = function() {
    let self = this;
    let mainContainer = $(this.DOM_SELECTORS.main_container);
    mainContainer.on("keyup", "[home-page-buttons]", 
        self.debounce(function(event) {
            event.stopPropagation();
            event.stopImmediatePropagation();
            let purpose = mainContainer.find(event.currentTarget).attr("purpose");
            if(typeof self[purpose] === "function") {
                self.addEventAndDomCache(event);
                self[purpose]();
                self.removeEventCache();
            }
        }, "", 200)
    );
};

MadaraConstructor.prototype.getCurrentTarget = function() {
    return this.EVENT_AND_DOM_CACHE.currentTarget;
};

MadaraConstructor.prototype.debounce = function(func, scope, delay) {
    let timer;
    return function() {
        clearTimeout( timer );
        let args = arguments;
        timer = setTimeout(function(scope, args) {
            func.apply(scope, args);
        }, delay, scope, args);
    };
}

MadaraConstructor.prototype.addEventAndDomCache = function(event) {
    let self = this;
    let extendedObject = {
        purpose             :   event.currentTarget.getAttribute("purpose"),
        currentTarget       :   $(this.DOM_SELECTORS.main_container).find(event.currentTarget),
        event               :   event
    };
    this.EVENT_AND_DOM_CACHE = $.extend(extendedObject, self.EVENT_AND_DOM_CACHE);
};

MadaraConstructor.prototype.removeEventCache = function() {
    delete this.EVENT_AND_DOM_CACHE.purpose;
    delete this.EVENT_AND_DOM_CACHE.currentTarget;
    delete this.EVENT_AND_DOM_CACHE.event;
};

MadaraConstructor.prototype.logoutUser = function() {
    let self = this;
    let currentTarget = this.EVENT_AND_DOM_CACHE.currentTarget;
    this.addLoaderInThisButton(currentTarget);
    let userDetails = {
        user_id :  "123"
    };
    let url = this.API.logout;
    let additionalAjaxOptions = {
        success :   function(successResp) {
            self.removeLoaderInThisButton(currentTarget);
            window.location.href = "/";
        },
        error   :   function(errorResp) {
            self.removeLoaderInThisButton(currentTarget);
            let errorContent = (JSON.parse(errorResp.responseText).message) ? self.checkAndGetResponseMessageFromResourceObject(JSON.parse(errorResp.responseText).message) : errorResp.statusText;
            self.updateBanner({ type : "failure", content : errorContent });
        }
    }
    this.makeAjaxRequest(url, userDetails, additionalAjaxOptions);
};

MadaraConstructor.prototype.getLandingModule = function() {
    return "dashboard";
};

MadaraConstructor.prototype.populateHome = function() {
    let mainContainer = $(this.DOM_SELECTORS.main_container);
    mainContainer.append(this.getHomeHtml());
    this.bindEvents();
    mainContainer.find("#module-" + this.getLandingModule()).click();
};

document.addEventListener("DOMContentLoaded", function() {
    new MadaraConstructor().populateHome();
});

//########    AJAX REQUEST    #########
MadaraConstructor.prototype.serialize = function(data) {
    var str = [];
    for(var p in data){
        if (data.hasOwnProperty(p)) {
            str.push(encodeURIComponent(p) + "=" + encodeURIComponent(data[p]));
        }
    }
    return '?' + str.join("&");
};

MadaraConstructor.prototype.makeAjaxRequest = function(url, data, additionalAjaxOptions) {
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