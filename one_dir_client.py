import bcrypt

from user import User
import admin
import db_access
import getpass


if __name__ == "__main__":

    user = None

    print "##########################"
    print ""

    print "Available Commands:"
    print "login"
    print "logout"
    print "print"
    print "update"
    print "delete"
    print "create"

    print ""
    print "Admin Functions:"
    print "users"
    print "change"
    print "files"
    print "remove"

    print ""
    print "##########################"

    # A quick note on security in this code:
    # The security here is designed as a proof of possibility, 
    # and SHOULD NOT EVER be used in a scenario which needs actual 
    # security. The same holds for the entire project.

    while True:
        print ""
        command = raw_input("Enter a command: ")

        if command == "print":
            if not user:
                print "no current user"
                continue
            print "email: " + user.email
            print "password: " + user.password

        if command == "login":
            email = raw_input("Email: ")
            password = getpass.getpass("Password: ")
            user = User(email, password, '')
            if user.login():
                print "Login successful!"
            else:
                user = None
                print "Login failed."

        if command == "logout":
            user = None

        elif command == "update":
            if not user:
                print "Please login first"
                continue

            new_email = raw_input("New Email: ")
            new_password = raw_input("New Password: ")

            user.update(new_email, bcrypt.hashpw(new_password, bcrypt.gensalt(10)))
            user.email = new_email
            user.password = new_password

        elif command == "delete":
            if not user:
                print "Please login first"
                continue

            confirm = raw_input("Are you sure? Y/n: ")

            if confirm == "Y" or confirm == "y" or confirm == "yes" or confirm == "Yes":
                print "deleting %s with password %s" % (user.email, user.password)
                
                user.delete()
                user = None

        elif command == "create":
            email = raw_input("Email: ")
            password = raw_input("Password: ")
            password_confirm = raw_input("Confirm Password: ")
            while password != password_confirm:
                print "Passwords do no match"
                password = raw_input("Password: ")
                password_confirm = raw_input("Confirm Password: ")

            user = User(email, password, '')
            user.create(bcrypt.hashpw(password, bcrypt.gensalt(10)))

        elif command == "users":
            if not user.email == 'admin':
                print "Must have admin privileges"
                continue

            print admin.list_users(user.password)

        elif command == "change":
            if not user.email == 'admin':
                print "Must have admin privileges"
                continue

            old_email = raw_input("Email: ")
            new_email = raw_input("New Email: ")
            new_password = raw_input("New Password: ")

            admin.update_user(user.password, old_email, new_email, bcrypt.hashpw(new_password, bcrypt.gensalt(10)))

        elif command == "files":
            if not user.email == 'admin':
                print "Must have admin privileges"
                continue

            email = raw_input("Email: ")

            db = db_access.connect()
            files = db_access.get_files(email, db)
            
            for file_name in files.keys():
                print file_name + ": " + str(files[file_name]) + " Bytes"

        elif command == "remove":
            if not user.email == 'admin':
                print "Must have admin privileges"
                continue

            email = raw_input("Email: ")

            admin.remove(user.password, email)

        elif command == "quit":
            break

