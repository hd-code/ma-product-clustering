<?php

namespace Webkul\IcecatConnectorBundle\DependencyInjection;

use Symfony\Component\Config\Definition\Builder\TreeBuilder;
use Symfony\Component\Config\Definition\ConfigurationInterface;

/**
 * This is the class that validates and merges configuration from your app/config files.
 *
 * To learn more see {@link http://symfony.com/doc/current/cookbook/bundles/configuration.html}
 */
class Configuration implements ConfigurationInterface
{
    /**
     * {@inheritdoc}
     */
    public function getConfigTreeBuilder()
    {
        $treeBuilder = new TreeBuilder();
        $rootNode = $treeBuilder->root('measures_config');
        $rootNode->useAttributeAsKey('family')
            ->prototype('array')
            ->children()
                ->scalarNode('standard')->isRequired()->end()
                ->arrayNode('units')->prototype('array')
                ->children()
                    ->append($this->addConvertNode())
                    ->scalarNode('symbol')->isRequired()->end()
                    ->scalarNode('name')->end()
                    ->scalarNode('unece_code')->end()
                    ->arrayNode('alternative_symbols')
                        ->prototype('scalar')->end()
                    ->end()
                ->end()
            ->end()
            ->end();

        // Here you should define the parameters that are allowed to
        // configure your bundle. See the documentation linked above for
        // more information on that topic.

        return $treeBuilder;
    }

    /**
     * Create a node definition for operations (could be extended to define new operations)
     * @return \Symfony\Component\Config\Definition\Builder\ArrayNodeDefinition|
     *         \Symfony\Component\Config\Definition\Builder\NodeDefinition
     */
    protected function addConvertNode()
    {
        $treeBuilder = new TreeBuilder();
        $node = $treeBuilder->root('convert');

        $node->requiresAtLeastOneElement()
            ->prototype('array')
                ->children()

                    ->scalarNode('add')
                    ->cannotBeEmpty()
                    ->end()

                    ->scalarNode('sub')
                    ->cannotBeEmpty()
                    ->end()

                    ->scalarNode('mul')
                    ->cannotBeEmpty()
                    ->end()

                    ->scalarNode('div')
                    ->cannotBeEmpty()
                    ->end()

                ->end()
            ->end();

        return $node;
    }
}
