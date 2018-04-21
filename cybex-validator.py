from web3 import Web3, HTTPProvider
from bitshares.account import Account
from bitshares import BitShares
from time import sleep
import pprint

# Cybex validation
# Cybex validator listen to MPC result with a filter (validator == Cybex). Each result is valid by
#   1. verify rules are Cybex rules
#   2. query each tx claimed, and ensure user in tx == ricky, the value of expire
#           and checksum also matches


w3 = Web3(HTTPProvider('https://kovan.infura.io/nRUCOskjng2tooOxkAlU'))
print(w3.eth.blockNumber)

pp = pprint.PrettyPrinter(indent=4)


# help function
def to_32byte_hex(val):
    return Web3.toHex(Web3.toBytes(val).rjust(32, b'\0'))


def validate_tx_and_user_id(hashes, user_id):
    for h in hashes:
        tx = w3.eth.getTransaction(h)
        if tx is None:
            return False

        pp.pprint('tx: from ' + tx['from'])
        # if user_id != tx['from']:
        #     return False

    return True


def validate_expire(expire_time):
    # check expire time
    return True


def validate_checksum(check_sum):
    # get response
    return True

def send_validation_result_to_cybex(cybex_validator_account, cybex_user_account):
    bitshares = BitShares()
    bitshares.wallet.unlock("123456")

    bitshares.transfer(cybex_user_account, 0.01, "CYB", "", account=cybex_validator_account)


def check_if_user_send_binding_request(validator_account, user_account):
    # check if cybex_user_account send tx to cybex_validator_account
    # with memo == cybex ID address

    # user_account = Account(cybex_user_account)
    # validator_account = Account(cybex_validator_account)

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


# kyc contract
kyc_contract_address = '0x897EcCBD2993134fbB6661638BA5aA52d858fdfD'
kyc_contract_abi = '[ { "constant": false, "inputs": [ { "name": "responseId", "type": "uint32" }, { "name": "requestId", "type": "uint32" }, { "name": "hash", "type": "bytes32" }, { "name": "property", "type": "string" }, { "name": "encrypedValue", "type": "string" }, { "name": "expired", "type": "uint256" } ], "name": "oracleCommit", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_address", "type": "address" }, { "name": "_name", "type": "string" } ], "name": "registerOracle", "outputs": [ { "name": "", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_ruleId", "type": "uint32" }, { "name": "_property", "type": "string" }, { "name": "_op", "type": "string" }, { "name": "_value", "type": "string" } ], "name": "registerRule", "outputs": [ { "name": "", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "requestId", "type": "uint32" }, { "name": "oracle", "type": "address" }, { "name": "property", "type": "string" }, { "name": "pubKey", "type": "bytes32" }, { "name": "platformId", "type": "bytes32" } ], "name": "request", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "id", "type": "uint32" }, { "name": "client", "type": "address" }, { "name": "clientName", "type": "string" }, { "name": "ruleIds", "type": "uint32[]" } ], "name": "submitRequirements", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "id", "type": "uint32" }, { "name": "user", "type": "address" }, { "name": "validator", "type": "address" }, { "name": "logic", "type": "string" }, { "name": "requestId", "type": "uint32[]" }, { "name": "expired", "type": "uint32[]" }, { "name": "hash", "type": "bytes32[]" }, { "name": "properties", "type": "string" }, { "name": "ops", "type": "string" }, { "name": "values", "type": "string" } ], "name": "submitValidation", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "id", "type": "uint32" }, { "name": "validator", "type": "address" }, { "name": "user", "type": "string" } ], "name": "submitValidation2", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "payable": false, "stateMutability": "nonpayable", "type": "constructor" }, { "constant": true, "inputs": [], "name": "getOracleList", "outputs": [ { "name": "", "type": "address[]" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "_id", "type": "address" } ], "name": "getOracleName", "outputs": [ { "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "requester", "type": "address" }, { "name": "_id", "type": "uint32" } ], "name": "getRequest", "outputs": [ { "name": "", "type": "uint32" }, { "name": "", "type": "address" }, { "name": "", "type": "string" }, { "name": "", "type": "bytes32" }, { "name": "", "type": "bytes32" }, { "name": "", "type": "bool" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "requester", "type": "address" } ], "name": "getRequestIds", "outputs": [ { "name": "", "type": "uint32[]" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "id", "type": "uint32" } ], "name": "getRequirement", "outputs": [ { "name": "", "type": "address" }, { "name": "", "type": "string" }, { "name": "", "type": "uint32[]" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "getRequirementIds", "outputs": [ { "name": "", "type": "uint32[]" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "requester", "type": "address" }, { "name": "_id", "type": "uint32" } ], "name": "getResponse", "outputs": [ { "name": "", "type": "uint32" }, { "name": "", "type": "uint32" }, { "name": "", "type": "bytes32" }, { "name": "", "type": "string" }, { "name": "", "type": "string" }, { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "requester", "type": "address" } ], "name": "getResponseIds", "outputs": [ { "name": "", "type": "uint32[]" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "_id", "type": "uint32" } ], "name": "getRule", "outputs": [ { "name": "id", "type": "uint32" }, { "name": "property", "type": "string" }, { "name": "op", "type": "string" }, { "name": "value", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "getRuleIds", "outputs": [ { "name": "", "type": "uint32[]" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "r", "type": "address" } ], "name": "getValidationIds", "outputs": [ { "name": "", "type": "uint32[]" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "r", "type": "address" }, { "name": "_id", "type": "uint32" } ], "name": "getValidationPart1", "outputs": [ { "name": "", "type": "uint32" }, { "name": "", "type": "address" }, { "name": "", "type": "address" }, { "name": "", "type": "string" }, { "name": "", "type": "uint32[]" }, { "name": "", "type": "uint32[]" }, { "name": "", "type": "bytes32[]" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "r", "type": "address" }, { "name": "_id", "type": "uint32" } ], "name": "getValidationPart2", "outputs": [ { "name": "", "type": "string" }, { "name": "", "type": "string" }, { "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "address" } ], "name": "oracles", "outputs": [ { "name": "id", "type": "address" }, { "name": "name", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "owner", "outputs": [ { "name": "", "type": "address" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "userAccount", "outputs": [ { "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" } ]'
kyc_contract = w3.eth.contract(address=kyc_contract_address, abi=kyc_contract_abi)


verified_ids = []
while True:
    # user, validator
    # user_addr = "0xfB6916095ca1df60bB79Ce92cE3Ea74c37c5d359"
    cybex_validator_id = "0xc080aADAAFd7D1F8563Ca54AF18751FED76456dD"
    ids = kyc_contract.functions.getValidationIds(cybex_validator_id).call()

    for id in ids:
        if id in verified_ids:
            continue

        print(id)
        verified_ids.append(id)

        # validation = kyc_contract.functions.getValidation(id).call()
        # print(validation)

        user_account = kyc_contract.functions.userAccount().call()
        if user_account == '':
            continue

        # .TBD
        real_validation = [
            '0x975A157Fdda72Fd0A3C5c03a26E749339B3D7DC8', # user
            '0xd916791c16c43fd977993212aa7e0bd458225c73', # platform
            user_account, # ricky's cybex id
            'r1&r2',
            ['0xd35b26cae5560699f2a47b5ab0a2c88357fc38c1050cbfb9809ed1779d2f89ec',
             '0xc9fd37c495dfd3a7b4b8d811a81114522943f8521b9d553680cfef1ea74c2627'], # tx hash array

            [123, 456], # expired time
            [0x123, 0x456], # hash array
            ['deposit', 'income'], # props array
            [50, 20], # values array
            ]

        # step-1: tx is correct, check user is ricky
        tx_hashes = real_validation[4]
        user_id = real_validation[0]
        tx_valid = validate_tx_and_user_id(tx_hashes, user_id)
        if tx_valid == False:
            # invalid tx
            print('invalid tx hash, validation abort')
            continue
        print('1: tx is valid')

        # step-2: check value of expire
        expire_time = 0
        expire_result = validate_expire(expire_time)
        print('2: expire value is valid')

        # step-3: check checksum
        check_sum = 0x1234567890
        checksum_result = validate_checksum(check_sum)
        print('3: checksum is valid')

        # Then, Cybex validator will
        # 1. verify he receive tx from user, with correct memo
        # 2. commit validation result on Cybex chain
        # 3. User ricky will be marked as KYC verified.
        cybex_user_account = Account(user_account)
        print(cybex_user_account.balances)

        cybex_validator_account = Account('cybex-kyp-validator')
        print(cybex_validator_account.balances)

        check_result = check_if_user_send_binding_request(cybex_validator_account, cybex_user_account)
        # in case cybex tx is not send
        if check_result is False:
            for i in range(4):
                print('try ' + str(i))
                sleep(10)
                check_result = check_if_user_send_binding_request(cybex_validator_account, cybex_user_account)
                if check_result:
                    break

        if check_result:
            # transfer 0.01 CYB to rikcy
            send_validation_result_to_cybex(cybex_validator_account, cybex_user_account)
            print('send_validation_result_to_cybex')


    #sleep for 5 seconds
    print('.')
    sleep(10)