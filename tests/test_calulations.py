import pytest
from app.calculations import add, subtract,multiply,divide,BankAccount,InsufficientFunds
# from app.calculations import add

@pytest.fixture()
def zero_bank_account():
    print("Creating empty bank acount")
    return BankAccount()

@pytest.fixture()
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1,num2,expected",
[
    (3,2,5),
    (2,2,4),
    (5,4,9)
])
def test_add(num1,num2,expected):
    print("testing add function")
    assert add(num1,num2)==expected
@pytest.mark.parametrize("num1,num2,expected",
[
    (3,2,1),
    (2,2,0),
    (5,4,1)
])    
def test_subtract(num1,num2,expected):
    assert subtract(num1,num2)==expected

def test_multiply():
    assert multiply(4,3)==12

def test_divide():
    assert divide(4,2)==2


def test_bank_set_initial_amount(bank_account):
    # bank_account=BankAccount(50)
    assert bank_account.balance==50

def test_bank_default_amount(zero_bank_account):
    print("Testing empty account")
    assert zero_bank_account.balance==0

def test_withdrawl(bank_account):
    # bank_account=BankAccount(50)
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_diposite(bank_account):
    # bank_account=BankAccount(50)
    bank_account.deposit(30)
    assert bank_account.balance==80

def test_collect_interest(bank_account):
    # bank_account=BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance,6) == 55


@pytest.mark.parametrize("deposited,withdrew,expected",
[
    (200,100,100),
    (50,10,40),
    (5000,1000,4000)
])  
def test_bank_transaction(zero_bank_account,deposited,withdrew,expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance==expected

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)


