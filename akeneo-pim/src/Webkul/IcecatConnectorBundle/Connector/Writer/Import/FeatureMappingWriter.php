<?php

namespace Webkul\IcecatConnectorBundle\Connector\Writer\Import;

$namespaceObject = new \Webkul\IcecatConnectorBundle\Listener\ClassDefinationForCompatibility();
$namespaceObject->checkVersionAndCreateClassAliases();

use Doctrine\ORM\EntityManager;
use Webkul\IcecatConnectorBundle\Entity\IcecatDataMapping;
use Webkul\IcecatConnectorBundle\Repository\IcecatDataMappingRepository;

$namespaceObject = new \Webkul\IcecatConnectorBundle\Listener\ClassDefinationForCompatibility();
$namespaceObject->checkVersionAndCreateClassAliases();

class FeatureMappingWriter implements
\ItemWriterInterface,
\StepExecutionAwareInterface
{
    /**
     * @const string
     */
    const ATTRIBUTE_DATA_MAPPING = 'icecate_attribute_data_mapping';

    /** @var IcecatDataMappingRepository */
    private $icecatDataMappingRepository;

    /** @var  EntityManager */
    protected $entityManager;
    
    /**
     * @param IcecatDataMappingRepository  $icecatDataMappingRepository
     * @param EntityManager                $EntityManager
     */
    public function __construct(
        IcecatDataMappingRepository $icecatDataMappingRepository,
        EntityManager $entityManager
    ) {
        $this->icecatDataMappingRepository = $icecatDataMappingRepository;
        $this->entityManager = $entityManager;
    }

    /**
     * {@inheritdoc}
     */
    public function write(array $items)
    {
        foreach ($items as $item) {
            $this->addMapping($item, self::ATTRIBUTE_DATA_MAPPING);
            $this->stepExecution->incrementSummaryInfo('write');
        }
    }

    /**
    * @param array  $mappingData
    * @param string $section
    *
    * @return void
    */
    protected function addMapping(array $attributeData, string $section): void
    {
        $mapping = $this->icecatDataMappingRepository->findOneBy(['externalId'=> $attributeData['sort_order'], 'section' => $section]);
        if (!$mapping) {
            $mapping = new IcecatDataMapping();
        }

        $mapping->setExternalId($attributeData['sort_order']);
        $mapping->setValue(json_encode($attributeData));
        $mapping->setCode($attributeData['code']);
        $mapping->setSection($section);
        $this->entityManager->persist($mapping);
        $this->entityManager->flush();
    }

    /**
     * {@inheritdoc}
     */
    public function setStepExecution(\StepExecution $stepExecution)
    {
        $this->stepExecution = $stepExecution;
    }
}
