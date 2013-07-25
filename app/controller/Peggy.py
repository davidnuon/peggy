from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('app', 'templates'))

class Peggy:   
    def __init__(self):
        print "Test"

    def GET(self):
    	template = env.get_template('app.html')

        return template.render(css=[
            {"url":"/static/css/style.css"},
            {"url":"/static/codemirror/lib/codemirror.css"},
        ], js=[
            {"url":"/static/js/jquery.js"},
            {"url":"/static/codemirror/lib/codemirror.js"},
            {"url":"/static/js/doc_store.js"},
            {"url":"/static/js/main.js"},
        ])
