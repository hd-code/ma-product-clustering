<?php

namespace Webkul\IcecatConnectorBundle\Component;

$namespaceObject = new \Webkul\IcecatConnectorBundle\Listener\ClassDefinationForCompatibility();
$namespaceObject->checkVersionAndCreateClassAliases();

class AttributeTypeResolver
{
    /**
     * @var array
     */
    private $attributeTypes = [
            ''                => \AttributeTypes::TEXT,
            '2d'              => \AttributeTypes::TEXT,
            '3d'              => \AttributeTypes::TEXT,
            'alphanumeric'    => \AttributeTypes::TEXT,
            'contrast ratio'  => \AttributeTypes::TEXT,
            'ratio'           => \AttributeTypes::TEXT,
            'text'            => \AttributeTypes::TEXT,
            'textarea'        => \AttributeTypes::TEXTAREA,
            'y_n'             => \AttributeTypes::BOOLEAN,
            'y_n_o'           => \AttributeTypes::OPTION_SIMPLE_SELECT,
            'dropdown'        => \AttributeTypes::OPTION_SIMPLE_SELECT,
            'multi_dropdown'  => \AttributeTypes::OPTION_SIMPLE_SELECT,
            'range'           => \AttributeTypes::TEXT,
    ];

    /**
     * @param string $icecatAttributeType
     * @param string|null $icecatFeatureUnit
     *
     * @return string
     *
     */
    public function validateAttributeType(string $icecatAttributeType, ?string $icecatFeatureUnit)
    {
        $attributeType = '';
        if (array_key_exists($icecatAttributeType, $this->attributeTypes)) {
            $attributeType = $this->attributeTypes[$icecatAttributeType];
        } elseif ($icecatAttributeType === 'numerical') {
            if (empty($icecatFeatureUnit)) {
                $attributeType =  \AttributeTypes::NUMBER;
            } else {
                $attributeType =  \AttributeTypes::METRIC;
            }
        }
        return $attributeType;
    }
}
