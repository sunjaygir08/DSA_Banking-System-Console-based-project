from collections import deque
import json
import os
from datetime import datetime
import random

# ==================== DATA STRUCTURES ====================
pending_transactions = deque()  # Queue for pending transactions
undo_stack = []  # Stack for undo operations
accounts = {}  # Dictionary for all accounts
transaction_counter = 1000  # Transaction ID counter
DATA_FILE = "bank_data.json"


# ==================== BANK ACCOUNT CLASS ====================
class BankAccount:
    def __init__(self, acc_no, name, pin, initial_balance=0):
        self.acc_no = acc_no
        self.name = name
        self.pin = pin
        self.balance = initial_balance
        self.status = "active"
        self.history = []
        self.daily_limit = 50000
        self.daily_used = 0
        self.beneficiaries = []
        self.creation_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def deposit(self, amount):
        """Deposit money to account"""
        if amount <= 0:
            return False, "Amount must be positive"
        
        if self.status == "frozen":
            return False, "❌ Account is frozen. Cannot deposit."
        
        self.balance += amount
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.history.append(
            f"[{timestamp}] Deposited Rs.{amount} | Balance: Rs.{self.balance}"
        )
        undo_stack.append(("deposit", self.acc_no, amount))
        return True, f"✅ Deposited Rs.{amount} successfully"

    def withdraw(self, amount):
        """Withdraw money from account"""
        if amount <= 0:
            return False, "Amount must be positive"
        
        if self.status == "frozen":
            return False, "❌ Account is frozen. Cannot withdraw."
        
        if self.daily_used + amount > self.daily_limit:
            remaining = self.daily_limit - self.daily_used
            return False, f"❌ Daily limit exceeded. Remaining limit: Rs.{remaining}"
        
        if amount > self.balance:
            return False, f"❌ Insufficient balance. Available: Rs.{self.balance}"
        
        # Fraud Detection
        if amount > 20000:
            print("⚠️  FRAUD ALERT: Large withdrawal detected!")
        
        self.balance -= amount
        self.daily_used += amount
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.history.append(
            f"[{timestamp}] Withdrew Rs.{amount} | Balance: Rs.{self.balance}"
        )
        undo_stack.append(("withdraw", self.acc_no, amount))
        return True, f"✅ Withdrew Rs.{amount} successfully"

    def show_history(self):
        """Display transaction history"""
        if not self.history:
            print("\n📋 Transaction History: No transactions yet")
            return
        
        print("\n" + "="*70)
        print("📋 TRANSACTION HISTORY".center(70))
        print("="*70)
        for item in self.history:
            print(f"  {item}")
        print("="*70)

    def to_dict(self):
        """Convert account to dictionary for JSON storage"""
        return {
            "acc_no": self.acc_no,
            "name": self.name,
            "pin": self.pin,
            "balance": self.balance,
            "status": self.status,
            "history": self.history,
            "daily_limit": self.daily_limit,
            "daily_used": self.daily_used,
            "beneficiaries": self.beneficiaries,
            "creation_date": self.creation_date
        }

    @staticmethod
    def from_dict(data):
        """Create account from dictionary"""
        acc = BankAccount(data["acc_no"], data["name"], data["pin"], data["balance"])
        acc.status = data["status"]
        acc.history = data["history"]
        acc.daily_limit = data["daily_limit"]
        acc.daily_used = data["daily_used"]
        acc.beneficiaries = data["beneficiaries"]
        acc.creation_date = data["creation_date"]
        return acc


# ==================== BANK SYSTEM CLASS ====================
class BankSystem:
    def __init__(self):
        self.load_data()

    def create_account(self):
        """Create new bank account"""
        print("\n" + "="*70)
        print("CREATE ACCOUNT".center(70))
        print("="*70)
        
        acc_no = input("\n📝 Enter Account Number: ").strip()
        
        if not acc_no:
            print("❌ Account number cannot be empty")
            return
        
        if acc_no in accounts:
            print("❌ Account already exists.")
            return
        
        name = input("📝 Enter Name: ").strip()
        if not name:
            print("❌ Name cannot be empty")
            return
        
        while True:
            pin = input("📝 Set PIN (4-6 digits): ").strip()
            if len(pin) >= 4 and len(pin) <= 6 and pin.isdigit():
                break
            print("❌ PIN must be 4-6 digits")
        
        initial_balance = 0
        try:
            initial_balance = float(input("💰 Enter Initial Balance (optional, press Enter for 0): ") or 0)
            if initial_balance < 0:
                print("❌ Balance cannot be negative")
                return
        except ValueError:
            print("❌ Invalid amount")
            return
        
        accounts[acc_no] = BankAccount(acc_no, name, pin, initial_balance)
        self.save_data()
        print(f"\n✅ Account created successfully!")
        print(f"   Account Number: {acc_no}")
        print(f"   Account Holder: {name}")
        print(f"   Initial Balance: Rs.{initial_balance}")

    def login(self):
        """Login to account"""
        print("\n" + "="*70)
        print("LOGIN".center(70))
        print("="*70)
        
        acc_no = input("\n📝 Enter Account Number: ").strip()
        pin = input("🔐 Enter PIN: ").strip()
        
        if acc_no not in accounts:
            print("❌ Account not found.")
            return None
        
        account = accounts[acc_no]
        
        if account.pin != pin:
            print("❌ Wrong PIN")
            return None
        
        if account.status == "frozen":
            print("❌ Account is frozen. Please contact admin.")
            return None
        
        print(f"\n✅ Login Successful! Welcome {account.name}")
        return account

    def deposit(self, user):
        """Deposit money"""
        print("\n" + "-"*70)
        print("DEPOSIT MONEY".center(70))
        print("-"*70)
        
        try:
            amount = float(input("\n💰 Enter Amount to Deposit: "))
            success, message = user.deposit(amount)
            print(f"\n{message}")
            print(f"   Current Balance: Rs.{user.balance}")
        except ValueError:
            print("❌ Invalid amount. Please enter a number.")

    def withdraw(self, user):
        """Withdraw money"""
        print("\n" + "-"*70)
        print("WITHDRAW MONEY".center(70))
        print("-"*70)
        
        try:
            amount = float(input("\n💰 Enter Amount to Withdraw: "))
            success, message = user.withdraw(amount)
            print(f"\n{message}")
            if success:
                print(f"   Current Balance: Rs.{user.balance}")
        except ValueError:
            print("❌ Invalid amount. Please enter a number.")

    def transfer(self, sender):
        """Transfer money to beneficiary"""
        print("\n" + "-"*70)
        print("TRANSFER MONEY".center(70))
        print("-"*70)
        
        if sender.status == "frozen":
            print("❌ Account is frozen. Cannot transfer.")
            return
        
        if not sender.beneficiaries:
            print("❌ No beneficiaries added. Add beneficiary first.")
            return
        
        print("\n📋 Your Beneficiaries:")
        for i, b in enumerate(sender.beneficiaries, 1):
            ben_acc = accounts[b]
            print(f"   {i}. {ben_acc.acc_no} - {ben_acc.name}")
        
        receiver_acc = input("\n📝 Enter Receiver Account Number: ").strip()
        
        if receiver_acc not in accounts:
            print("❌ Receiver not found.")
            return
        
        if receiver_acc not in sender.beneficiaries:
            print("❌ Receiver not added as beneficiary.")
            return
        
        if receiver_acc == sender.acc_no:
            print("❌ Cannot transfer to same account.")
            return
        
        try:
            amount = float(input("💰 Enter Amount: "))
            
            if amount <= 0:
                print("❌ Amount must be positive")
                return
            
            if amount > sender.balance:
                print(f"❌ Insufficient Balance. Available: Rs.{sender.balance}")
                return
            
            # Create transaction
            global transaction_counter
            transaction_id = transaction_counter
            transaction_counter += 1
            
            sender.balance -= amount
            sender.daily_used += amount
            receiver = accounts[receiver_acc]
            receiver.balance += amount
            
            timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            
            sender.history.append(
                f"[{timestamp}] Transferred Rs.{amount} to {receiver.name} ({receiver_acc}) | TXN ID: {transaction_id} | Balance: Rs.{sender.balance}"
            )
            receiver.history.append(
                f"[{timestamp}] Received Rs.{amount} from {sender.name} ({sender.acc_no}) | TXN ID: {transaction_id} | Balance: Rs.{receiver.balance}"
            )
            
            undo_stack.append(("transfer", sender.acc_no, receiver_acc, amount))
            pending_transactions.append((transaction_id, sender.acc_no, receiver_acc, amount))
            
            print(f"\n✅ Transfer Successful!")
            print(f"   Transaction ID: {transaction_id}")
            print(f"   Amount: Rs.{amount}")
            print(f"   To: {receiver.name}")
            print(f"   Your Balance: Rs.{sender.balance}")
            
        except ValueError:
            print("❌ Invalid amount. Please enter a number.")

    def add_beneficiary(self, account):
        """Add beneficiary account"""
        print("\n" + "-"*70)
        print("ADD BENEFICIARY".center(70))
        print("-"*70)
        
        b = input("\n📝 Enter Beneficiary Account Number: ").strip()
        
        if b not in accounts:
            print("❌ Account not found.")
            return
        
        if b == account.acc_no:
            print("❌ Cannot add own account as beneficiary.")
            return
        
        if b in account.beneficiaries:
            print("❌ Already added as beneficiary.")
            return
        
        account.beneficiaries.append(b)
        ben_name = accounts[b].name
        print(f"\n✅ Beneficiary Added: {ben_name} ({b})")

    def show_account_details(self, user):
        """Show account details"""
        print("\n" + "="*70)
        print("ACCOUNT DETAILS".center(70))
        print("="*70)
        print(f"  Account Number:  {user.acc_no}")
        print(f"  Account Holder:  {user.name}")
        print(f"  Current Balance: Rs.{user.balance}")
        print(f"  Account Status:  {user.status.upper()}")
        print(f"  Created Date:    {user.creation_date}")
        print(f"  Daily Limit:     Rs.{user.daily_limit}")
        print(f"  Daily Used:      Rs.{user.daily_used}")
        if user.beneficiaries:
            print(f"  Beneficiaries:   {', '.join(user.beneficiaries)}")
        print("="*70)

    def view_beneficiaries(self, user):
        """View all beneficiaries"""
        print("\n" + "-"*70)
        print("MY BENEFICIARIES".center(70))
        print("-"*70)
        
        if not user.beneficiaries:
            print("  No beneficiaries added yet.")
        else:
            for i, b in enumerate(user.beneficiaries, 1):
                ben_acc = accounts[b]
                print(f"  {i}. {ben_acc.name} ({b})")
        print("-"*70)

    def undo_transaction(self):
        """Undo last transaction"""
        print("\n" + "-"*70)
        print("UNDO TRANSACTION".center(70))
        print("-"*70)
        
        if not undo_stack:
            print("  ❌ No transaction to undo.")
            return
        
        last_action = undo_stack.pop()
        
        if last_action[0] == "deposit":
            action, acc_no, amount = last_action
            account = accounts[acc_no]
            account.balance -= amount
            print(f"  ✅ Deposit of Rs.{amount} undone.")
            print(f"     Updated Balance: Rs.{account.balance}")
        
        elif last_action[0] == "withdraw":
            action, acc_no, amount = last_action
            account = accounts[acc_no]
            account.balance += amount
            print(f"  ✅ Withdrawal of Rs.{amount} undone.")
            print(f"     Updated Balance: Rs.{account.balance}")
        
        elif last_action[0] == "transfer":
            action, sender_acc, receiver_acc, amount = last_action
            sender = accounts[sender_acc]
            receiver = accounts[receiver_acc]
            sender.balance += amount
            receiver.balance -= amount
            print(f"  ✅ Transfer of Rs.{amount} undone.")
            print(f"     Sender Balance: Rs.{sender.balance}")
            print(f"     Receiver Balance: Rs.{receiver.balance}")

    def freeze_account(self):
        """Freeze account (Admin)"""
        acc_no = input("📝 Enter Account Number to Freeze: ").strip()
        
        if acc_no not in accounts:
            print("❌ Account not found.")
            return
        
        accounts[acc_no].status = "frozen"
        print(f"🔒 Account {acc_no} has been FROZEN")
        self.save_data()

    def unfreeze_account(self):
        """Unfreeze account (Admin)"""
        acc_no = input("📝 Enter Account Number to Unfreeze: ").strip()
        
        if acc_no not in accounts:
            print("❌ Account not found.")
            return
        
        accounts[acc_no].status = "active"
        print(f"🔓 Account {acc_no} has been UNFROZEN")
        self.save_data()

    def admin_panel(self):
        """Admin panel to view all accounts"""
        print("\n" + "="*70)
        print("ADMIN PANEL".center(70))
        print("="*70)
        
        if not accounts:
            print("  No accounts in the system.")
            return
        
        print(f"\n{'Acc No':<12} {'Name':<15} {'Balance':<12} {'Status':<10}")
        print("-"*70)
        for acc in accounts.values():
            status_icon = "🔒" if acc.status == "frozen" else "✅"
            print(f"{acc.acc_no:<12} {acc.name:<15} Rs.{acc.balance:<11} {status_icon} {acc.status}")
        print("="*70)

    def view_transactions(self):
        """View all pending transactions"""
        print("\n" + "="*70)
        print("PENDING TRANSACTIONS".center(70))
        print("="*70)
        
        if not pending_transactions:
            print("  No pending transactions.")
            return
        
        for tx_id, sender, receiver, amount in pending_transactions:
            print(f"  TX ID: {tx_id} | {sender} → {receiver} | Rs.{amount}")
        print("="*70)

    def save_data(self):
        """Save all accounts to JSON file"""
        try:
            data = {acc_no: acc.to_dict() for acc_no, acc in accounts.items()}
            with open(DATA_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving data: {e}")

    def load_data(self):
        """Load accounts from JSON file"""
        global accounts
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                    accounts = {acc_no: BankAccount.from_dict(acc_data) for acc_no, acc_data in data.items()}
        except Exception as e:
            print(f"❌ Error loading data: {e}")


# ==================== MAIN PROGRAM ====================
def print_header():
    """Print application header"""
    print("\n" + "="*70)
    print("🏦 BANKING SYSTEM - CONSOLE APPLICATION 🏦".center(70))
    print("="*70)


def main_menu():
    """Main menu"""
    print("\n" + "-"*70)
    print("MAIN MENU".center(70))
    print("-"*70)
    print("  1. Create Account")
    print("  2. Login")
    print("  3. Admin Panel")
    print("  4. Undo Transaction")
    print("  5. View Pending Transactions")
    print("  6. Exit")
    print("-"*70)


def user_menu():
    """User menu after login"""
    print("\n" + "-"*70)
    print("USER MENU".center(70))
    print("-"*70)
    print("  1. Deposit")
    print("  2. Withdraw")
    print("  3. Transfer")
    print("  4. Add Beneficiary")
    print("  5. View Beneficiaries")
    print("  6. Transaction History")
    print("  7. Account Details")
    print("  8. Logout")
    print("-"*70)


def admin_menu():
    """Admin menu"""
    print("\n" + "-"*70)
    print("ADMIN MENU".center(70))
    print("-"*70)
    print("  1. View All Accounts")
    print("  2. Freeze Account")
    print("  3. Unfreeze Account")
    print("  4. Back to Main Menu")
    print("-"*70)


def main():
    """Main program loop"""
    bank = BankSystem()
    print_header()
    
    while True:
        main_menu()
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            bank.create_account()
            bank.save_data()
        
        elif choice == "2":
            user = bank.login()
            
            if user:
                while True:
                    user_menu()
                    ch = input("Enter your choice: ").strip()
                    
                    if ch == "1":
                        bank.deposit(user)
                        bank.save_data()
                    
                    elif ch == "2":
                        bank.withdraw(user)
                        bank.save_data()
                    
                    elif ch == "3":
                        bank.transfer(user)
                        bank.save_data()
                    
                    elif ch == "4":
                        bank.add_beneficiary(user)
                        bank.save_data()
                    
                    elif ch == "5":
                        bank.view_beneficiaries(user)
                    
                    elif ch == "6":
                        user.show_history()
                    
                    elif ch == "7":
                        bank.show_account_details(user)
                    
                    elif ch == "8":
                        print(f"\n👋 Thank you {user.name}! Logging out...\n")
                        break
                    
                    else:
                        print("❌ Invalid choice. Please try again.")
        
        elif choice == "3":
            while True:
                admin_menu()
                ch = input("Enter your choice: ").strip()
                
                if ch == "1":
                    bank.admin_panel()
                
                elif ch == "2":
                    bank.freeze_account()
                
                elif ch == "3":
                    bank.unfreeze_account()
                
                elif ch == "4":
                    break
                
                else:
                    print("❌ Invalid choice. Please try again.")
        
        elif choice == "4":
            bank.undo_transaction()
            bank.save_data()
        
        elif choice == "5":
            bank.view_transactions()
        
        elif choice == "6":
            print("\n" + "="*70)
            print("Thank you for using Banking System!".center(70))
            print("Goodbye! 👋".center(70))
            print("="*70 + "\n")
            bank.save_data()
            break
        
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()