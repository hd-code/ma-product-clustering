<?php

namespace Webkul\IcecatConnectorBundle\Connector\Processor\Import;

use Webkul\IcecatConnectorBundle\Component\MeasurementHandler;

$namespaceObject = new \Webkul\IcecatConnectorBundle\Listener\ClassDefinationForCompatibility();
$namespaceObject->checkVersionAndCreateClassAliases();

class FetaureMappingProcessor extends \AbstractProcessor
{
    /** @var array */
    protected $measuresConfig = [];

    /** @var MeasurementHandler*/
    protected $measurementHandler;
    
    /**
     * @param MeasurementHandler $measurementHandler
    */
    public function __construct(MeasurementHandler $measurementHandler)
    {
        $this->measurementHandler = $measurementHandler;
        $measurements = $this->measurementHandler->getMeasurements();
        if(!empty($measurements)) {
            $this->measuresConfig = $measurements;
        }
    }

    /**
     * {@inheritdoc}
     */
    public function process($item): array
    {
        if ($item['type'] === \AttributeTypes::METRIC || $item['type'] === \AttributeTypes::NUMBER) {
            $measureSign = $item['measureSign'];
            unset($item['measureSign']);
            if (!empty($measureSign)) {
                $metricData = $this->getMetricData($measureSign);
                if (!empty($metricData)) {
                    $item = array_merge($item, $metricData);
                } else {
                    $item['type'] = \AttributeTypes::NUMBER;
                }
            }
        }

        return $item;
    }
     
    /**
    * @param string $unitCode
    *
    * @return array
    */
    public function getMetricData(string $unitCode): array
    {
        $metricData = [];
        foreach ($this->measuresConfig as $metricFamily => $metricFamilyConfig) {
            foreach ($metricFamilyConfig['units'] as $unit => $unitConfig) {
                if (isset($unitConfig['symbol']) && $unitConfig['symbol'] === $unitCode) {
                    $metricData['metric_family'] = $metricFamily;
                    $metricData['default_metric_unit'] = $metricFamilyConfig['standard'];
                    break;
                }
            }
        }

        return $metricData;
    }

}
