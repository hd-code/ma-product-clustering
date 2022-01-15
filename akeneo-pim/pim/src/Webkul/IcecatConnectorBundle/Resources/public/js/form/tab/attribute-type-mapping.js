'use strict';

define(
    [
        'jquery',
        'underscore',
        'oro/translator',
        'pim/form',
        'pim/i18n',
        'pim/user-context',
        'pim/fetcher-registry',
        'pim/security-context',
        'pim/dialog',
        'icecatconnector/template/tab/attribute-type',
        'jquery-ui'
    ],
    function (
        $,
        _,
        __,
        BaseForm,
        i18n,
        UserContext,
        FetcherRegistry,
        SecurityContext,
        Dialog,
        template
    ) {
        return BaseForm.extend({
            className: 'tabbable tabs-left',
            template: _.template(template),
            attributes: [],
            icecatAttributes: [],
            events: {
                'click .remove-attribute': 'removeAttributeRequest',
                'change select.attributes': 'updateModel',
            },
            pimAttributeTypes : {
                "pim_catalog_identifier": "Identifier",
                "pim_catalog_text": "Text",
                "pim_catalog_textarea": "Text Area",
                "pim_catalog_simpleselect": "Simple Select",
                // "pim_catalog_multiselect": "Multi Select",
                "pim_catalog_image": "Image",
                "pim_catalog_price_collection": "Price",
                // "pim_catalog_number": "Number",
                // "pim_catalog_metric": "Metric",
                "pim_catalog_boolean": "Yes/ No",
                "pim_catalog_date": "Date",
            },

            /**
             * {@inheritdoc}
             */
            initialize: function (config) {
                this.config = config.config;

                BaseForm.prototype.initialize.apply(this, arguments);
            },

            /**
             * {@inheritdoc}
             */
            configure: function () {
                this.trigger('tab:register', {
                    code: this.config.tabCode ? this.config.tabCode : this.code,
                    label: __(this.config.title)
                });

                this.onExtensions('add-attribute:add', this.addAttributes.bind(this));

                return FetcherRegistry.getFetcher('icecatconnector-get-data-mapping')
                    .search({attribute_groups: 'other'})
                    .then(function (attributes) {
                        if (_.isEmpty(this.icecatAttribute)) {
                            this.icecatAttributes = attributes;
                        }
                    }.bind(this)).then(function () {
                        return BaseForm.prototype.configure.apply(this, arguments);
                    }.bind(this));
            },
            
            /**
             * {@inheritdoc}
             */
            render: function () {
                var attributesType = this.getFormData().attributesType;
                this.$el.empty().append(this.template({
                    pimAttributeTypes: this.pimAttributeTypes,
                    attributesType: attributesType,
                    icecatAttributes: this.icecatAttributes,
                    i18n: i18n,
                    UserContext: UserContext,
                    __: __,
                    hasRightToRemove: this.hasRightToRemove(),
                    currentLocale   : UserContext.get('uiLocale'),
                }));
                
                this.delegateEvents();
                $('.select2').select2();
                this.$('*[data-toggle="tooltip"]').tooltip();
                BaseForm.prototype.render.apply(this, arguments);
            
                return this;
            },

            /**
             * Add attributes to the model
             *
             * @param {Event}
             */
            addAttributes: function (event) {
                var formData = _.extend({}, this.getFormData());
                _.each(event.codes, function(code) {
                    formData.attributesType[code] = 'pim_catalog_text';
                });

                formData.attributesType = Object.assign({},formData.attributesType);
                this.setData(formData);
                this.render();
               
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
             * Add attributes to the model
             *
             * @param {Event}
             */
            removeAttributeRequest: function (event) {
                if (!SecurityContext.isGranted(this.config.removeAttributeACL)) {
                    return;
                }

                var dataset = event.currentTarget.dataset;
                var label =  dataset.attributeLabel ? dataset.attributeLabel : dataset.attributeCode;
                Dialog.confirmDelete(
                    __(this.config.confirmation.message, {attribute: label}),
                    __(this.config.confirmation.title),
                    function () {
                        this.removeAttribute(dataset.attributeCode);
                    }.bind(this),
                    __(this.config.confirmation.subTitle),
                    __(this.config.confirmation.buttonText)
                );
            },

            /**
             * Remove attribute from collection
             *
             * @param {string} code
             */
            removeAttribute: function (code) {
                var formData = _.extend({}, this.getFormData());
                delete formData.attributesType[code];
                this.setData(formData);
                this.render();
            },

            /**
             * Does the user has right to remove an attribute
             *
             * @return {Boolean}
             */
            hasRightToRemove: function () {
                var currentAttributeGroupIsNotOther = this.config.otherGroup !== this.getFormData().code;
                return currentAttributeGroupIsNotOther &&
                    SecurityContext.isGranted(this.config.removeAttributeACL)
            },

            /**
             * Does the user has right to add an attribute
             *
             * @return {Boolean}
             */
            hasRightToAdd: function () {
                var currentAttributeGroupIsNotOther = this.config.otherGroup !== this.getFormData().code;
                return currentAttributeGroupIsNotOther &&
                    SecurityContext.isGranted(this.config.addAttributeACL)
            },
        });
    });
