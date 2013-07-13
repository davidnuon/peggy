import web
import jinja2

from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('app', 'templates'))

urls = (
    '/app/(.*)', 'App',
    '/app', 'App',
    
    '/(.*)', 'Index'
)
app = web.application(urls, globals())

class Index:        
    def GET(self, name):
    	template = env.get_template('index.html')

    	return template.render(css=[{"url":"/static/css/landing.css"}]) 


class App:        
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


if __name__ == "__main__":
    app.run()