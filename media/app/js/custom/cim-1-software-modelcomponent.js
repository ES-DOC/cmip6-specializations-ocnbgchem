(function (APP, $) {

    // ECMAScript 5 Strict Mode
    "use strict";

    // Document type specific stylers.
    APP.docStylers["cim-1-software-modelcomponent"] = function ($ds) {
        var $components;

        $components = $ds.find(".cim-1-software-modelcomponent-components");
        $components.find("> nav").addClass("pull-left");
        $components.find("> section").addClass("pull-right");
    };

    // Document type specific script snippets.
    APP.docScripts["cim-1-software-modelcomponent"] = function ($ds) {
        var $components,
            state,
            setComponent;

        // Set DOM fragments of interest.
        $components = $ds.find(".cim-1-software-modelcomponent-components");

        // Managed state.
        state = {
            id: undefined
        };

        // Sets current component.
        setComponent = function (id) {
            // Escape if re-selecting.
            if (id === state.id) {
                return;
            }

            // Reset UI.
            if (state.id) {
                $components.find("#nav-" + state.id).removeClass("selected");
                $components.find("#" + state.id).hide();
            }

            // Update state.
            state.id = id;

            // Update UI.
            $components.find("#nav-" + state.id).addClass("selected");
            $components.find("#" + state.id).show();
        };

        // Wire component navigation events.
        $components.find("> nav a").click(function (e) {
            setComponent($(this).attr("id").slice(4));
            e.preventDefault();
        });
        $components.find("> section h3 > span").click(function () {
            setComponent($(this).attr("id").slice(11));
        });

        // Hide components.
        $components.find("> section").hide();

        // Auto-select first component.
        $components.find("> nav ul:first-child > li:first-child a").click();
    };

}(this.APP, this.$));
