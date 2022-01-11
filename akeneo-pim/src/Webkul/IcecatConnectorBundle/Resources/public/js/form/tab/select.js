'use strict';

define(
    [
        'jquery',
        'underscore',
        'pim/product/add-select/attribute',
        'pim/formatter/choices/base',
        'pim/common/add-select/line',
        'pim/fetcher-registry',
    ],
    function (
        $,
        _,
        AddAttributeSelect,
        ChoicesFormatter,
        LineView,
        FetcherRegistry
    ) {
        return AddAttributeSelect.extend({
            className: 'AknButtonList-item add-attribute',
            lineView: LineView,
            defaultConfig: {
                select2: {
                    placeholder: 'webkul_enrich.form.mapping.extra_mapping.attribute.btn.add_attributes',
                    title: 'pim_enrich.form.common.tab.attributes.info.search_attributes',
                    buttonTitle: 'webkul_enrich.form.mapping.extra_mapping.attribute.btn.add',
                    countTitle: 'webkul_enrich.form.mapping.extra_mapping.attribute.info.attributes_selected',
                    emptyText: 'pim_enrich.form.common.tab.attributes.info.no_available_attributes',
                    classes: 'pim-add-attributes-multiselect',
                    minimumInputLength: 0,
                    dropdownCssClass: 'add-attribute',
                    closeOnSelect: false
                },
                resultsPerPage: 10,
                searchParameters: {
                    attributes:{},
                    options: {exclude_unique: true}
                    },
                mainFetcher: 'icecatconnector-get-icecat-attribute',
                events: {
                    disable: null,
                    enable: null,
                    add: 'add-attribute:add'
                }
            },

            /**
             * Render this extension
             *
             * @return {Object}
             */
            render: function () {
                if (!this.hasRightToAdd()) {
                    return this;
                }

                return AddAttributeSelect.prototype.render.apply(this, arguments);
            },

            /**
             * {@inheritdoc}
             */
            prepareChoices: function (items) {
                return _.chain(items).map(function (item) {
                    var choice = ChoicesFormatter.formatOne(item);
                    return choice;
                }).value();
            },

            /**
             * Does the user has right to add an attribute
             *
             * @return {Boolean}
             */
            hasRightToAdd: function () {
                return this.getParent().hasRightToAdd();
            },

             /**
             * Fetches items from the backend.
             *
             * @param {Object} searchParameters
             *
             * @return {Promise}
             */
            fetchItems: function (searchParameters) {
                // var attributes = _.keys(this.getFormData().attributes);
                // searchParameters.attributes = attributes;
                return this.getItemsToExclude()
                    .then(function (identifiersToExclude) {
                        searchParameters.options.excluded_identifiers = identifiersToExclude;

                        return FetcherRegistry.getFetcher(this.mainFetcher).search(searchParameters);
                    }.bind(this));
            },
        });
    }
);

