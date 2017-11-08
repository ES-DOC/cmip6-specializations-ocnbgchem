(function (APP, CONSTANTS, _, $, console, window) {

    // ECMAScript 5 Strict Mode
    "use strict";

    // Placeholder.
    APP.utils = {};

    // Cache of loaded templates.
    var templateCache = {};

    // Outputs message to brwoser logging console.
    // @msg          Logging message.
    APP.log = APP.utils.log = function (msg) {
        console.log(new Date() + " :: " + CONSTANTS.logging.PREFIX + msg);
    };

    // Opens the target url.
    // @url     URL to be opened.
    // @inTab   Flag indicating whether url will be opened in a new browser tab or not.
    APP.utils.openURL = function (url, inTab) {
        if (inTab === true) {
            window.open(url);
        } else {
            window.location = url;
        }
    };

    // Opens the homepage.
    APP.utils.openHomepage = function () {
        APP.utils.openURL(CONSTANTS.URLS.HOME_PAGE, true);
    };

    // Opens the target email.
    // @address         Target email address.
    // @subject         Target email subject.
    APP.utils.openEmail = function (address, subject, message) {
        var email = "mailto:{0}?subject={1}&body={2}";

        subject = subject || CONSTANTS.EMAIL.SUBJECT;
        message = message || CONSTANTS.EMAIL.MESSAGE;

        email = email.replace('{0}', address);
        email = email.replace('{1}', subject);
        email = email.replace('{2}', message);

        window.location.href = email;
    };

    // Opens module support email.
    // @module         Module for which a support email is being sent.
    APP.utils.openSupportEmail = function () {
        var subject;

        subject = "ES-DOC :: SUPPORT :: {0} (v{1})";
        subject = subject.replace("{0}", APP.NAME.toUpperCase());
        subject = subject.replace("{1}", APP.VERSION);
        APP.utils.openEmail(CONSTANTS.EMAIL.SUPPORT, subject);
    };

    // Renders a view.
    // @type          View type.
    // @options       View options.
    // @container     View container.
    APP.utils.render = function (types, options, container) {
        var typeset, view, rendered = [];

        typeset = _.isArray(types) ? types : [types];
        _.each(typeset, function (ViewType) {
            view = new ViewType(options).render();
            rendered.push(view);
            if (!_.isUndefined(container)) {
                if (_.has(container, '$el')) {
                    container.$el.append(view.$el);
                } else {
                    container.append(view.$el);
                }
            }
        }, this);

        return typeset.length === 1 ? rendered[0] : rendered;
    };

    // Renders an html view and injects it into DOM.
    // @template            View template.
    // @data                View template data.
    // @container           View container.
    APP.utils.renderHTML = function (template, data, container) {
        var html = data ? template(data) : template();

        if (!_.isUndefined(container)) {
            if (_.has(container, '$el')) {
                container.$el.append(html);
            } else {
                container.append(html);
            }
        }
    };

    // Returns a rendered template.
    // @templateID          View template ID.
    // @templateData        View template data.
    // @container           View container.
    APP.utils.renderTemplate = function (templateID, templateData, view) {
        var template, html;

        if (!_.has(templateCache, templateID)) {
            templateCache[templateID] = _.template($('#' + templateID).html());
        }
        template = templateCache[templateID];
        html = template(templateData);

        if (view && view.$el) {
            view.$el.append(html);
        } else if (view) {
            view.replaceWith(html);
        } else {
            return html;
        }
    };

    // Returns URL query param value.
    // @name                URL query param name.
    // @defaultValue        URL query param default value.
    APP.utils.getURLParam = function (name, defaultValue, retainCase) {
        var
            result = new RegExp('[\\?&]' + name + '=([^&#]*)').exec(window.location.href);
        if (!result) {
            return defaultValue;
        }
        result = (result[1] || defaultValue);
        return (retainCase === true) ? result : result.toLowerCase();
    };

}(
    this.APP,
    this.APP.constants,
    this._,
    this.$,
    this.console,
    this.window
));
