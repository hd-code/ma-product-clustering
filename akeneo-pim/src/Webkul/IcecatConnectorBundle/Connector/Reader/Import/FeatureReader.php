<?php

namespace Webkul\IcecatConnectorBundle\Connector\Reader\Import;

use Prewk\XmlStringStreamer;
use SimpleXMLElement;
use Webkul\IcecatConnectorBundle\Component\AttributeTypeResolver;
use Webkul\IcecatConnectorBundle\Component\HttpClient;
use Webkul\IcecatConnectorBundle\Component\IcecatEndpoints;
use Webkul\IcecatConnectorBundle\Component\IcecatLocales;
use Webkul\IcecatConnectorBundle\Component\MeasurementHandler;
use Webkul\IcecatConnectorBundle\Connector\Reader\Import\BaseReader;
use Webkul\IcecatConnectorBundle\Repository\IcecatMappingRepository;
$namespaceObject = new \Webkul\IcecatConnectorBundle\Listener\ClassDefinationForCompatibility();
$namespaceObject->checkVersionAndCreateClassAliases();

class FeatureReader extends BaseReader implements
\ItemReaderInterface,
\StepExecutionAwareInterface,
\InitializableInterface
{
    /** @const string */
    const XPATH_NAME = 'Names/Name[@langid=%s]';

    /** @const string */
    const FEATURE_XML_FILE = '/tmp/FeaturesList.xml';

    /** @var XmlStringStreamer */
    protected $xmlStreamer;

    /** @var \StepExecution */
    protected $stepExecution;

    /** @var HttpClient */
    private $httpClient;

    /** @var IcecatMappingRepository */
    private $icecatMappingRepository;

    /** @var array */
    private $localeMapping = [];

    /** @var array */
    private $locales = [];

    /** @var array */
    private $icecateLocaleMappingById =[];

    /** @var array */
    private $icecatAttributeToImport =[];

    /** @var array */
    protected $measuresConfig = [];
    
    /** @var array */
    protected $attributeTypeMapping;

    /** @var MeasurementHandler*/
    protected $measurementHandler;

    /**
     * @param HttpClient                   $httpClient
     * @param IcecatMappingRepository      $icecatMappingRepository
     * @param AttributeTypeResolver        $attributeTypeResolver
     * @param AttributeRepositoryInterface $attributeRepositary
     * @param MeasurementHandler           $measurementHandler
     */
    public function __construct(
        HttpClient $httpClient,
        IcecatMappingRepository $icecatMappingRepository,
        AttributeTypeResolver $attributeTypeResolver,
        \AttributeRepositoryInterface $attributeRepositary,
        MeasurementHandler $measurementHandler
    ) {
        $this->httpClient = $httpClient;
        $this->icecatMappingRepository = $icecatMappingRepository;
        $this->attributeTypeResolver = $attributeTypeResolver;
        $this->attributeRepositary = $attributeRepositary;
        $this->measurementHandler = $measurementHandler;
    }

    /**
     * {@inheritdoc}
     */
    public function initialize()
    {
        if (null === $this->xmlStreamer) {
            $jobParameters = $this->stepExecution->getJobParameters();
            $localeMapping = $this->icecatMappingRepository->findOneBySection('webkul_icecat_locale_mapping');
            if (!$localeMapping) {
                throw new \Exception("Locale mapping not found, please map Icecat Locale with Akeneo Locale");
            }
            $measurements = $this->measurementHandler->getMeasurements();
            if(!empty($measurements)) {
                $this->measuresConfig = $measurements;
            }
            $attributeTypeMapping = $this->icecatMappingRepository->findOneBySection('icecate_attribute_type_mapping');
            $attributeTypeMapping = $attributeTypeMapping ? $attributeTypeMapping->getValue() : '';
            $this->attributeTypeMapping = $attributeTypeMapping ? json_decode($attributeTypeMapping, true) : [];
            $this->localeMapping = json_decode($localeMapping->getValue(), true);
            $jobLocale = $jobParameters->get('filters')['structure']['locale'];
            $this->jobLocales = gettype($jobLocale) !== 'array' ? [$jobLocale] : $jobLocale;
            $this->icecateLocaleMappingById = IcecatLocales::$IcecatLocalesMappingById;
            $this->icecatAttributeToImport  = $jobParameters->get('icecatAttributes');

            if (!file_exists(self::FEATURE_XML_FILE)) {
                $downloadDirectory = $jobParameters->get('downloadDirectory');
                $filename = $jobParameters->get('fileName');
                $url = $jobParameters->get('xmlFileUrl');
                $credentialMapping = $this->icecatMappingRepository->findOneBySection(['webkul_credential_mapping']);
                $credentials = $credentialMapping ? json_decode($credentialMapping->getValue(), true) : [];
                $this->httpClient->setCredentials($credentials);
                $this->stepExecution->addSummaryInfo('download.start', $filename);
                $downloadedFile = $this->httpClient->download($url, $filename, $downloadDirectory, true);
                $this->stepExecution->addSummaryInfo('download.success', $downloadedFile);
            }
            
            $this->xmlStreamer = XmlStringStreamer::createStringWalkerParser(self::FEATURE_XML_FILE, [
                'captureDepth' => 4,
            ]);
        }
    }

    /**
     * {@inheritdoc}
     */
    public function read()
    {
        $feature = null;
        while (!$feature && $node = $this->xmlStreamer->getNode()) {
            $featureXml = simplexml_load_string($node);
            if (!$featureXml) {
                return null;
            }

            $feature = $this->format($featureXml);
            if (!$feature) {
                continue;
            }

            $this->stepExecution->incrementSummaryInfo('read');
        }

        return $feature;
    }

    /**
     * @param SimpleXMLElement $xmlFeature object to format
     *
     * @return array
     */
    public function format(SimpleXMLElement $xmlFeature): ?array
    {
        $attribute = $xmlFeature->attributes();
        $code = 'icecat_'. (int) $attribute['ID'];
        if (!in_array($code, $this->icecatAttributeToImport)) {
            return null;
        }
        
        $attributeExist = $this->attributeRepositary->findOneByIdentifier($code);
        if ($attributeExist) {
            $this->stepExecution->incrementSummaryInfo('read');
            $this->stepExecution->incrementSummaryInfo('process');
            return null;
        }

        $measure = $xmlFeature->Measure;
        $measureSign = $measure ? (string) $measure->attributes()['Sign'] : null;
        if (in_array($measureSign, $this->ignoredSigns)) {
            return null;
        }
        $attributeType = $this->attributeTypeResolver->validateAttributeType((string) $attribute['Type'], $measureSign);
        if (!$attributeType) {
            throw new \InvalidArgumentException(sprintf('Unresolvable type %s for feature id %s', $attribute['feature_type'], $attribute['feature_id']));
        }
        
        $attributeLabels = $this->getLabels($xmlFeature);

        return $this->convertAttributeData($attribute, $attributeLabels, $measureSign, $attributeType);
    }

    /**
    * @param SimpleXMLElement $xmlFeature object to format
    * @param array            $attributeLabels
    * @param string|null      $measureSign
    * @param string           $attributeType
    *
    * @return array
    */
    public function convertAttributeData(SimpleXMLElement $attribute, array $attributeLabels, ?string $measureSign, string $attributeType): ?array
    {
        $code = 'icecat_'. (int) $attribute['ID'];
        $attributeType  = isset($this->attributeTypeMapping[$code]) ? $this->attributeTypeMapping[$code]  : $attributeType;
        $item = [
            'code'                   => $code,
            'localizable'            => true,
            'scopable'               => true,
            'sort_order'             => (int) $attribute['ID'],
            'type'                   => $attributeType,
            'unique'                 => false,
            'useable_as_grid_filter' => false,
            'group'                  => 'other',
        ];

        $item['wysiwyg_enabled'] =  $item['type'] === \AttributeTypes::TEXTAREA ? true : null;
        if ($item['type'] === \AttributeTypes::METRIC || $item['type'] === \AttributeTypes::NUMBER) {
            if (!empty($measureSign)) {
                $metricData = $this->getMetricData($measureSign);
                if (!empty($metricData)) {
                    $item = array_merge($item, $metricData);
                } else {
                    $item['type'] = \AttributeTypes::NUMBER;
                }
            }
            $item["negative_allowed"] = false;
        }
        if (in_array(
            $item['type'],
            [\AttributeTypes::NUMBER, \AttributeTypes::PRICE_COLLECTION, \AttributeTypes::METRIC]
        )
                ) {
            $item['decimals_allowed'] = true;
        }

        return array_merge($item, $attributeLabels);
    }

    /**
    * @param SimpleXMLElement $xmlFeature
    *
    * @return array
    */
    public function getLabels(SimpleXMLElement $xmlFeature): array
    {
        $attributeLabels = [];
        foreach ($this->jobLocales as $jobLocaleCode) {
            if (isset($this->localeMapping[$jobLocaleCode]) && isset($this->icecateLocaleMappingById[$this->localeMapping[$jobLocaleCode]])) {
                if ($label = $xmlFeature->xpath(sprintf(self::XPATH_NAME, $this->icecateLocaleMappingById[$this->localeMapping[$jobLocaleCode]]))) {
                    $attributeLabels['labels'][$jobLocaleCode] = (string) $label[0];
                }
            }
        }

        return $attributeLabels;
    }

    /**
    *  @param string $unitCode
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

    /**
     * {@inheritdoc}
     */
    public function setStepExecution(\StepExecution $stepExecution)
    {
        $this->stepExecution = $stepExecution;
    }

}
