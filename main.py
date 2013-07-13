import web
import jinja2

urls = (
    '/(.*)', 'Index'
)
app = web.application(urls, globals())

class Index:        
    def GET(self, name):
        if not name: 
            name = 'World'
        return 'Hello, ' + name + '!'

if __name__ == "__main__":
    app.run()