<?php

namespace Webkul\IcecatConnectorBundle\Component;

$namespaceObject = new \Webkul\IcecatConnectorBundle\Listener\ClassDefinationForCompatibility();
$namespaceObject->checkVersionAndCreateClassAliases();

class MediaStorer
{
    /** @var \FileStorerInterface $storer */
    protected $storer;

    /** @var uploadDir */
    protected $uploadDir;

    /**
    * @param \FileStorerInterface $storer
    * @param string uploadDir
    */
    public function __construct(\FileStorerInterface $storer, string $uploadDir)
    {
        $this->storer    = $storer;
        $this->uploadDir = $uploadDir;
    }

    /**
    * FUNCTION STORE THE IMAGE AND RETURN THE FILE KEY
    *
    * @param string $imageName
    * @param string rawImage
    *
    * @return string
    */
    public function store(string $imageName, string $rawImage): string
    {
        $filePath = $this->getImagePath($imageName, $rawImage);
        $rawFile = new \SplFileInfo($filePath);
        $file = $this->storer->store($rawFile, \FileStorage::CATALOG_STORAGE_ALIAS);
        
        return $file->getKey();
    }

    /**
    * @param string $imageName
    * @param string rawImage
    *
    * @return string
    */
    protected function getImagePath(string $imageName, string $rawImage): string
    {
        $localpath = $this->uploadDir.'/'.$imageName;
        if (!file_exists(dirname($localpath))) {
            mkdir(dirname($localpath), 0777, true);
        }

        @file_put_contents($localpath, $rawImage);

        return $localpath;
    }
}
