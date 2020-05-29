from ofxparse import OfxParser
import codecs
import json


def get_ofx(path, file_name):
    with codecs.open(path + file_name, encoding="ISO-8859-1") as fileobj:
        ofx = OfxParser.parse(fileobj)

    return ofx


def print_transaction(transaction):
    print(transaction.id)  # id
    print(transaction.date)  # date
    print(transaction.amount)  # value
    print(transaction.memo)  # description


def write_in_file(file, transaction):
    to_write = {
        "value": str(transaction.amount),
        "date": str(transaction.date)[:10],
        "description": transaction.memo if len(transaction.memo) > 100 else transaction.memo[:100],
        "observation": "",
        "account": 1,
        "category": 18
    }
    file.writelines(json.dumps(to_write) + ',\n')


path = 'financial_control/core/static/'
files = ['202001.ofx', '202002.ofx', '202003.ofx', '202004.ofx']

file = open(path + 'extrato.json', "w")
file.write('[\n')

for file_name in files:
    ofx = get_ofx(path, file_name)
    account = ofx.account
    statement = account.statement

    for transaction in statement.transactions:
        write_in_file(file, transaction)

file.write('\n]')
file.close()

# # The OFX object
# ofx.account               # An Account object

# # AccountType
# # (Unknown, Bank, CreditCard, Investment)

# # Account

# account = ofx.occount
# account.account_id        # The account number
# # The account number (deprecated -- returns account_id)
# account.number
# account.routing_number    # The bank routing number
# account.branch_id         # Transit ID / branch number
# account.type              # An AccountType object
# account.statement         # A Statement object
# account.institution       # An Institution object

# # InvestmentAccount(Account)

# account.brokerid          # Investment broker ID
# account.statement         # An InvestmentStatement object

# # Institution

# institution = account.institution
# institution.organization
# institution.fid

# # Statement

# statement = account.statement
# statement.start_date          # The start date of the transactions
# statement.end_date            # The end date of the transactions
# statement.balance             # The money in the account as of the statement date
# # The money available from the account as of the statement date
# statement.available_balance
# statement.transactions        # A list of Transaction objects

# # InvestmentStatement

# statement = account.statement
# statement.positions           # A list of Position objects
# statement.transactions        # A list of InvestmentTransaction objects

# # Transaction

# for transaction in statement.transactions:
#     transaction.payee
#     transaction.type
#     transaction.date
#     transaction.amount
#     transaction.id
#     transaction.memo
#     transaction.sic
#     transaction.mcc
#     transaction.checknum

# # InvestmentTransaction

# for transaction in statement.transactions:
#     transaction.type
#     transaction.tradeDate
#     transaction.settleDate
#     transaction.memo
#     transaction.security      # A Security object
#     transaction.income_type
#     transaction.units
#     transaction.unit_price
#     transaction.comission
#     transaction.fees
#     transaction.total
#     transaction.tferaction

# # Positions

# for position in statement.positions:
#     position.security       # A Security object
#     position.units
#     position.unit_price
#     position.market_value

# # Security

# security = transaction.security
# # or
# security = position.security
# security.uniqueid
# security.name
# security.ticker
# security.memo
