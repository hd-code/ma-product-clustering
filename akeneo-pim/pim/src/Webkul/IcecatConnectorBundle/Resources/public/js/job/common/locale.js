'use strict';
define([
    'jquery',
    'underscore',
    'oro/translator',
    'pim/form',
    'pim/fetcher-registry',
    'icecatconnector/template/job/common/locale',
    'jquery.select2'
],
    function (
        $,
        _,
        __,
        BaseForm,
        FetcherRegistry,
        template
    ) {
        return BaseForm.extend({
            className: 'AknFieldContainer',
            template: _.template(template),
            initialLocales: null,
            locales: null,

            /**
             * Configures this extension.
             *
             * @return {Promise}
             */
            configure: function () {
                this.listenTo(this.getRoot(), 'pim_enrich:form:entity:bad_request', this.render.bind(this));
                return BaseForm.prototype.configure.apply(this, arguments);
            },

            /**
             * {@inheritdoc}
             */
            render: function () {
                if (!this.configured) {
                    return this;
                }

                FetcherRegistry.getFetcher('locale').fetchActivated().then(function (locales) {
                    this.$el.html(this.template({
                        currentLocale: this.getFormData().configuration.fallbackLocale,
                        locales: locales,
                        label :  __('webkul_enrich.form.job_instance.tab.global.fallbacklocale.title'),
                        tooltip: __('webkul_enrich.form.job_instance.tab.global.fallbacklocale.help'),
                        requiredLabel: __('pim_enrich.form.required'),
                        errors: this.getParent().getValidationErrorsForField('locales')
                    }));

                    this.$('.select2').select2().on('change', this.updateState.bind(this));
                    this.$('[data-toggle="tooltip"]').tooltip();
                    this.renderExtensions();
                }.bind(this));

                return this;
            },

            /**
             * Sets new locales on change.
             *
             * @param {Object} event
             */
            updateState: function (event) {
                var locale = event.val;
                var data = this.getFormData();
                data.configuration.fallbackLocale = locale;
                this.setData(data);
            },
        });
    }
);
