import os

from twisted.web.server import Site, NOT_DONE_YET
from twisted.internet import reactor
from twisted.web.resource import Resource


class FileServerResource(Resource):
    def __init__(self):
        Resource.__init__(self)
        self.putChild("user", UserResource())
        self.putChild("check", CheckResource())
        self.putChild("files", FileResource())


class UserResource(Resource):
    def getChild(self, path, request):
        return self

    def render_POST(self, request):
        urlparts = request.path.split("/")
        if urlparts[-1] == 'auth':
            # Need to escape the args for security
            print "Doing auth stuff! Got data: %s" % request.content.read()
        elif urlparts[-1] == 'create':
            # Same as above
            print "Creating a user! Got data: %s" % request.content.read()
        return "<html><head/><body><p> You'll get a user once we do the backend. </p></body></html>"


class CheckResource(Resource):
    def render_GET(self, request):
        print "Got a check request!"
        return '<html><head/><body>\
        <h1>This will be meaningful once the back end is built. For now, a cat.</h1><br/>\
        <a href="http://thecatapi.com"><img src="http://thecatapi.com/api/images/get?format=src&type=gif"></a>\
        </body></html>'


# May need to fix things to stream properly.
class FileResource(Resource):
    # Gets file specified in query string. I *think* this streams it, though I need to verify that.
    def render_GET(self, request):
        request.setHeader('Content-Length', os.stat(request.args['filename'][0]).st_size)
        with open(request.args['filename'][0], 'rb') as readFile:
            request.write(readFile.read())
        request.finish()
        return NOT_DONE_YET

    # Again, I *think* this streams the file (though, now that I think about it, content.read() definitely doesn't...)
    def render_PUT(self, request):
        with open(request.args['filename'][0], 'wb') as writeFile:
            writeFile.write(request.content.read())
        request.write('received')
        request.finish()
        return NOT_DONE_YET


if __name__ == "__main__":
    resource = FileServerResource()
    factory = Site(resource)
    reactor.listenTCP(3240, factory)
    reactor.run()