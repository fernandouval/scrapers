from datetime import date, datetime, time
#from utils import download, load_data, save_data, parse_date
import urllib2, sys
import re, lxml.html, lxml.etree, StringIO, datetime, csv

from selenium import webdriver

git = 'https://github.com/fernandouval/scrapers/blob/master/bicicleterias.py'

def a1122():
	gitdata = 'https://github.com/fernandouval/scrapers/tree/master/data/1122.csv'
	page = 1
	lastTitle = ''
	while page:
		url = 'http://www.1122.com.uy/rubro-zona/montevideo/bicicleterias/PRD1000147/Z01000&page='+str(page)
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		body = response.read()
		doc = lxml.html.document_fromstring(body)
		divs = doc.xpath('//div[@id="divCentroResultados"]/div')
		print 'tamano: '+str(len(divs))
		count = 0
		page += 1
		for div in divs:
			#de la izquierda sacamos btitle0
			anuncio = div.cssselect('a')[0]
			title = anuncio.text_content()
			print title
			print count
			anuncioUrl = anuncio.attrib['href']
			if (count == 0):
				if (lastTitle == title):
					page = 0
					break
				else:
					#Nos quedamos con el primero
					lastTitle = title
			count += 1
			an_req = urllib2.Request(anuncioUrl)
			an_response = urllib2.urlopen(an_req)
			an_body = an_response.read()
			an_doc = lxml.html.document_fromstring(an_body)
			vcard = an_doc.cssselect('.vcard')[0]
			addr = vcard.cssselect('.street-address')[0].text_content()+', '+ vcard.cssselect('.region')[0].text_content()
			tel = vcard.cssselect('.tel')[0].text_content().replace("Tel.:", "").strip()
			cel = vcard.cssselect('.cel')[0].text_content().replace("Cel.:", "").strip()
			phone = tel+'-'+cel
			web = vcard.cssselect('.webpage a')[0].attrib['href']
			if (web.strip() == 'http://'):
				web = ''
			extra = vcard.cssselect('.hours')[0].text_content()+"\n"+vcard.cssselect('.additionaltext')[0].text_content()
			lat = vcard.cssselect('.latitude')[0][0].attrib['title']
			lon = vcard.cssselect('.longitude')[0][0].attrib['title']
			geo = lat+","+lon
			data = [
				title.strip().encode('utf8', 'replace'),
				addr.strip().encode('utf8', 'replace'),
				geo, 
				web, 
				phone,
				anuncioUrl,
				git,
				gitdata
			];
			with open('data/1122.csv', 'ab') as csvfile:
				csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				csvwriter.writerow(data)


def planetauruguay():
	gitdata = 'https://github.com/fernandouval/scrapers/tree/master/data/1122.csv'
	url = 'http://www.planetauruguay.com/uruguay/bicicletas'
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	body = response.read()
	doc = lxml.html.document_fromstring(body)
	divs = doc.cssselect('.listado')[0].cssselect('ul')[0].cssselect('li')
	for div in divs:
		anuncio = div.cssselect('h2')[0].cssselect('a')[0]
		title = anuncio.text_content()
		print title
		anuncioUrl = anuncio.attrib['href']
		print anuncioUrl
		driver = webdriver.Firefox()
		driver.get(anuncioUrl)
		driver.find_element_by_id('linkvertelefono').click()
		tel = driver.find_element_by_id('telefonocontainer').text
		urlDir = driver.find_element_by_id('verdireccionmapa').find_element_by_tag_name('a').get_attribute('href')
		#driver.get_screenshot_as_file('screen.png')
		driver.close()
		sys.exit()
		an_req = urllib2.Request(anuncioUrl)
		an_response = urllib2.urlopen(an_req)
		an_body = an_response.read()
		an_doc = lxml.html.document_fromstring(an_body)
		vcard = an_doc.cssselect('.vcard')[0]
		addr = vcard.cssselect('.street-address')[0].text_content()+', '+ vcard.cssselect('.region')[0].text_content()
		tel = vcard.cssselect('.tel')[0].text_content().replace("Tel.:", "").strip()
		cel = vcard.cssselect('.cel')[0].text_content().replace("Cel.:", "").strip()
		phone = tel+'-'+cel
		web = vcard.cssselect('.webpage a')[0].attrib['href']
		if (web.strip() == 'http://'):
			web = ''
		extra = vcard.cssselect('.hours')[0].text_content()+"\n"+vcard.cssselect('.additionaltext')[0].text_content()
		lat = vcard.cssselect('.latitude')[0][0].attrib['title']
		lon = vcard.cssselect('.longitude')[0][0].attrib['title']
		geo = lat+","+lon
		data = [
			title.strip().encode('utf8', 'replace'),
			addr.strip().encode('utf8', 'replace'),
			geo, 
			web, 
			phone,
			anuncioUrl,
			git,
			gitdata
		];
		with open('data/1122.csv', 'ab') as csvfile:
			csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			csvwriter.writerow(data)

planetauruguay()