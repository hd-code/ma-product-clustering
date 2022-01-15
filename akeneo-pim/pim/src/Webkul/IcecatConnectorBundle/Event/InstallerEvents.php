<?php

namespace Webkul\IcecatConnectorBundle\Event;

/**
 * Events dispached during installation process
 */
final class InstallerEvents
{
    /**
     * This event is dispatched after the module installtion
     */
    const POST_ICECAT_MODULE_INSTALLATION= 'wk_installer.post_icecat_module_installation';
}
