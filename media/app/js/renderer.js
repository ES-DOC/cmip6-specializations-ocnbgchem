(function (APP, $, _) {

    // ECMAScript 5 Strict Mode
    "use strict";

    // Forward declare vars.
    var initDocumentNavigation,
        initDocumentSet,
        initGroupSet,
        initGroupSetNavigation,
        styleDocumentSet,
        wireDocumentNavigation;

    // Document download event handler.
    APP.events.on("viewer:download", function (html) {
        var $html, $ds, $gs;

        // Convert API response to HTML DOM.
        $html = $(html);

        // Escape if there are no documents to display.
        $ds = $html.find('article.esdoc-document');
        if (!$ds.length) {
            APP.events.trigger("viewer:feedback",
                               'warning',
                               'Document search returned no documents.');
            return;
        }

        // Toggle PDF button accordingly.
        if (APP.getURLParam('renderMethod') === "ID") {
            if (_.find(APP.constants.pdfDownloadableDocumentTypes, function (dt) {
                return $ds.hasClass(dt);
            })) {
                // console.log("TODO: activate PDF button");
                $('.esdoc-pdf').removeClass('hidden');
            }
        }

        // Initialize document set.
        initDocumentSet($ds);

        // Initialize group set.
        $gs = $html.find('nav.esdoc-document-group-set');
        if ($gs.length) {
            initGroupSet($gs, $ds);
        }

        // Trigger application event.
        APP.events.trigger("documents:rendered");
    });

    // Initializes document navigation buttons.
    // $d       Document DOM node.
    initDocumentNavigation = function ($d) {
        var $anchors, $h2;

        // Set anchors.
        $anchors = $d.find("> header > nav > ul > li > a");
        if ($anchors.length <= 1) {
            return;
        }

        // Create buttons.
        $h2 = $d.find("> header > h2");
        $h2.append(_.map($anchors, function ($a, index) {
            var $btn;
            $a = $($a);
            $btn = $("<button class='btn btn-default pull-right'></button>");
            $btn.text($a.text());
            if (index === 0) {
                $btn.addClass("active");
            }
            $btn.attr('href', $a.attr('href'))

            return $btn;
        }).reverse());

        // Wires document navigation event handlers.
        wireDocumentNavigation($d);
    };

    // Initializes document navigation.
    // $d      Document DOM.
    // $btn    Button to be set as initially active.
    wireDocumentNavigation = function ($d) {
        var setSection, state;

        // Managed state.
        state = {
            href: undefined,
            $btn: undefined
        };

        setSection = function ($btn) {
            // Escape if re-selecting.
            if ($btn.attr('href') === state.href) {
                return;
            }

            // Reset UI.
            if (state.href) {
                $d.find(state.href).hide();
                state.$btn.removeClass('active');
            }

            // Update state.
            state.href = $btn.attr('href');
            state.$btn = $btn;

            // Update UI.
            $d.find(state.href).show();
            $btn.addClass('active');
        };

        // Wire upto section button click event.
        $d.find("> header > h2 > button").click(function (e) {
            setSection($(this));
            e.preventDefault();
        });

        // Hide all sections.
        $d.find("> section").hide();

        // Auto-display first section.
        $d.find("> header > h2 > button.active").click();
    };

    // Applies general styles to document set.
    styleDocumentSet = function ($ds) {
        var $articles,
            $footers,
            $headersPrimary,
            $headersSecondary,
            $mainSectionHeaders,
            $navs,
            $nullFields,
            $paragraphs,
            $sections,
            $tables;

        // Set DOM fragments of interest.
        $articles = $ds;
        $footers = $ds.find("> footer");
        $headersPrimary = $ds.find('h1, h2, h3, h4');
        $headersSecondary = $ds.find('h5, h6');
        $navs = $ds.find('> header > nav');
        $nullFields = $ds.find('.esdoc-null-field');
        $paragraphs = $ds.find('article p');
        $sections = $ds.find("article > section");
        $tables = $ds.find('table');

        // Hide footers.
        $footers.hide();

        // Style headers.
        $ds.find("> header h2").addClass("bg-primary");
        $ds.find("> section > header h3").addClass("bg-primary");
        $ds.find("> section > section > header h4").addClass("bg-info");
        $ds.find("> section > section > header h3").addClass("bg-primary");
        $ds.find("> section > section:not(.esdoc-nav-target) > section > header h4").addClass("bg-info");
        $ds.find("> section > section.esdoc-nav-target > section > header h4").addClass("bg-primary");
        $ds.find("> section > section > section > section > header h5").addClass("bg-info");

        // Hide default navs and set custom navs.
        $navs.hide();
        _.each($articles, function ($article) {
            initDocumentNavigation($($article));
        });

        // Remove null fields.
        $nullFields.remove();

        // Convert inline links to HTML hyperlinks.
        $ds.find(".esdoc-field-hyperlink").attr("target", "_blank");
        $ds.find(".esdoc-field-value").linkify({
            target: "_blank"
        });
        $paragraphs.linkify({
            target: "_blank"
        });

        // Style tables.
        $tables.addClass("table table-hover table-condensed bg-esdoc");
        $tables.find("tr td.esdoc-field-name").addClass("col-md-3");
        $tables.find("tr td.esdoc-field-subname").addClass("col-md-1");
    };

    // Initializes document set DOM.
    // $ds      Document set DOM.
    initDocumentSet = function ($ds) {
        // Apply general styling.
        styleDocumentSet($ds);

        // Apply document specific styling.
        _.each(_.keys(APP.docStylers), function (docType) {
            var $dsDocType = $ds.filter('.' + docType);
            if ($dsDocType.length) {
                APP.docStylers[docType]($dsDocType);
            }
        });

        // Invoke document specific scripts.
        _.each(_.keys(APP.docScripts), function (docType) {
            var $dsDocType = $ds.filter('.' + docType);
            if ($dsDocType.length) {
                APP.docScripts[docType]($dsDocType);
            }
        });

        // Inject into page.
        $('#documentSet').append($ds);
    };

    // Initializes group set DOM.
    // $gs      Group set DOM.
    initGroupSet = function ($gs, $ds) {
        var $gsDropdowns;

        // Set bootstrap nav.
        $gs.find("> ul").addClass("nav nav-pills");

        // Set multi-document group dropdowns.
        $gsDropdowns = $gs.find("li.esdoc-document-group-multi");
        $gsDropdowns.addClass("dropdown");
        $gsDropdowns.find("> a")
            .append("<span class='caret'></span>")
            .addClass("dropdown-toggle")
            .attr("data-toggle", "dropdown");
        $gsDropdowns.find("> ul")
            .addClass("dropdown-menu");

        // Initialise group set navigation.
        initGroupSetNavigation($gs, $ds);

        // Inject into page.
        $('#groupSet').append($gs);
        $('#groupSet').removeClass('hidden');
    };

    // Initializes group set navigation.
    // $gs      Group set DOM.
    initGroupSetNavigation = function ($gs, $ds) {
        var setDocument, state;

        // Managed state.
        state = {
            $nav: undefined,
            id: undefined
        };

        setDocument = function ($nav) {
            var id;

            // Escape if re-selecting.
            if ($nav === state.$nav) {
                return;
            }

            // Reset UI.
            if (state.id) {
                $('#' + state.id).hide();
                state.$nav.parent().removeClass("active");
                state.$nav.parents('.esdoc-document-group-multi').removeClass("active");
            }

            // Update state.
            state.$nav = $nav;
            state.id = $nav.attr("href").slice(1);

            // Update UI.
            $('#' + state.id).show();
            state.$nav.parent().addClass("active");
            state.$nav.parents('.esdoc-document-group-multi').addClass("active");
        };

        // Wire upto document click event.
        $gs.find(".esdoc-document-nav").click(function (e) {
            setDocument($(this));
            e.preventDefault();
        });

        // Auto-display first document.
        $ds.hide();
        $gs.find(".esdoc-document-nav.first").click();
    };

}(this.APP, this.$, this._));
