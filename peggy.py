import cgi
import urllib
import time

from google.appengine.api import users
from google.appengine.ext import ndb
from models.document import Document
from controllers.base.page import Page

import webapp2
import jinja2
import os

import constants

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'tmpl')
tohtml = lambda x:  x.replace('&lt;','<').replace('&gt;', '>')

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_PATH),
    extensions=['jinja2.ext.autoescape'],
    autoescape=False)

TEMPLATE_404 = JINJA_ENVIRONMENT.get_template('404.html')
TEMPLATE_500 = JINJA_ENVIRONMENT.get_template('500.html')

class MainPage(Page):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('front.html')
		self.response.write(template.render({}))

class New(webapp2.RequestHandler):		
	def post(self):
		documentName = Document.newname()
		htmlcontent = constants.HTML_DEFAULT
		csscontent = constants.CSS_DEFAULT

		documents = Document(parent=Document.getkey(documentName))		
		documents.htmlcontent = htmlcontent
		documents.csscontent = csscontent
		documents.documentName = documentName
		documents.name = constants.DEFAULT_NAME
		documents.key = Document.getkey(documentName)
		documents.put()
		
		query_params = {'documentName':documentName}
		self.redirect('/edit?' + urllib.urlencode(query_params))		

class View(webapp2.RequestHandler):
	def get(self):		
		htmlcontent = self.request.get('htmlcontent')
		csscontent = self.request.get('csscontent')	
		documentName = self.request.get('documentName')
		
		documents_query = Document.query(ancestor=Document.getkey(documentName))
		document = documents_query.fetch()

		if len(document) == 0:
			self.response.write(TEMPLATE_404.render({}))
			return

		document = document[0]
		template = JINJA_ENVIRONMENT.get_template('view.html')
		self.response.write(template.render({
			'htmlcontent' : document.htmlcontent,
			'csscontent' : document.csscontent,
			'editurl' : '/edit?' + urllib.urlencode({'documentName' : documentName}),
			'title' : document.name,
			'id' : documentName
		}))

class ListDocuments(webapp2.RequestHandler):
	def get(self):
		documents_query = Document.query()
		documents = documents_query.fetch()

		documents = map(lambda x: { 
			'name' : x.documentName, 
			'url' : '/view?' + urllib.urlencode({'documentName' : x.documentName}),
			'editurl' : '/edit?' + urllib.urlencode({'documentName' : x.documentName}),
			'humanname' : x.name or '[No name]',
			'date' : x.date
			}, documents)

		template = JINJA_ENVIRONMENT.get_template('list.html')
		self.response.write(template.render({ 'list' : documents }))
								  
class Edit(webapp2.RequestHandler):
	def get(self):
		documentName = self.request.get('documentName')
		documents_query = Document.query(ancestor=Document.getkey(documentName))
		
		document = documents_query.fetch()
		if len(document) == 0:
			self.response.write(TEMPLATE_404.render({}))
			return

		document = document[0]
		template = JINJA_ENVIRONMENT.get_template('editor.html')
		self.response.write(template.render({
			'htmlcontent' : document.htmlcontent,
			'csscontent' : document.csscontent,
			'humanname' : document.name,
			'id' : documentName,
			'title' : 'Editing ' + document.name
		}))

class Save(webapp2.RequestHandler):
	def post(self):
		self.response.write('<html><body>')
		htmlcontent = self.request.get('htmlcontent')
		csscontent = self.request.get('csscontent')	
		documentName = self.request.get('documentName')
		humanname = self.request.get('humanname')
		
		documents_query = Document.query(ancestor=Document.getkey(documentName))
		document = documents_query.fetch()[0]
		
		document.htmlcontent = htmlcontent
		document.csscontent = csscontent
		document.name = humanname

		document.put()

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/new', New),
	('/view', View),
	('/list', ListDocuments),
	('/edit', Edit),
	('/save', Save)], debug=True)
