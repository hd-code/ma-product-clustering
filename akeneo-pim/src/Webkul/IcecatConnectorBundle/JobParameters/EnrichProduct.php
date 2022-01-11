<?php

namespace Webkul\IcecatConnectorBundle\JobParameters;

$namespaceObject = new \Webkul\IcecatConnectorBundle\Listener\ClassDefinationForCompatibility();
$namespaceObject->checkVersionAndCreateClassAliases();

use Symfony\Component\Validator\Constraints\Collection;
use Symfony\Component\Validator\Constraints\NotBlank;
use Symfony\Component\Validator\Constraints\Optional;
use Symfony\Component\Validator\Constraints\Type;

class EnrichProduct implements
    \ConstraintCollectionProviderInterface,
    \DefaultValuesProviderInterface
{
    /** @var array */
    protected $supportedJobNames;

    /** @var \ChannelRepositoryInterface */
    protected $channelRepository;

    /**
     * @param \ChannelRepositoryInterface     $channelRepository
     * @param array                           $supportedJobNames
     */
    public function __construct(
        array $supportedJobNames,
        \ChannelRepositoryInterface $channelRepository
    ) {
        $this->supportedJobNames = $supportedJobNames;
        $this->channelRepository = $channelRepository;
    }

    /**
     * {@inheritdoc}
     */
    public function getDefaultValues()
    {
        $channels = $this->channelRepository->getFullChannels();
        $defaultChannelCode = isset($channels[0]) ? $channels[0]->getCode() : null;
        $defaultLocalesCode = isset($channels[0]) ? $channels[0]->getLocaleCodes() : [];
        $defaultLocaleCode  = isset($defaultLocalesCode[0]) ? $defaultLocalesCode[0] : null;
        $parameters['filters'] = [
            'data'=> [
                [
                    'field'    => 'categories',
                    'operator' => \Operators::IN_CHILDREN_LIST,
                    'value'    => []
                ]
            ],
            'structure' => [
                'scope'   => $defaultChannelCode,
                'locales' => $defaultLocalesCode,
                'locale'  => $defaultLocaleCode,
            ],
        ];
        
        $parameters['downloadImage'] = true;
        $parameters['fallbackLocale'] = $defaultLocaleCode;
        $parameters['realTimeVersioning'] = true;
        $parameters['enabledComparison'] = false;
        $parameters['convertVariantToSimple'] = false;

        return $parameters;
    }

    /**
     * {@inheritdoc}
     */
    public function getConstraintCollection()
    {
        $constraintFields = [];
        $constraintFields['user_to_notify'] = new Optional();
        $constraintFields['filters'] = [
            new Collection(
                [
                    'fields'           => [
                        'structure' => [
                            new \FilterStructureLocale(['groups' => ['Default', 'DataFilters']]),
                            new Collection(
                                [
                                    'fields'             => [
                                        'locales'    => new NotBlank(),
                                        'locale'     => new NotBlank(),
                                        'scope'      => new NotBlank(),
                                        'attributes' => new Type(
                                            [
                                                'type'  =>  'array',
                                                'groups' => ['Default', 'DataFilters'],
                                            ]
                                        ),
                                    ],
                                    'allowMissingFields' => true,
                                ]
                            ),
                        ],
                    ],
                    'allowExtraFields' => true,
                ]
            ),
        ];

        $constraintFields['enabledComparison']  = new Optional();
        $constraintFields['realTimeVersioning'] = new Optional();
        $constraintFields['downloadImage']      = new Optional();
        $parameters['fallbackLocale']           = new NotBlank();

        return new Collection([
                            'fields' => $constraintFields,
                            'allowExtraFields' => true,
                            'allowMissingFields' => true,
                        ]);
    }

    /**
     * {@inheritdoc}
    */
    public function supports(\JobInterface $job)
    {
        return in_array($job->getName(), $this->supportedJobNames);
    }
}
