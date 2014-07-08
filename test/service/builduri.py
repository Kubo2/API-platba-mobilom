#!python

__name__ = "builduri"
__doc__ = "Simple module for building URIs"

import re

def builduri(host, protocol = 'http', components = []):
	"build URI from passed protocol, hostname and path components"
	uri = protocol.lower() + "://" + host.lower() + "/"
	uri += buildpath(components = components).lstrip('/')
	return uri

def extenduri(uri, components):
	path = buildpath(components = components)
	uri = uri.rstrip('/') + '/' + path.lstrip('/')
	return uri

def extendquery(uri, params):
	try:
		uri, query = uri.split(r'?', 1) # intentionally raw string
	except ValueError:
		raise NotImplementedError("Zadaný parameter 'uri' musí už obsahovať query string na rozšírenie")

	return appendquery(uri, params) + '&' + query

def appendquery(uri, params):
	return uri + '?' + buildquery(params)

def buildpath(components = []):
	if not len(components): 
		return '/'
	return re.sub(
		r'/{2,}'
		, '/'
		, '/'.join(components)
	)

def buildquery(params):
	"build query string from a dictionary of variables"
	query = "?"
	for key in params:
		if len(query) > 1: query += "&"
		query += key + "=" + params[key]
	return query.lstrip("?")

def urlencode(url):
	from urllib.parse import quote_plus
	return quote_plus(url)

def urldecode(url):
	from urllib.parse import unquote_plus
	return unquote_plus(url)