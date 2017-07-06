(function (APP) {
    // ECMAScript 5 Strict Mode
    "use strict";

    // Declare constants used within plugin.
    APP.constants = {
        // Application constants.
        app: {
            // Returns title.
            getTitle: function () {
                return APP.NAME;
            },

            // Returns version.
            getVersion: function () {
                var result;
                result = ' (v';
                result += APP.VERSION;
                result += ')';
                return result;
            },

            // Returns caption.
            getCaption: function (includeVersion) {
                var caption;
                caption = APP.NAME;
                caption += ' - ';
                caption += APP.options.activePlugin;
                if (includeVersion) {
                    caption += ' (v';
                    caption += APP.VERSION;
                    caption += ')';
                }
                return caption;
            }
        },

        // Set of api related constants.
        api: {
            // Base url in various modes.
            baseURL: {
                dev: "http://localhost:5000",
                prod: "https://api.es-doc.org",
                test: "https://test-api.es-doc.org"
            },

            // URL to download setup data.
            setupURL: "/2/summary/search/setup",

            // URL to download search data.
            searchURL: "/2/summary/search",

            // URL to download search data.
            documentSearchURL: "/2/document/search",

            // URL to download document as PDF.
            pdfURL: "/2/document/retrieve?encoding=pdf&document_id={id}&document_version={version}"
        },

        // Set of email related constants.
        email: {
            // Contact email.
            contact: "es-doc-contact@list.woc.noaa.gov",

            // Support email.
            support: "es-doc-support@list.woc.noaa.gov",

            // Default email subject.
            defaultSubject: 'ES-DOC :: subject goes here',

            // Default email message.
            defaultMessage: "Dear ES-DOC support team,"
        },

        // ES-DOC homepage.
        homepage: {
            dev: "../esdoc-web-splash/index.html",
            prod: "https://es-doc.org",
            test: "https://test-es-doc.org"
        },

        // Set of document types that can be downloaded to PDF.
        // pdfDownloadableDocumentTypes: [
        //     'cim-2-designing-numericalexperiment'
        // ],
        pdfDownloadableDocumentTypes: [],

        // Text to display in lieu of null value.
        NULL_FIELD: '--',

        // Delay in milliseconds before UI updates are performed so as to avoid ugly flickering.
        uiUpdateDelay: 1000
    };

}(this.APP));
