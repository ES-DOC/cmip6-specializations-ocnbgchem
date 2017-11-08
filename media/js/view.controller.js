// --------------------------------------------------------
// search/view._.js - Main page view.
// --------------------------------------------------------
(function (APP, STATE, _, $, Backbone) {

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

            // Topic: further info click.
            'click .topic-further-info-button': function (e) {
                APP.events.trigger("topic:display-info", $(e.target).val());
            },

            // Table: value change.
            'change #tableFilter': function (e) {
                APP.events.trigger("table:update", $(e.target).val());
            },

            // Group: value change.
            'change #subTopicGroupFilter': function (e) {
                APP.events.trigger("subTopicGroup:update", $(e.target).val());
            }
        },

        // Backbone: view initializer.
        initialize: function (p) {
            APP.events.on("project:updated", this._onProjectUpdated, this);
            APP.events.on("topic:updated", this._onTopicUpdated, this);
            APP.events.on("topic:display-info", this._displayTopicFurtherInfo, this);
            APP.events.on("table:updated", this._onTableUpdated, this);
            APP.events.on("subTopicGroup:updated", this._onSubTopicGroupUpdated, this);
        },

        // Backbone: view renderer.
        render: function () {
            var self = this;

            _.each([
                "template-header",
                "template-filters",
                "template-property-sets"
                ], function (template) {
                APP.utils.renderTemplate(template, null, this);
            }, this);
            $('#topicFurtherInfoModal').modal({
                'show': false
            });
            $('#topicFurtherInfoModal').on("show.bs.modal", function (e) {
                var $html;

                $html = APP.utils.renderTemplate("template-topic-info", null);
                $(".modal-content").replaceWith($html);
            });

            return this;
        },

        _renderTopicFurtherInfo: function (e) {
            var $html;

            $html = APP.utils.renderTemplate("template-topic-info", null);
            $(".modal-content").replaceWith($html);
        },

        _displayTopicFurtherInfo: function () {
            // $(".topic-authors").text(STATE.topic.authors.join(", ") || "--");
            // $(".topic-contributors").text(STATE.topic.contributors.join(", ") || "--");
            // $(".topic-contact").text(STATE.topic.contact || "--");

            // $(".topic-qcstatus").text(STATE.topic.qcStatus || "--");
            // $(".topic-contact").text(STATE.topic.contact || "--");
            // $(".topic-contact").text(STATE.topic.contact || "--");

            $('#topicFurtherInfoModal').modal('show');
        },

        _onProjectUpdated: function () {
            var $html;

            $html = APP.utils.renderTemplate("template-topic-filter", null);
            this.$("#topicFilter").replaceWith($html);
            this.$("#topicFilterLabel").text(STATE.config.labels.topic + ":");

            this._onTopicUpdated()
        },

        _onTopicUpdated: function () {
            var $html;

            $html = APP.utils.renderTemplate("template-table-filter", null);
            this.$("#tableFilter").replaceWith($html);

            this._onTableUpdated();
        },

        _onTableUpdated: function () {
            var $html;

            $html = APP.utils.renderTemplate("template-subtopic-group-filter", null);
            this.$("#subTopicGroupFilter").replaceWith($html);

            this._onSubTopicGroupUpdated();
        },

        _onSubTopicGroupUpdated: function () {
            var $html;

            $html = APP.utils.renderTemplate("template-property-sets", null);
            this.$("#propertySets").replaceWith($html);
        }
    });

}(
    this.APP,
    this.APP.state,
    this._,
    this.$,
    this.Backbone
));
