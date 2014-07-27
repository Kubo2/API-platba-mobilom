<?php

namespace PlatbaMobilom {
	use Nette,
		Nette\Object;

	final class FeedBack extends Object {
		/**
		 * @var string
		 * @var float
		 * @final
		 */
		private $message, $price;

		final public function __construct($message, $price) {
			$this->message = $message;
			$this->price = $price;
		}

		final public function __toString() {
			return sprintf(
				PlatbaMobilom::FEEDBACK_FORMAT,
				$this->price,
				$this->message
			);
		}

		final public function getMessage() {
			return $this->message;
		}

		final public function getPrice() {
			return $this->price;
		}
	}
}