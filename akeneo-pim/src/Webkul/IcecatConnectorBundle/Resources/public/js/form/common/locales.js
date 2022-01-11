'use strict';
define(
    [
        'jquery',
        'underscore',
        'oro/translator',
        'icecatconnector/template/form/common/locales',
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
             * Renders locales dropdown.
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
                        this.setChannelLocales(_.pluck(scope.locales,'code'));
                        this.$el.html(
                            this.template({
                                isEditable: this.isEditable(),
                                __: __,
                                locales: this.getLocales(),
                                isMultiple: this.config.multiple,
                                label : this.config.label,
                                tooltip: this.config.tooltip,
                                availableLocales: !scope ? [] : scope.locales,
                                errors: this.getParent().getValidationErrorsForField('locale')
                            })
                        );

                        this.$('.select2.locales').select2().on('change', this.updateState.bind(this));
                        this.$('[data-toggle="tooltip"]').tooltip();
                        this.renderExtensions();

                    }.bind(this));

                return this;
            },

            /**
             * Sets specified locales into root model.
             *
             * @param {Array} locales
             */
            setChannelLocales: function (locales) {
                var data = this.getFormData();
                data.configuration.filters.structure.locales = locales;
                this.setData(data);
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
             * Sets new locales on field change.
             *
             * @param {Object} event
             */
            updateState: function (event) {
                this.setLocales(event.val);
            },

            /**
             * Sets specified locales into root model.
             *
             * @param {Array} codes
             */
            setLocales: function (codes) {
                var data = this.getFilters();
                var before = data.structure.locale;
                data.structure.locale = codes;
                this.setData(data);
                if (before !== codes) {
                    this.getRoot().trigger('locales:update:after', codes);
                }
            },
            
            /**
             * Gets locales from root model.
             *
             * @returns {Array}
             */
            getLocales: function () {
                var structure = this.getFilters().structure;

                if (_.isUndefined(structure)) {
                    return [];
                }

                return _.isUndefined(structure.locale) ? [] : structure.locale;
            },

            /**
             * Resets locales after channel has been modified then re-renders the view.
             */
            channelUpdated: function () {
                this.initializeDefaultLocales()
                    .then(function () {
                        this.render();
                    }.bind(this));
            },

            /**
             * Sets locales corresponding to the current scope (default state).
             *
             * @return {Promise}
             */
            initializeDefaultLocales: function () {
                return fetcherRegistry.getFetcher('channel')
                    .fetch(this.getCurrentScope())
                    .then(function (scope) {
                        var locales = _.pluck(scope.locales, 'code');
                        this.setLocales(locales.length > 0 ? locales[0] : '');
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
