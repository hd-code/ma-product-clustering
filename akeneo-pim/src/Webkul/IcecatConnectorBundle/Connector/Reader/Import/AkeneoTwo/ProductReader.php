<?php

namespace Webkul\IcecatConnectorBundle\Connector\Reader\Import\AkeneoTwo;

$namespaceObject = new \Webkul\IcecatConnectorBundle\Listener\ClassDefinationForCompatibility();
$namespaceObject->checkVersionAndCreateClassAliases();

use Webkul\IcecatConnectorBundle\Repository\IcecatMappingRepository;
use Webkul\IcecatConnectorBundle\Component\HttpClient;
use Webkul\IcecatConnectorBundle\Component\EnrichProduct;
use Webkul\IcecatConnectorBundle\Component\IcecatEndpoints;
use Webkul\IcecatConnectorBundle\Component\IcecatLocales;

$namespaceObject = new \Webkul\IcecatConnectorBundle\Listener\ClassDefinationForCompatibility();
$namespaceObject->checkVersionAndCreateClassAliases();

class ProductReader extends \DatabaseProductReader
{
    /** @var ProductQueryBuilderFactoryInterface */
    protected $pqbFactory;

    /** @var ChannelRepositoryInterface */
    protected $channelRepository;

    /** @var MetricConverter */
    protected $metricConverter;

    /** @var StepExecution */
    protected $stepExecution;

    /** @var CursorInterface */
    protected $products;
    
    /** @var string */
    protected $productId;

    /** @var string */
    protected $vendor;

    /** @var IcecatMappingRepository */
    private $icecatMappingRepository;

    /** @var \AttributeRepositoryInterface */
    protected $attributeRepository;

    /** @var HttpClient */
    protected $httpClient;

    /** @var EnrichProduct */
    protected $enrichProduct;

    /** @var string */
    protected $fallbackLocale;

    /** @var array */
    protected $icecatLocales;

    /** @var string */
    protected $scope;

    /** @var array */
    protected $attributeMappingData;

    /** @var array */
    protected $extraAttributeMapping = [];

    /** @var boolean */
    protected $downloadImage;

    /** @var bool */
    private $firstRead = true;

    /**
     * @param \ProductQueryBuilderFactoryInterface $pqbFactory
     * @param \ChannelRepositoryInterface          $channelRepository
     * @param \CompletenessManager                 $completenessManager
     * @param \MetricConverter                     $metricConverter
     * @param \ConfigManager                       $configManager
     * @param bool                                 $generateCompleteness
     * @param \HttpClient                          $httpClient
     * @param \EnrichProduct                       $enrichProduct
     */
    public function __construct(
        \ProductQueryBuilderFactoryInterface $pqbFactory,
        \ChannelRepositoryInterface $channelRepository,
        \CompletenessManager $completenessManager,
        \MetricConverter $metricConverter,
        IcecatMappingRepository $icecatDataMappingRepository,
        $generateCompleteness,
        HttpClient $httpClient,
        EnrichProduct $enrichProduct,
        \AttributeRepositoryInterface $attributeRepository
    ) {
        parent::__construct($pqbFactory, $channelRepository, $completenessManager, $metricConverter, $generateCompleteness);
        $this->icecatMappingRepository = $icecatDataMappingRepository;
        $this->httpClient = $httpClient;
        $this->enrichProduct = $enrichProduct;
        $this->attributeRepository = $attributeRepository;
    }

    /**
     * {@inheritdoc}
     */
    public function initialize()
    {
        $jobParameters = $this->stepExecution->getJobParameters();
        $localeMapping = $this->icecatMappingRepository->findOneBySection('webkul_icecat_locale_mapping');
        if (!$localeMapping) {
            throw new \Exception("Locale mapping not found, please map Icecat Locale with Akeneo Locale");
        }
        if (!$attributemapping = $this->icecatMappingRepository->findOneBySection('webkul_attribute_mapping')) {
            throw new \Exception("Icecat attribute mapping not found");
        }
        
        $this->attributeMappingData = json_decode($attributemapping->getValue(), true);
       
        if (!isset($this->attributeMappingData['ean_attribute'])
            || !isset($this->attributeMappingData['product_id'])
            || !isset($this->attributeMappingData['vendor'])
        ) {
            throw new \Exception("Icecat Ean attribute or Product code or Vendor is not mapped with Akeneo attribute, please map this to enrich your product");
        }
        
        if ($extraAttributeMapping = $this->icecatMappingRepository->findOneBySection('icecate_attribute_data_mapping')) {
            $this->extraAttributeMapping = json_decode($extraAttributeMapping->getValue(), true);
        }

        $this->eanAttributeCode = $this->attributeMappingData['ean_attribute'];
        $this->productId        = $this->attributeMappingData['product_id'];
        $this->vendor           = $this->attributeMappingData['vendor'];
        $this->localeMapping    = json_decode($localeMapping->getValue(), true);
        $this->scope            = $jobParameters->get('filters')['structure']['scope'];
        $this->downloadImage    = $jobParameters->get('downloadImage');
        $this->fallbackLocale   = $jobParameters->get('fallbackLocale');
        $jobLocale              = $jobParameters->get('filters')['structure']['locale'];
        if (gettype($jobLocale) !== 'array') {
            $jobLocale = [$jobLocale];
        }

        $this->icecatLocales    = $this->getIcecatLocales($jobLocale);
        $credentialMapping = $this->icecatMappingRepository->findOneBySection(['webkul_credential_mapping']);
        $credentials = $credentialMapping ? json_decode($credentialMapping->getValue(), true) : [];
        $this->httpClient->setCredentials($credentials);

        parent::initialize();
    }

    /**
     * {@inheritdoc}
     */
    public function read()
    {
        $product = null;
        $standardProduct= null;
        if ($this->products->valid()) {
            if (!$this->firstRead) {
                $this->products->next();
            }
            $product = $this->products->current();
        }

        if (null !== $product) {
            $this->stepExecution->incrementSummaryInfo('read');

            $channel = $this->getConfiguredChannel();
            if (null !== $channel) {
                $this->metricConverter->convert($product, $channel);
            }

            $standardProduct = $this->formatProduct($product);
        }

        $this->firstRead = false;

        return $standardProduct;
    }
    
    /**
     * Format item
     *
     * @var \ProductInterface $item
     */
    protected function formatProduct($item)
    {
        $mainImageAttribute = null;
        $eanValue = $item->getValue($this->eanAttributeCode) ? (string)$item->getValue($this->eanAttributeCode)->getData() : '';
        $productId = $item->getValue($this->productId) ? (string)$item->getValue($this->productId)->getData() : '';
        $pimVendorAttribute = $this->attributeRepository->findOneByIdentifier($this->vendor);
        $isVendorScopable = $pimVendorAttribute && $pimVendorAttribute->isScopable() ? true : false;
        $isVendorisLocalizable = $pimVendorAttribute && $pimVendorAttribute->isLocalizable() ? true : false;
        $attributeAsImage = $item->getFamily() ? $item->getFamily()->getAttributeAsImage() : null;
        if ($attributeAsImage) {
            $mainImageAttribute = $attributeAsImage->getCode();
        }
        $standardProduct = [];
        $categories = [];
        if ($item->getCategories() && $categoriesArray= $item->getCategories()->toArray()) {
            foreach ($categoriesArray as $category) {
                $categories[] = $category->getCode();
            }
        }
        
        $productData = [
            'identifier'     => $item->getIdentifier(),
            'enabled'        => $item->isEnabled(),
            'categories'     => $categories,
            'family'         => $item->getFamily() ? $item->getFamily()->getCode() : '',
            'groups'         => [],
            'values'         => [],
        ];

        foreach ($this->icecatLocales as $akeneoLocale =>$icecatLocale) {
            $vendor = $this->vendor;
            if ($isVendorScopable) {
                $vendor .= '-'.$this->scope;
            }
            if ($isVendorisLocalizable) {
                $vendor .= '-'.$akeneoLocale;
            }

            $vendor = $item->getValues()->getByKey($vendor) ? (string) $item->getValues()->getByKey($vendor)->getData() : '';
            $query = sprintf(IcecatEndpoints::PRODUCT_WITH_EAN, trim($eanValue), $icecatLocale);
            $product = $this->httpClient->createRequest('GET', '', [
                'query' => $query,
            ]);

            $errorMessage = '';
            if (strpos($product, 'ErrorMessage')) {
                if (preg_match('/ErrorMessage="(.*?)"/', $product, $errorFound) == 1) {
                    $errorMessage = isset($errorFound[1]) ? $errorFound[1] : 'Not a valid responce from icecat';
                }
            }

            if ($errorMessage) {
                $query = sprintf(
                    IcecatEndpoints::PRODUCT_WITH_ID,
                    trim($productId),
                    trim($vendor),
                    $icecatLocale
                );
                $product = $this->httpClient->createRequest('GET', '', [
                    'query' => $query,
                ]);
                
                $otherErrorMessage = '';
                if (strpos($product, 'ErrorMessage')) {
                    if (preg_match('/ErrorMessage="(.*?)"/', $product, $errorFound) == 1) {
                        $otherErrorMessage = isset($errorFound[1]) ? $errorFound[1] : 'Not a valid responce from icecat';
                    }
                }

                if ($otherErrorMessage) {
                    $errorMessage = $otherErrorMessage;
                } else {
                    $errorMessage = '';
                }
            }
           
            if ($errorMessage) {
                $this->stepExecution->addWarning(
                    $errorMessage,
                    [],
                    new \DataInvalidItem([
                        'debug_line' => __LINE__,
                        'icecat_locale' => $icecatLocale,
                        $this->eanAttributeCode => $eanValue,
                        $this->productId => $productId,
                        $this->vendor => $vendor,
                    ])
                );
                continue;
            }

            $context = [
                'scope'            => $this->scope,
                'locale'           => $akeneoLocale,
                'downloadImage'    => $this->downloadImage,
                'attributeAsImage' => $mainImageAttribute,
                'fallback_locale'  => $this->fallbackLocale,
            ];
           
            $standardProduct = array_merge_recursive(
                $standardProduct,
                $this->enrichProduct->enrich(
                    $this->attributeMappingData,
                    $this->extraAttributeMapping,
                    $product,
                    $context
                )
            );
        }

        return array_merge($productData, $standardProduct);
    }

    /**
    * @param array $jobLocales
    *
    * @return array
    */
    public function getIcecatLocales(array $jobLocales): array
    {
        $icecatLocalesCode = [];
        $icecatLocaleIds = IcecatLocales::$IcecatLocalesMappingById;
        foreach ($jobLocales as $jobLocaleCode) {
            if (isset($this->localeMapping[$jobLocaleCode]) && isset($icecatLocaleIds[$this->localeMapping[$jobLocaleCode]])) {
                $icecatLocalesCode[$jobLocaleCode] =$this->localeMapping[$jobLocaleCode];
            }
        }
        return $icecatLocalesCode;
    }
}
