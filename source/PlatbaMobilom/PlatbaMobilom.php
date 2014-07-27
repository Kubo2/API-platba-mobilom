<?php

namespace {
	// require composer autoloader
	require dirname(dirname(__FILE__)) . "/stuff/autoload.php";
} namespace PlatbaMobilom {
	use 
		Nette,
		Nette\Object,
		Nette\Utils\Callback;

	require "IDaemon.php";
	require "FeedBack.php";

	/**
	 * @example test/service/pm-test.php
	 */
	class PlatbaMobilom extends Object implements IDaemon {
		const SERVICE_IP = '109.74.149.29';
		const SERVICE_MIME_TYPE = 'text/plain';

		const RESULT_OK = "OK";
		const RESULT_ERROR = "FAIL";
		
		const ARG_ID = 'id';
		const ARG_RESULT = 'res';
		const ARG_TEL = 'msisdn';
		const ARG_MESSAGE = 'text';

		const FEEDBACK_FORMAT = "%-.2f\n%s";

		private $receiveHandler, $parseHandler;
		private $receiveUrl, $parseUrl;
		private $keyword;

		/**
		 * Constructs and returns new instance of {@code PlatbaMobilom} class.
		 */
		public function __construct($urlReceive, $urlParse, $keyword) {
			$this ->keyword = $keyword;
			$this ->receiveUrl = trim($urlReceive, '/');
			$this ->parseUrl = trim($urlParse, '/');
		}

		public function setReceiveHandler($handler) {
			$this ->receiveHandler = Callback::check($handler);
		}

		public function setParseHandler($handler) {
			$this ->parseHandler = Callback::check($handler);
		}

		public function handle() {
			$URI = rtrim(
						substr(
							$_SERVER["REQUEST_URI"], // scan requested uri
							0, // form first character
							strlen($_SERVER["REQUEST_URI"]) - strlen($_SERVER["QUERY_STRING"]) // and skip query string
						),
				'?' // remove any extra trailing question-mark
			);

			header("Content-Type: text/plain; charset=utf-8");

			if(empty($_GET[self::ARG_ID])) return;
			$id = sha1($_GET[self::ARG_ID]);

			if(basename($URI) == $this->receiveUrl) {
				$phoneNo = $_GET[self::ARG_TEL];
				$sms = substr(
					trim($_GET[self::ARG_MESSAGE]),
					strlen($this->keyword) + 1
				);
				echo $this->_handleReceive($phoneNo, $sms, $id);
				return;
			} else if(basename($URI) == $this->parseUrl) {
				if($this->_handleParse($_GET[self::ARG_RESULT], $id)) {
					echo self::RESULT_OK;
				} else {
					echo self::RESULT_ERROR;
				}
				return;
			} /*else {
				// can simply be skipped
			}*/
		}

		public static function createFeedBack($message, $price = 0.00) {
			return new FeedBack($message, $price);
		}

		private function _handleReceive($n, $t, $i) {
			$fb = Callback::invoke($this->receiveHandler, $n, $t, $i);
			return $fb;
		}

		private function _handleParse($r, $i) {
			$result = Callback::invoke($this->parseHandler, $r, $i);
			return $result;
		}
	}
}
