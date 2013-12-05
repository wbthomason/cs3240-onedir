import os
import json
import time
from subprocess import call

from twisted.web.server import Site, NOT_DONE_YET
from twisted.internet import ssl, reactor
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

        # Assume both email and password are being changed. No change is 
        # accomplished by passing the same arg for new.
        elif urlparts[-1] == 'update':
            old_email = request.args['old_email'][0]
            old_password = request.args['old_password'][0]
            new_email = request.args['new_email'][0]
            new_password = request.args['new_password'][0]

            if db_access.login(old_email, old_password, self.db):
                db_access.update_account(old_email, old_password, new_email, new_password, self.db)
                call("mv " + "./files/%s" % old_email + " ./files/%s" % new_email, shell=True)

        elif urlparts[-1] == 'delete':
            email = request.args['email'][0]
            password = request.args['password'][0]

            if db_access.login(email, password, self.db):
                db_access.delete_account(email, self.db)
                call("rm -rf " + "./files/%s" % email, shell=True)
                return json.dumps({'auth_key': 0})

        elif urlparts[-1] == 'admin':
            password = request.args['password'][0]
            if db_access.login('admin', password, self.db):
                command = request.args['command'][0]

                if command == "users":
                    return json.dumps({'users':db_access.list_users(self.db)})

                elif command == "files":
                    email = request.args['email'][0]
                    return json.dumps({'files':db_access.get_files(email, self.db)})

                elif command == "change":
                    old_email = request.args['old_email'][0]
                    new_email = request.args['new_email'][0]
                    new_password = request.args['new_password'][0]

                    db_access.update_account(old_email, '', new_email, new_password, self.db)

                elif command == "remove":
                    email = request.args['email'][0]

                    db_access.delete_account(email, self.db)

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

        # Behind the scenes work to get versioning data
        username = request.args['username'][0]
        file_name_raw = request.args['filename'][0]
        version = int(db_access.get_version(username, file_name_raw, self.db))

        file_parts = file_name_raw.split(".")
        file_parts.append( str(version) )

        # Python is a beautiful, terrifying language
        file_name = "."
        file_name = file_name.join(file_parts)


        request.setHeader('Content-Length', os.stat(directory + file_name).st_size)
        with open("./files/%s/%s" % (username, file_name), 'rb') as readFile:
            request.write(readFile.read())

        request.finish()
        return NOT_DONE_YET

    # Again, I *think* this streams the file (though, now that I think about it, content.read() definitely doesn't...)
    def render_PUT(self, request):
        file_name_raw = request.args['filename'][0]
        username = request.args['username'][0]

        # Get the version number, increment it by 1, and secretly make that the file name
        version = int(db_access.get_version(username, file_name_raw, self.db))

        file_parts = file_name_raw.split(".")
        file_parts.append( str(version + 1) )

        # Python is a beautful, terrifying language
        file_name = "."
        file_name = file_name.join(file_parts)

        # Update the DB with current version
        db_access.inc_version(username, file_name_raw, version, self.db)
        # Because nested one-liners are great coding practice
        morepath = '/'.join(file_name.split('/')[:-1])
        directory = "./files/%s/" % request.args['username'][0]
        full_dir = directory + morepath + '/'
        if not os.path.exists(full_dir):
            os.makedirs(full_dir)

        with open(directory + file_name, 'wb') as writeFile:
            writeFile.write(request.content.read())

        cur = self.db.cursor()
        user_id = int(db_access.get_id(username, self.db))
        file_size = int(request.args['filesize'][0])

        updated = "INSERT INTO user_files (user_id, file, size, last_update) VALUES ('%(uid)d', '%(file)s', '%(size)d', '%(time)f') " \
                  "ON DUPLICATE KEY UPDATE last_update='%(time)f', size='%(size)d'" \
                  % {'uid': user_id, 'file': file_name_raw, 'size': file_size, 'time': time.time()}
        # "UPDATE user_files SET last_update='%f' WHERE file='%s' AND user_id='%d'" % (time.time(), file_name, user_id)
        cur.execute(updated)
        self.db.commit()
        request.write('received')
        request.finish()
        return NOT_DONE_YET

    def render_DELETE(self, request):
        file_name_raw = request.args['filename'][0]
        username = request.args['username'][0]
        cur = self.db.cursor()
        user_id = int(db_access.get_id(username, self.db))
        killswitch = "DELETE FROM user_files WHERE user_id='%(uid)d' AND file='%(filename)s'" % {'uid': user_id,
                                                                                                 'filename': file_name_raw}
        cur.execute(killswitch)
        self.db.commit()
        directory = "./files/%s/" % request.args['username'][0]
        print directory + file_name_raw + '*'
        call("rm -rf " + directory + file_name_raw + '*', shell=True)
        request.finish()
        return NOT_DONE_YET


if __name__ == "__main__":
    resource = FileServerResource()
    factory = Site(resource)
    with open("onedirkey.crt") as keycert:
        cert = ssl.PrivateCertificate.loadPEM(keycert.read())

    reactor.listenTCP(3240, factory)
    print "Listening on 3240."
    reactor.run()
