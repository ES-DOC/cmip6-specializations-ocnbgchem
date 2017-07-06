(function (APP, $, _, window, document) {

    // ECMAScript 5 Strict Mode
    "use strict";

    // Forward declare module vars.
    var getDRSKey,
        getDRSPath,
        setters;

    // Returns a drs key to be appended to the calculated path.
    getDRSKey = function (key) {
        if (_.isUndefined(key) || _.isString(key) === false || $.trim(key).length === 0) {
            return '';
        }
        return '/' + $.trim(key);
    };

    // Returns full DRS path.
    getDRSPath = function () {
        var path, i;

        path = getDRSKey(APP.getURLParam('project'));
        for (i = 0; i < 7; i++) {
            path += getDRSKey(APP.getURLParam('key0' + i));
        }

        return path;
    };

    // Supported url param setters.
    setters = {
        'DRSPATH': function (params) {
            _.extend(params, {
                searchType: 'drs',
                drsPath: getDRSPath()
            });
        },

        'ID': function (params) {
            _.extend(params, {
                id: (APP.getURLParam('id')).toLowerCase(),
                searchType: 'id',
                version: (APP.getURLParam('version') || 'latest').toLowerCase()
            });
        },

        'EXTERNALID': function (params, idType) {
            _.extend(params, {
                externalID: APP.getURLParam('id'),
                externalType: idType,
                searchType: 'externalid'
            });
        },

        'FILEID': function (params) {
            setters.EXTERNALID(params, 'file');
        },

        'SIMULATIONID': function (params) {
            setters.EXTERNALID(params, 'simulation');
        },

        'DATASETID': function (params) {
            setters.EXTERNALID(params, 'dataset');
        },

        'NAME': function (params) {
            _.extend(params, {
                institute: APP.getURLParam('institute'),
                name: APP.getURLParam('name').toUpperCase(),
                searchType: 'name',
                type: APP.getURLParam('type').toUpperCase()
            });
            if (_.isUndefined(params.institute)) {
                delete params.institute;
            };
        }
    };

    // Initialise on document ready event.
    $(document).ready(function () {
        var renderMethod, params;

        // Set render method.
        renderMethod = APP.getURLParam('renderMethod', 'ID');

        // Initialise parameters.
        params = {
            client: APP.getURLParam('client', APP.defaults.client),
            encoding: 'html',
            project: APP.getURLParam('project')
        };

        // Set render method specific parameters.
        if (_.has(setters, renderMethod)) {
            setters[renderMethod](params);
        }

        // Trigger event.
        APP.events.trigger("api:invoke", params);
    });

}(this.APP, this.$, this._, this.window, this.document));
