import sys
import getpass
from . import login, logout, login_check

def print_help_msg():
    print("Usage: ")
    print("    # login check")
    print("    python -m py_buaa_login status\n")
    print("    # login")
    print("    python -m py_buaa_login login \"<username>\" \"<password>\"")
    print("    python -m py_buaa_login login --stdin\n")
    print("    # logout")
    print("    python -m py_buaa_login logout")

def main(argv_list:list[str]):

    # help
    if len(argv_list) == 0 or ("--help" in argv_list):
        print_help_msg()
        return

    # login check
    elif argv_list[0] == "status":
        if len(argv_list) != 1:
            print("Usage: \n    python -m py_buaa_login status")
            return
        print("checking login status ...")
        if login_check():
            print("status: logged in.")
        else:
            print("status: logged out.")
        return
    
    # login
    elif argv_list[0] == "login":
        if "--stdin" in argv_list:
            username = input("username: ")
            password = getpass.getpass("password: ")
        
        elif len(argv_list) != 3:
            print("Usage: \n    python -m py_buaa_login login \"<username>\" \"<password>\"")
            print("Usage: \n    python -m py_buaa_login login --stdin")
            return
        
        else:
            username = argv_list[1]
            password = argv_list[2]
        login(username, password)

    # logout
    elif argv_list[0] == "logout":
        if len(argv_list) != 1:
            print("Usage: \n    python -m py_buaa_login logout")
            return
        logout()

    else:
        print_help_msg()
        return

if __name__ == "__main__":
    main(sys.argv[1:])
