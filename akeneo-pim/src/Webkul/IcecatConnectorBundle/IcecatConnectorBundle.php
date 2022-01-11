<?php

namespace Webkul\IcecatConnectorBundle;

use Symfony\Component\DependencyInjection\ContainerBuilder;
use Symfony\Component\HttpKernel\Bundle\Bundle;
use Webkul\IcecatConnectorBundle\DependencyInjection\MeasuresCompilerPass;

class IcecatConnectorBundle extends Bundle
{
    /**
     * {@inheritdoc}
     */
    public function build(ContainerBuilder $container)
    {
        parent::build($container);
        $measuresConfigDir = __DIR__ . '/Resources/config/measures';
        $container->addCompilerPass(new MeasuresCompilerPass($measuresConfigDir));
    }
}
