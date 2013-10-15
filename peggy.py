import cgi
import urllib
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

MAIN_PAGE_FOOTER_TEMPLATE = """\
	<form action="/new" method="post">
	  <div><input value="id" name="user_ID"></div>
	  <div><input value="docName" name="documentName"></div>
	  <div><input type="submit" value="New Document"></div>
	</form>
	
	<form action="/view" method="get">
	  <div><input value="id" name="user_ID"></div>
	  <div><input type="submit" value="View Document"></div>
	</form>
	<hr>	 
"""

EDIT_PAGE_TEMPLATE = """\
	<form action="/save" method="post">
	  <input type="hidden" name="documentName" value="%s">
	  <input type="hidden" name="user_ID" value="%s">
	  <div><textarea name="htmlcontent" rows="3" cols="60" >%s</textarea></div>
	  <div><textarea name="csscontent" rows="3" cols="60"  >%s</textarea></div>
	  
	  <div><input type="submit" value="Save"></div>
	</form>
"""

LOGIN_TEMPLATE = """\
	<a href="%s">%s</a>
	</body>
</html> 
"""

DEFAULT_ID = 'default_id'

def document_key(user_ID=DEFAULT_ID):
	"""Constructs a Datastore key for a Guestbook entity with guestbook_name."""
	return ndb.Key('Documents', user_ID)

class Documents(ndb.Model):
	documentName = ndb.StringProperty()
	htmlcontent = ndb.StringProperty(indexed=False)
	csscontent = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.write('<html><body>')
		self.response.write(MAIN_PAGE_FOOTER_TEMPLATE)
		
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
		self.response.write(LOGIN_TEMPLATE % (url, url_linktext))
		
class New(webapp2.RequestHandler):		
	def post(self):
		self.response.write('<html><body>')
		user_ID = self.request.get('user_ID', DEFAULT_ID)
		documentName = self.request.get('documentName')
		htmlcontent = ""
		csscontent = ""
		
		documents = Documents(parent=document_key(user_ID))		
		documents.htmlcontent = htmlcontent
		documents.csscontent = csscontent
		documents.documentName = documentName
		#Key('Documents', 'id', 'Documents', 6122080743456768)
		documents.key = ndb.Key('Documents', user_ID, 'Documents', documentName)
		self.response.write(str(documents) + "<br>")
		
		dkey = documents.put()
		
		self.response.write(dkey)
		query_params = {'user_ID':user_ID, 'documentName':documentName}
		self.redirect('/edit?' + urllib.urlencode(query_params))		

class View(webapp2.RequestHandler):
	def get(self):		
		self.response.write('<html><body>')
		user_ID = self.request.get('user_ID', DEFAULT_ID)
		documents_query = Documents.query(
			ancestor=document_key(user_ID))
			
		documents = documents_query.fetch(10)
		
		self.response.write('<form action="/edit" id="docName">')
		self.response.write('<select name="documentName" form="docName">')
		for document in documents:
			if str(document.documentName) != "None":
				self.response.write('<option value="' + str(document.documentName) + '">' + str(document.documentName) + '</option>')					
		self.response.write('</select>')
		self.response.write('<input type="hidden" name="user_ID" value="' + user_ID +'">')
		self.response.write('<input type="submit">')
		self.response.write('</form>')
		
		



		
		
		#self.response.write('%s<br>' % (cgi.escape(str(documents))))		
		
								  
class Edit(webapp2.RequestHandler):
	def get(self):
		self.response.write('<html><body>')
		user_ID = self.request.get('user_ID', DEFAULT_ID)
		documentName = self.request.get('documentName')
		documents_query = Documents.query(ancestor=document_key(user_ID))
		
		documents = documents_query.fetch(10)
		document2 = None		
		for document in documents:
			if str(document.documentName) == documentName:
				self.response.write("YES!")		
				document2 = document
				break
		
		self.response.write(str(document.documentName))		
		
		#docu = Documents()
		#docu.htmlcontent = "dd"
		#docu.documentName = "unSaved"		
		#docu.key = ndb.Key('Documents', user_ID, 'Documents', documentName)		
		#self.response.write("<br>"+ str(docu))		
		#self.response.write(cgi.escape(str(documents)))		
		#self.response.write(len(documents))
		#dkey = ndb.key("Documents", "id")
		#self.response.write(dkey)
		#doc = dkey.get()
		#self.response.write(doc.htmlcontent)
		
		if document2 != None:
			#self.response.write(document2.htmlcontent)
			self.response.write(EDIT_PAGE_TEMPLATE % (documentName, user_ID, document2.htmlcontent, document2.csscontent))
		else:
			self.response.write(EDIT_PAGE_TEMPLATE % ("","","", ""))
		
		#dkey = document_key(user_ID)
		#doc = dkey.get()
		#document.put()
		
		#self.response.write(dkey)		
		
		#self.response.write('%s<br>' % (cgi.escape(str(documents))))

class Save(webapp2.RequestHandler):
	def post(self):
		self.response.write('<html><body>')
		htmlcontent = self.request.get('htmlcontent')
		csscontent = self.request.get('csscontent')	
		user_ID = self.request.get('user_ID', DEFAULT_ID)
		documentName = self.request.get('documentName')
		
		documents_query = Documents.query(ancestor=document_key(user_ID))
		documents = documents_query.fetch(10)
		
		self.response.write(htmlcontent)
		self.response.write(user_ID)
		
		document2 = None
		for document in documents:
			if str(document.documentName) == documentName:
				document2 = document
				break
				
		document2.htmlcontent = htmlcontent
		document2.csscontent = csscontent
		document2.put()	
		
		#documents = documents_query.fetch(2) 	
		#document = documents[0]
		#document.htmlcontent=htmlcontent
		#document.csscontent=csscontent
		#documents.put()
		
		query_params = {'user_ID':user_ID,'documentName':documentName}
		self.redirect('/edit?' + urllib.urlencode(query_params))

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/new', New),
	('/view', View),
	('/edit', Edit),
	('/save', Save)], debug=True)