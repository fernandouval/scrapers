#!/usr/bin/env python
# -*- coding: latin-1 -*-

from datetime import date, datetime, time
#from utils import download, load_data, save_data, parse_date
import urllib2
import re, lxml.html, lxml.etree, StringIO, datetime, csv

def comerciosdemontevideo():
	page = 1
	lastTitle = ''
	while page:
		url = 'http://www.comerciosdemontevideo.com.uy/comercios.php?id=190&page='+str(page)
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		body = response.read()
		doc = lxml.html.document_fromstring(body)
		divs = doc.cssselect('.gold .binfo')
		count = 0
		page += 1
		for div in divs:
			#de la izquierda sacamos btitle0
			title = div.cssselect('.bizq .btitle')[0].cssselect('a')[0].text_content()
			print title
			if (count == 0):
				if (lastTitle == title):
					page = 0
					break
				else:
					#Nos quedamos con el primero
					lastTitle = title
			count += 1
			#de la derecha sacamos bdir0,bphone, bweb
			derDiv = div.cssselect('.bder')
			addr = derDiv[0].cssselect('.bdir')[0].text_content()
			phone = derDiv[0].cssselect('.bphone')[0].text_content()
			web = derDiv[0].cssselect('.bweb')[0].text_content()
			data = [
				title.strip().encode('utf8', 'replace'),
				addr.strip().encode('utf8', 'replace'),
				'', 
				web.replace("Web:", "").strip(), 
				phone.replace("Tel:", "").strip(),
				url
			];
			with open('data/comerciosdemontevideo.csv', 'ab') as csvfile:
				csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				csvwriter.writerow(data)

def paginasamarillas(rubro):
	if (rubro == 'bicis'):
		rubroUrl = 'bicicletas_-_reparacion_y_repuestos/56400'
	else:
		rubroUrl = 'automotores_-_estacionamientos/177400'
	page = 1
	lastTitle = ''
	while page:
		url = 'http://paginasamarillas.com.uy/voltprod/sitio/rubro/'+rubroUrl+'/zona/Montevideo/pagina-'+str(page)
		hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
		req = urllib2.Request(url, headers=hdr)
		response = urllib2.urlopen(req)
		body = response.read()
		doc = lxml.html.document_fromstring(body)
		divs = doc.cssselect('.box_reg_master')
		count = 0
		page += 1
		print 'LAST: '+lastTitle
		for div in divs:
			#de la izquierda sacamos btitle0
			title = div.cssselect('h3 a')[0].text_content()
			print title
			if (count == 0):
				if (lastTitle == title):
					page = 0
					break
				else:
					#Nos quedamos con el primero
					lastTitle = title
			count += 1
			#de la derecha sacamos bdir0,bphone, bweb
			infoDiv = div.cssselect('.registro_databasica strong')
			addr = infoDiv[0].text_content()
			phone = infoDiv[1].text_content()
			web = ''
			data = [
				title.strip().encode('utf8', 'replace'),
				addr.strip().encode('utf8', 'replace'),
				'', 
				web.replace("Web:", "").strip(), 
				phone.replace("Tel:", "").strip(),
				url
			];
			with open('data/paginasamarillas-'+rubro+'.csv', 'ab') as csvfile:
				csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				csvwriter.writerow(data)

def amerpages():
	page = 1
	lastTitle = ''
	while page:
		url = "http://amerpages.com/spa/uruguay/items/search/page:"+str(page)+"/category:1121/city:1030100026"
		hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
		req = urllib2.Request(url, headers=hdr)
		response = urllib2.urlopen(req)
		body = response.read()
		doc = lxml.html.document_fromstring(body)
		divs = doc.cssselect('.listing')
		count = 0
		page += 1
		for div in divs:
			infoDiv = div.cssselect('.listingDetails')[0]
			#de la izquierda sacamos btitle0
			title = infoDiv.cssselect('h3 a')[0].text_content()
			print title
			if (count == 0):
				if (lastTitle == title):
					page = 0
					break
				else:
					#Nos quedamos con el primero
					lastTitle = title
			count += 1
			addr = infoDiv.cssselect('.address')[0].text_content()
			phone = ''
			web = ''
			data = [
				title.strip().encode('utf8', 'replace'),
				addr.strip().encode('utf8', 'replace'),
				'', 
				web.replace("Web:", "").strip(), 
				phone.replace("Tel:", "").strip(),
				url
			];
			with open('data/amerpages.csv', 'ab') as csvfile:
				csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				csvwriter.writerow(data)

paginasamarillas('bicis')