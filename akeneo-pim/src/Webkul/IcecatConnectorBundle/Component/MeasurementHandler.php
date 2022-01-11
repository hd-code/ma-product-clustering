<?php

namespace Webkul\IcecatConnectorBundle\Component;

class MeasurementHandler
{
    /** @var array */
    protected $measuresConfig = [];

    /** @var */
    protected $measurementFamilyRepository;

    /**
     * @param array|null                   $measures
     * @param                              $measurementFamilyRepository
     */
    public function __construct(
        ?array $measures,
        $measurementFamilyRepository
    ) {
        if($measures) {
            $this->measuresConfig = $measures['measures_config'];
        }
        $this->measurementFamilyRepository = $measurementFamilyRepository;
    }

    /**
    * @return array
    */
    public function getMeasurements()
    {
        $normalizedMeasurementFamilies = [];
        if($this->measurementFamilyRepository) {
            $measurementFamiles = $this->measurementFamilyRepository->all();
            if(!empty($measurementFamiles)) {
                foreach($measurementFamiles as $family) {
                    $normalizedMeasurementFamily = $family->normalize();
                    $normalizedMeasurementFamilies[$normalizedMeasurementFamily['code']] = [
                        'standard' => $normalizedMeasurementFamily['standard_unit_code'],
                        'units' => $normalizedMeasurementFamily['units'],
                    ];
                }
            }
        } else {
            return $this->measuresConfig;
        }

        return $normalizedMeasurementFamilies;
    }
}
