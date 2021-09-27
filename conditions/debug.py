



from common.load_file import LoadFile

path = "/Users/gz05024ml/Documents/bybit_test/conditions/data/public_topic.yml"
a = LoadFile(path).load_yaml()
print(a)
print(a['USDT_Petperual']['topic'][0])
print(a['USDT_Petperual']['testnet'])

