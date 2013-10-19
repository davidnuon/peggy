import cgi
import urllib
import time

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2
import jinja2
import os

import constants

path = os.path.join(os.path.dirname(__file__), 'tmpl')
timestr = lambda : str( int(time.mktime(time.gmtime())) )
tohtml = lambda x:  x.replace('&lt;','<').replace('&gt;', '>')

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(path),
    extensions=['jinja2.ext.autoescape'],
    autoescape=False)


def document_key(id):
	return ndb.Key('Documents', id)

class Documents(ndb.Model):
	documentName = ndb.StringProperty()
	htmlcontent = ndb.StringProperty(indexed=False)
	csscontent = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('front.html')
		self.response.write(template.render({}))

class New(webapp2.RequestHandler):		
	def post(self):
		self.response.write('<html><body>')
		documentName = timestr()
		htmlcontent = constants.HTML_DEFAULT

		csscontent = constants.CSS_DEFAULT
		
		documents = Documents(parent=document_key(documentName))		
		documents.htmlcontent = htmlcontent
		documents.csscontent = csscontent
		documents.documentName = documentName
		documents.key = document_key(documentName)

		dkey = documents.put()
		
		self.response.write(dkey)
		query_params = {'documentName':documentName}
		self.redirect('/edit?' + urllib.urlencode(query_params))		

class View(webapp2.RequestHandler):
	def get(self):		
		htmlcontent = self.request.get('htmlcontent')
		csscontent = self.request.get('csscontent')	
		documentName = self.request.get('documentName')
		
		documents_query = Documents.query(ancestor=document_key(documentName))
		document = documents_query.fetch()[0]

		template = JINJA_ENVIRONMENT.get_template('view.html')
		self.response.write(template.render({
			'htmlcontent' : document.htmlcontent,
			'csscontent' : document.csscontent,
			'id' : documentName
		}))
								  
class Edit(webapp2.RequestHandler):
	def get(self):
		self.response.write('<html><body>')
		documentName = self.request.get('documentName')
		documents_query = Documents.query(ancestor=document_key(documentName))
		
		documents = documents_query.fetch()[0]


		template = JINJA_ENVIRONMENT.get_template('editor.html')
		self.response.write(template.render({
			'htmlcontent' : documents.htmlcontent,
			'csscontent' : documents.csscontent,
			'id' : documentName
		}))

class Save(webapp2.RequestHandler):
	def post(self):
		self.response.write('<html><body>')
		htmlcontent = self.request.get('htmlcontent')
		csscontent = self.request.get('csscontent')	
		documentName = self.request.get('documentName')
		
		documents_query = Documents.query(ancestor=document_key(documentName))
		document = documents_query.fetch()[0]
		
		document.htmlcontent = htmlcontent
		document.csscontent = csscontent

		document.put()

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/new', New),
	('/view', View),
	('/edit', Edit),
	('/save', Save)], debug=True)
