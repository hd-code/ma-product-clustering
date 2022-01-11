'use strict';

define([
        'underscore',
        'jquery',
        'routing',
        'pim/form/common/save',
        'pim/template/form/save',
        'oro/messenger'
    ],
    function(
        _,
        $,
        Routing,
        SaveForm,
        template,
        messenger
    ) {
        return SaveForm.extend({
            config: [],
            template: _.template(template),
            currentTabKey: 'current_form_tab',
            events: {
                'click .save': 'save'
            },

            initialize: function (config) {
                this.config = config.config;
            },

            /**
             * {@inheritdoc}
             */
            render: function () {
                this.$el.html(this.template({
                    label: _.__('pim_enrich.entity.save.label')
                }));
                var saveBtn = this.$('.save');
                saveBtn.addClass('icecat-save-config');
               
            },

            /**
             * {@inheritdoc}
             */
            save: function () {
                this.getRoot().trigger('pim_enrich:form:entity:pre_save', this.getFormData());
                this.showLoadingMask();
                var data = this.stringify(this.getFormData());
                $.ajax({
                    method: 'POST',
                    url: this.getSaveUrl(),
                    contentType: 'application/json',
                    data: data
                })
                .then(this.postSave.bind(this))
                .fail(this.fail.bind(this))
                .always(this.hideLoadingMask.bind(this));
            },

            stringify: function(formData) {
                if('undefined' != typeof(formData['mapping']) && formData['mapping'] instanceof Array) {
                    formData['mapping'] = $.extend({}, formData['mapping']);
                }

                if('undefined' != typeof(formData['otherMapping']) && formData['otherMapping'] instanceof Array) {
                    formData['otherMapping'] = $.extend({}, formData['otherMapping']);
                }

                if('undefined' != typeof(formData['header']) && formData['header'] instanceof Array) {
                    formData['header'] = $.extend({}, formData['header']);
                }
                return JSON.stringify(formData);                
            },

            /**
             * {@inheritdoc}
             */
            getSaveUrl: function () {
                if(this.config && this.config.url) {
                    var tab = null;
                    switch(sessionStorage.getItem(this.currentTabKey)) {
                        case 'webkul-icecat-connector-configuration-tab-credential':
                            tab = 'credential';
                            break;
                        case 'webkul-icecat-connector-configuration-tab-mapping':
                            tab = 'mapping';
                            break;
                        case 'webkul-icecat-connector-configuration-tab-other-mapping':
                            tab = 'other-mapping';
                            break;
                        case 'webkul-icecat-connector-configuration-tab-other-attribute':
                            tab = 'extra-mapping';
                            break;
                        case 'webkul-icecat-connector-configuration-tab-attribute-type-mapping':
                            tab = 'attribute-type-mapping';
                            break;
                        default:
                            tab = 'localeMapping';
                            break;
                    }

                    var url = this.config.url;
                    return Routing.generate(url) + '/' +tab;
                }
            },

            /**
             * {@inheritdoc}
             */
            postSave: function (data) {
                this.setData(data);
                this.getRoot().trigger('pim_enrich:form:entity:post_fetch', data);
                SaveForm.prototype.postSave.apply(this, arguments);
            },
             
            fail: function (response) {
                let errorMessage = this.updateFailureMessage;
                switch (response.status) {
                case 400:
                    this.getRoot().trigger(
                        'pim_enrich:form:entity:bad_request',
                        {'sentData': this.getFormData(), 'response': response.responseJSON}
                    );
                 
                    errorMessage = response.responseJSON[0] !== undefined ?
                        response.responseJSON[0].message :
                        errorMessage;
                    break;
                case 500:
                    const message = response.responseJSON ? response.responseJSON : response;
                    this.getRoot().trigger('pim_enrich:form:entity:error:save', message);
                    break;
                default:
                }

                messenger.notify(
                    'error',
                    errorMessage
                );
            }
        });
    }
);
