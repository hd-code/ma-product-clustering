<?php

namespace Webkul\IcecatConnectorBundle\Controller;

use Doctrine\ORM\EntityManager;
use Oro\Bundle\SecurityBundle\Annotation\AclAncestor;
use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\Form\Form;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Validator\Constraints\NotBlank;
use Webkul\IcecatConnectorBundle\Component\HttpClient;
use Webkul\IcecatConnectorBundle\Component\IcecatEndpoints;
use Webkul\IcecatConnectorBundle\Component\IcecatLocales;
use Webkul\IcecatConnectorBundle\Component\Version;
use Webkul\IcecatConnectorBundle\Entity\IcecatMapping;
use Webkul\IcecatConnectorBundle\Repository\IcecatMappingRepository;
use Webkul\IcecatConnectorBundle\Repository\IcecatDataMappingRepository;
use Webkul\IcecatConnectorBundle\Repository\IcecatDataMappingSearchableRepository;

class MappingController extends Controller
{
    /** @const */
    const CREDENTIAL_MAPPING_SECTION = 'webkul_credential_mapping';

    /** @const */
    const ICECAT_LOCALE_MAPPING_SECTION = 'webkul_icecat_locale_mapping';

    /** @const */
    const ICECAT_ATTRIBUTE_MAPPING_SECTION = 'icecate_attribute_data_mapping';

    /** @const */
    const ICECAT_ATTRIBUTE_TYPE_MAPPING_SECTION = 'icecate_attribute_type_mapping';

    /** @const */
    const ATTRIBUTE_MAPPING_SECTION = 'webkul_attribute_mapping';

    /** @const */
    const UNAUTHORIZED = 'Unauthorized';
    
    /** @const */
    const NOT_FOUND = 'Not Found';

    /** @var  EntityManager */
    protected $entityManager;

    /** @var IcecatMappingRepository */
    protected $icecatMappingRepository;

    /** @var IcecatDataMappingRepository */
    protected $icecatDataMappingRepository;

    /** @var IcecatDataMappingSearchableRepository */
    protected $icecatDataMappingSearchableRepository;

    /** @var HttpClient */
    protected $httpClient;

    /**
     * @param IcecatMappingRepository               $icecateConfigRepository
     * @param IcecatDataMappingRepository           $icecatDataMappingRepository
     * @param IcecatDataMappingSearchableRepository $icecatDataMappingSearchableRepository
     * @param EntityManager                         $EntityManager
     * @param HttpClient                            $httpClient
     */
    public function __construct(
        IcecatMappingRepository               $icecatMappingRepository,
        IcecatDataMappingRepository           $icecatDataMappingRepository,
        IcecatDataMappingSearchableRepository $icecatDataMappingSearchableRepository,
        EntityManager                         $entityManager,
        HttpClient                            $httpClient
    ) {
        $this->icecatMappingRepository               = $icecatMappingRepository;
        $this->icecatDataMappingRepository           = $icecatDataMappingRepository;
        $this->icecatDataMappingSearchableRepository = $icecatDataMappingSearchableRepository;
        $this->entityManager                         = $entityManager;
        $this->httpClient                            = $httpClient;
    }

    /**
     * @AclAncestor("webkul_icecat_connector_configuration")
     *
     * @return JsonResponse
     */
    public function getAction(): JsonResponse
    {
        $mapping = $this->getMapping([
            'credentialMapping'     => self::CREDENTIAL_MAPPING_SECTION,
            'attributeMapping'      => self::ATTRIBUTE_MAPPING_SECTION,
            'icecatLocaleMapping'   => self::ICECAT_LOCALE_MAPPING_SECTION,
            'attributes'            => self::ICECAT_ATTRIBUTE_MAPPING_SECTION,
            'attributesType'        => self::ICECAT_ATTRIBUTE_TYPE_MAPPING_SECTION,
        ], true);

        return new JsonResponse($mapping);
    }

    /**
     * @AclAncestor("webkul_icecat_connector_configuration")
     *
     * @return JsonResponse
     */
    public function getDataMappingAction(): JsonResponse
    {
        $mapping = [];
        $icecatDataMappings = $this->icecatDataMappingRepository->findBy(['section' => self::ICECAT_ATTRIBUTE_MAPPING_SECTION]);
        if ($icecatDataMappings) {
            foreach ($icecatDataMappings as $icecatDataMapping) {
                $mapping[$icecatDataMapping->getCode()] = json_decode($icecatDataMapping->getValue(), true);
            }
        }
        $mapping['moduleVersion'] = Version::CURRENT_VERSION;
        
        return new JsonResponse($mapping);
    }

    /**
     * @AclAncestor("webkul_icecat_connector_configuration")
     *
     * @return JsonResponse
     */
    public function getIcecatAttributeAction(Request $request): JsonResponse
    {
        $mapping = [];
        $options = $request->query->get('options');
        $options['attributes'] = $request->query->get('attributes');
        $options['section'] = self::ICECAT_ATTRIBUTE_MAPPING_SECTION;
        $icecatDataMappings = $this->icecatDataMappingSearchableRepository->findBySearch(
            $request->query->get('search'),
            $options
        );

        if ($icecatDataMappings) {
            foreach ($icecatDataMappings as $icecatDataMapping) {
                $mapping[] = json_decode($icecatDataMapping->getValue(), true);
            }
        }

        return new JsonResponse($mapping);
    }

    /**
     * @AclAncestor("webkul_icecat_connector_configuration")
     *
     * @return JsonResponse
     */
    public function getIcecateLocalesAction(): JsonResponse
    {
        return new JsonResponse(IcecatLocales::$IcecatLocales);
    }
  
    /**
     * @AclAncestor("webkul_icecat_connector_configuration")
     *
     * @param Request $request
     *
     * @return JsonResponse
     */
    public function saveMappingAction(Request $request): JsonResponse
    {
        $params = json_decode($request->getContent(), true);
        $currentTab = $request->attributes->get('tab');
        switch ($currentTab) {
            case('credential'):
                if (isset($params['credentialMapping']['password'])
                    && $params['credentialMapping']['password'] === str_repeat('*', 20)) {
                    $credentialData = $this->getMapping([
                            'credentialMapping'     => self::CREDENTIAL_MAPPING_SECTION,
                        ], false);
                    $params['credentialMapping']['password'] = $credentialData['credentialMapping']['password'];
                }

                $response = $this->authenticateCredential($request, $params);
                if ($response['status'] !== Response::HTTP_OK) {
                    return new JsonResponse([['message' => $response['message']]], $response['status']);
                }

                $this->addMapping(['credentialMapping' => $params['credentialMapping']], self::CREDENTIAL_MAPPING_SECTION);
                
                break;

            case('mapping'):
                if (isset($params['attributeMapping'])) {
                    $this->addMapping(['attributeMapping' => $params['attributeMapping']], self::ATTRIBUTE_MAPPING_SECTION);
                }

                break;

            case('extra-mapping'):
                if (isset($params['attributes'])) {
                    $this->addMapping(['attributes' => $params['attributes']], self::ICECAT_ATTRIBUTE_MAPPING_SECTION);
                }

                break;
            case('attribute-type-mapping'):
                if (isset($params['attributesType'])) {
                    $this->addMapping(['attributesType' => $params['attributesType']], self::ICECAT_ATTRIBUTE_TYPE_MAPPING_SECTION);
                }

                break;
            default:
                if (isset($params['icecatLocaleMapping'])) {
                    $this->addMapping(['icecatLocaleMapping' => $params['icecatLocaleMapping']], self::ICECAT_LOCALE_MAPPING_SECTION);
                }
                break;
        }

        return new JsonResponse(['successful' => true]);
    }

    /**
     * @param array $params
     *
     * @return array
     */
    protected function authenticateCredential(Request $request, array $params)
    {
        $validation = $this->validateParams($request, $params);
        if ($validation['status'] !== Response::HTTP_OK) {
            return $validation;
        }

        $response = $this->httpClient->createRequest(
            'GET',
            IcecatEndpoints::ICECAT_REFERENCE_URL,
            [],
            array_values($params['credentialMapping'])
        );
       
        if (strpos($response, self::UNAUTHORIZED)) {
            $validation['status'] = Response::HTTP_BAD_REQUEST;
            $validation['message'] = 'Unauthorized icecat login credentials ';
        } elseif (strpos($response, self::NOT_FOUND)) {
            $validation['status'] = Response::HTTP_BAD_REQUEST;
            $validation['message'] = 'Not found exception';
        }
       
        return $validation;
    }

    /**
     * @param Request $request;
     * @param array $params
     *
     * @return array
     */
    protected function validateParams(Request $request, array $params): array
    {
        $response['status'] = Response::HTTP_OK;
        if (!isset($params['credentialMapping'])) {
            $response['status'] = Response::HTTP_BAD_REQUEST;
            $response['message'] = 'Found empty Icecat credential, please fill credential';
            
            return $response;
        }

        $form = $this->getConfigForm();
        $form->submit($params['credentialMapping']);
        $form->handleRequest($request);
        if (!$form->isValid()) {
            $credentialEmptyFields = [];
            $errors = $form->getErrors(true);
            foreach ($errors as $key => $error) {
                $credentialEmptyFields[] = $error->getOrigin()->getName();
            }

            if (!empty($credentialEmptyFields)) {
                $response['status'] = Response::HTTP_BAD_REQUEST;
                $response['message'] = implode(' & ', $credentialEmptyFields). (count($credentialEmptyFields) > 1 ? ' fields are empty ' : ' field is empty '). 'please check';
            }
        }

        return $response;
    }
    
    /**
     * @return form
     */
    private function getConfigForm(): Form
    {
        $form = $this->createFormBuilder(null, [
                    'allow_extra_fields' => true,
                    'csrf_protection' => false
                ]);

        foreach ($this->getFieldContraints() as $field => $constraint) {
            $form->add($field, null, [
                    'constraints' => is_array($constraint) ? $constraint : [
                        $constraint
                    ]
                ]);
        }

      
        return $form->getForm();
    }

    /**
     * @return array
     */
    private function getFieldContraints():array
    {
        return [
            'username' => new NotBlank(),
            'password' => new NotBlank(),
        ];
    }

    /**
    * @param array $mappingData
    * @param string $section
    *
    * @return void
    */
    protected function addMapping(array $mappingData, string $section): void
    {
        // $mappingData= array_filter(array_map('array_filter', $mappingData));
        foreach ($mappingData as $mappingKey => $mappingValues) {
            $mappingValues = array_filter($mappingValues);
            $mapping = $this->icecatMappingRepository->findOneBy(['name'=> $mappingKey, 'section' => $section]);
            if (!$mapping) {
                $mapping = new IcecatMapping();
            }

            if ('credentialMapping' === $mappingKey
                && isset($mappingValues['password'])
                && $mappingValues['password'] === str_repeat('*', 20)
                && $mapping->getValue()) {
                $oldCredentials = json_decode($mapping->getValue(), true);
                $mappingValues['password'] = $oldCredentials['password'];
            }

            $mapping->setName($mappingKey);
            $mapping->setValue(json_encode($mappingValues));
            $mapping->setSection($section);
            $this->entityManager->persist($mapping);
            $this->entityManager->flush();
        }
    }

    /**
     * @param array $mappingSections
     * @param bool  $convertPass
     *
     * @return array
     */
    protected function getMapping(array $mappingSections, bool $convertPassword): array
    {
        $mapping = [];
        foreach ($mappingSections as $mappingKey => $mappingSection) {
            $icecatMapping = $this->icecatMappingRepository->findOneBy(['section' => $mappingSection]);
            $mapping[$mappingKey] =[];
            if ($icecatMapping) {
                $data = json_decode($icecatMapping->getValue(), true);
                if ($convertPassword
                    && 'credentialMapping' === $mappingKey
                    && isset($data['password'])) {
                    $data['password'] = str_repeat('*', 20);
                }

                $mapping[$mappingKey] = $data;
            }
        }

        return $mapping;
    }

    /**
     * @return array
     */
    public function getExtraAttributeMapping(): array
    {
        $mappings = [];
        $icecatExtraAttributeMappings = $this->icecatMappingRepository->findBy(['section' => self::ICECAT_ATTRIBUTE_MAPPING_SECTION]);
        if ($icecatExtraAttributeMappings) {
            foreach ($icecatExtraAttributeMappings as $icecatExtraAttributeMapping) {
                $mappings[$icecatExtraAttributeMapping->getName()] = $icecatExtraAttributeMapping->getValue();
            }
        }

        return $mappings;
    }
}
