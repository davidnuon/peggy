import web
import jinja2

from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('app', 'templates'))

urls = (
    '/(.*)', 'Index'
)
app = web.application(urls, globals())

class Index:        
    def GET(self, name):
    	template = env.get_template('index.html')

    	return template.render(css=[{"url":"/static/css/landing.css"}]) 

if __name__ == "__main__":
    app.run()