# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 11:39:40 2021

"""

class Tenant:

    #constructor
    def __init__(self, name, aptNo):
        self.__name = name
        self.__aptNo = aptNo

    #returns name
    def getName(self):
        return self.__name

    #returns apartment number
    def getAptNo(self):
        return self.__aptNo

    #displays tenant info
    def display(self):
        print(self.__aptNo, self.__name)


class TenantList:

    #constructor, reads from tenants.txt file
    def __init__(self):
        self.__tenants = []

        with open("tenants.txt", 'a+') as t:
            t.seek(0)
            for line in t:
                values = line.strip().split(",")
                tempTenant = Tenant(values[0], int(values[1]))
                self.__tenants.append(tempTenant)

    #inserts tenant into list and stores into a text file for data persistence
    def insertTenant(self, tenant):
        tLine = "{},{}".format(tenant.getName(), tenant.getAptNo())

        with open("tenants.txt", 'a+') as t:
                t.write(tLine + "\n")
        self.__tenants.append(tenant)

    #returns tenant list
    def getTenants(self):
        return self.__tenants

    #displays contents of tenant list
    def display(self):
        for t in self.__tenants:
            t.display()


class AddTenant:

    #gets input for adding tenant, handles errors, inserts into tenant list
    def getInput(self, tenantList, rentRecord):
        dataIsValid = False

        while dataIsValid != True:
            dataIsValid = True
            name = input("Please enter tenant's name: ")
            aptNo = input("Please enter tenant's apartment number: ")

            try:
                aptNo = int(aptNo)
            except ValueError:
                print("Please enter an integer for the apartment number.")
                dataIsValid = False
                continue
            aptNo = int(aptNo)
            tenants = tenantList.getTenants()

            if tenants:
                for t in tenants:
                    if aptNo == t.getAptNo():
                        print("This apartment is already occupied.")
                        dataIsValid = False
                        continue

                    if name.lower() == t.getName().lower():
                        print("This tenant already exists.")
                        dataIsValid = False
                        continue

        tenant = Tenant(name, aptNo)
        rentRow = RentRow(name)
        tenantList.insertTenant(tenant)
        rentRecord.insertBlankRentRow(rentRow)


class RentRow:

    #constructor
    def __init__(self, name):
        self.__rent = [0] * 12
        self.__tenant = name

    #sets rent amount for specified month for instance of RentRow object
    def setRent(self, month, amount):
        self.__rent[month - 1] = amount

    #displays rent row information
    def display(self):
        print(f"{self.__tenant:20}" , end = "")
        for r in self.__rent:
            print(f"{r:<6}", end = "")
        print()

    #returns sum of all rent payments for instance of RentRow object
    def getSumOfRow(self):
        return sum(self.__rent)

    #returns name of tenant stored in instance of object
    def getTenantName(self):
        return self.__tenant


class RentRecord:

    #constructor, reads from rents.txt file
    def __init__(self):
        self.__rents = []
        with open("rents.txt", 'a+') as r:
            r.seek(0)

            for line in r:
               values = line.strip().split(",")
               tempRentRow = RentRow(values[0])

               for month, amount in enumerate(values[1:]):
                   tempRentRow.setRent(month + 1, int(amount))

               self.__rents.append(tempRentRow)

    # sets all payments to 0 for rentRow param and inserts into rent list,
    #as well as adds to rent.txt file for data persistence
    def insertBlankRentRow(self, rentRow):
        rLine = rentRow.getTenantName() + ",0" * 12

        with open("rents.txt", 'a+') as r:
            r.write(rLine + "\n")
        self.__rents.append(rentRow)

    #returns total of all rental payments made across all tenants
    def getTotalRentPaid(self):
        return sum([rentRow.getSumOfRow() for rentRow in self.__rents])

    #displays rent information for all RentRow objects stored in the RentRecord
    def display(self):
        print("Name\t\t\t\tJan   Feb   Mar   Apr   May   Jun   Jul   Aug   Sep   Oct   Nov   Dec")
        print("-"*90)
        for r in self.__rents:
            r.display()

    #updates the specified tenant's RentRow for the specified month, changing it to the
    #specified amount and changing the respective line in rents.txt file
    def updateRentRow(self, name, amount, month):
        oldStr = ""
        newStr = ""
        with open("rents.txt", 'r+') as r:
            for line in r:
                oldStr = line
                values = line.split(",")
                if values[0] == name:
                    values[month] = str(amount)
                    delimiter = ","
                    newStr = delimiter.join(values)
                    break
        with open("rents.txt") as r:
            fileData = r.read()

        newData = fileData.replace(oldStr, newStr)

        with open("rents.txt", 'w') as r:
            r.write(newData)

        for rentRow in self.__rents:
            if rentRow.getTenantName() == name:
                rentRow.setRent(month, amount)

    #returns rents list
    def getRents(self):
        return self.__rents

    #returns True if specified tenant has a rent row in the RentRecord, else false
    def tenantHasRentRecord(self, name):
        for r in self.__rents:
            if r.getTenantName().lower() == name.lower():
                return True

        return False


class InputRentalPayment:

    #gets input for adding rental payment, handles errors, inserts into rent record
    def getInput(self, rentRecord):
        dataIsValid = False
        tenantHasRentRecord = False

        while dataIsValid != True or tenantHasRentRecord != True:
            dataIsValid = True
            tenantHasRentRecord = True
            name = input("Please enter the name of the tenant paying rent: ")

            if rentRecord.tenantHasRentRecord(name) != True:
                print("This tenant does not exist. Please enter this tenant using 'Add Tenant' functionality.")
                tenantHasRentRecord = False
                return

            amount = input("Please enter the rent amount: ")

            try:
                amount = int(amount)

            except ValueError:
                print("You must enter a number.")
                dataIsValid = False
                continue

            amount = int(amount)
            month = input("Please enter the month this rent is for (1-12): ")

            if month.isdigit() != True or int(month) < 1 or int(month) > 12:
                print("Please enter an integer between 1-12.")
                dataIsValid = False
                continue
            month = int(month)
            rentRecord.updateRentRow(name.title(), amount, month)


class Expense:
    # Constructor
    def __init__(self, month, day, category, amount, payee):
        self.__month = month
        self.__day = day
        self.__category = category
        self.__amount = amount
        self.__payee = payee

    # Collection of get methods
    def getMonth(self):
        return self.__month

    def getDay(self):
        return self.__day

    def getCategory(self):
        return self.__category

    def getAmount(self):
        return self.__amount

    def getPayee(self):
        self.__payee

    # Displays expense information
    def display(self):
        print("{}/{: <5}".format(self.__month, self.__day), "{: <11}".format(self.__payee),
              "${: <10.2f}".format(self.__amount), self.__category)


class ExpenseRecord:

    # Constructor. Reads from expenses.txt file
    def __init__(self):
        self.__expenses = []
        with open("expenses.txt", 'a+') as e:
            e.seek(0)
            for line in e:
                values = line.strip().split(",")
                tempExpense = Expense(values[0], values[1], values[2], float(values[3]), values[4])
                self.__expenses.append(tempExpense)

    # Inserts expense into expenses list and adds to expense.txt file for data persistence
    def insertExpense(self, month, day, category, amount, payee):
        eLine = "{},{},{},{},{}".format(month, day, category, amount, payee)
        with open("expenses.txt", 'a+') as e:
                e.write(eLine + "\n")
        expenseLog = Expense(month, day, category, amount, payee)
        self.__expenses.append(expenseLog)

    # Returns total amount of all expenses stored in expenses list
    def getTotalExpensesPaid(self):
        totalExpense = 0
        for e in self.__expenses:
            totalExpense += e.getAmount()
        return totalExpense

    # Displays expense information for all expenses stored in expenses list
    def display(self):
        print("Date\tPayee\t\tAmount\t\tCategory")
        print("-"*41)
        for e in self.__expenses:
            e.display()


class InputExpense:

    # Gets input for adding expense, inserts into expense record
    def getInput(self, expenseRecord):
        validDate = False
        validAmount = False

        while not validDate:
            try:
                month = int(input("Enter the month (1-12): "))
                day = int(input("Enter the day (1-31): "))

            except ValueError:
                print("Input was invalid")

            else:
                if 1 <= month <= 12 and 1 <= day <= 31:
                    validDate = True

                else:
                    print("Input was invalid. Please input a valid date")

        name = input("Enter the name of the payee: ")

        while not validAmount:
            try:
                amount = round(float(input("Enter the amount expended: ")), 2)

            except ValueError:
                print("Input was invalid")

            else:
                if amount < 1:
                    print("Input was invalid")

                else:
                    validAmount = True

        category = input("Enter the category of the expense: ")
        expenseRecord.insertExpense(month, day, category, amount, name)


class AnnualSummary:
    # Constructor
    def __init__(self, rentRecord, expenseRecord):
        self.__rentAmt = rentRecord.getTotalRentPaid()
        self.__expenseAmt = expenseRecord.getTotalExpensesPaid()

    # Displays the total amount spent and received during the year categorically. This includes the profit
    def display(self):
        print("Income:\nRent ${:.2f}".format(self.__rentAmt))
        print("-"*20, "\nExpenses:")
        expenseCategory = {}

        f = open("expenses.txt", "r")

        for line in f:
            nextLine = line.split(",")

            if nextLine[2].lower() in expenseCategory:
                expenseCategory[nextLine[2].lower()] = expenseCategory[nextLine[2].lower()] + float(nextLine[3])

            else:
                expenseCategory[nextLine[2].lower()] = float(nextLine[3])

        f.close()

        for key in expenseCategory:
            print(key, "${:.2f}".format(expenseCategory[key]))

        print("-"*20, "\nBalance:", "${:.2f}".format(self.__calculateProfit()))

    # Calculates the total of the amount expended
    def __sum(self, expenseCategory):
        sumSpent = 0
        for key in expenseCategory:
            sumSpent += expenseCategory[key]

        return sumSpent

    # Calculates the profit based off of expenditure and rent received
    def __calculateProfit(self):
        profit = self.__rentAmt - self.__expenseAmt
        return profit


# Prompts the user the input the correct login credentials.
def logIn():
    username = "Austin"
    password = "343"
    inputUser = input("Please enter your user name: ")
    inputPass = input("Please enter your password: ")

    while inputUser != username or inputPass != password:
        print("Username and/or password was incorrect. Please try again.")
        inputUser = input("Please enter your user name: ")
        inputPass = input("Please enter your password: ")


def main():
    logIn()
    inputTenantScreen = AddTenant()
    inputRentScreen = InputRentalPayment()
    inputExpenseScreen = InputExpense()
    tenantList = TenantList()
    rentRecord = RentRecord()
    expenseRecord = ExpenseRecord()
    choice = ''

    while choice != 'q':
        print("Press 'i' to input data\nPress 'd' to display a report\nPress 'q' to quit program")
        choice = input()

        if choice == 'i':
            print("Enter 't' to add tenant\nEnter 'r' to record rent payment\nEnter 'e' to record expense")
            choice = input()

            if choice == 't':
                inputTenantScreen.getInput(tenantList, rentRecord)

            if choice == 'r':
                inputRentScreen.getInput(rentRecord)

            if choice == 'e':
                inputExpenseScreen.getInput(expenseRecord)

        if choice == 'd':
            print("Enter 't' to display tenant list\n"
                  "Enter 'r' to display rental records\n"
                  "Enter 'e' to display expense reports\n"
                  "Enter 'a' to display annual report")
            choice = input()

            if choice == 't':
                tenantList.display()

            if choice == 'r':
                rentRecord.display()

            if choice == 'e':
                expenseRecord.display()

            if choice == 'a':
                annualRecord = AnnualSummary(rentRecord, expenseRecord)
                annualRecord.display()


if __name__ == "__main__":
    main()
