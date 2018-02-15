from Savoir import Savoir
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError
import json

rpcuser = 'multichainrpc'
rpcpasswd = 'CLF82NnCCsuJa1FMhU6fQuueoRWBDrA6SQDwD9mjNfed'
rpchost = '159.65.1.34'
rpcport = '4774'
chainname = 'ideachain'

api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)
# coba=api.listaddresses()
coba=api.createrawsendfrom('1a1vDdo2skGtYJr2M7TEFGMaUzPeXuMbkUnBTW',json.loads('{"1a1mP9mLQFmPc3wXwoQLLSaBEgxsbPqH56syBb":{"KUDO":20}}'))
coba=api.createrawsendfrom('1a1vDdo2skGtYJr2M7TEFGMaUzPeXuMbkUnBTW',json.loads('{"1a1mP9mLQFmPc3wXwoQLLSaBEgxsbPqH56syBb":{"KUDO":17}}'))
if 'error' in coba:
	print(coba['error']['message'])
else:
	sign=api.signrawtransaction(coba,[],["V7vTJgN4o4Ua7kiP3sPCQDBdwWXk2xH82ZYzHdteAk5npTPMT41RAFoH"])
	if 'error' in sign:
		print(sign['error']['message'])
	else:
		publish=api.sendrawtransaction(sign['hex'])
		print(publish)

# print(sign['hex'])
# publish=api.sendrawtransaction(sign['hex'])
# print(publish)

#what might go wrong 1: invalid address
#what might go wrong 2: insufficient balance
#what might go wrong 3: wrong private key
