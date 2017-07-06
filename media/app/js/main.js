// --------------------------------------------------------
// $ :: JQuery nonconflict reference.
// See :: http://www.tvidesign.co.uk/blog/improve-your-jquery-25-excellent-tips.aspx#tip19
// --------------------------------------------------------
this.window.$ = this.window.$jq = this.jQuery.noConflict();

(function (root, $, _, Backbone, window) {

    // ECMAScript 5 Strict Mode
    "use strict";

    // Root Application module.
    var APP = root.APP = {
        // Title.
        title: "ES-DOC Viewer",

        // Version.
        VERSION: '0.9.7.4',

        // Copyright statement.
        copyrightYear: new Date().getFullYear(),

        // Document scripts to be invoked during rendering.
        docScripts: {},

        // Document styling to be applied during rendering.
        docStylers: {},

        // Event dispatcher.
        events: _.extend({}, Backbone.Events)
    };

    // Returns URL query param value.
    // @name                URL query param name.
    // @defaultValue        URL query param default value.
    APP.getURLParam = function (name, defaultValue) {
        var result,
            results;

        results = new RegExp('[\\?&]' + name + '=([^&#]*)').exec(window.location.href);
        if (!results) {
            result = defaultValue;
        } else {
            result = (results[1] || defaultValue).toUpperCase();
        }
        if (result) {
            result = $.trim(result);
        }

        return result;
    };

    // Event handler: document(s) rendered.
    APP.events.on("documents:rendered", function () {
        $('#userFeedback').hide();
        $('body > footer').show();
    });

    // Event handler: user feedback.
    APP.events.on("viewer:feedback", function (type, text) {
        $("#userFeedback")
            .removeClass("alert-info")
            .addClass("alert-" + type);
        $("#userFeedback h3").html(text);
    });

    // Event handler: open splash page.
    $('.esdoc-logo').click(function () {
        window.open(APP.defaults.homepage);
    });

    // Event handler: open splash page.
    $('.esdoc-pdf').click(function () {
        var link;

        link = APP.defaults.pdfPage;
        link = link.replace("{id}", APP.getURLParam('id'));
        link = link.replace("{project}", APP.getURLParam('project'));
        link = link.replace("{version}", APP.getURLParam('version'));

        window.open(link);
    });

    // Event handler: open support email.
    $('.esdoc-support').click(function () {
        var subject,
            message,
            email = "mailto:{0}?subject={1}&body={2}";

        subject = "ES-DOC :: SUPPORT :: {0} (v{1}) :: support question";
        subject = subject.replace("{0}", "Viewer");
        subject = subject.replace("{1}", APP.version);

        message = "Dear ES-DOC support team,";

        email = email.replace('{0}', "es-doc-support@list.woc.noaa.gov");
        email = email.replace('{1}', subject);
        email = email.replace('{2}', message);

        window.location.href = email;
    });

}(this, this.$, this._, this.Backbone, this.window));