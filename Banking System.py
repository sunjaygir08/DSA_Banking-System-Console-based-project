from collections import deque
import random

# Queue for pending transactions
pending_transactions = deque()

# Stack for undo
undo_stack = []

# Dictionary for accounts
accounts = {}


class BankAccount:
    def __init__(self, acc_no, name, pin):
        self.acc_no = acc_no
        self.name = name
        self.pin = pin
        self.balance = 0
        self.status = "active"
        self.history = []
        self.daily_limit = 25000
        self.daily_used = 0
        self.beneficiaries = []

    def deposit(self, amount):
        self.balance += amount
        self.history.append(f"Deposited Rs.{amount}")
        undo_stack.append(("deposit", self.acc_no, amount))

    def withdraw(self, amount):

        if self.status == "frozen":
            print("Account is frozen.")
            return

        if self.daily_used + amount > self.daily_limit:
            print("Daily limit exceeded.")
            return

        if amount > self.balance:
            print("Insufficient balance.")
            return

        self.balance -= amount
        self.daily_used += amount

        self.history.append(f"Withdraw Rs.{amount}")
        undo_stack.append(("withdraw", self.acc_no, amount))

        # Fraud Detection
        if amount > 20000:
            print("Fraud Alert: Large withdrawal detected!")

    def show_history(self):
        print("\nTransaction History")
        for item in self.history:
            print(item)


class BankSystem:

    def create_account(self):

        acc_no = input("Enter Account Number: ")

        if acc_no in accounts:
            print("Account already exists.")
            return

        name = input("Enter Name: ")
        pin = input("Set PIN: ")

        accounts[acc_no] = BankAccount(acc_no, name, pin)

        print("Account created successfully.")

    def login(self):

        acc_no = input("Enter Account Number: ")
        pin = input("Enter PIN: ")

        if acc_no not in accounts:
            print("Account not found.")
            return None

        account = accounts[acc_no]

        if account.pin != pin:
            print("Wrong PIN")
            return None

        print("Login Successful")
        return account

    def transfer(self, sender):

        receiver_acc = input("Enter Receiver Account: ")

        if receiver_acc not in accounts:
            print("Receiver not found.")
            return

        if receiver_acc not in sender.beneficiaries:
            print("Receiver not added as beneficiary.")
            return

        amount = int(input("Enter Amount: "))

        # Failed Transaction Simulation
        transaction_id = random.randint(1000, 9999)

        if amount > sender.balance:
            print("Insufficient Balance")
            return

        sender.balance -= amount

        # Simulate pending transaction
        pending_transactions.append(
            (transaction_id, sender.acc_no, receiver_acc, amount)
        )

        print(f"Transaction Pending... ID: {transaction_id}")

        # Complete transaction
        receiver = accounts[receiver_acc]
        receiver.balance += amount

        sender.history.append(
            f"Transferred Rs.{amount} to {receiver_acc}"
        )

        receiver.history.append(
            f"Received Rs.{amount} from {sender.acc_no}"
        )

        print("Transaction Successful")

    def add_beneficiary(self, account):

        b = input("Enter Beneficiary Account Number: ")

        if b not in accounts:
            print("Account not found.")
            return

        account.beneficiaries.append(b)

        print("Beneficiary Added")

    def undo_transaction(self):

        if not undo_stack:
            print("No transaction to undo.")
            return

        action, acc_no, amount = undo_stack.pop()

        account = accounts[acc_no]

        if action == "deposit":
            account.balance -= amount

        elif action == "withdraw":
            account.balance += amount

        print("Last transaction undone.")

    def freeze_account(self):

        acc_no = input("Enter Account Number: ")

        if acc_no in accounts:
            accounts[acc_no].status = "frozen"
            print("Account Frozen")

    def admin_panel(self):

        print("\nAll Accounts")

        for acc in accounts.values():
            print(
                f"{acc.acc_no} | {acc.name} | Balance: {acc.balance} | Status: {acc.status}"
            )


bank = BankSystem()

while True:

    print("\n===== BANKING SYSTEM =====")
    print("1. Create Account")
    print("2. Login")
    print("3. Undo Transaction")
    print("4. Freeze Account")
    print("5. Admin Panel")
    print("6. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        bank.create_account()

    elif choice == "2":

        user = bank.login()

        if user:

            while True:

                print("\n--- USER MENU ---")
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Transfer")
                print("4. Add Beneficiary")
                print("5. Transaction History")
                print("6. Logout")

                ch = input("Enter choice: ")

                if ch == "1":
                    amt = int(input("Enter Amount: "))
                    user.deposit(amt)

                elif ch == "2":
                    amt = int(input("Enter Amount: "))
                    user.withdraw(amt)

                elif ch == "3":
                    bank.transfer(user)

                elif ch == "4":
                    bank.add_beneficiary(user)

                elif ch == "5":
                    user.show_history()

                elif ch == "6":
                    break

    elif choice == "3":
        bank.undo_transaction()

    elif choice == "4":
        bank.freeze_account()

    elif choice == "5":
        bank.admin_panel()

    elif choice == "6":
        print("Thank You")
        break