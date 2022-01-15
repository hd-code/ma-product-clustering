<?php

namespace Webkul\IcecatConnectorBundle\Listener;

use Symfony\Component\HttpKernel\Event\GetResponseEvent;
use Symfony\Component\Console\Event\ConsoleCommandEvent;

class ClassDefinationForCompatibility
{
    public function onKernelRequest(GetResponseEvent $event)
    {
        $this->checkVersionAndCreateClassAliases();
    }

    public function createUserSystem(ConsoleCommandEvent $event)
    {
        $this->checkVersionAndCreateClassAliases();
    }

    public function checkVersionAndCreateClassAliases()
    {
        if (class_exists('Akeneo\Platform\CommunityVersion')) {
            $versionClass = new \Akeneo\Platform\CommunityVersion();
        } elseif (class_exists('Pim\Bundle\CatalogBundle\Version')) {
            $versionClass = new \Pim\Bundle\CatalogBundle\Version();
        }
        
        $version = $versionClass::VERSION;
        if (version_compare($version, '3.0', '>=')) {
            $this->akeneoVersion3();
        } else {
            $this->akeneoVersion2();
        }
    }

    public function akeneoVersion3()
    {
        $AliaseNames = [
            'AttributeOptionRepository'                 =>  'Akeneo\Pim\Structure\Bundle\Doctrine\ORM\Repository\AttributeOptionRepository',
            'AttributeOptionType'                       =>  'Akeneo\Pim\Structure\Bundle\Form\Type\AttributeOptionType',
            'SimpleFactoryInterface'                    =>  'Akeneo\Tool\Component\StorageUtils\Factory\SimpleFactoryInterface',
            'SaverInterface'                            =>  'Akeneo\Tool\Component\StorageUtils\Saver\SaverInterface',
            'Operators'                                 =>  'Akeneo\Pim\Enrichment\Component\Product\Query\Filter\Operators',
            'AbstractProcessor'                         =>  'Akeneo\Pim\Enrichment\Component\Product\Connector\Processor\MassEdit\AbstractProcessor',
            'AttributeOptionInterface'                  =>  'Akeneo\Pim\Structure\Component\Model\AttributeOptionInterface',
            'AttributeInterface'                        =>  'Akeneo\Pim\Structure\Component\Model\AttributeInterface',
            'AttributeOption'                           =>  'Akeneo\Pim\Structure\Component\Mode\AttributeOption',
            'AttributeTypes'                            =>  'Akeneo\Pim\Structure\Component\AttributeTypes',
            'AttributeRepositoryInterface'              =>  'Akeneo\Pim\Structure\Component\Repository\AttributeRepositoryInterface',
            'CompletenessManager'                       =>  'Akeneo\Pim\Enrichment\Component\Product\Manager\CompletenessManager',
            'ConstraintCollectionProviderInterface'     =>  'Akeneo\Tool\Component\Batch\Job\JobParameters\ConstraintCollectionProviderInterface',
            'ChannelRepositoryInterface'                =>  'Akeneo\Channel\Component\Repository\ChannelRepositoryInterface',
            'DefaultValuesProviderInterface'            =>  'Akeneo\Tool\Component\Batch\Job\JobParameters\DefaultValuesProviderInterface',
            'DatabaseProductReader'                     =>  'Akeneo\Pim\Enrichment\Component\Product\Connector\Reader\Database\ProductReader',
            'DataInvalidItem'                           =>  'Akeneo\Tool\Component\Batch\Item\DataInvalidItem',
            'FileStorage'                               =>  'Akeneo\Pim\Enrichment\Component\FileStorage',
            'FileStorerInterface'                       =>  'Akeneo\Tool\Component\FileStorage\File\FileStorerInterface',
            'FilterStructureLocale'                     =>  'Akeneo\Pim\Enrichment\Component\Product\Validator\Constraints\FilterStructureLocale',
            'InitializableInterface'                    =>  'Akeneo\Tool\Component\Batch\Item\InitializableInterface',
            'ItemReaderInterface'                       =>  'Akeneo\Tool\Component\Batch\Item\ItemReaderInterface',
            'ItemWriterInterface'                       =>  'Akeneo\Tool\Component\Batch\Item\ItemWriterInterface',
            'JobInterface'                              =>  'Akeneo\Tool\Component\Batch\Job\JobInterface',
            'MetricConverter'                           =>  'Akeneo\Pim\Enrichment\Component\Product\Converter\MetricConverter',
            'ObjectUpdaterInterface'                    =>  'Akeneo\Tool\Component\StorageUtils\Updater\ObjectUpdaterInterface',
            'ProductInterface'                          =>  'Pim\Component\Catalog\Model\ProductInterface',
            'ProductQueryBuilderFactoryInterface'       =>  'Akeneo\Pim\Enrichment\Component\Product\Query\ProductQueryBuilderFactoryInterface',
            'SearchableRepositoryInterface'             =>  'Akeneo\Tool\Component\StorageUtils\Repository\SearchableRepositoryInterface',
            'StepExecution'                             =>  'Akeneo\Tool\Component\Batch\Model\StepExecution',
            'StepExecutionAwareInterface'               =>  'Akeneo\Tool\Component\Batch\Step\StepExecutionAwareInterface',
        ];
        
        foreach ($AliaseNames as $alias => $aliasPath) {
            if ((interface_exists($aliasPath) || class_exists($aliasPath)) && !class_exists($alias) && !interface_exists($alias)) {
                \class_alias($aliasPath, $alias);
            }
        }
    }

    public function akeneoVersion2()
    {
        $AliaseNames = [
            'AttributeOptionRepository'                 =>  'Pim\Bundle\CatalogBundle\Doctrine\ORM\Repository\AttributeOptionRepository',
            'AttributeOptionType'                       =>  'Pim\Bundle\EnrichBundle\Form\Type\AttributeOptionType',
            'SimpleFactoryInterface'                    =>  'Akeneo\Component\StorageUtils\Factory\SimpleFactoryInterface',
            'SaverInterface'                            =>  'Akeneo\Component\StorageUtils\Saver\SaverInterface',
            'Operators'                                 =>  'Pim\Component\Catalog\Query\Filter\Operators',
            'AbstractProcessor'                         =>  'Pim\Bundle\EnrichBundle\Connector\Processor\AbstractProcessor',
            'AttributeOptionInterface'                  =>  'Pim\Component\Catalog\Model\AttributeOptionInterface',
            'AttributeInterface'                        =>  'Pim\Component\Catalog\Model\AttributeInterface',
            'AttributeOption'                           =>  'Pim\Bundle\CatalogBundle\Entity\AttributeOption',
            'AttributeTypes'                            =>  'Pim\Component\Catalog\AttributeTypes',
            'AttributeRepositoryInterface'              =>  'Pim\Component\Catalog\Repository\AttributeRepositoryInterface',
            'CompletenessManager'                       =>  'Pim\Component\Catalog\Manager\CompletenessManager',
            'ChannelRepositoryInterface'                =>  'Pim\Component\Catalog\Repository\ChannelRepositoryInterface',
            'ConstraintCollectionProviderInterface'     =>  'Akeneo\Component\Batch\Job\JobParameters\ConstraintCollectionProviderInterface',
            'DatabaseProductReader'                     =>  'Pim\Component\Connector\Reader\Database\ProductReader',
            'DataInvalidItem'                           =>  'Akeneo\Component\Batch\Item\DataInvalidItem',
            'DefaultValuesProviderInterface'            =>  'Akeneo\Component\Batch\Job\JobParameters\DefaultValuesProviderInterface',
            'FileStorage'                               =>  'Pim\Component\Catalog\FileStorage',
            'FileStorerInterface'                       =>  'Akeneo\Component\FileStorage\File\FileStorerInterface',
            'FilterStructureLocale'                     =>  'Pim\Component\Connector\Validator\Constraints\FilterStructureLocale',
            'InitializableInterface'                    =>  'Akeneo\Component\Batch\Item\InitializableInterface',
            'ItemReaderInterface'                       =>  'Akeneo\Component\Batch\Item\ItemReaderInterface',
            'ItemWriterInterface'                       =>  'Akeneo\Component\Batch\Item\ItemWriterInterface',
            'JobInterface'                              =>  'Akeneo\Component\Batch\Job\JobInterface',
            'MetricConverter'                           =>  'Pim\Component\Catalog\Converter\MetricConverter',
            'ObjectUpdaterInterface'                    =>  'Akeneo\Component\StorageUtils\Updater\ObjectUpdaterInterface',
            'ProductInterface'                          =>  'Akeneo\Pim\Enrichment\Component\Product\Model\ProductInterface',
            'ProductQueryBuilderFactoryInterface'       =>  'Pim\Component\Catalog\Query\ProductQueryBuilderFactoryInterface',
            'SearchableRepositoryInterface'             =>  'Akeneo\Component\StorageUtils\Repository\SearchableRepositoryInterface',
            'StepExecution'                             =>  'Akeneo\Component\Batch\Model\StepExecution',
            'StepExecutionAwareInterface'               =>  'Akeneo\Component\Batch\Step\StepExecutionAwareInterface',
        ];

        foreach ($AliaseNames as $alias => $aliasPath) {
            if ((interface_exists($aliasPath) || class_exists($aliasPath)) && !class_exists($alias) && !interface_exists($alias)) {
                \class_alias($aliasPath, $alias);
            }
        }
    }
}
