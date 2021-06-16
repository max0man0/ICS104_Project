# This work done by group 10:
# Mohammed Alzayani, 201915730, (50%)
# Abdullah Alhifthi, 201963030, (50%)

from time import sleep
import datetime

# A global constant containing the threshold of the money one can have in their account
THRESHOLD = -1000

def main():
    # Asks the user until receiving a valid input
    feature = input("Enter 'L' for login or 'S' for sign up: ").upper()
    while feature != "S" and feature != "L":
        print("Invalid input")
        feature = input("Enter 'L' for login or 'S' for sign up: ").upper()
    
    # Calls the function from the input (feature)
    if feature == "S":
        create()
    elif feature == "L":
        login()
    
    return


## Checks if the number is unique (doesn't have repeated digits)
#  @param strNum: A string of numbers that shouldn't have repeated digits
#  @return True or False
#
def isUnique(strNum):
    unique = True
    
    # Checks each number (num1) in strNum if it matches any of the following numbers (num2) 
    for num1 in strNum:
        index = strNum.find(num1)
        for num2 in strNum[index+1:]:
            if num1 == num2:
                unique = False
    
    return unique


## Checks if the email is of format "g20XXXXXXX@kfupm.edu.sa", where X is a digit
#  @param email: String to compare with the format "g20XXXXXXX@kfupm.edu.sa"
#  @return True or False
#
def isKFUPMEmail(email):
    valid = False
    
    # Checks the username
    if email[:3] == "g20" and email[3:10].isdigit():
        # Checks the organization and domain
        if email[10:] == "@kfupm.edu.sa":
            valid = True
            
    return valid


## Creates (or Overwrites) a file named [cardNumber].txt (where [cardNumber] is the card number entered by the user)
#  that contains the account and transaction information of the user, then redirect the user to the login feature
#
def create():
    # Print the sign up banner
    print(" --------")
    print("/Sign Up/")
    print("--------" )
    
    # Asks the user for the card number. It must contain 4 non-repeated digits
    cardNumber = input("Enter card number of 4 digits (none repeated): ")
    while len(cardNumber) != 4 or not cardNumber.isdigit() or not isUnique(cardNumber):
        print("Invalid input")
        cardNumber = input("Enter card number of 4 digits (none repeated): ")
    
    # Prints a new line to seperate card number from PIN
    print()
    
    # Asks the user for the PIN. It must contain 4 non-repeated digits
    PIN = input("Enter PIN of 4 digits (none repeated): ")
    while len(PIN) != 4 or not PIN.isdigit() or not isUnique(PIN):
        print("Invalid input")
        PIN = input("Enter PIN of 4 digits (none repeated): ")

    # Prints a new line to seperate PIN from Email
    print()
    
    # Asks the user for the email and make sure that the email is of format 'g20XXXXXXX@kfupm.edu.sa'
    email = input("Enter email address of format 'g20XXXXXXX@kfupm.edu.sa': ")
    while not isKFUPMEmail(email):
        print("Invalid format")
        email = input("Enter email address of format 'g20XXXXXXX@kfupm.edu.sa': ")
    
    # Opens the file for writing to transfer the information
    file = open(cardNumber + ".txt", "w")
    
    # Writes the information into the file
    file.write(cardNumber+"\n")
    file.write(PIN+"\n")
    file.write(email+"\n")
    file.write("Account Balance : 0\n")
    
    # Closes the file
    file.close()
    
    # Sleeps for 1.5 seconds
    sleep(1.5)
    
    # Redirects the user to the login feature
    login()
    return


## Compares the credentials in the file with the user's input. If it matches, it redirects the user to the main menu
#
def login():
    # Prints the login banner
    print(" ------")
    print("/Login/")
    print("------" )
    
    fileFound = False
    
    # Asks the user to enter a card number. It must have the same name as the file to read,
    # and if the user forgot to sign up before then give him a chance to sign up
    cardNumber = input("Enter card number (or 'S' to sign up): ")
    while not fileFound and cardNumber.lower() != "s":
        try:
            infile = open(cardNumber+".txt", "r")
            fileFound = True
        except IOError:
            print("Card number does not match. There is no file")
            cardNumber = input("Enter card number (or 's' to sign up): ")    
    if cardNumber.lower() == "s":
        create()
        return
    
    # Reads the lines of the file into a list
    linesList = infile.readlines()
    # Closes the file
    infile.close()
    
    # Prints a new line to seperate card number from PIN
    print()
    
    # Gets PIN from the file
    actualPIN = linesList[1].rstrip()
    
    # Compares the inputed PIN with the actual PIN
    inputPIN = input("Enter PIN: ")
    while inputPIN != actualPIN:
        print("PIN does not match")
        PIN = input("Enter PIN: ")
    
    # Removes all of the dashes from the list of lines in case of a forced termination
    while "-\n" in linesList:
        linesList.remove("-\n")
    
    # Writes a dash that indicates the start of the session
    outfile = open(cardNumber+".txt", "w")
    outfile.writelines(linesList)
    outfile.write("-\n")
    outfile.close()
    
    terminated = False
    while not terminated:
        # Always sleeps before showing the menu
        sleep(1.5)
        
        # Prints menu
        print()
        print("Bank Account Program")
        print("=========================================")
        print("1.    Show account information")
        print("2.    Change PIN number")
        print("3.    Withdraw amount of money")
        print("4.    Deposit amount of money")
        print("5.    Pay bills")
        print("6.    View the last transactions")
        print("7.    Terminate the program")
        print("=========================================")
        
        # Validates feature number
        feature = input("Enter wanted feature: ")
        while not feature.isdigit() or not (1 <= int(feature) <= 7):
            print("Invalid input")
            feature = input("Enter wanted feature: ")
        print()
        
        # Calls the function from the input (feature)
        if feature == '1':
            show(cardNumber)
        elif feature == '2':
            changePINFun(cardNumber)
        elif feature == '3':
            withdrawFun(cardNumber)
        elif feature == '4':
            depositFun(cardNumber)
        elif feature == '5':
            payBillFun(cardNumber)
        elif feature == '6':
            viewTransactionFun(cardNumber)
        elif feature == '7':
            terminated = terminateFun(cardNumber)
        
    return


## Shows the user's account details saved in the txt file
#  @param file: the name of the txt file
#
def show(file):
    # Read the lines of the file into a list
    infile = open(file+".txt", "r")
    linesList = infile.readlines()[:4]
    infile.close()
    
    # Format the contents of the list
    linesList[0] = "Card number: " + linesList[0]
    linesList[1] = "PIN: " + linesList[1]
    linesList[2] = "Email: " + linesList[2]
    
    # Print the contents of the list
    for line in linesList:
        print(line,end="")
        
    return


## Changes the PIN of the account and updates the txt file accordingly
#  @param file: the name of the txt file
#
def changePINFun(file):
    # Read the lines of the file into a list
    infile = open(file+".txt", "r")
    linesList = infile.readlines()
    infile.close()
    
    # Ask the user for the PIN. It must contain 4 non-repeated digits
    newPIN = input("Enter the new PIN of 4 digits (none repeated): ")
    while len(newPIN) != 4 or not newPIN.isdigit() or not isUnique(newPIN):
        print("Invalid input")
        newPIN = input("Enter the new PIN of 4 digits (none repeated): ")
        
    # Updates the PIN in the list of lines
    linesList[1] = newPIN + "\n"
    
    # Write the list of lines into the txt file
    outfile = open(file+".txt", "w")
    outfile.writelines(linesList)
    outfile.close()
    
    return

## Asks the user for a float and validate the input (must be a positive float)
#  @param message: string to be displayed to the user. Default value: None
#  @return the positive float gotten from the user
#
def getPositiveFloat(message = None):
    valid = False
    number = 0
    
    while not valid or number < 0:
        try:
            number = float(input(message))
            valid = True
            if number < 0:
                print('Enter a positive number')
        except ValueError:
            print('Enter a positive number')
            
    return number


## Gets the current local date and time
#  @return a string containing local date and local time seperated by a space
#
def getDateAndTime():
    now = datetime.datetime.now()
    
    localDate = now.strftime("%x")
    localTime = now.strftime("%X")
    
    return localDate + " " + localTime


## Asks the user if they want to take a loan (This is the extra service)
#  @param completeAmount: the amount of money to complete the transaction (amount to loan)
#  @param untilThreshold: the amount of money until reaching the thershold if you take the loan
#  @return a string containing 'y' for yes or 'n' for no
#
def getLoanConfirmation(completeAmount, untilThreshold):
    print("You do not have enough money to complete the transaction.")
    print("Do you want to take a loan of %.2f ?" % completeAmount)
    confirmation = input("If you take the loan you will have %.2f SAR until you reach the threshold. (y to take n to refuse): " % untilThreshold ).lower()
    while confirmation != 'y' and confirmation != 'n':
        print("Invalid input")
        print("Do you want to take a loan of %.2f ?" % completeAmount)
        confirmation = input("If you take the loan you will have %.2f SAR until you reach the threshold. (y to take n to refuse): " % untilThreshold ).lower()
        
    return(confirmation)
 

## Withdraws money from the user's account, then updates the account balance in the txt file accordingly.
#  @param file: the name of the txt file
#
def withdrawFun(file):
    # Reads the lines of the file into a list
    infile = open(file + ".txt", "r")
    linesList = infile.readlines()
    infile.close()
    
    loanTaken = False
    loanConfirmation = 'n'
    
    # Gets the balance from the list of lines of the file
    balance = float(linesList[3][18:].rstrip())
    
    # Checks if the user has enough money to withdraw
    if balance == THRESHOLD:
        print("You cannot withdraw")
    else:
        # Asks the user for the amount of money to withdraw
        # If the amount of money to withdraw will subceed the threshold 
        # then it asks the user for another input
        money = getPositiveFloat("Enter the amount you want to withdraw: ")
        while balance - money < THRESHOLD:
            print('You will subceed the threshold.')
            money = getPositiveFloat("Enter the amount you want to withdraw: ")
        # If the user doesn't have enough money to complete the transaction but will not subceed the threshold
        while not loanTaken and loanConfirmation == 'n' and balance - money < 0:
            # The amount of money to complete the transaction (amount to loan)
            completeAmount = abs(balance - money)
            # The amount of money until reaching the thershold if you take the loan
            untilThreshold = abs(completeAmount + THRESHOLD)
            # Asks the user if he wants to take a loan
            loanConfirmation = getLoanConfirmation(completeAmount,untilThreshold)
            
            if loanConfirmation == 'n':
                # Asks the user for the amount of money to withdraw again if the user doesn't want to take the loan
                # If the amount of money to withdraw will subceed the threshold 
                # then it asks the user for another input
                money = getPositiveFloat("Enter the amount you want to withdraw: ")
                while balance - money < THRESHOLD:
                    print('You will subceed the threshold.')
                    money = getPositiveFloat("Enter the amount you want to withdraw: ")
            elif loanConfirmation == 'y':
                # Deducts from the account balance in the list of lines if the user wants to take the loan
                balance = balance - money
                linesList[3] = "Account Balance = " + str(balance) + "\n"
                loanTaken = True
                
        if balance - money >= 0:
            # Deducts from the account balance in the list of lines if no loan is needed
            balance = balance - money
            linesList[3] = "Account Balance = " + str(balance) + "\n"
        
        # Adds the transaction information to the end of the list of lines
        transaction = getDateAndTime() + "||Withdraw||"+str(money) + "\n"
        linesList.append(transaction)
        
        # Writes the list of lines into the file
        outfile = open(file + ".txt", "w")
        outfile.writelines(linesList)
        outfile.close()
        
    return
    
    
## Adds to the account balance in the txt file
#  @param file: the name of the txt file
#
def depositFun(file):
    # Reads the lines of the file into a list
    infile = open(file + ".txt", "r")
    linesList = infile.readlines()
    infile.close()
    
    # Asks the user for the amount of money to deposit
    money = getPositiveFloat("Enter the amount to deposit: ")
    
    # Adds to the account balance in the list of lines
    balance = float(linesList[3][18:].rstrip())
    balance = balance + money
    linesList[3] = "Account Balance = " + str(balance) + "\n"
    
    # Adds the transaction information to the end of the list of lines
    transaction = getDateAndTime() + "||Deposit||"+str(money) + "\n"
    linesList.append(transaction)
    
    # Writes the list of lines into the file
    outfile = open(file + ".txt", "w")
    outfile.writelines(linesList)
    outfile.close()
    
    return


## Pays a bill from the user's account, deduct this bill from the account 
#  and updates the account details in the file accordingly.
#  @param file: the name of the txt file
#
def payBillFun(file):
    # Reads the lines of the file into a list
    infile = open(file + ".txt", "r")
    linesList = infile.readlines()
    infile.close()
    
    # Asks the user for the name of the bill
    billName = input("Enter the name of the Bill: ")
    
    # Asks the user for the card number of the receiving account. It must contain 4 non-repeated digits
    receiverAccount = input('Enter the card number of the receiving account "4 digits (none repeated)": ')
    while len(receiverAccount) != 4 or not isUnique(receiverAccount):
        print("Invalid input")
        receiverAccount = input('Enter the card number of the receiving account "4 digits (none repeated)": ')
    
    loanTaken = False
    loanConfirmation = 'n'
    
    # Gets the balance from the list of lines of the file
    balance = float(linesList[3][18:].rstrip())
    
    # Checks if the user has enough money to withdraw
    if balance == THRESHOLD:
        print("You cannot transfer")
        return
    else:
        # Asks the user for the amount of money to withdraw
        # If the amount of money to withdraw will subceed the threshold 
        # then it asks the user for another input
        money = getPositiveFloat("Enter the amount you want to transfer: ")
        while balance - money < THRESHOLD:
            print('You will subceed the threshold.')
            money = getPositiveFloat("Enter the amount you want to transfer: ")
        # If the user doesn't have enough money to complete the transaction but will not subceed the threshold
        while not loanTaken and loanConfirmation == 'n' and balance - money < 0:
            # The amount of money to complete the transaction (amount to loan)
            completeAmount = abs(balance - money)
            # The amount of money until reaching the thershold if you take the loan
            untilThreshold = abs(completeAmount + THRESHOLD)
            # Asks the user if he wants to take a loan
            loanConfirmation = getLoanConfirmation(completeAmount,untilThreshold)
            
            if loanConfirmation == 'n':
                # Asks the user for the amount of money to withdraw again if the user doesn't want to take the loan
                # If the amount of money to withdraw will subceed the threshold 
                # then it asks the user for another input
                money = getPositiveFloat("Enter the amount you want to transfer: ")
                while balance - money < THRESHOLD:
                    print('You will subceed the threshold.')
                    money = getPositiveFloat("Enter the amount you want to transfer: ")
            elif loanConfirmation == 'y':
                # Deducts from the account balance in the list of lines if the user wants to take the loan
                balance = balance - money
                linesList[3] = "Account Balance = " + str(balance) + "\n"
                loanTaken = True
                
        if balance - money >= 0:
            # Deducts from the account balance in the list of lines if no loan is needed
            balance = balance - money
            linesList[3] = "Account Balance = " + str(balance) + "\n"
        
        # Adds the transaction information to the end of the list of lines
        transaction = getDateAndTime() + "||PayBill||" + billName + "||" + receiverAccount + "||" + str(money) + "\n"
        linesList.append(transaction)
        
        # Writes the list of lines into the file
        outfile = open(file + ".txt", "w")
        outfile.writelines(linesList)
        outfile.close()
        
        return

    
## Shows the history of transactions of the user's account based on the file.
#  @param file: the name of the txt file
#
def viewTransactionFun(file):
    # Reads the lines of the file into a list
    infile = open(file + ".txt", "r")
    linesList = infile.readlines()
    infile.close()
    
    # Puts a test value at the end of the list of liunes
    TESTVALUE = 'TEST'
    linesList.append(TESTVALUE)
    
    # Checks if there are any transactions in the history of the account
    # by checking if the 6th row of the file is the test value
    """
    Sample txt file:
    1234
    5678
    g20XXXXXXX@kfupm.edu.sa
    Account Balance = 0
    -
    TEST
    """
    if linesList[5] == TESTVALUE:
        # If there are no transactions
        print("No transactions")
    else:
        # Prints the history of transactions
        # Exculdes the dash (indicator of the start of the session)
        for i in range(len(linesList[4:-1])):
            if linesList[4 + i] != "-\n":
                print(linesList[4 + i],end="")
                
    return


## Shows the last transactions on the account during the session then terminates the program
#  @param file: the name of the txt file
#  @return True, indicating the termination of the program
#
def terminateFun(file):
    # Reads the lines of the file into a list
    infile = open(file + ".txt", "r")
    linesList = infile.readlines()
    infile.close()
    
    # Gets the index of the dash (indicator of the start of the session)
    indicatorIndex = linesList.index("-\n")
    
    # Prints the history of transactions from the dash onwards
    for line in linesList[indicatorIndex+1:]:
        print(line, end="")
    
    # Remove the dash from the list of lines
    linesList.pop(indicatorIndex)
    
    # Writes the list of lines into the file
    outfile = open(file+".txt", "w")
    outfile.writelines(linesList)
    outfile.close()
    
    return True

# Start the program
main()
