from bitshares.account import Account
from bitshares import BitShares

account = Account("ricky-shi")
print(account.balances)


def init_wallet():
    # from bitshares import BitShares
    bitshares = BitShares()
    bitshares.wallet.create("123456")

    # cybex-kyp-validator
    bitshares.wallet.addPrivateKey("")


def do_transfer():
    bitshares = BitShares()
    bitshares.wallet.unlock("123456")
    bitshares.transfer("ricky-shi", 0.01, "CYB", "", account="cybex-kyp-validator")


def check_if_user_send_binding_request(cybex_validator_account, cybex_user_account):
    # check if cybex_user_account send tx to cybex_validator_account
    # with memo == cybex ID address

    user_account = Account(cybex_user_account)
    validator_account = Account(cybex_validator_account)

    user_id = user_account["id"]
    validator_id = validator_account["id"]

    for h in validator_account.history():
        op_code = h["op"][0]

        if op_code == 0:
            op_details = h["op"][1]
            if 'memo' in op_details.keys():
                from_account_id = h["op"][1]['from']
                to_account_id = h["op"][1]['to']

                # memo should be decrypted to get canon ID
                # and we
                memo = h["op"][1]['memo']

                print('from: ' + from_account_id + ", to: " + to_account_id)
                if user_id == from_account_id and validator_id == to_account_id:
                    return True

    return False



# init_wallet()
# do_transfer()

result = check_if_user_send_binding_request("cybex-kyp-validator", "hello-world11")
print(result)

#
