var MadaraLoginConstructor = function() {
    this.DOM_SELECTORS = {
        login_main_container    :   "#login-main-container",
        user_name               :   "#user-name",
        password                :   "#password"    
    },
    this.templates = {
        mainLoginHtml : 
                        `<div id="login-container" class="login-bg-image wh100 flex-col flexM">
                            <div class="flex-col flexM login-wrapper gap10">
                                <div id="login-header" class="font30 clrW">{login_text}</div>
                                <div id="login-inputs" class="login-inputs-container flex-col gap20">
                                    <div id="username-input">
                                        <input id="user-name" type="text" class="login-input-element w100" placeholder="{username}" autocomplete="false">
                                    </div>
                                    <div id="password-input">
                                        <input id="password" type="password" class="login-input-element w100" placeholder="{password}" autocomplete="false">
                                    </div>
                                    <div id="login-submit-button" login-page-buttons purpose="loginUser" class="login-submit-button flexM clrW curP">{submit_text}</div>
                                </div>
                            </div>
                        </div>`
    },
    this.EVENT_AND_DOM_CACHE = {},
    this.API = {
        login : "login"       //This is a random Open API. Please replace this with our API
    }
};

MadaraLoginConstructor.prototype.getResource = function(key) {
    let resourceValue = Resource[key];
    if(!resourceValue) {
        return key;
    }
    return resourceValue;
};

MadaraLoginConstructor.prototype.getLoginHtml = function() {
    return this.templates.mainLoginHtml.replace(/{submit_text}/g, this.getResource("submit"))
                                        .replace(/{login_text}/g, this.getResource("login"))
                                        .replace(/{username}/g, this.getResource("username"))
                                        .replace(/{password}/g, this.getResource("password"));
};

MadaraLoginConstructor.prototype.bindEvents = function() {
    this.bindClickEvent();
    this.bindKeyUpEvent();
};

MadaraLoginConstructor.prototype.bindClickEvent = function() {
    let self = this;
    let loginMainContainer = $(this.DOM_SELECTORS.login_main_container);
    loginMainContainer.on("click", "[login-page-buttons]", function(event) {
        event.stopImmediatePropagation();
        event.stopImmediatePropagation();
        let purpose = loginMainContainer.find(event.currentTarget).attr("purpose");
        if(typeof self[purpose] === "function") {
            self.addEventAndDomCache(event);
            self[purpose]();
            self.removeEventCache();
        }
    })
};

MadaraLoginConstructor.prototype.bindKeyUpEvent = function() {
    let self = this;
    let loginMainContainer = $(this.DOM_SELECTORS.login_main_container);
    loginMainContainer.on("keypress", function(event) {
        event.stopImmediatePropagation();
        if (event.which === 13) {                           // 13 is the Enter key
            event.preventDefault();
            let validLogin = self.ValidateAndGetCredentials();
            if(!validLogin) {
                return;
            }
            self.loginUser();    
        }
    });
};

MadaraLoginConstructor.prototype.ValidateAndGetCredentials = function() {
    let userName = $(this.DOM_SELECTORS.user_name).val();
    let password = $(this.DOM_SELECTORS.password).val();
    if(userName === "" || password === "") {
        alert("Please fill all the fields");
        return;
    }
    return {
        user_name   :   userName,
        password    :   password
    };
};

MadaraLoginConstructor.prototype.addEventAndDomCache = function(event) {
    let self = this;
    let extendedObject = {
        purpose             :   event.currentTarget.getAttribute("purpose"),
        currentTarget       :   $(this.DOM_SELECTORS.login_main_container).find(event.currentTarget),
        event               :   event
    };
    this.EVENT_AND_DOM_CACHE = $.extend(extendedObject, self.EVENT_AND_DOM_CACHE);
};

MadaraLoginConstructor.prototype.removeEventCache = function() {
    delete this.EVENT_AND_DOM_CACHE.purpose;
    delete this.EVENT_AND_DOM_CACHE.currentTarget;
    delete this.EVENT_AND_DOM_CACHE.event;
};

MadaraLoginConstructor.prototype.loginUser = function() {
    let validLogin = this.ValidateAndGetCredentials();
    if(!validLogin) {
        return;
    }
    let userDetails = validLogin;
    let url = this.API.login;
    let additionalAjaxOptions = {
        success :   function(successResp) {
            if (successResp.status === 'success'){
                window.location.href = '/home';
            }
            else if (successResp.status === 'failed'){
                alert("Login Error");
            }
        },
        error   :   function(errorResp) {
            console.log(errorResp);
        }
    }
    this.makeAjaxRequest(url, userDetails, additionalAjaxOptions,"POST")
};

MadaraLoginConstructor.prototype.populateLoginPage = function() {
    $(this.DOM_SELECTORS.login_main_container).append(this.getLoginHtml());
    this.bindEvents();
};

document.addEventListener("DOMContentLoaded", function() {
    new MadaraLoginConstructor().populateLoginPage();
});

//########    AJAX REQUEST    #########
MadaraLoginConstructor.prototype.makeAjaxRequest = function(url, data, additionalAjaxOptions,method) {
	data = data || {};
	let options = {
		contenttype : "application/json", 			//NO I18N
		url 		: url,
		data 		: data,
		headers		: { "Accept" : "*/*" }	,		//NO I18N
        type        : method
	};
	options = $.extend( {}, (additionalAjaxOptions || {}), options );
	return $.ajax(options);
};