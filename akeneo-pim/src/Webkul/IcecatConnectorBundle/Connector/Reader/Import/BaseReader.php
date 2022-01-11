<?php

namespace Webkul\IcecatConnectorBundle\Connector\Reader\Import;

$namespaceObject = new \Webkul\IcecatConnectorBundle\Listener\ClassDefinationForCompatibility();
$namespaceObject->checkVersionAndCreateClassAliases();

class BaseReader
{
    /**
     * Metric sign that akeneo not manage
     *
     * @var array
     *
     */
    protected $ignoredSigns = [
        '€',
        'cent(s)',
        'x',
        'lines',
        'pages',
        'entries',
        'slides',
        'levels of grey',
        'user(s)',
        'person(s)',
        'sheets',
        'buttons',
        'locations',
        'scans',
        'pass(es)',
        'scans',
        'discs',
        'copies',
        'clicks',
        'label(s)',
        'coins',
        'shots',
        'coins per minute',
        'octave(s)',
        'piece(s)',
        'EER',
        'staples',
        'cycles per logical sector',
        'banknotes/min',
        'pc(s)',
    ];
}
