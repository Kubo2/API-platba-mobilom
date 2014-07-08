#!python

__doc__ = "provides console help messages"

import builduri

def helpFormat():
	print("\n\nFormát: ")

def indentFormat(messages):
	print("\t" + "\n\t".join([message for message in messages]))

def requireFormat(messages):
	helpFormat()
	indentFormat(messages)

def printURI():
	requireFormat([
			"Zadajte prosím relatívnu cestu od koreňa webu tj. napr. /adresár/.",
			"Služba si sama doplní http://localhost/ a cestu k testom."
		])

def printTel():
	requireFormat([
			"dvanásť miestne číslo bez úvodného +",
			"Príklad: 4219nnnnnnnn"
		])
