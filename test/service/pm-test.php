<?php

/**
 * File handling requests from pay.platbamobilom.sk simulation.
 */

require dirname(dirname(dirname(__FILE__))) . "/source/PlatbaMobilom/PlatbaMobilom.php";

$pmDaemon = new PlatbaMobilom\PlatbaMobilom('/receive', '/parse', 'app');

$pmDaemon->receiveHandler = function($phoneNo, $messageText, $identifier) {
	// prijatie správy
	//echo "Receive handler:";
	//print_r(func_get_args());

	// návratová hodnota musí byť PlatbaMobilom\FeedBack
	// PlatbaMobilom::createFeedBack(string $message [, float $price = 0.0 ])
	return PlatbaMobilom\PlatbaMobilom::createFeedBack("Dakujeme za Vasu SMS spravu. Tato sprava nie je spoplatnena.");
};

$pmDaemon->parseHandler = function($result, $identifier) {
	// spracovanie platby
	//echo "Parse handler:";
	//print_r(func_get_args());;

	return $result === PlatbaMobilom\PlatbaMobilom::RESULT_OK;
};

$pmDaemon->handle();
