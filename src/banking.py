import logging
from datetime import UTC, date, datetime

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
# Create a logger for this module
logger = logging.getLogger(__name__)


# Custom exception for insufficient funds
class InsufficientFundsError(Exception):
    """Custom exception for insufficient funds in the account."""

    def __init__(self, message, attempted_amount):
        super().__init__(message)
        self.attempted_amount = attempted_amount


# BankAccount class with logging and error handling
class BankAccount:
    def __init__(
        self, account_number, currency="USD", _account_type="checking", balance=0.0
    ):

        self.account_number = account_number
        self.currency = currency
        self._account_type = _account_type
        self.__balance = balance

    # balance property with getter and setter to ensure balance cannot be negative
    @property
    def balance(self):
        return self.__balance

    # setter for balance with logging and validation
    @balance.setter
    def balance(self, value):
        if value < 0:
            logger.error("Attempted to set negative balance: %s", value)
            raise ValueError("Balance cannot be negative")
        self.__balance = value

    # getter for account number
    @property
    def account_number(self):
        return self._account_number

    # setter for account number
    @account_number.setter
    def account_number(self, value):
        self._account_number = value

    # getter for currency
    @property
    def currency(self):
        return self._currency

    # setter for currency
    @currency.setter
    def currency(self, value):
        self._currency = value

    # getter for account type
    @property
    def account_type(self):
        return self._account_type

    # Deposit method with logging and validation
    def deposit(self, amount):
        if amount < 0:
            logger.error("Invalid deposit amount: %s", amount)
            raise ValueError("Deposit amount must be non-negative")
        self.balance = self.balance + amount
        logger.info("Deposit successful. New balance: %s", self.balance)

    # withdrawal method with logging and validation
    def withdraw(self, amount):
        if amount < 0:
            logger.error("Invalid withdrawal amount: %s", amount)
            raise ValueError("Withdrawal amount must be non-negative")

        min_balance = 100.0 if self._account_type == "savings" else 0.0

        if amount > self.balance - min_balance:
            logger.error("Insufficient funds for withdrawal of %s", amount)
            raise InsufficientFundsError("Insufficient funds for withdrawal", amount)

        self.balance = self.balance - amount
        logger.info("Withdrawal successful. New balance: %s", self.balance)

    # currency conversion method with logging and validation
    def convert_currency(self, target_currency, exchange_rate):
        if exchange_rate <= 0:
            logger.error("Invalid exchange rate: %s", exchange_rate)
            raise ValueError("Exchange rate must be positive")
        converted = self.balance * exchange_rate
        print(f"{converted:.2f} {target_currency}")

    # class method to create a savings account with logging and validation
    @classmethod
    def create_savings(cls, account_number, currency="USD", balance=100.0):
        if balance < 100.0:
            logger.error("Savings account requires a minimum balance of 100")
            raise ValueError("Initial savings balance must be at least 100")
        return cls(account_number, currency, "savings", balance)

    # static method to validate account number with logging and validation
    @staticmethod
    def is_valid_account_number(account_number):
        return account_number.isdigit() and len(account_number) == 10


# Phase 4: Customer class implementation
class Customer:
    user_count = 0

    def __init__(self, name, birth_date):
        age = (datetime.now(tz=UTC).date() - birth_date).days // 365
        if age < 18:
            logger.error("Customer %s is under 18", name)
            raise ValueError("Customer must be at least 18 years old")

        self.name = name
        self.birth_date = birth_date
        Customer.user_count += 1
        self._user_id = Customer.user_count
        self.__accounts = []

    @property
    def user_id(self):
        return self._user_id

    @property
    def accounts(self):
        return self.__accounts

    def add_account(self, account):
        if BankAccount.is_valid_account_number(account.account_number):
            self.__accounts.append(account)
        else:
            logger.error("Invalid account number: %s", account.account_number)

    def get_total_balance(self):
        return sum(acc.balance for acc in self.__accounts)

    def transfer(self, source_account, target_account, amount):
        try:
            source_account.withdraw(amount)
            target_account.deposit(amount)
        except (InsufficientFundsError, ValueError) as e:
            logger.error("Transfer failed: %s", e)


def menu():
    customers = []
    while True:
        print(
            "1. Add customer\n2. Add account\n3. Deposit\n4. Withdraw\n5. Transfer\n6. Exit"
        )
        choice = input("> ")
        try:
            if choice == "1":
                name = input("Name: ")
                birth_date = date.fromisoformat(input("Birth date (YYYY-MM-DD): "))
                customers.append(Customer(name, birth_date))
            elif choice == "2":
                uid = int(input("User id: "))
                customer = next(c for c in customers if c.user_id == uid)
                acc_num = input("Account number (10 digits): ")
                acc_type = input("Type (checking/savings): ")
                account = (
                    BankAccount.create_savings(acc_num)
                    if acc_type == "savings"
                    else BankAccount(acc_num, _account_type=acc_type)
                )
                customer.add_account(account)
            # ... deposit/withdraw/transfer follow the same pattern
            elif choice == "6":
                break
        except (ValueError, InsufficientFundsError, StopIteration) as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    menu()
