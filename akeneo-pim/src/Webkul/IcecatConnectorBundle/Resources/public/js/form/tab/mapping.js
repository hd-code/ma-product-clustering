"use strict";

define(
    [
        'underscore',
        'oro/translator',
        'pim/form',
        'icecatconnector/template/tab/mapping',
        'pim/fetcher-registry',
        'pim/user-context',
        'oro/loading-mask',
    ],
    function (
        _,
        __,
        BaseForm,
        template,
        FetcherRegistry,
        UserContext,
        LoadingMask,
    ) {
        return BaseForm.extend({
            events: {
                'change select.attributeMapping': 'updateModel',
            },
            template: _.template(template),
            label: __('webkul_icecat_connector.tab.mapping.title'),
            code: 'icecat_connector_mapping',
            attributes: [],
            commonAttributes: [
                {
                    name: 'ean_attribute',
                    label: 'webkul_icecat_connector.tab.mapping.common_attribute.ean.label',
                    supportedType: ['pim_catalog_identifier', 'pim_catalog_numbers', 'pim_catalog_text'],
                    supportedTypeLabel: 'Unique and Identifiers, text or number attributes',
                    isMultiple: false,
                    unique: true,
                    wrapper: 'attributeMapping'
                },
                {
                    name: 'product_id',
                    label: 'webkul_icecat_connector.tab.mapping.common_attribute.product_code.label',
                    supportedType: ['pim_catalog_identifier', 'pim_catalog_numbers', 'pim_catalog_text'],
                    supportedTypeLabel: 'Unique and Identifiers, text or number attributes',
                    isMultiple: false,
                    unique: true,
                    wrapper: 'attributeMapping'
                },
                {
                    name: 'vendor',
                    label: 'webkul_icecat_connector.tab.mapping.common_attribute.vendor.label',
                    supportedType: ['pim_catalog_simpleselect', 'pim_catalog_text'],
                    supportedTypeLabel: 'Simple select or text attributes',
                    isMultiple: false,
                    unique: false,
                    wrapper: 'attributeMapping'
                },
                {
                    name: 'Name',
                    label: 'webkul_icecat_connector.tab.mapping.common_attribute.name.label',
                    supportedType: ['pim_catalog_text'],
                    supportedTypeLabel: 'Text',
                    isMultiple: false,
                    unique: false,
                    wrapper: 'attributeMapping'
                },
                {
                    name: 'Title',
                    label: 'webkul_icecat_connector.tab.mapping.common_attribute.title.label',
                    supportedType: ['pim_catalog_text'],
                    supportedTypeLabel: 'Text',
                    isMultiple: false,
                    unique: false,
                    wrapper: 'attributeMapping'
                },
                {
                    name: 'description',
                    label: 'webkul_icecat_connector.tab.mapping.common_attribute.description.label',
                    supportedType: ['pim_catalog_textarea', 'pim_catalog_text'],
                    supportedTypeLabel: 'Text or textarea attributes',
                    isMultiple: false,
                    unique: false,
                    wrapper: 'attributeMapping'
                },
                {
                    name: 'short_description',
                    label: 'webkul_icecat_connector.tab.mapping.common_attribute.short_description.label',
                    supportedType: ['pim_catalog_textarea', 'pim_catalog_text'],
                    supportedTypeLabel: 'Text or textarea attributes',
                    isMultiple: false,
                    unique: false,
                    wrapper: 'attributeMapping'
                },
                {
                    name: 'summary_description',
                    label: 'webkul_icecat_connector.tab.mapping.common_attribute.summary_description.label',
                    supportedType: ['pim_catalog_textarea', 'pim_catalog_text'],
                    supportedTypeLabel: 'Text or textarea attributes',
                    isMultiple: false,
                    unique: false,
                    wrapper: 'attributeMapping'
                },
                {
                    name: 'short_summary_description',
                    label: 'webkul_icecat_connector.tab.mapping.common_attribute.short_summary_description.label',
                    supportedType: ['pim_catalog_textarea', 'pim_catalog_text'],
                    supportedTypeLabel: 'Text or textarea attributes',
                    isMultiple: false,
                    unique: false,
                    wrapper: 'attributeMapping'
                },
                {
                    name: 'pictures',
                    label: 'webkul_icecat_connector.tab.mapping.common_attribute.pictures.label',
                    supportedType: ['pim_catalog_image'],
                    supportedTypeLabel: 'Image attributes',
                    isMultiple: true,
                    unique: false,
                    wrapper: 'attributeMapping'
                }
            ],

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
                if (_.isEmpty(this.attributes)) {
                    this.attributes = FetcherRegistry.getFetcher('attribute').search({ options: { 'page': 1, 'limit': 10000 } });
                }

                Promise.all([this.attributes]).then(function (values) {
                    var attributes = this.sortByLabel(values[0]);
                    var attributeMapping = this.getFormData()['attributeMapping'];
                    this.$el.html(this.template({
                        attributes: attributes,
                        commonAttributes: this.commonAttributes,
                        attributeMapping: attributeMapping,
                        mappedAttribute: _.flatten(_.toArray(attributeMapping)),
                        currentLocale: UserContext.get('uiLocale'),
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
                var wrapper = $(event.target).attr('data-wrapper') ? $(event.target).attr('data-wrapper') : 'mapping';
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
                    var textA = typeof (a.labels[UserContext.get('uiLocale')]) !== 'undefined' && a.labels[UserContext.get('uiLocale')] ? a.labels[UserContext.get('uiLocale')].toUpperCase() : a.code.toUpperCase();
                    var textB = typeof (b.labels[UserContext.get('uiLocale')]) !== 'undefined' && b.labels[UserContext.get('uiLocale')] ? b.labels[UserContext.get('uiLocale')].toUpperCase() : b.code.toUpperCase();
                    return (textA < textB) ? -1 : (textA > textB) ? 1 : 0;
                });
                return data;
            },

        });
    }
)