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
<<<<<<< HEAD

		csscontent = constants.CSS_DEFAULT
=======
		csscontent = constants.CSS_DEFAULT

>>>>>>> appengine_dl
		
		documents = Document(parent=Document.getkey(documentName))		
		documents.htmlcontent = htmlcontent
		documents.csscontent = csscontent
		documents.documentName = documentName
<<<<<<< HEAD
=======
		documents.name = constants.DEFAULT_NAME
>>>>>>> appengine_dl
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
			'id' : documentName
		}))
<<<<<<< HEAD
=======

class ListDocuments(webapp2.RequestHandler):
	def get(self):
		documents_query = Document.query()
		documents = documents_query.fetch()

		documents = map(lambda x: { 
			'name' : x.documentName, 
			'url' : '/view?' + urllib.urlencode({'documentName' : x.documentName}),
			'humanname' : x.name or '[No name]'
			}, documents)

		template = JINJA_ENVIRONMENT.get_template('list.html')
		self.response.write(template.render({ 'list' : documents }))
>>>>>>> appengine_dl
								  
class Edit(webapp2.RequestHandler):
	def get(self):
		documentName = self.request.get('documentName')
		documents_query = Document.query(ancestor=Document.getkey(documentName))
		
<<<<<<< HEAD
		documents = documents_query.fetch()[0]


		template = JINJA_ENVIRONMENT.get_template('editor.html')
		self.response.write(template.render({
			'htmlcontent' : documents.htmlcontent,
			'csscontent' : documents.csscontent,
=======
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
>>>>>>> appengine_dl
			'id' : documentName
		}))

class Save(webapp2.RequestHandler):
	def post(self):
		self.response.write('<html><body>')
		htmlcontent = self.request.get('htmlcontent')
		csscontent = self.request.get('csscontent')	
		documentName = self.request.get('documentName')
<<<<<<< HEAD
=======
		humanname = self.request.get('humanname')
>>>>>>> appengine_dl
		
		documents_query = Document.query(ancestor=Document.getkey(documentName))
		document = documents_query.fetch()[0]
		
		document.htmlcontent = htmlcontent
		document.csscontent = csscontent
<<<<<<< HEAD
=======
		document.name = humanname
>>>>>>> appengine_dl

		document.put()

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/new', New),
	('/view', View),
<<<<<<< HEAD
=======
	('/list', ListDocuments),
>>>>>>> appengine_dl
	('/edit', Edit),
	('/save', Save)], debug=True)
