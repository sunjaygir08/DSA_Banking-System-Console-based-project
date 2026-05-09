# 🏦 Banking System - Console Application

A console-based banking system built with Python, demonstrating core DSA concepts (Stack, Queue, Dictionary). Features complete account management, secure transactions, and admin controls.

---

## ✨ Features

**User Features:**
- ✅ Create Account (PIN security)
- ✅ Login & Authentication
- ✅ Deposit & Withdraw
- ✅ Transfer to Beneficiaries
- ✅ Add Beneficiaries
- ✅ View Transaction History
- ✅ Account Details

**Admin Features:**
- ✅ View All Accounts
- ✅ Freeze/Unfreeze Accounts
- ✅ Undo Transactions

**System Features:**
- ✅ Data Persistence (JSON)
- ✅ Daily Limits (Rs. 50,000)
- ✅ Fraud Detection (>Rs. 20,000 alerts)
- ✅ Transaction IDs & Timestamps

---

## 🏗️ DSA Concepts Used

| Data Structure | Purpose | Time Complexity |
|---|---|---|
| **Stack** | Undo transactions (LIFO) | O(1) |
| **Queue** | Pending transactions (FIFO) | O(1) |
| **Dictionary** | Account lookup by account number | O(1) |
| **List** | Transaction history | O(1) append |

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.6+
- No external dependencies

### Run the Program
```bash
python "Banking System.py"
```
Data automatically saves to `bank_data.json`

---

## 💻 Quick Start

### Main Menu
```
1. Create Account
2. Login
3. Admin Panel
4. Undo Transaction
5. View Pending Transactions
6. Exit
```

### Example: Create Account
```
Account Number: 1001
Name: John Doe
PIN (4-6 digits): 1234
Initial Balance: 10000
✅ Account created!
```

### Example: Login & Deposit
```
Account: 1001
PIN: 1234
✅ Login successful!

User Menu → Deposit → Amount: 5000
✅ Deposited Rs.5000 | Balance: Rs.15000
```

---

## 📁 Project Files

| File | Description |
|------|---|
| `Banking System.py` | Main application (500+ lines) |
| `bank_data.json` | Auto-generated account data |
| `README.md` | This file |

---

## 🔐 Security

- 4-6 digit PIN authentication
- Active/Frozen account status
- Daily withdrawal limit (Rs. 50,000)
- Input validation on all fields
- Unique transaction IDs

---

## 📊 Database Structure (bank_data.json)

```json
{
  "1001": {
    "acc_no": "1001",
    "name": "John Doe",
    "pin": "1234",
    "balance": 15000,
    "status": "active",
    "daily_limit": 50000,
    "daily_used": 5000,
    "beneficiaries": ["1002"],
    "creation_date": "09-05-2026 10:30:45",
    "history": [...]
  }
}
```

---

## 📈 Complexity Analysis

**Time Complexity:**
- Create Account: O(1)
- Login: O(1)
- Deposit/Withdraw: O(1)
- Transfer: O(1)
- View History: O(n)
- Undo: O(1)
- Admin Panel: O(m)

**Space Complexity:** O(m×t + u + p)
- m = accounts, t = transactions, u = undo operations, p = pending transactions

---

## 💡 Usage Example

```
1. Create account 1001 (John Doe, Balance: 10,000)
2. Create account 1002 (Jane Smith, Balance: 5,000)
3. Login as John (1001)
4. Add 1002 as beneficiary
5. Deposit Rs. 5,000 → Balance: 15,000 (Stack: push)
6. Transfer Rs. 2,000 to Jane (Queue: add pending)
7. Jane receives Rs. 2,000
8. Undo deposit (Stack: pop) → Balance: 10,000
9. Admin views all accounts
```

---

## ⚠️ Notes

- Data auto-saves to JSON after each transaction
- Daily limits don't auto-reset (stays until next calendar day in real system)
- No admin password (demo purposes)
- Large withdrawal alerts (>Rs. 20,000) are informational only

---

## 🎓 Learning Concepts

This project Explain Concepts of:
- Data Structures (Stack, Queue, Dictionary, List)
- Object-Oriented Programming (OOP)
- File I/O & JSON serialization
- System design & architecture
- Console application development

---

## 📊 Project Stats

- **Lines of Code**: ~500+
- **Classes**: 2 (BankAccount, BankSystem)
- **Methods**: 20+
- **Data Structures**: 4

---

## 📝 License

MIT License - Free to use and modify

---

**Version**: 1.0.0 | **Updated**: May 9, 2026
