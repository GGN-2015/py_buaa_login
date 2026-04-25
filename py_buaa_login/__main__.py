import sys
import getpass
from . import test, login, logout, login_check

def print_help_msg():
    print("Usage: ")
    print("    # test selenium")
    print("    python -m py_buaa_login test")
    print("    python -m py_buaa_login test \"<url>\"\n")
    print("    # login check")
    print("    python -m py_buaa_login status\n")
    print("    # login")
    print("    python -m py_buaa_login login \"<username>\" \"<password>\"")
    print("    python -m py_buaa_login login --stdin\n")
    print("    # logout")
    print("    python -m py_buaa_login logout\n")
    print("    # options")
    print("    --head: show browser window.")
    print("    --help: show this help message.")

def has_and_remove(list_val:list[str], s_val:str) -> tuple[bool, list[str]]:
    return (
        s_val in list_val,
        [
            item
            for item in list_val
            if item != s_val
        ]
    )

def main(argv_list:list[str]):
    with_head, argv_list = has_and_remove(argv_list, "--head")

    # help
    if len(argv_list) == 0 or ("--help" in argv_list):
        print_help_msg()
        return
    
    # test selenium
    elif argv_list[0] == "test":
        if len(argv_list) == 1:
            url = "https://www.google.com"
        elif len(argv_list) == 2:
            url = argv_list[1]
        else:
            print("Usage: \n    python -m py_buaa_login test")
            print("Usage: \n    python -m py_buaa_login test \"<url>\"")
            return
        suc = test(headless=not with_head, url=url)
        if suc:
            print("Test successfully.")
        else:
            print("Test failed.")
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
        login(username, password, not with_head)

    # logout
    elif argv_list[0] == "logout":
        if len(argv_list) != 1:
            print("Usage: \n    python -m py_buaa_login logout")
            return
        logout(not with_head)

    else:
        print_help_msg()
        return

if __name__ == "__main__":
    main(sys.argv[1:])
