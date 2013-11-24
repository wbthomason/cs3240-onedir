import os
import json
import time

from twisted.web.server import Site, NOT_DONE_YET
from twisted.internet import reactor
from twisted.web.resource import Resource

import db_access


class FileServerResource(Resource):
    def __init__(self):
        Resource.__init__(self)
        self.db = db_access.connect()
        self.putChild("user", UserResource(self.db))
        self.putChild("check", CheckResource(self.db))
        self.putChild("files", FileResource(self.db))


class UserResource(Resource):
    def __init__(self, db):
        Resource.__init__(self)
        self.db = db

    def getChild(self, path, request):
        return self

    def render_POST(self, request):
        urlparts = request.path.split("/")
        if urlparts[-1] == 'auth':
            # Need to escape the args for security
            email = request.args['email'][0]
            passw = request.args['passw'][0]
            print "Doing auth stuff! Got data: %s, %s" % (email, passw)
            if not db_access.login(email, passw, self.db):
                return json.dumps({'auth_key': 0})
        elif urlparts[-1] == 'create':
            # Same as above
            email = request.args['email'][0]
            passw = request.args['passw'][0]
            print "Creating a user! Got data: %s, %s" % (email, passw)
            db_access.create_account(email, passw, self.db)
        return json.dumps({'auth_key': 1})


class CheckResource(Resource):
    def __init__(self, db):
        Resource.__init__(self)
        self.db = db

    def render_GET(self, request):
        print "Got a check request!"
        id = db_access.get_id(request.args['email'][0], self.db)
        last_check = request.args['last_check'][0]
        cur = self.db.cursor()
        checker = "SELECT file FROM user_files WHERE user_id='%d' AND last_update > '%f'" % (int(id), float(last_check))
        cur.execute(checker)
        res = cur.fetchall()
        data = [item[0] for item in res]
        print data
        return json.dumps(data)

# May need to fix things to stream properly.
class FileResource(Resource):
    def __init__(self, db):
        Resource.__init__(self)
        self.db = db

    # Gets file specified in query string. I *think* this streams it, though I need to verify that.
    def render_GET(self, request):
        print "Request for %s" % request.path
        directory = "./files/%s/" % request.args['username'][0]
        request.setHeader('Content-Length', os.stat(directory + request.args['filename'][0]).st_size)
        with open("./files/%s/%s" % (request.args['username'][0], request.args['filename'][0]), 'rb') as readFile:
            request.write(readFile.read())

        request.finish()
        return NOT_DONE_YET

    # Again, I *think* this streams the file (though, now that I think about it, content.read() definitely doesn't...)
    def render_PUT(self, request):
        file_name = request.args['filename'][0]
        directory = "./files/%s/" % request.args['username'][0]
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(directory + file_name, 'wb') as writeFile:
            writeFile.write(request.content.read())

        cur = self.db.cursor()
        user_id = int(db_access.get_id(request.args['username'][0], self.db))
        updated = "INSERT INTO user_files (user_id, file, last_update) VALUES ('%(uid)d', '%(file)s', '%(time)f') " \
                  "ON DUPLICATE KEY UPDATE last_update='%(time)f'" \
                  % {'uid': user_id, 'file': file_name, 'time': time.time()}
        # "UPDATE user_files SET last_update='%f' WHERE file='%s' AND user_id='%d'" % (time.time(), file_name, user_id)
        cur.execute(updated)
        self.db.commit()
        request.write('received')
        request.finish()
        return NOT_DONE_YET


if __name__ == "__main__":
    resource = FileServerResource()
    factory = Site(resource)
    reactor.listenTCP(3240, factory)
    print "Listening on 3240."
    reactor.run()