(function (APP, $) {

    // ECMAScript 5 Strict Mode
    "use strict";

    // Invoke api event handler.
    APP.events.on("api:invoke", function (params) {
        var url;

        // Set URL.
        url = APP.defaults.apiBaseURL + APP.constants.api.documentSearchURL;
        url += "-";
        url += params.searchType;
        delete params.searchType;

        // Invoke API.
        $.get(url, params)
            // ... success handler.
            .done(function (data) {
                setTimeout(function () {
                    APP.events.trigger("viewer:download", data);
                }, APP.constants.uiUpdateDelay);
            })

            // ... failure handler.
            .fail(function () {
                setTimeout(function () {
                    var error;

                    error = "An error occurred whilst downloading your document.";
                    error += "<br/><br/>";
                    error += "Verify that the document request parameters are correct.";
                    error += "<br/><br/>";
                    error += "If the problem persists please contact the ES-DOC support team.";
                    APP.events.trigger("viewer:feedback", 'danger', error);
                }, APP.constants.uiUpdateDelay);
            });
    });

}(this.APP, this.$));
