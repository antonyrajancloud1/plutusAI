let MadaraConstructor = function() {
    this.DOM_SELECTORS = {
        main_container          :   "#main-container",
        login_main_container    :   "#login-main-container",
        home_container          :   "#home-container",
        lhs_container           :   "#lhs-container",
        lhs_module_container    :   "#lhs-module-container",
        rhs_container           :   "#rhs-container",
        footer_container        :   "#footer-container"
    };
    this.project_name   =   "Madara";
    this.EVENT_AND_DOM_CACHE = {};
    this.whiteListedProperties = {
        getConfigurations   : [ "actions", "index_name", "levels", "trend_check_points", "strike", "safe_sl", "stage" ],
        getOrderBook        : [ "entry_time", "script_name", "qty", "entry_price", "exit_price", "status", "exit_time" ],
        getBrokerInfo       : [ "actions", "broker_name", "broker_user_id", "broker_user_name", "broker_mpin", "broker_api_token" ]   
    };
};

MadaraConstructor.prototype.templates = {
    mainHtml : 
                `<div id="home-container" class="wh100 flex-col home-bg-container">
                    <div id="banner-container"></div>
                    <div id="header-container" class="flexC header-container p5">
                        <div class="flexG textC font30 clrD">{project_name}</div>
                        {logout}
                    </div>
                    <div id="body-container" class="flex wh100 flexG">
                        <div id="lhs-container" class="ovrflwH">
                            <div id="lhs-module-container" class="flex-col lhs-container h100 posrel ovrflwA flexG">
                                {modules_html}
                            </div>
                        </div>
                        <div id="rhs-container" class="flex wh100 flexG"></div>
                    </div>
                    <div id="footer-container" class="flex">
                    </div>
                </div>`,

    eachModuleHtml :
                    `<div id="module-{module_id}" class="font18 lhs-module flexM curP clrD" home-page-buttons purpose="view{purpose}">
                        {module}
                    </div>`,

    loaderHtml : 
                `<div id="rhs-center-loader" class="h100 w100 flexM fdirC">
                    <div class="rloader posrel"></div>
                </div>`,

    dataTableHtml : 
                    `<div id="{module}-container" class="wh100 flexG pL35 pR35 pT20 pB20 clrD">
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

    actionsHtml : `<div id="actions-container" class="flexM gap20">
                        {start_button}
                        {stop_button}
                        {edit_button}
                  </div>`,

    startButton : `<div id="start-index" purpose="startIndex" home-page-buttons index="{index}" class="action-button xs fa fa-play curP clrG start-index-button p5 bdrR4" title="{start_index_title}"></div>`,

    stopButton : `<div id="stop-index" purpose="stopIndex" home-page-buttons index="{index}" class="action-button xs fa fa-stop curP clrR stop-index-button p5 bdrR4" title="{stop_index_title}"></div>`,

    editButton : `<div id="edit-{module}" purpose="{purpose_of_edit}" home-page-buttons index="{index}" class="action-button fa xs fa-pencil curP clrB edit-config-button p5 bdrR4" title="{edit_module_title}"></div>`,

    logoutHtml : 
                `<div id="logout-button" home-page-buttons class="primary-button logout-button clrD curP flexM bdrR10 sm" purpose="logoutUser" userId>
                    {logout_text}
                </div>`,

    bannerHtml : 
                `<div id="banner-wrapper" class="{banner_type} banner-wrapper clrD dN textC">
                    <div class="font16">{banner_content}</div>
                </div>`,

    formHtml : 
                `<div id="index-edit-configuration-form" class="index-edit-configuration-form mask-bg">
                    <div id="form-main-container" class="form-main-container flex-col flexG clrD">
                        <div id="form-header" class="flexM pB15 pL15 pR15 fontB fontItalic form-header justifySB">
                            <div class="font24">{index_configuration}</div>
                            <div class="fa fa-close close-icon font14 curP" purpose="closeEditConfigurationForm" home-page-buttons title="{close}"></div>
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
                    `<div id="no-data-found-container" class="wh100 flexG pL35 pR35 pT20 pB20 clrD  flexM gap10 font24">  
                        <div class="fa fa-close clrR flex"></div>
                        <div class="fontItalic">{no_data_text}</div>
                    </div>`
};

MadaraConstructor.prototype.getWindowLocationOrigin = function() {
    return window.location.origin;
};

MadaraConstructor.prototype.API = {
    home                :   "/home",
    login               :   "/login",
    logout              :   "/logout",
    getConfigValues     :   "/get_config_values",
    updateConfigValues  :   "/update_config_values",
    addUser             :   "/add_user",
    getBrokerDetails    :   "/get_broker_details",
    addBrokerDetails    :   "/add_broker_details",
    editBrokerDetails   :   "/edit_broker_details",
    getOrderBookDetails :   "/get_order_book_details",
    startIndex          :   "/start_index",
    stopIndex           :   "/stop_index",
    getPlans            :   "/plans",
    editPlans           :   "/edit_plans"
};

MadaraConstructor.prototype.getLHSModulesList = function() {
    return [ "configurations", "orderBook", "brokerInfo", "scalper","plans", "needHelp" ];
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

MadaraConstructor.prototype.getHomeHtml = function() {
    return this.templates.mainHtml.replace(/{modules_html}/g, this.getLHSModulesHtml())
                                    .replace(/{logout}/g, this.getLogoutButton())
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
    let dateObject = new Date(time);
    return dateObject.toDateString().split(' ').slice(1).join(' ') + ", " + dateObject.toLocaleTimeString(["en-US"], { hour12 : true, hour : '2-digit', minute : '2-digit' });
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
                        let tableCellContent = property === "status" ? Resource[configurationObject[property]] : property.includes("time") ? self.getFormattedTime(configurationObject[property]) : configurationObject[property];
                        eachConfigurationCell += self.templates.tableCell.replace(/{table_cell_content}/g, tableCellContent ? tableCellContent : "-")
                                                                            .replace(/{tooltip_content}/g, tableCellContent ? tableCellContent : "")
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
                                                            .replace(/{edit_button}/g, self.getEditButton());
                                                            
                actionsHtml = actionsHtml.replace(/{index}/g, configuration)
                                        .replace(/{module}/g, "configurations")
                                        .replace(/{purpose_of_edit}/g, "editThisIndexConfiguration");

                let eachConfigurationCell = self.templates.tableCell.replace(/{table_cell_content}/g, actionsHtml)
                                                                    .replace(/{tooltip_content}/g, "")
                                                                    .replace(/{disable_status}/g, disableStatus ? "disabled actions-table-cell" : "actions-table-cell");

                eachConfigurationCell += self.templates.tableCell.replace(/{table_cell_content}/g, Resource[configuration])
                                                                    .replace(/{tooltip_content}/g, Resource[configuration])
                                                                    .replace(/{disable_status}/g, disableStatus ? "disabled" : "");

                whiteListedProperties.forEach(property => {
                    if(property !== "index_name" && property !== "actions") {
                        let tableCellContent = (property === "stage") ? Resource[configurationObject[property]] : configurationObject[property];
                        eachConfigurationCell += self.templates.tableCell.replace(/{table_cell_content}/g, tableCellContent ? tableCellContent : "-")
                                                                            .replace(/{tooltip_content}/g, tableCellContent ? tableCellContent : "")
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

MadaraConstructor.prototype.closeEditConfigurationForm = function() {
    this.closeEditForm("#index-edit-configuration-form");
};

MadaraConstructor.prototype.closeEditForm = function(domId) {               // Common method to close forms
    $(domId).remove();
};

MadaraConstructor.prototype.populateFormForEditingBrokerDetail = function(brokerDetails) {
    let inputHtml = "";
    let blackListedProperties = ["broker_name", "index_group", "token_status"];
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

MadaraConstructor.prototype.populateFormForEditingIndexConfiguration = function(indexData) {
    let inputHtml = "";
    let blackListedProperties = ["index_name","stage"];
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
    let formHtml = this.templates.formHtml.replace(/{input_elements}/g, inputHtml)
                                            .replace(/{index_configuration}/g, Resource["index_config"] + Resource[indexData.index_name])
                                            .replace(/{index_name}/g, indexData.index_name)
                                            .replace(/{main_key}/g, "index_name")
                                            .replace(/{update_config}/g, Resource["update_config"])
                                            .replace(/{purpose_of_submit}/g, "updateConfigurations")
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

MadaraConstructor.prototype.bindEvents = function() {
    this.bindClickEvent();
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
    })
};

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

MadaraConstructor.prototype.populateHome = function() {
    let mainContainer = $(this.DOM_SELECTORS.main_container);
    mainContainer.append(this.getHomeHtml());
    this.bindEvents();
    mainContainer.find("#module-configurations").click();
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
        data = JSON.stringify(data)
    }
	let options = {
		url 		: url,
		headers		: { 
            Accept          :   "*/*",
            ContentType     :   "application/json"
        }			
	};
    if(additionalAjaxOptions.type !== "GET") {
        options.data = data;
    }
	options = $.extend( {}, (additionalAjaxOptions || {}), options );
	return $.ajax(options);
};
