<?php

namespace Webkul\IcecatConnectorBundle\Component;

$namespaceObject = new \Webkul\IcecatConnectorBundle\Listener\ClassDefinationForCompatibility();
$namespaceObject->checkVersionAndCreateClassAliases();

use Symfony\Component\Form\FormFactoryInterface;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Serializer\Normalizer\NormalizerInterface;
use SimpleXMLElement;
use Webkul\IcecatConnectorBundle\Component\MeasurementHandler;
use Webkul\IcecatConnectorBundle\Component\TempStorageDir;

/**
 * Convert XML product string into an Akeneo standard array format
 */
class EnrichProduct
{
    /** @var array */
    protected $measuresConfig = [];

    /** @var \AttributeRepositoryInterface */
    protected $attributeRepository;

    /** @var \AttributeOptionRepository */
    protected $attributeOptionRepository;

    /** @var TempStorageDir */
    protected $uploadDir;

    /** @var string */
    protected $locale;

    /** @var string */
    protected $scope;

    /** @var array */
    protected $akeneoLocales;

    /** @var \SimpleFactoryInterface  */
    protected $optionFactory;

    /** @var FormFactoryInterface */
    protected $formFactory;

    /** @var NormalizerInterface */
    protected $optionNormalizer;

    /** @var \SaverInterface */
    protected $optionSaver;

    /** @var MeasurementHandler*/
    protected $measurementHandler;

    /**
     * @param \AttributeRepositoryInterface $attributeRepository
     * @param \AttributeOptionRepository $attributeOptionRepository,
     * @param TempStorageDir                $mediaStorer,
     * @param \SimpleFactoryInterface       $optionFactory,
     * @param FormFactoryInterface          $formFactory,
     * @param NormalizerInterface           $optionNormalizer,
     * @param \SaverInterface               $optionSaver
     * @param MeasurementHandler            $measurementHandler
     */
    public function __construct(
        \AttributeRepositoryInterface $attributeRepository,
        \AttributeOptionRepository $attributeOptionRepository,
        TempStorageDir $mediaStorer,
        \SimpleFactoryInterface $optionFactory,
        FormFactoryInterface $formFactory,
        NormalizerInterface $optionNormalizer,
        \SaverInterface $optionSaver,
        MeasurementHandler $measurementHandler
    ) {
        $this->attributeRepository = $attributeRepository;
        $this->attributeOptionRepository = $attributeOptionRepository;
        $this->uploadDir = $mediaStorer->getTmpStorageDirectory();
        $this->optionFactory = $optionFactory;
        $this->formFactory = $formFactory;
        $this->optionNormalizer = $optionNormalizer;
        $this->optionSaver = $optionSaver;
        $this->measurementHandler = $measurementHandler;
        $measurements = $this->measurementHandler->getMeasurements();
        if(!empty($measurements)) {
            $this->measuresConfig = $measurements;
        }
    }

    /**
     * {@inheritdoc}
     */
    public function enrich(array $attributeMappingData, array $extraAttributeMapping, string $xmlString, array $context = [])
    {
        $standardItem     = [];
        $this->locale     = $context['locale'];
        $this->scope      = $context['scope'];
        $attributeAsImage = $context['attributeAsImage'];
        $downloadImage    = $context['downloadImage'];
        $this->akeneoLocales    = $context['akeneoLocales'];
        $fallbackLocale   = $context['fallback_locale'];
        $simpleXmlNode    = simplexml_load_string($xmlString);
        $icecatProduct    = $simpleXmlNode->Product;
        $standardItem     = $this->getCommonAttributeInfo($standardItem, $icecatProduct, $attributeMappingData, $fallbackLocale, $attributeAsImage, $downloadImage);
        foreach ($icecatProduct->ProductFeature as $xmlFeature) {
            $featureId = (int)$xmlFeature->Feature->attributes()['ID'];
            $icecatCode = 'icecat_'.$featureId;
            if (isset($extraAttributeMapping[$icecatCode])
                && $pimCode = $extraAttributeMapping[$icecatCode]
            ) {
                $pimAttribute = $this->attributeRepository->findOneByIdentifier($pimCode);
                if (null === $pimAttribute
                    || (!$pimAttribute->isLocalizable() && $this->locale != $fallbackLocale)) {
                    continue;
                }

                $code = (string) $xmlFeature->attributes()['ID'];
                $value = (string)$xmlFeature->attributes()['Presentation_Value'];
                $localValue = (string)$xmlFeature->LocalValue->attributes()['Value'];
                $unit = (string)$xmlFeature->LocalValue->Measure->Signs->Sign;
                $standardItem = $this->addProductValue(
                    $standardItem,
                    $pimAttribute,
                    $value,
                    $localValue,
                    $unit,
                    $code
                );
            }
        }

        return $standardItem;
    }

    /**
     * @param array            $standardItem
     * @param SimpleXMLElement $icecatProduct
     * @param array            $attributeMappingData
     * @param string           $fallbackLocale
     * @param string           $attributeAsImage
     * @param bool             $downloadImage
     *
     * @return array
     */
    protected function getCommonAttributeInfo(array $standardItem, SimpleXMLElement $icecatProduct, array $attributeMappingData, string $fallbackLocale, ?string $attributeAsImage, bool $downloadImage):array
    {
        foreach ($attributeMappingData as $attributeKey => $akeneoAttribute) {
            if (!is_array($akeneoAttribute)) {
                $pimAttribute = $this->attributeRepository->findOneByIdentifier($akeneoAttribute);
                if (null === $pimAttribute
                    || (!$pimAttribute->isLocalizable() && $this->locale != $fallbackLocale)) {
                    continue;
                }
            }

            switch ($attributeKey) {
                case 'Name':
                case 'Title':
                    if (isset($icecatProduct->attributes()[$attributeKey])) {
                        $value = (string)$icecatProduct->attributes()[$attributeKey];
                        $standardItem = $this->addProductValue(
                            $standardItem,
                            $pimAttribute,
                            null,
                            $value,
                            null
                        );
                    }
                    break;
                case 'summary_description':
                case 'short_summary_description':
                case 'description':
                case 'short_description':
                case 'vendor':
                    if ($icecatProduct->SummaryDescription) {
                        if ($attributeKey === 'summary_description') {
                            $value = (string)$icecatProduct->SummaryDescription->LongSummaryDescription;
                        } elseif ($attributeKey === 'short_summary_description') {
                            $value = (string)$icecatProduct->SummaryDescription->ShortSummaryDescription;
                        } elseif ($attributeKey === 'description') {
                            $value = (string)$icecatProduct->ProductDescription->attributes()['LongDesc'];
                        } elseif ($attributeKey === 'short_description') {
                            $value = (string)$icecatProduct->ProductDescription->attributes()['ShortDesc'];
                        } else {
                            $value = (string)$icecatProduct->Supplier->attributes()['Name'];
                        }

                        $standardItem = $this->addProductValue(
                            $standardItem,
                            $pimAttribute,
                            null,
                            $value,
                            null
                        );
                    }
                    break;

                case 'pictures':
                    $icecatProductGallery = (array)$icecatProduct->ProductGallery;
                    if (isset($icecatProductGallery['ProductPicture']) && $downloadImage) {
                        $productPicture = $icecatProductGallery['ProductPicture'];
                        if ($productPicture instanceof SimpleXMLElement) {
                            $productPicture = [$productPicture];
                        }
                        foreach ($akeneoAttribute as $mainImageKey =>$mainImage) {
                            if ($attributeAsImage !== $mainImage) {
                                continue;
                            }
                            $mainImageAttribute = $this->attributeRepository->findOneByIdentifier($mainImage);
                            unset($akeneoAttribute[$mainImageKey]);
                            if (null === $mainImageAttribute
                                || (!$mainImageAttribute->isLocalizable() && $this->locale != $fallbackLocale)) {
                                continue;
                            }
                            $picture = $this->getPicture($mainImage, $productPicture, true);
                            if ($picture) {
                                $standardItem = $this->addProductValue(
                                    $standardItem,
                                    $mainImageAttribute,
                                    null,
                                    $picture,
                                    null
                                );
                            }
                        }
                        
                        foreach ($akeneoAttribute as $imageKey =>$imageAttribute) {
                            if (empty($productPicture)) {
                                break;
                            }

                            $imagePimAttribute = $this->attributeRepository->findOneByIdentifier($imageAttribute);
                            unset($akeneoAttribute[$imageKey]);

                            if (null === $imagePimAttribute) {
                                continue;
                            }

                            $picture = $this->getPicture($imageAttribute, $productPicture, false);
                            if ($picture) {
                                $standardItem = $this->addProductValue(
                                    $standardItem,
                                    $imagePimAttribute,
                                    null,
                                    $picture,
                                    null
                                );
                            }
                        }
                    }
                    break;
                default:
            }
        }

        return $standardItem;
    }

    /**
     * @param array       $standardItem
     * @param string      $locale
     * @param string      $pimCode
     * @param mixed       $value
     * @param mixed       $localValue
     * @param string      $unit
     * @param string|null $code
     * 
     * @return array
     */
    protected function addProductValue(array $standardItem, $pimAttribute, $value, $localValue, $unit, $optionCode = null): array
    {
        $locale = $this->locale;
        $scope  = $this->scope;
        if (!$pimAttribute->isLocalizable()) {
            $locale = null;
        }

        if (!$pimAttribute->isScopable()) {
            $scope = null;
        }
        
        if (\AttributeTypes::METRIC === $pimAttribute->getType() && null !== $unit) {
            // $attributeMetricUnit = $this->getMetricData($unit);
            // $unit = $attributeMetricUnit ? $attributeMetricUnit : $pimAttribute->getDefaultMetricUnit();
            $unit = $pimAttribute->getDefaultMetricUnit();
            $localValue = $this->formatMetricValue($localValue, $unit);
        } elseif (\AttributeTypes::PRICE_COLLECTION === $pimAttribute->getType() && null !== $unit) {
            $localValue = $this->formatPriceValue($localValue, $unit);
        } elseif (\AttributeTypes::BOOLEAN === $pimAttribute->getType()) {
            $localValue = $value == 'Y' ? true : false;
        } elseif (\AttributeTypes::NUMBER === $pimAttribute->getType()) {
            $localValue = $this->formatNumberValue($value);
        } elseif (\AttributeTypes::OPTION_MULTI_SELECT === $pimAttribute->getType()
            || \AttributeTypes::OPTION_SIMPLE_SELECT === $pimAttribute->getType()
        ) {
            $localValue = $value ? $this->findOptionCode($pimAttribute, $value, $optionCode) : null;
        }
        // elseif (\AttributeTypes::OPTION_MULTI_SELECT === $pimAttribute->getType()) {
            // $icecatValues = explode(',', $value);
            // $pimValues = [];
            // foreach ($icecatValues as $icecatValue) {
            //     if ($icecatValue) {
            //         $pimValues[] = $this->findOptionCode($pimAttribute, $icecatValue);
            //     }
            // }
            // $localValue = !empty($pimValues) ? $pimValues : null;
        // } 
        

        if ($localValue !== '') {
            $standardItem['values'][$pimAttribute->getCode()] = [
                [
                    'data'   => $localValue,
                    'locale' => $locale,
                    'scope'  => $scope,
                ],
            ];
        }
        
        return $standardItem;
    }

    /**
     * @param string $icecatValue
     * @param string $icecatUnit
     *
     * @return array
     */
    protected function formatMetricValue(string $icecatValue, string $unit): array
    {
        return [
            'amount' => str_replace(',', '.', $icecatValue),
            'unit' => $unit,
        ];
    }

    /**
     * @param string $icecatValue
     * @param string $icecatUnit
     *
     * @return array
     */
    protected function formatPriceValue(string $icecatValue, string $icecatUnit): array
    {
        return [
            [
                'data' => $icecatValue,
                'currency' => $icecatUnit,
            ],
        ];
    }

    /**
     * @param string $icecatValue
     *
     * @return string|int
     */
    protected function formatNumberValue(string $icecatValue)
    {
        $intValue = filter_var($icecatValue, FILTER_VALIDATE_INT);

        return false !== $intValue ? $intValue : $icecatValue;
    }

    /**
     * @param \AttributeInterface $pimAttribute
     * @param string              $icecatValue
     * @param string              $optionCode
     *
     * @return string
     */
    protected function findOptionCode(
        \AttributeInterface $pimAttribute, 
        string $icecatValue,
        string $optionCode
    ) {
        $result = $this->attributeOptionRepository->createQueryBuilder('o')
            ->select('o.code')
            ->innerJoin('o.attribute', 'a')
            ->leftJoin('o.optionValues', 't')
            ->Where('o.code = :option_code')
            ->orWhere('t.value IN (:option_labels)')
            ->andWhere('a.code = :attribute_code')
            ->setParameters(['attribute_code' => $pimAttribute->getCode(),'option_code' => $optionCode,'option_labels' => [$icecatValue]])
            ->setMaxResults(1)
            ->getQuery()
            ->getOneOrNullResult();

        if(isset($result['code'])) {
            $option = $this->attributeOptionRepository->findOneByCode($result['code']);
            if($option) {
                $optionLabels = $option->getOptionValues()->toArray();
                $optionData['id'] = $option->getId();
                $optionData['code'] = $option->getCode();
                $optionData['optionValues'] = [];
                foreach ($this->akeneoLocales as $locale) {
                    if(isset($optionLabels[$locale])) {
                        $optionLabel = $optionLabels[$locale]->getValue();
                        if($this->locale == $locale) {
                            $optionLabel = $icecatValue;
                        }
                        $optionData['optionValues'][$locale] = [
                            'locale' => $locale,
                            'value' => $optionLabel,
                            'id' => $optionLabels[$locale]->getId(),
                        ];
                    }
                }
                if(!empty($optionData['optionValues'])) {
                    $this->manageFormSubmission($option, $optionData);
                }
            }
            
            return $result['code'];
        }

        return $this->createOption($pimAttribute, $icecatValue, $optionCode);

    }

    /**
     * Create attribute option
     *
     * @param \AttributeInterface $attribute
     * @param string              $optionValue
     * @param string              $optionCode
     *
     * @return null|string
     */
    protected function createOption(\AttributeInterface $attribute, string $optionValue, string $optionCode)
    {
        // $optionCode = '';
        $optionData = [];
        foreach ($this->akeneoLocales as $locale) {
            // $translatedLocale = $locale;
            // $optionLabel = $this->translate($optionValue, $this->locale, $locale);
            // if (!$optionCode) {
            //     $optionCode = $this->convertToCode($optionLabel);
            // }
            $optionData['optionValues'][$locale] = [
                'locale' => $locale,
                'value' => $optionValue,
                'id' => null,
            ];
        }

        // if (!$optionCode) {
        //     return null;
        // }
        $optionData['code'] = $optionCode;

        $attributeOption = $this->optionFactory->create();
        $attributeOption->setAttribute($attribute);

        return $this->manageFormSubmission($attributeOption, $optionData);
    }

    /**
     * Translate string into other language
     *
     * @param string $string
     * @param string $currentLocale
     * @param string $convertingLocale
     *
     * @return string
     */
    protected function translate($string, $currentLocale, $convertingLocale)
    {
        $result = file_get_contents("https://translate.googleapis.com/translate_a/single?client=gtx&ie=UTF-8&oe=UTF-8&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&dt=at&sl=".$currentLocale."&tl=".$convertingLocale."&hl=hl&q=".urlencode($string), $_SERVER['DOCUMENT_ROOT']."/transes.html");
        $result = json_decode($result);

        return $result[0][0][0];
    }
    
    /**
     *
     * @param string $imageAttributes
     * @param string $attributeAsImage
     * @param string $productImages
     *
     * @return null|string
     */
    protected function getPicture(string $imageAttribute, array &$productImages, bool $isMainImage): ?string
    {
        $picture = null;
        foreach ($productImages as $xmlPictureKey =>$xmlPicture) {
            $url = (string)$xmlPicture->attributes()['Pic500x500'];
            if (!$url) {
                $url = (string)$xmlPicture->attributes()['Pic'];
            }

            if (empty($url)) {
                continue;
            }

            $isMain = (string)$xmlPicture->attributes()['IsMain'];
            if ($isMainImage) {
                if ($isMain !== "Y") {
                    continue;
                }

                $imagePath = $this->imageStorer($url);
                if ($imagePath) {
                    $picture = $imagePath;
                }

                unset($productImages[$xmlPictureKey]);
            } else {
                if ($imagePath = $this->imageStorer($url)) {
                    $picture = $imagePath;
                    unset($productImages[$xmlPictureKey]);
                }
            }
            
            break;
        }

        return $picture;
    }

    /**
     * Store image at given path
     *
     * @param string $filePath
     *
     * @return string
     */
    protected function imageStorer($filePath)
    {
        stream_context_set_default([
            'ssl' => [
                'verify_peer' => false,
                'verify_peer_name' => false,
            ],
        ]);

        @get_headers($filePath);
        $fileName = explode('/', $filePath);
        $fileName = end($fileName);

        $localpath = $this->uploadDir."/tmpstorage/".$fileName;
        if (!file_exists(dirname($localpath))) {
            mkdir(dirname($localpath), 0777, true);
        }

        if (file_exists($localpath)) {
            if (!exif_imagetype($localpath) || !(filesize($localpath) > 0)) {
                $this->customPutContents($localpath, $filePath);
            }
        } else {
            $this->customPutContents($localpath, $filePath);
        }

        return $localpath;
    }

    public function customPutContents($local_path='', $source_url='')
    {
        $time_limit = ini_get('max_execution_time');
        $memory_limit = ini_get('memory_limit');
    
        set_time_limit(0);
        ini_set('memory_limit', '-1');
        
        $remote_contents=$this->getDownloadRemoteImage($source_url);
        
        file_put_contents($local_path, $remote_contents);
    
        set_time_limit($time_limit);
        ini_set('memory_limit', $memory_limit);
    }

    public function getDownloadRemoteImage($url)
    {
        $ch = \curl_init($url);
        \curl_setopt($ch, CURLOPT_HEADER, 0);
        \curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        \curl_setopt($ch, CURLOPT_BINARYTRANSFER, 1);
        \curl_setopt($ch, CURLOPT_TIMEOUT, 300);

        $rawImage = \curl_exec($ch);
        \curl_close($ch);
        
        return $rawImage;
    }

    /**
     * Manage form submission of an attribute option
     *
     * @param \AttributeOptionInterface $attributeOption
     * @param array                     $data
     *
     * @return null|string
     */
    protected function manageFormSubmission(
        \AttributeOptionInterface $attributeOption,
        array $data = []
    ) {
        if (class_exists('Akeneo\Pim\Structure\Bundle\Form\Type\AttributeOptionType')) {
            $form = $this->formFactory->createNamed('option', \Akeneo\Pim\Structure\Bundle\Form\Type\AttributeOptionType::class, $attributeOption);
        } else {
            $form = $this->formFactory->createNamed('option', \Pim\Bundle\EnrichBundle\Form\Type\AttributeOptionType::class, $attributeOption);
        }
        
        $form->submit($data, false);

        if ($form->isValid()) {
            $this->optionSaver->save($attributeOption);

            $option = $this->optionNormalizer->normalize($attributeOption, 'array', ['onlyActivatedLocales' => true]);
            return isset($option['code']) ? $option['code'] : null;
        }

        return null;
    }

    /**
     * Covert value to code
     *
     * @param string $name
     * @param string $substr
     *
     * @return string
     */
    public function convertToCode($name, $substr = true)
    {
        setlocale(LC_ALL, 'en_US.utf8');
        $name = iconv('utf-8', 'ascii//TRANSLIT', $name);
        $name = preg_replace('/[^a-zA-Z0-9\']/', '_', strtolower($name));
        $code = ltrim($name, '_');
        // $code = preg_replace(['#\s#', '#-#', '#[^a-zA-Z0-9_\s]#'], ['_', '_', ''], strtolower($name));
        // $code = preg_replace("/(_)\\1+/", "$1", $code);
        
        if ($substr) {
            $code = substr($code, 0, 100);
        }
        
        return $code;
    }

    /**
    * @param string $unitCode
    *
    * @return string|null
    */
    public function getMetricData(string $unitCode)
    {
        $attributeMetricFamily = null;
        foreach ($this->measuresConfig as $metricFamily => $metricFamilyConfig) {
            foreach ($metricFamilyConfig['units'] as $unit => $unitConfig) {
                if (isset($unitConfig['symbol']) && $unitConfig['symbol'] === $unitCode) {
                    $attributeMetricFamily = $unitConfig['code'];
                    break;
                }
            }
        }

        return $attributeMetricFamily;
    }
}
