<?php

namespace Webkul\IcecatConnectorBundle\Repository;

use Doctrine\ORM\EntityManager;

/**
 * IcecatMappingRepository
 *
 * This class was generated by the Doctrine ORM. Add your own custom
 * repository methods below.
 */
class IcecatMappingRepository extends \Doctrine\ORM\EntityRepository
{
    /**
     * @param EntityManager $em
     *
     * @param string $class
     */
    public function __construct(EntityManager $em, string $class)
    {
        parent::__construct($em, $em->getClassMetadata($class));
    }

    /**
     * @param array $mappingSections
     *
     * @return array
     */
    protected function findBySection(array $mappingSections): array
    {
        $mapping = [];
        foreach ($mappingSections as $mappingKey => $mappingSection) {
            $xmlConfigData = $this->findBy(['section' => $mappingSection]);
            if ($xmlConfigData) {
                $mapping[$configKey] =[];
                foreach ($xmlConfigData as $value) {
                    $mapping[$configKey][$value->getName()] = $value->getValue();
                }
            }
        }

        return $mapping;
    }
}
