from twisted.web.server import Site
from twisted.web.static import File
from twisted.internet import reactor

resource = File('./files')
factory = Site(resource)
reactor.listenTCP(3240, factory)
reactor.run()