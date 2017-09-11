(function (APP, $, _) {

    // ECMAScript 5 Strict Mode
    "use strict";


    // Commence setup when document has loaded.
    $(document).ready(function () {

        // Render main view.
        APP.view = new APP.MainView();
        APP.view.render();

        // Update DOM.
        $("body").append(APP.view.el);
        APP.log("ui initialized");

        // Fire events.
        APP.events.trigger("ui:initialized");

    });

}(this.APP, this.$, this._));
