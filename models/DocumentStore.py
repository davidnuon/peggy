class Document(object):
	"""A Class representing a Document"""
	def __init__(self, _id, name, contents):
		super(Document, self).__init__()
		self._id = _id
		self._name = name
		self._contents = contents


	@property
	def id(self):
		return self._id



	@property
	def name(self):
		return self._name


	@name.setter
	def name(self, str):
		self._name = str

	@property
	def content(self):
		return self._contents


	@content.setter
	def content(self, str):
		self._contents = str

	def __str__(self):
		name = self._name
		content = self._contents[20:]

		if len(content) <= 0:
			content = "(Empty Document)"

		return "<%d:, Name: %s , Content: %s>" % (self._id, name, content)

class DocumentGroup(object):
	"""class for describing a group of documents"""
	def __init__(self, doc_store, ids):
		super(DocumentGroup, self).__init__()
		self.links = []
		self.doc_store = doc_store

		for i in ids:
			self.links.append(i)

	def get_docs_array(self):
		return map(lambda x : self.doc_store.get_doc(x), self.links)

	def __str__(self):
		out = "["

		for n in self.links:
			out += self.doc_store.get_doc(n).__str__()
			out += ", "

		out += "]"

		return out
							
class DocumentStore(object):
	"""A Class for managing documents"""
	def __init__(self):
		super(DocumentStore, self).__init__()
		self.documents = {}
		self.group = {}

		self._document_count = 0

	def add(self, id, doc):
		_id = str(id)

		self.documents[_id] = doc

	def new_doc(self, name, contents):
		out = self._document_count

		self.add(out, Document(
			self._document_count, name, contents))

		self._document_count += 1

		return out

	def get_doc(self, id):
		return self.documents[str(id)]

	def get_group(self, name):
		return self.group[name]


	def new_group(self, name, ids):
		self.group[name] = DocumentGroup(self, ids)


	def __str__(self):
		out = "["

		for n in self.documents:
			out += self.documents[n].__str__()
			out += ", "

		out += "]"

		return out

def test():
	test_doc_store = DocumentStore()

	for x in xrange(0, 10):
		test_doc_store.new_doc("html", "test")

	test_doc_store.new_group("beginner", [1,3,4])
	beginner = test_doc_store.get_group("beginner").get_docs_array()
	print beginner[0].name
	beginner[0].name = "This is a test."
	print beginner[0]._id

if __name__ == "__main__":
	test()