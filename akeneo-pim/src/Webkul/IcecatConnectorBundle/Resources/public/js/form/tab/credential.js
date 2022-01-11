"use strict";

define(
    [
        'underscore',
        'oro/translator',
        'pim/form',
        'icecatconnector/template/tab/credential',
        'oro/loading-mask',
    ],
    function(
        _,
        __,
        BaseForm,
        template,
        LoadingMask,
    ) {
        return BaseForm.extend({
            events: {
                'change input.AknTextField.credentialMapping': 'updateModel',
            },
            template: _.template(template),
            label: __('webkul_icecat_connector.tab.credential.title'),
            code: 'icecat_connector_credential',
            credentialAttributes: [
                {
                    name : 'username',
                    type : 'text',
                    label: 'webkul_icecat_connector.tab.credential.credential_attribute.username.label',
                    wrapper : 'credentialMapping'
                },
                {
                    name : 'password',
                    type : 'password',
                    label: 'webkul_icecat_connector.tab.credential.credential_attribute.password.label',
                    wrapper : 'credentialMapping'
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
               
                this.$el.html(this.template({
                    credentialAttributes: this.credentialAttributes,
                    credentialMapping: this.getFormData()['credentialMapping'],
                }));
                    
                this.$('*[data-toggle="tooltip"]').tooltip();
                loadingMask.hide().$el.remove();
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
                const value = event.target.value;

                if (typeof(data[wrapper]) === 'undefined' || !data[wrapper] || typeof(data[wrapper]) !== 'object' || data[wrapper] instanceof Array) {
                    data[wrapper] = {};
                }

                if (typeof(data[wrapper][name]) === 'undefined') {
                    data[wrapper][name] = {};
                }

                data[wrapper][name] = value;
                this.setData(data);
            },
        });
    }
)