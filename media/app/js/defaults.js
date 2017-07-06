(function (APP, host) {
    // ECMAScript 5 Strict Mode
    "use strict";

    // Declare defaults used within plugin.
    APP.defaults = {
        client: "unknown",

        document : {
            type : 'CIM.1.MISC.DOCUMENTSET',
            version : 'latest'
        },

        // Execution mode.
        mode: 'dev'
    };

    // Set mode.
    if (host && host.indexOf('es-doc.org') >= 0) {
        if (host.indexOf('test') >= 0) {
            APP.defaults.mode = 'test';
        } else {
            APP.defaults.mode = 'prod';
        }
    }

    // Set API base url.
    APP.defaults.apiBaseURL = APP.constants.api.baseURL[APP.defaults.mode];

    // Set home page.
    APP.defaults.homepage = APP.constants.homepage[APP.defaults.mode];

    // Set PDF link url.
    APP.defaults.pdfPage = APP.defaults.apiBaseURL + APP.constants.api.pdfURL;

}(this.APP, this.window.location.host));