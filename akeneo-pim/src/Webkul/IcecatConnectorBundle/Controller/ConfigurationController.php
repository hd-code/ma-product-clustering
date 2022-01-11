<?php

namespace Webkul\IcecatConnectorBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\Filesystem\Filesystem;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;

class ConfigurationController extends Controller
{
    /**
     * Get the history class
     *
     * @param Request $request
     *
     * @return JsonResponse
     */
    public function getHistoryClassAction(Request $request): JsonResponse
    {
        if (class_exists('Akeneo\Platform\CommunityVersion')) {
            $versionClass = new \Akeneo\Platform\CommunityVersion();
        } elseif (class_exists('Pim\Bundle\CatalogBundle\Version')) {
            $versionClass = new \Pim\Bundle\CatalogBundle\Version();
        }

        $version = $versionClass::VERSION;
        $historyClass = 'Akeneo\Component\Batch\Model\JobInstance';
        
        if ($version > '3.0') {
            $historyClass = 'Akeneo\Tool\Component\Batch\Model\JobInstance';
        }
   
        return new JsonResponse(['history_class'=> $historyClass]);
    }
}
