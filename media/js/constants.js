(function(APP) {

    // ECMAScript 5 Strict Mode
    "use strict";

    // Declare constants used within plugin.
    APP.constants = {
        URLS: {
            // ES-DOC homepage.
            HOME_PAGE: "https://es-doc.org",
        },

        // Set of email related constants.
        EMAIL: {
            // Contact email.
            CONTACT: "cmip6-help@es-doc.org",

            // Support email.
            SUPPORT: "cmip6-help@es-doc.org",

            // Default email subject.
            SUBJECT: 'ES-DOC SPECIALIZATIONS :: subject goes here',

            // Default email message.
            MESSAGE: "Dear ES-DOC SPECIALIZATIONS support team,"
        },

        // Logging related.
        logging: {
            PREFIX: "ES-DOC-SPECIALIZATIONS :: "
        }
    };

    // Configurable information related to supported projects.
    APP.config = {
        cmip5: {
            labels: {
                topic: "Component",
                subTopic: "Sub-Component"
            }
        },
        cmip6: {
            labels: {
                topic: "Realm",
                subTopic: "Process"
            }
        }
    };

}(
    this.APP
));
