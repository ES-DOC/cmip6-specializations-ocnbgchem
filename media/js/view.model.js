(function (root, APP, EVENTS, _) {

    // ECMAScript 5 Strict Mode
    "use strict";

    // Initialize view state.
    var STATE = root.STATE = APP.state = {
        config: null,
        project: null,
        projects: [],
        topics: null,
        topic: null,
        subTopicGroups: null,
        subTopicGroup: null,
        shortTables: null,
        shortTable: null,

        getProperties: function (subTopic) {
            return _.filter(subTopic.properties, function (i) {
                return _.contains(STATE.shortTable.identifiers, i.id);
            });
        },

        setProject: function (p) {
            STATE.project = p;
            STATE.config = APP.config[p.id];
            STATE.topics = p.topics;
            STATE.setTopic(p.topics[0]);
        },

        setTopic: function (t) {
            STATE.topic = t;
            STATE.subTopicGroups = t.subTopicGroups;
            STATE.shortTables = t.shortTables;
            STATE.setSubTopicGroup(t.subTopicGroups[0]);
            STATE.setShortTable(t.shortTables[0]);
        },

        setSubTopicGroup: function (stg) {
            STATE.subTopicGroup = stg;
        },

        setShortTable: function (st) {
            STATE.shortTable = st;
        }
    };

    EVENTS.on("project:update", function (identifier) {
        STATE.setProject(_.find(STATE.projects, function (i) {
            return i.id === identifier;
        }));
        EVENTS.trigger("project:updated");
    });

    EVENTS.on("topic:update", function (identifier) {
        STATE.setTopic(_.find(STATE.topics, function (i) {
            return i.id === identifier;
        }));
        EVENTS.trigger("topic:updated");
    });

    EVENTS.on("subTopicGroup:update", function (identifier) {
        STATE.setSubTopicGroup(_.find(STATE.subTopicGroups, function (i) {
            return i.id === identifier;
        }));
        EVENTS.trigger("subTopicGroup:updated");
    });

    EVENTS.on("shortTable:update", function (identifier) {
        STATE.setShortTable(_.find(STATE.shortTables, function (i) {
            return i.id === identifier;
        }));
        EVENTS.trigger("shortTable:updated");
    });

    // Register topic.
    APP.registerTopic = function (topic) {
        var p, st;

        // Set project.
        p = _.find(STATE.projects, function (i) {
            return i.id === topic.project;
        });
        if (_.isUndefined(p)) {
            p = {
                id: topic.project,
                label: topic.project.toUpperCase(),
                topic: topic,
                topics: [topic]
            };
            STATE.projects.push(p);
        } else {
            p.topics.push(topic);
        }

        // Set topic subTopicGroups.
        topic.subTopicGroups = [
            {
                id: "a",
                label: "All",
                subTopics: topic.subTopics
            }
        ];
        _.each(topic.subTopics, function (i) {
            topic.subTopicGroups.push({
                id: i.id,
                label: i.label,
                subTopics: [i]
            });
        });
        topic.subTopicGroup = topic.subTopicGroups[0];

        // Set short tables.
        st = {
            id: "default",
            label: '--',
            identifiers: []
        };
        _.each(topic.subTopics, function (i) {
            _.each(i.properties, function (j) {
                st.identifiers.push(j.id);
            });
        });
        topic.shortTable = st;
        topic.shortTables = [st].concat(topic.shortTables);

        // Set global state.
        if (_.isNull(STATE.project)) {
            STATE.setProject(p);
        }
    };

}(
    this,
    this.APP,
    this.APP.events,
    this._
));
