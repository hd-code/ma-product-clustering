'use strict';
define(
    [
        'jquery',
        'underscore',
        'oro/translator',
        'icecatconnector/template/form/common/currencies',
        'pim/form',
        'pim/fetcher-registry',
        'jquery.select2'
    ],
    function (
        $,
        _,
        __,
        template,
        BaseForm,
        fetcherRegistry
    ) {
        return BaseForm.extend({
            className: 'AknFieldContainer',
            template: _.template(template),

            /**
             * Initializes configuration.
             *
             * @param {Object} config
             */
            initialize: function (config) {
                this.config = config.config;

                return BaseForm.prototype.initialize.apply(this, arguments);
            },

            /**
             * Configures this extension.
             *
             * @return {Promise}
             */
            configure: function () {
                this.listenTo(this.getRoot(), 'channel:update:after', this.channelUpdated.bind(this));

                return BaseForm.prototype.configure.apply(this, arguments);
            },
            /**
             * Renders currencies dropdown.
             *
             * @returns {Object}
             */
            render: function () {
                if (!this.configured) {
                    return this;
                }
                
                fetcherRegistry.getFetcher('channel')
                    .fetch(this.getFilters().structure.scope)
                    .always(function (scope) {
                        var availableCurrencies = this.getCurrenciesInCodeLabel(!scope ? [] : scope.currencies);
                        this.$el.html(
                            this.template({
                                isEditable: this.isEditable(),
                                __: __,
                                currencies: this.getCurrencies(),
                                availableCurrencies: availableCurrencies,
                                errors: this.getParent().getValidationErrorsForField('currencies')
                            })
                        );

                        this.$('.select2.currencies').select2().on('change', this.updateState.bind(this));
                        this.$('[data-toggle="tooltip"]').tooltip();

                        this.renderExtensions();
                    }.bind(this));

                return this;
            },

            getCurrenciesInCodeLabel: function(currencies) {
                var result = [];
                _.each(currencies, function(currency) {
                    result.push({
                        'code': currency,
                        'label': currency,                        
                    });
                });

                return result;
            },
            /**
             * Returns whether this filter is editable.
             *
             * @returns {boolean}
             */
            isEditable: function () {
                return undefined !== this.config.readOnly ?
                    !this.config.readOnly :
                    true;
            },

            /**
             * Sets new currencies on field change.
             *
             * @param {Object} event
             */
            updateState: function (event) {
                this.setCurrencies(event.val);
            },

            /**
             * Sets specified currencies into root model.
             *
             */
            setCurrencies: function (code) {
                
                var data = this.getFilters();
                var before = data.structure.currency;

                data.structure.currency = code;
                this.setData(data);

                if (before !== code) {
                    this.getRoot().trigger('currency:update:after', code);
                }
            },

            /**
             * Gets currencies from root model.
             *
             * @returns {Array}
             */
            getCurrencies: function () {
                var structure = this.getFilters().structure;

                if (_.isUndefined(structure)) {
                    return '';
                }
                var currencies = _.isUndefined(structure.currency) ? '' : structure.currency; 
                return currencies.toString();
            },

            /**
             * Resets currencies after channel has been modified then re-renders the view.
             */
            channelUpdated: function () {
                this.initializeDefaultCurrencies()
                    .then(function () {
                        this.render();
                    }.bind(this));
            },

            /**
             * Sets currencies corresponding to the current scope (default state).
             *
             * @return {Promise}
             */
            initializeDefaultCurrencies: function () {
                return fetcherRegistry.getFetcher('channel')
                    .fetch(this.getCurrentScope())
                    .then(function (scope) {
                        if(scope.currencies.length > 0) {
                            this.setCurrencies(scope.currencies[0]);
                        } else {
                            this.setCurrencies('');
                        }
                    }.bind(this));
            },

            /**
             * Gets current scope from root model.
             *
             * @return {String}
             */
            getCurrentScope: function () {
                return this.getFilters().structure.scope;
            },

            /**
             * Get filters
             *
             * @return {object}
             */
            getFilters: function () {
                return this.getFormData().configuration.filters;
            }
        });
    }
);
