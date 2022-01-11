<?php
namespace Webkul\IcecatConnectorBundle\Component;

/**
 * This class contains all Icecat api endpoints.
 */
class IcecatEndpoints
{
    /**
     * @const string
     *
     */
    const BASE_URI = 'https://data.icecat.biz/xml_s3/xml_server3.cgi';

    /**
     * @const string
     *
     */
    const PRODUCT_WITH_ID = 'prod_id=%s;vendor=%s;lang=%s;output=productxml';

    /**
     * @const string
     *
     */
    const PRODUCT_WITH_EAN = 'ean_upc=%s;lang=%s;output=productxml';

    /**
     * Initial Full Icecat
     *
     * @const string
     *
     */
    const FULL_ICECAT_INITIAL = 'https://data.icecat.biz/export/level4/%s/files.index.xml.gz';
    
    /**
     * Initial Open Icecat
     *
     * @const string
     *
     */
    const OPEN_ICECAT_INITIAL = 'https://data.icecat.biz/export/freexml/%s/files.index.xml.gz';

    /**
     * Update Full Icecat
     *
     * @const string
     *
     */
    const FULL_ICECAT_UPDATE = 'https://data.icecat.biz/export/level4/%s/files.index.xml.gz';
    
    /**
     * Update Open Icecat
     *
     * @const string
     *
     */
    const OPEN_ICECAT_UPDATE = 'https://data.icecat.biz/export/freexml/%s/daily.index.xml.gz';

    /**
     * On market Full Icecat
     *
     * @const string
     *
     */
    const FULL_ICECAT_ON_MARKET = 'https://data.icecat.biz/export/level4/%s/on_market.index.xml.gz';
    
    /**
     * On market Open Icecat
     *
     * @const string
     *
     */
    const OPEN_ICECAT_ON_MARKET = 'https://data.icecat.biz/export/freexml/%s/on_market.index.xml.gz';

    /**
     * Icecat feature list
     *
     * @const string
     *
     */
    const ICECAT_FEATURE_LIST = 'FeaturesList.xml.gz';

    /**
     * Icecat category list
     *
     * @const string
     *
     */
    const ICECAT_CATEGORY_LIST = 'CategoriesList.xml.gz';

    /**
     * Icecat measures list
     *
     * @const string
     *
     */
    const ICECAT_MEASURES_LIST = 'MeasuresList.xml.gz';

    /**
     * Icecat reference url
     *
     * @const string
     *
     */
    const ICECAT_REFERENCE_URL = 'http://data.icecat.biz/export/freexml.int/refs/';
}
