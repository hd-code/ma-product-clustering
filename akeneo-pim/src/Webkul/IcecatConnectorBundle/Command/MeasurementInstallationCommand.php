<?php

namespace Webkul\IcecatConnectorBundle\Command;

use Symfony\Component\Console\Input\ArrayInput;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\EventDispatcher\EventDispatcherInterface;
use Symfony\Component\EventDispatcher\GenericEvent;
use Webkul\IcecatConnectorBundle\Event\InstallerEvents;

class MeasurementInstallationCommand extends Command
{
    protected static $defaultName = 'measurementinstallation:setup:install';

    /** @var EventDispatcherInterface */
    protected $eventDispatcher;

    public function __construct(EventDispatcherInterface $eventDispatcher)
    {
        parent::__construct();
        $this->eventDispatcher = $eventDispatcher;
    }
    
    protected function configure()
    {
        $this->setName('measurementinstallation:setup:install')
            ->setDescription('Install Icecat Akeneo connector setup')
            ->setHelp('setups icecat bundle installation');
    }
 
    protected function execute(InputInterface $input, OutputInterface $output)
    {
        $errorFlag = false;

        /* version wise loading */
        if (class_exists('Pim\Bundle\CatalogBundle\Version')) {
            // version 2
            $versionClass = new \Pim\Bundle\CatalogBundle\Version();
        } elseif (class_exists('Akeneo\Platform\CommunityVersion')) {
            // version 3 or later
            $versionClass = new \Akeneo\Platform\CommunityVersion();
        }
        
        $version = $versionClass::VERSION;

        if ($version >= "5.0") {
            $this->dispatchGroupEvent(InstallerEvents::POST_ICECAT_MODULE_INSTALLATION);
        }

        return 0;
    }

    /**
     * @param string $event
     * @param null   $argument
     */
    private function dispatchGroupEvent($event, $argument = null)
    {
        $this->eventDispatcher->dispatch(
            $event,
            new GenericEvent($argument)
        );
    }
}
