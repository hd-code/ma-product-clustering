<?php

namespace Webkul\IcecatConnectorBundle\Component;

use Symfony\Component\DependencyInjection\ContainerInterface;

/**
 * Tmp storage directory class
 */
class TempStorageDir
{
    /** @var ContainerInterface */
    protected $container;

    /**
     * @param ContainerInterface $container
     */
    public function __construct(ContainerInterface $container)
    {
        $this->container = $container;
        $this->setTmpStorageDirectory();
    }

    /**
     * Get tmp storage directory
     *
     * @return string
     */
    public function getTmpStorageDirectory(): string
    {
        return $this->tmpDir;
    }

    /**
     * Set tmp storage directory
     *
     * @return void
     */
    public function setTmpStorageDirectory(): void
    {
        $this->tmpDir = sys_get_temp_dir();
        if ($this->container->has('tmp_storage_dir')) {
            $this->tmpDir = $this->container->get('tmp_storage_dir');
        }
    }
}
