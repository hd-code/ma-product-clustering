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
        'icecatconnector/template/job/icecat-attribute',
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
                'change select.attributes': 'updateModel',
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
                    .fetchAll()
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
                var attributes = this.getFormData().configuration.icecatAttributes;
                this.$el.empty().append(this.template({
                    attributes: attributes,
                    icecatAttributes: this.icecatAttributes,
                    i18n: i18n,
                    UserContext: UserContext,
                    __: __,
                    tooltip: __('webkul_enrich.form.job_instance.tab.icecat_attribute.help'),
                    mappedAttribute : _.flatten(_.toArray(attributes)),
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
                formData.configuration.icecatAttributes = _.union(formData.configuration.icecatAttributes, event.codes);
                this.setData(formData);
                this.render();
            },

            /**
             * Update model after value change
             *
             * @param {Event} event
             */
            updateModel: function (event) {
                var data = this.getFormData();
                data.configuration.icecatAttributes = event.val;
                this.setData(data);
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
