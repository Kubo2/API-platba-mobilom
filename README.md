Rozhranie webovej služby „Platba Mobilom“
================================

Trieda <code>PlatbaMobilom</code> predstavuje abstraktné rozhranie (vrstvu) pre komunikáciu 
so serverom webovej služby <a href="http://platbamobilom.zoznam.sk/">platbamobilom.zoznam.sk</a>.


Rozhranie
------------

```php

class PlatbaMobilom extends IntellObject {
	/* constants */
	const string SERVICE_IP = '109.74.149.29' ;
	const string SERVICE_MIME_TYPE = 'text/plain' ;
	const string RESULT_OK = "OK" ;
	const string RESULT_ERROR = "FAIL" ;
	const string ARG_ID = 'id' ;
	const string ARG_RESULT = 'res' ;
	const string ARG_TEL = 'msisdn' ;
	const string ARG_MESSAGE = 'text';

	/* events */	
	/* methods */
	PlatbaMobilom __construct(string $urlReceive, string $urlParse, string $keyword)
	void handle()
	void setReceiveHandler(callback $handler)
	void setParseHandler(callback $handler)
	static FeedBack createFeedBack()
}

```


Implementácia
-----------------

Štandardné použitie triedy je nasledovné:

```php
<?php

require "source/PlatbaMobilom/PlatbaMobilom.php";
use PlatbaMobilom\PlatbaMobilom;

$service = new PlatbaMobilom('/prijatie', '/spracovanie', 'app');

/**
 * Receive handler. First URL - see docs.
 *
 * @param int   phone number of customer
 * @param string   the text of message customer sent, without leading application keyword
 * @param string(40)   sha-1 hash of received identifier
 * @return PlatbaMobilom\FeedBack   instance of FeedBack carriage
 */
$service->receiveHandler = function($phoneNo, $messageText, $identifier) {
	// prijatie správy
	// návratová hodnota musí byť PlatbaMobilom\FeedBack
	// PlatbaMobilom::createFeedBack(string $message [, float $price = 0.0 ])
	return PlatbaMobilom::createFeedBack("Dakujeme za Vasu SMS spravu.");
};


/**
 * Parse handler. Second URL.
 *
 * @param string   Either one of PlatbaMobilom::RESULT_OK or PlatbaMobilom::RESULT_ERROR constants
 * @param string(40)   sha-1 hash of received identifier
 * @return bool   true if parse was successful, false otherwise
 */
$service->parseHandler = function($result, $identifier) {
	// spracovanie platby
};

$service->handle();


?>
```
