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
        tables: [],
        table: null,
        subTopicGroups: null,
        subTopicGroup: null,

        setProject: function (p) {
            STATE.project = p;
            STATE.config = APP.config[p.id];
            STATE.topics = p.topics;
            STATE.setTopic(STATE.topics[0]);
        },

        setTopic: function (tp) {
            STATE.topic = tp;
            STATE.tables = tp.tables;
            STATE.setTable(tp.tables[0]);
        },

        setTable: function (t) {
            STATE.table = t;
            STATE.subTopicGroups = t.subTopicGroups;
            STATE.setSubTopicGroup(t.subTopicGroups[0]);
        },

        setSubTopicGroup: function (stg) {
            STATE.subTopicGroup = stg;
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

    EVENTS.on("table:update", function (identifier) {
        STATE.setTable(_.find(STATE.tables, function (i) {
            return i.id === identifier;
        }));
        EVENTS.trigger("table:updated");
    });

    EVENTS.on("subTopicGroup:update", function (identifier) {
        STATE.setSubTopicGroup(_.find(STATE.subTopicGroups, function (i) {
            return i.id === identifier;
        }));
        EVENTS.trigger("subTopicGroup:updated");
    });


    // Register topic.
    APP.registerTopic = function (topic) {
        var p, subTopics;

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

        // Exclude sub-topics without properties.
        topic.subTopics = _.filter(topic.subTopics, (i) => {
            return i.properties.length > 0;
        });

        // Set default table.
        topic.tables = [{
            id: "default",
            label: "--",
            subTopicGroups: [{
                id: "a",
                label: "All",
                subTopics: topic.subTopics
            }].concat(_.map(topic.subTopics, function (i) {
                return {
                    id: i.id,
                    label: i.label,
                    subTopics: [i]
                };
            }))
        }];

        // Set other tables.
        _.each(topic.shortTables, function (st) {
            var properties, subTopicIdentifiers, subTopics;


            // Set property identifiers.
            properties = _.pluck(st.properties, 'id');
            properties = _.filter(properties, function (id) {
                return id.toLowerCase().startsWith('cim') === false;
            });
            if (st.id === 'aerosol') {
                console.log(properties);                    
            }

            // Set sub-topics.
            subTopicIdentifiers = _.uniq(_.map(properties, function (id) {
                return id.split('.').slice(0, 3).join('.');
            }));
            if (st.id === 'aerosol') {
                console.log(subTopicIdentifiers);
            }

            subTopics = _.map(subTopicIdentifiers, function (i) {
                return _.find(topic.subTopics, function (j) {
                    return j.id === i;
                });
            });
            subTopics = _.map(subTopics, function (i) {
                return {
                    description: i.description,
                    id: i.id,
                    label: i.label,
                    properties: _.filter(i.properties, function (j) {
                        return _.contains(properties, j.id);
                    })
                };
            });

            // Set table.
            topic.tables.push({
                id: st.id,
                label: st.label,
                subTopicGroups: [{
                    id: "a",
                    label: "All",
                    subTopics: subTopics
                }].concat(_.map(subTopics, function (i) {
                    return {
                        id: i.id,
                        label: i.label,
                        subTopics: [i]
                    };
                }))
            });
        });
    };

}(
    this,
    this.APP,
    this.APP.events,
    this._
));
