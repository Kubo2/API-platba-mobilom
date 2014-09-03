#!python

__doc__ = """
 - — — — — — — — — — — — — — — — — — — — — — — — — — — —
 | Jednoduchá simulácia webovej služby servera pay.platbamobilom.sk.
 | Jej spustením v príkazovom riadku dôjde k simulácii prijatia SMS od zákazníka.
 | Pre viac informácii o fungovaní spomenutej webovej služby nájdete v adresári /doc
 | repozitára projektu vo formáte PDF kópiu technickej príručky tretej strany (služby).
 | 
 | Určené pre testovanie triedy Kubo2\PlatbaMobilom napísanej v PHP.
 |
 | - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
 | Run directly from command line.

"""

# helper
# req.urlopen("http://localhost:80/projects/platba-mobilom/test/prijatie.php?id=nejake-idecko&msisdn=0910253030&text=ac+Kubo2+vip")

from sys import stdin, stdout, stderr, argv
import urllib.request as httpreq
import os.path
import random

import servicehelper
import builduri

if __name__ != "__main__" :
	raise NameError("Služba PlatbaMobilom nie je znovupoužiteľný modul.")


digitsplusletters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

GET_ID = 'id' ;
GET_RESULT = 'res' ;
GET_TEL = 'msisdn' ;
GET_MESSAGE = 'text';

# relatívna cesta k adresáru projektu na http://localhost/
url = ""
# relatívna url akcie 'prijatie SMS'
recurl = "/receive"
# relatívna url akcie 'spracovanie platby'
parseurl = "/parse"
# náhodne vygenerovaný testovací identifikátor (max 20 znakov)
"názov 'cid' je skratka od client-identifier, pretože v pythone je id rezervované slovo"
cid = ''.join(random.choice(digitsplusletters) for i in range(20))
# telefónne číslo, z ktorého prišla SMS
tel = ""
# kompletný text správy
msg = ""

# z tohoto súboru sa číta vždy iba prvý riadok
# prvý riadok musí byť relatívna cesta adresára projektu na http://localhost/
# má druhú prioritu z troch možností poskytnutia url tj. ak nezadáme argv,
# číta sa z tohto súboru
urlfile = "./partner-path"

if not len(argv) > 1 and not os.path.isfile(urlfile):
	stdout.write("Zadajte umiestnenie projektu na webovom serveri (http://localhost/...): ")
	stdout.flush()
	url = stdin.readline().strip()

	if not len(url) or url == "\n":
		servicehelper.printURI()
		exit(9)

elif len(argv) == 2:
	url = argv[1]

else:
	try:
		fp = open(urlfile, 'r')
		url = fp.readline().strip()
		fp.close()

	except IOError:
		stderr.write("Unable to obtain the basic information for right functioning of this service.")
		url = '/'

# print(url)

URI = builduri.builduri(host = "localhost", components = [url, "test/service"])
# print(URI)

"zisťujeme parameter 'tel' - telefónne číslo"
print()
stdout.write("Zadajte prosím telefónne číslo zákazníka: ") and stdout.flush()
tel = stdin.readline(12).strip()

if not len(tel):
	servicehelper.printTel()
	exit(9)

stdout.write("Zadajte prosím funkčnú SMS správu : ") and stdout.flush()
msg = stdin.readline().strip()


# === === === === === === ===

"pošleme dva razy dva testovacie požiadavaky na server 'partnera' + logovanie do konzole"
recuri = builduri.appendquery(builduri.extenduri(URI, [recurl]), {
	GET_ID: cid,
	GET_TEL: tel,
	GET_MESSAGE: builduri.urlencode(msg)
})
parseuri = builduri.appendquery(builduri.extenduri(URI, [parseurl]), {
	GET_ID: cid
})

attrs = []
print("\nPrijatá textová SMS správa.")
attrs.append("id požiadavky: " + cid)
attrs.append("telefónne číslo: " + tel)
attrs.append("text správy: " + msg)
servicehelper.indentFormat(attrs)

attrs = []
print("\nPrvé volanie skriptu na serveri partnera...")
try:
	# priajtie 1
	request = httpreq.urlopen(recuri)
	print(" * %s .. 1" % recuri)
	result = request.read().decode()
	print("\n===Response:\n%s\n" % result)
	
	try:
		aparseuri = builduri.extendquery(parseuri, {GET_RESULT: 'OK'})
		request = httpreq.urlopen(aparseuri)
		print(" * %s .. 1" % aparseuri)
		print("\ntest (%s): %s\n" % ('{response} === "OK"', request.read().decode() == 'OK'))
	except:
		raise
except:
	print("Chyba: Prvé volanie skončilo chybou")

print("\nDruhé volanie skriptu na serveri partnera...")
try:
	# priajtie 2
	request = httpreq.urlopen(recuri)
	print(" * %s .. 1" % recuri)
	result = request.read().decode()
	print("\n===Response:\n%s\n" % result)
	
	try:
		bparseuri = builduri.extendquery(parseuri, {GET_RESULT: 'FAIL'})
		request = httpreq.urlopen(bparseuri)
		print(" * %s .. 1" % bparseuri)
		#print(request.read().decode())
		print("\ntest (%s): %s\n" % ('{response} === "FAIL"', request.read().decode() == 'FAIL'))
	except err:
		raise
except:
	print("Chyba: Druhé volanie skončilo chybou")





# používateľ musí ukončiť skript klávesou / hodí sa pri priamom spúšťaní
#stdin.read( 1 );
