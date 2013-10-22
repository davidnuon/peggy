import time
from google.appengine.ext import ndb

class Document(ndb.Model):
	documentName = ndb.StringProperty()
	name = ndb.StringProperty()
	htmlcontent = ndb.StringProperty(indexed=False)
	csscontent = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

	@staticmethod
	def getkey(id):
		return ndb.Key('Document', id)

	@staticmethod
	def newname():
		return str( int(time.mktime(time.gmtime())) )