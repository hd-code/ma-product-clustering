"use strict";

define(
    [
        'underscore',
        'oro/translator',
        'pim/form',
        'magento2/template/configuration/tab/documentation',
        'routing'
    ],
    function(
        _,
        __,
        BaseForm,
        template,
        Routing
    ) {
        return BaseForm.extend({
            isGroup: true,
            label: __('magento2.documentation'),
            template: _.template(template),
            code: 'magento2.documentation.tab',
            events: {
                'change .AknFormContainer-Mappings input': 'updateModel',
                'click .wk_toggler': 'toggleClass',
            },
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
                this.$el.html(this.template({
                    fields: this.fields,
                    model: this.getFormData()['mappings'],
                    moduleVersion: this.getFormData()['moduleVersion'],
                }));
                $('.AknIconButton').tooltip();
                this.delegateEvents();

                return BaseForm.prototype.render.apply(this, arguments);
            },

            /**
             * Update model after value change
             *
             * @param {Event} event
             */
            updateModel: function (event) {
                var data = this.getFormData();
                if(!data['mappings'])
                    data['mappings'] = {};

                data['mappings'][$(event.target).attr('name')] = event.target.value;
                this.setData(data);
            },
            toggleClass: function() {
                $('.wk_toggler').toggleClass('active');
            },
        });
    }
);
