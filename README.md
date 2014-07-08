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
}

```


Implementácia
-----------------

Štandardné použitie triedy je nasledovné:

```php
<?php

$service = new PlatbaMobilom('/prijatie', '/spracovanie', 'app');
$service->receiveHandler = function($phoneNo, $messageText) {
	// prijatie správy
	// návratová hodnota musí byť PlatbaMobilom\FeedBack
	// PlatbaMobilom::createFeedBack(string $message [, float $price = 0.0 ])
	return PlatbaMobilom::createFeedBack("Dakujeme za Vasu SMS spravu.");
};

$service->parseHandler = function($result) {
	// spracovanie platby
}


?>
```
