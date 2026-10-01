from datetime import UTC, datetime

import pytest

from src.banking import BankAccount, Customer, InsufficientFundsError


def test_deposit_increases_balance():
    acc = BankAccount("1234567890")
    acc.deposit(100)
    assert acc.balance == 100


def test_withdraw_raises_on_insufficient_funds():
    acc = BankAccount("1234567890", balance=50)
    with pytest.raises(InsufficientFundsError):
        acc.withdraw(100)


def test_savings_minimum_balance_enforced():
    acc = BankAccount.create_savings("1234567890", balance=200)
    with pytest.raises(InsufficientFundsError):
        acc.withdraw(150)


def test_is_valid_account_number():
    assert BankAccount.is_valid_account_number("1234567890") is True
    assert BankAccount.is_valid_account_number("12345") is False


def test_customer_rejects_underage():
    today = datetime.now(tz=UTC).date()
    with pytest.raises(ValueError):
        Customer("Minor", today.replace(year=today.year - 10))


def test_customer_accepted_if_adult():
    today = datetime.now(tz=UTC).date()
    customer = Customer("Adult", today.replace(year=today.year - 20))
    assert customer.name == "Adult"
    assert customer.birth_date == today.replace(year=today.year - 20)
