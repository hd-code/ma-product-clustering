<?php

namespace Webkul\IcecatConnectorBundle\DependencyInjection;

use Symfony\Component\Config\FileLocator;
use Symfony\Component\DependencyInjection\ContainerBuilder;
use Symfony\Component\DependencyInjection\Loader;
use Symfony\Component\HttpKernel\DependencyInjection\Extension;

/**
 * This is the class that loads and manages your bundle configuration.
 *
 * @link http://symfony.com/doc/current/cookbook/bundles/extension.html
 */
class IcecatConnectorExtension extends Extension
{
    /**
     * {@inheritdoc}
     */
    public function load(array $configs, ContainerBuilder $container)
    {
        $configuration = new Configuration();
        $config = $this->processConfiguration($configuration, $configs);
        $loader = new Loader\YamlFileLoader($container, new FileLocator(__DIR__.'/../Resources/config'));
        $loader->load('controllers.yml');
        $loader->load('cli_command.yml');
        $loader->load('job_parameters.yml');
        $loader->load('processors.yml');
        $loader->load('repositories.yml');
        $loader->load('services.yml');
        $loader->load('writers.yml');
        $loader->load('readers.yml');
        
        if (class_exists('Pim\Bundle\CatalogBundle\Version')) {
            $versionClass = new \Pim\Bundle\CatalogBundle\Version();
        } elseif (class_exists('Akeneo\Platform\CommunityVersion')) {
            $versionClass = new \Akeneo\Platform\CommunityVersion();
        }
        
        $version = $versionClass::VERSION;
        $versionDirectoryPrefix = '2x/';
        if ($version >= '5.0') {
            $versionDirectoryPrefix = '5x/';
        } elseif ($version >= '3.0') {
            $versionDirectoryPrefix = '3x/';
        }

        $loader->load($versionDirectoryPrefix . 'parameters.yml');
        $loader->load($versionDirectoryPrefix . 'jobs.yml');
        $loader->load($versionDirectoryPrefix . 'steps.yml');
        $loader->load($versionDirectoryPrefix . 'readers.yml');
    }
}
