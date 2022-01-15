<?php

namespace Webkul\IcecatConnectorBundle\Repository;

use Doctrine\ORM\EntityManagerInterface;
use Doctrine\ORM\QueryBuilder;

$namespaceObject = new \Webkul\IcecatConnectorBundle\Listener\ClassDefinationForCompatibility();
$namespaceObject->checkVersionAndCreateClassAliases();

/**
 * IcecatDataMapping searchable repository
 */
class IcecatDataMappingSearchableRepository implements \SearchableRepositoryInterface
{
    /** @var EntityManagerInterface */
    protected $entityManager;

    /** @var string */
    protected $entityName;
    /**
     * @param EntityManagerInterface $entityManager
     * @param string                 $entityName
     */
    public function __construct(EntityManagerInterface $entityManager, $entityName)
    {
        $this->entityManager = $entityManager;
        $this->entityName = $entityName;
    }
    
    public function findBySearch($search = null, array $options = [])
    {
        $section = $options['section'];
        $qb = $this->entityManager->createQueryBuilder()->select('a')->from($this->entityName, 'a');
        $qb->Where('a.section like :section');
        $qb->setParameter('section', '%' . $section . '%');
        if (null !== $search && '' !== $search) {
            $qb->andWhere('a.value like :search');
            $qb->setParameter('search', '%' . trim($search, ' ') . '%');
            $qb->distinct();
        }

        // if($options['attributes']) {
        //     $qb->andWhere($qb->expr()->notIn('a.code', ':attributes'));
        //     $qb->setParameter('attributes', $options['attributes']);
        // }

        $qb = $this->applyQueryOptions($qb, $options);

        return $qb->getQuery()->getResult();
    }
    /**
     * @param QueryBuilder $qb
     * @param array        $options
     *
     * @return QueryBuilder
     */
    protected function applyQueryOptions(QueryBuilder $qb, array $options)
    {
        if (isset($options['limit'])) {
            $qb->setMaxResults((int) $options['limit']);
            if (isset($options['page'])) {
                $qb->setFirstResult((int) $options['limit'] * ((int) $options['page'] - 1));
            }
        }

        return $qb;
    }
}
