<?php

namespace Webkul\IcecatConnectorBundle\Connector\Reader\Import;

use Prewk\XmlStringStreamer;
use SimpleXMLElement;
use Webkul\IcecatConnectorBundle\Component\AttributeTypeResolver;
use Webkul\IcecatConnectorBundle\Component\HttpClient;
use Webkul\IcecatConnectorBundle\Component\IcecatEndpoints;
use Webkul\IcecatConnectorBundle\Component\IcecatLocales;
use Webkul\IcecatConnectorBundle\Connector\Reader\Import\BaseReader;
use Webkul\IcecatConnectorBundle\Repository\IcecatMappingRepository;

$namespaceObject = new \Webkul\IcecatConnectorBundle\Listener\ClassDefinationForCompatibility();
$namespaceObject->checkVersionAndCreateClassAliases();

class FeatureMappingReader extends BaseReader implements
\ItemReaderInterface,
\StepExecutionAwareInterface,
\InitializableInterface
{
    /**
     * @const string
     */
    const XPATH_NAME = 'Names/Name[@langid=%s]';

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

    /**
     * @param HttpClient                   $httpClient
     * @param IcecatMappingRepository      icecatMappingRepository
     * @param AttributeTypeResolver        $attributeTypeResolver
     */
    public function __construct(
        HttpClient $httpClient,
        IcecatMappingRepository $icecatMappingRepository,
        AttributeTypeResolver $attributeTypeResolver
    ) {
        $this->httpClient = $httpClient;
        $this->icecatMappingRepository = $icecatMappingRepository;
        $this->attributeTypeResolver = $attributeTypeResolver;
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

            $this->localeMapping = json_decode($localeMapping->getValue(), true);
            $jobLocale = $jobParameters->get('filters')['structure']['locale'];
            $this->jobLocales = gettype($jobLocale) !== 'array' ? [$jobLocale] : $jobLocale;
            $this->icecateLocaleMappingById = IcecatLocales::$IcecatLocalesMappingById;
            $filename = $jobParameters->get('fileName');
            $url = $jobParameters->get('xmlFileUrl');
            $credentialMapping = $this->icecatMappingRepository->findOneBySection(['webkul_credential_mapping']);
            $credentials = $credentialMapping ? json_decode($credentialMapping->getValue(), true) : [];
            $this->httpClient->setCredentials($credentials);
            $downloadDirectory = $jobParameters->get('downloadDirectory');
            $this->stepExecution->addSummaryInfo('download.start', $filename);
            $downloadedFile = $this->httpClient->download($url, $filename, $downloadDirectory, true);
            $this->stepExecution->addSummaryInfo('download.success', $downloadedFile);
            $this->xmlStreamer = XmlStringStreamer::createStringWalkerParser($downloadedFile, [
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
        $measure = $xmlFeature->Measure;
        $measureSign = $measure ? (string) $measure->attributes()['Sign'] : null;
        if (in_array($measureSign, $this->ignoredSigns)) {
            return null;
        }

        $attribute = $xmlFeature->attributes();
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
        $attributeData = [
            'code'        => 'icecat_'. (int) $attribute['ID'],
            'sort_order'  => (int) $attribute['ID'],
            'type'        => $attributeType,
            'measureSign' => $measureSign
        ];

        $attributeData = array_merge($attributeData, $attributeLabels);
    
        return $attributeData;
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
     * {@inheritdoc}
     */
    public function setStepExecution(\StepExecution $stepExecution)
    {
        $this->stepExecution = $stepExecution;
    }
}
