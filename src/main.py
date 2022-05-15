import os

import controller
import initializeFB


def menu():
    orgid, email = controller.getOrgID()
    print()
    
    while True:
        print("Welcome to CreepDonuts server manager")
        print(f'account: {email}')
        print(f'Organsation: {orgid}')
        print()
        print("1.Start logging")
        print("2.Start detection")
        print("3.Check IDS status")
        print("4.Initialize IDS")
        print()
        print("0.exit")
        print()
        choice = input("Please enter your choice: ")
        if choice == '0':
            print()
            input("Press ENTER to exit......")
            break
        elif choice == '1':
            print()
            controller.startlogging(orgid)
            input("Press ENTER back to main menu......")
        
        elif choice == '2':
            print()
            controller.startAnalysis(orgid)
            input("Press ENTER back to main menu......")
        
        elif choice == '3':
            print()
            controller.checkstatus(orgid)
            input("Press ENTER back to main menu......")
        
        elif choice == '4':
            print()
            controller.initializeIDS(orgid)
            input("Press ENTER back to main menu......")
        
        else:
            print()
            input("Please select a correct option......\nPress ENTER back to main menu......")
            print()






if __name__ == "__main__":
    menu()