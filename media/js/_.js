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
        TITLE: "ES-DOC Specializations Viewer",

        // Version.
        NAME: 'Specializations Viewer',

        // Version.
        VERSION: '0.9.8.1',

        // Copyright statement.
        copyrightYear: new Date().getFullYear(),

        // Event dispatcher.
        events: _.extend({}, Backbone.Events),

        // Registered specializations.
        SPECIALIZATIONS: []
    };

}(this, this.$, this._, this.Backbone, this.window));