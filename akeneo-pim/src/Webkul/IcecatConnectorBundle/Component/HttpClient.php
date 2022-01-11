<?php

namespace Webkul\IcecatConnectorBundle\Component;

use GuzzleHttp\Client;
use GuzzleHttp\ClientInterface;
use GuzzleHttp\Exception\ClientException;
use Symfony\Component\HttpFoundation\Response;
use Webkul\IcecatConnectorBundle\Component\IcecatEndpoints;
use Webkul\IcecatConnectorBundle\Repository\IcecatMappingRepository;

/**
 * Http client used to icecat operation
 */
class HttpClient
{
    /** @var array */
    private $credentials = [];

    /** @var ClientInterface */
    private $guzzle;

    public function __construct()
    {
        $this->guzzle = new Client(['base_uri' => IcecatEndpoints::BASE_URI]);
    }

    /**
     * @param array $credentials
     */
    public function setCredentials($credentials): void
    {
        $this->credentials = $credentials;
    }

    /**
     *
     * @param string $method
     * @param string $requestUri
     * @param array  $options
     * @param array  $credentials
     *
     * @return string
     */
    public function createRequest(string $method, string $requestUri = '', array $options = [], array $credentials = []): string
    {
        $params = [
            'auth'  => !empty($credentials) ? $credentials : array_values($this->credentials),
        ];
        $params = array_merge($params, $options);
        
        try {
            $response = $this->guzzle->request($method, $requestUri, $params);
        } catch (ClientException $e) {
            if (Response::HTTP_NOT_FOUND === $e->getCode() || Response::HTTP_UNAUTHORIZED === $e->getCode()) {
                return new Response(null, $e->getCode());
            }
        }
        
        return $response->getBody()->getContents();
    }

    /**
     * @param string $requestUri
     * @param string $basename
     * @param string $targetDirectory
     * @param bool   $gunzip
     *
     * @return string
     */
    public function download(string $requestUri, string $basename, string $targetDirectory, bool $gunzip): string
    {
        $outputPath = $targetDirectory . '/' . $basename;
        $this->createRequest('GET', $requestUri, ['sink' => $outputPath]);
        if ($gunzip) {
            $outputPath = $this->uncompress($outputPath);
        }
       
        return $outputPath;
    }

    /**
     * @param string $sourceFile compressed source file
     *
     * @return string Uncompressed output file path
     */
    protected function uncompress(string $sourceFile): string
    {
        $input = gzopen($sourceFile, 'rb');
        $outputPath = preg_replace('/.gz$/', '', $sourceFile);
        $ouput = fopen($outputPath, 'wb');
        
        /**while not EOF */
        while (!gzeof($input)) {
            fwrite($ouput, gzread($input, 4096));
        }

        fclose($ouput);
        gzclose($input);

        return $outputPath;
    }
}
