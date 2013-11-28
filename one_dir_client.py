import user
import admin

if __name__ == "__main__":
    email = raw_input("Email: ")
    password = raw_input("Password: ")
    user = User(email, password, '')

    if(user.login()):
    	while True:
    		print "Available Commands:"
    		print "login"
    		print "update"
    		print "delete"
    		print "create"

    		print ""
    		print "Admin Functions:"
    		print "users"
    		print "change"
    		print "files"
    		print "remove"

    		command = raw_input("Enter a command: ")

    		if command == "login":
    			email = raw_input("Email: ")
    			password = raw_input("Password: ")
    			user = User(email, password, '')
    			if user.login():
    				print "Login successful!"
    			else:
    				user = None
    				print "Login failed."

    		elif command == "update":
    			if not user:
    				print "Please login first"
    				continue

    			new_email = raw_input("New Email: ")
    			new_password = raw_input("New Password: ")

    			user.update(new_email, new_password)

    		elif command == "delete":
    			if not user:
    				print "Please login first"
    				continue

    			confirm = raw_input("Are you sure? Y/n: ")

    			if confirm == "Y" or confirm == "y" or confirm == "yes" or confirm == "Yes":
    				user.delete()

    		elif command == "create":
    			email = raw_input("Email: ")
    			password = raw_input("Password: ")
    			password_confirm = raw_input("Confirm Password: ")
    			while password != password_confirm:
    				print "Passwords do no match"
    				password = raw_input("Password: ")
    				password_confirm = raw_input("Confirm Password: ")
    			
    			user = User(email, password, '')
    			user.create()

    		elif command == "users":
    			if not user.email == 'admin':
    				print "Must have admin privileges"
    				continue

    			print admin.list_users()

    		elif command == "change":
    			if not user.email == 'admin':
    				print "Must have admin privileges"
    				continue

    			old_email = raw_input("Email: ")
    			new_email = raw_input("New Email: ")
    			new_password = raw_input("New Password: ")

    			admin.update_user(old_email, new_email, new_password)

    		elif command == "files":
    			if not user.email == 'admin':
    				print "Must have admin privileges"
    				continue

    			email = raw_input("Email: ")

    			print admin.list_files(email)

    		elif command == "remove":
    			if not user.email == 'admin':
    				print "Must have admin privileges"
    				continue

    			email = raw_input("Email: ")

    			admin.remove(email)

