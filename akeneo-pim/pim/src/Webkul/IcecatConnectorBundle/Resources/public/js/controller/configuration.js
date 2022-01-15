'use strict';
define(
    [
        'jquery',
        'underscore',
        'oro/translator',
        'pim/controller/front',
        'pim/form-builder',
        'pim/page-title',
        'routing'
    ],
    function ($, _, __, BaseController, FormBuilder, PageTitle, Routing) {
        return BaseController.extend({
            
            /**
             * {@inheritdoc}
             */
            renderForm: function () {
                return $.when(
                    FormBuilder.build('webkul-icecat-connector-configuration-form'),
                    $.get(Routing.generate('webkul_icecat_connector_mapping_get'))
                ).then((form, response) => {
                    this.on('pim:controller:can-leave', function (event) {
                        form.trigger('pim_enrich:form:can-leave', event);
                    });
                    form.setData(response[0]);
                    form.setElement(this.$el).render();

                    return form;
                });
            }
        });
    }
);