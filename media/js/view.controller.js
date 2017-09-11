// --------------------------------------------------------
// search/view._.js - Main page view.
// --------------------------------------------------------
(function (APP, _, $, Backbone, window) {

    // ECMAScript 5 Strict Mode
    "use strict";

    // Main module level view.
    APP.MainView = Backbone.View.extend({
        // Backbone: view event handlers.
        events: {
            // Open email: support.
            'click button.esdoc-support': function () {
                APP.utils.openSupportEmail();
            },

            // Open page: home.
            'click img.esdoc-logo': function () {
                APP.utils.openHomepage();
            },

            // Project: value change.
            'change #projectFilter': function (e) {
                APP.events.trigger("project:update", $(e.target).val());
            },

            // Topic: value change.
            'change #topicFilter': function (e) {
                APP.events.trigger("topic:update", $(e.target).val());
            },

            // Group: value change.
            'change #subTopicGroupFilter': function (e) {
                APP.events.trigger("subTopicGroup:update", $(e.target).val());
            },

            // Short Table: value change.
            'change #shortTableFilter': function (e) {
                APP.events.trigger("shortTable:update", $(e.target).val());
            }
        },

        // Backbone: view initializer.
        initialize: function (p) {
            APP.events.on("project:updated", this._onProjectUpdated, this);
            APP.events.on("topic:updated", this._onTopicUpdated, this);
            APP.events.on("subTopicGroup:updated", this._onSubTopicGroupUpdated, this);
            APP.events.on("shortTable:updated", this._onShortTableUpdated, this);
        },

        // Backbone: view renderer.
        render: function () {
            _.each([
                "template-header",
                "template-filters",
                "template-property-sets"
                ], function (template) {
                APP.utils.renderTemplate(template, null, this);
            }, this);

            return this;
        },

        _onProjectUpdated: function () {
            var $html;

            $html = APP.utils.renderTemplate("template-topic-filter", null);
            this.$("#topicFilter").replaceWith($html);
            this.$("#topicFilterLabel").text(STATE.config.labels.topic + ":");

            $html = APP.utils.renderTemplate("template-subtopic-group-filter", null);
            this.$("#subTopicGroupFilter").replaceWith($html);
            this.$("#subTopicGroupFilterLabel").text(STATE.config.labels.subTopic + ":");

            $html = APP.utils.renderTemplate("template-short-table-filter", null);
            this.$("#shortTableFilter").replaceWith($html);

            $html = APP.utils.renderTemplate("template-property-sets", null);
            this.$("#propertySets").replaceWith($html);
        },

        _onTopicUpdated: function () {
            var $html;

            $html = APP.utils.renderTemplate("template-subtopic-group-filter", null);
            this.$("#subTopicGroupFilter").replaceWith($html);

            $html = APP.utils.renderTemplate("template-short-table-filter", null);
            this.$("#shortTableFilter").replaceWith($html);

            $html = APP.utils.renderTemplate("template-property-sets", null);
            this.$("#propertySets").replaceWith($html);
        },

        _onSubTopicGroupUpdated: function () {
            var $html;

            $html = APP.utils.renderTemplate("template-property-sets", null);
            this.$("#propertySets").replaceWith($html);
        },

        _onShortTableUpdated: function () {
            var $html;

            $html = APP.utils.renderTemplate("template-property-sets", null);
            this.$("#propertySets").replaceWith($html);
        }
    });

}(
    this.APP,
    this._,
    this.$,
    this.Backbone,
    this.window
));
