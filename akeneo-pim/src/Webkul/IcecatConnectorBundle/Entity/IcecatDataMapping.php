<?php

namespace Webkul\IcecatConnectorBundle\Entity;

class IcecatDataMapping
{
    /**
     * @var int
     */
    private $id;

    /**
     * @var int
     */
    private $externalId;

    /**
     * @var string
     */
    private $code;

    /**
     * @var string
     */
    private $value;

    /**
     * @var string
     */
    private $section;

    /**
     * Get id
     *
     * @return int
     */
    public function getId()
    {
        return $this->id;
    }

    /**
     * Set externalId
     *
     * @param int $externalId
     *
     * @return IcecatDataMapping
     */
    public function setExternalId($externalId)
    {
        $this->externalId = $externalId;
        return $this;
    }

    /**
     * Get externalId
     *
     * @return int
     */
    public function getExternalId()
    {
        return $this->externalId;
    }

    /**
     * Set value
     *
     * @param string $value
     *
     * @return IcecatDataMapping
     */
    public function setValue($value)
    {
        $this->value = $value;

        return $this;
    }

    /**
     * Get value
     *
     * @return string
     */
    public function getValue()
    {
        return $this->value;
    }

    /**
     * Set code
     *
     * @param string $code
     *
     * @return IcecatDataMapping
     */
    public function setCode($code)
    {
        $this->code = $code;
        return $this;
    }

    /**
     * Get code
     *
     * @return IcecatDataMapping
     */
    public function getCode()
    {
        return $this->code;
    }

    /**
     * Set section
     *
     * @param string $section
     *
     * @return IcecatDataMapping
     */
    public function setSection($section)
    {
        $this->section = $section;
        return $this;
    }

    /**
     * Get section
     *
     * @return string
     */
    public function getSection()
    {
        return $this->section;
    }
}
