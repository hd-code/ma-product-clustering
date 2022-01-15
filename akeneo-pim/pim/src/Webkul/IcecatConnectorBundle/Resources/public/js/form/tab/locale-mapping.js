'use strict';

define([
    'jquery',
    'underscore',
    'oro/translator',
    'pim/form',
    'pim/fetcher-registry',
    'icecatconnector/template/tab/locale-mapping',
    'oro/loading-mask',
],
    function (
        $,
        _,
        __,
        BaseForm,
        fetcherRegistry,
        template,
        LoadingMask,
    ) {
        return BaseForm.extend({
            events: {
                'change select.icecatLocaleMapping': 'updateModel',
            },

            label: __('webkul_icecat_connector.tab.locale_mapping.title'),
            code: 'icecat_connector_locale_mapping',
            template: _.template(template),
            availableLocales: [],
            icecateLocales: [],

            /**
             * {@inheritdoc}
             */
            configure: function () {
                this.trigger('tab:register', {
                    code: this.code,
                    label: this.label
                });

                return BaseForm.prototype.configure.apply(this, arguments);
            },

            /**
             * {@inheritdoc}
             */
            render: function () {
                var loadingMask = new LoadingMask();
                loadingMask.render().$el.appendTo(this.getRoot().$el).show();

                if (_.isEmpty(this.availableLocales)) {
                    this.availableLocales = fetcherRegistry.getFetcher('locale').fetchActivated()
                }
                if (_.isEmpty(this.icecateLocales)) {
                    this.icecateLocales = fetcherRegistry.getFetcher('icecatconnector-icecat-locale').fetchAll()
                }

                Promise.all([this.availableLocales, this.icecateLocales]).then(function (values) {
                    var availableLocales = this.sortByLabel(values[0]);
                    var icecateLocales = values[1];
                    this.$el.html(this.template({
                        availableLocales: availableLocales,
                        icecatLocales: icecateLocales,
                        icecatLocaleMapping: this.getFormData()['icecatLocaleMapping'],
                        mappedLocale: _.values(this.getFormData()['icecatLocaleMapping'])
                    }));

                    $('.select2').select2();
                    this.$('*[data-toggle="tooltip"]').tooltip();
                    loadingMask.hide().$el.remove();
                }.bind(this));

                this.delegateEvents();

                return BaseForm.prototype.render.apply(this, arguments);
            },

            /**
             * Update model after value change
             *
             * @param {Event} event
             */
            updateModel: function (event) {
                const name = event.target.name;
                const data = this.getFormData();
                var wrapper = $(event.target).attr('data-wrapper');
                var value = $(event.target).val();
                if (typeof (data[wrapper]) === 'undefined' || !data[wrapper] || typeof (data[wrapper]) !== 'object' || data[wrapper] instanceof Array) {
                    data[wrapper] = {};
                }

                if (typeof (data[wrapper][name]) === 'undefined') {
                    data[wrapper][name] = {};
                }

                data[wrapper][name] = value !== 'Select Atribute' ? value : '';

                this.setData(data);
                this.render();
            },

            /**
             * sort the Labels 
             *
             * @param array data
             */
            sortByLabel: function (data) {
                data.sort(function (a, b) {
                    var textA = a.label.toUpperCase();
                    var textB = b.label.toUpperCase();
                    return (textA < textB) ? -1 : (textA > textB) ? 1 : 0;
                });
                return data;
            },
        });
    });
