(function (APP, $, _) {

    // ECMAScript 5 Strict Mode
    "use strict";

    // Initialise state from URL parameters.
    $(document).ready(function () {
        var target, targets, project, topic;

        target = APP.utils.getURLParam('target');
        if (_.isUndefined(target)) {
            APP.state.setProject(APP.state.projects[0]);
            return;
        }
        targets = target.split('.');

        if (targets.length >= 1 || targets.length <= 2) {
            project = _.find(APP.state.projects, function (i) {
                return i.id === targets[0];
            });
        }
        project = project || APP.state.projects[0];

        if (targets.length === 2) {
            topic = _.find(project.topics, function (i) {
                return i.id === targets.join('.');
            });
        }
        topic = topic || project.topics[0];

        // Initialise state.
        APP.state.setProject(project);
        APP.state.setTopic(topic);
    });

    // Commence setup when document has loaded.
    $(document).ready(function () {
        // Render view.
        APP.view = new APP.MainView();
        APP.view.render();

        // Update DOM.
        $("body").append(APP.view.el);
        APP.log("ui initialized");

        // Fire events.
        APP.events.trigger("ui:initialized");

    });

}(this.APP, this.$, this._));
