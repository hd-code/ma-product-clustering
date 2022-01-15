'use strict';
define([
    'pim/common/tab/history',
    'pim/fetcher-registry',
    'pim/common/grid',
],
    function (
        BaseHistory,
        FetcherRegistry,
        Grid,
    ) {
        return BaseHistory.extend({
            /**
            * {@inheritdoc}
            */
            render: function () {
                FetcherRegistry.getFetcher('icecatconnector-history-class').fetchAll()
                    .then((historyClass) => {
                        this.config.class = historyClass.history_class;
                        if (!this.historyGrid) {
                            this.historyGrid = new Grid(
                                'history-grid',
                                {
                                    object_class: this.config.class,
                                    object_id: this.getFormData().meta.id
                                }
                            );
                        }
                        this.$el.empty().append(this.historyGrid.render().$el);
                        return this;
                    });
            }
        });
    }
);