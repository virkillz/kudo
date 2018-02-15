from Savoir import Savoir
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError

rpcuser = 'multichainrpc'
rpcpasswd = '8kwZ4sS9oSGxdiFLK2TwMf2zqxPwfLr9XkUdkgU9upwL'
rpchost = '139.59.105.130'
rpcport = '6264'
chainname = 'virkillchain'

api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)
# newaddress=api.createkeypairs()
# tryimport=api.importaddress(newaddress[0]['address'],'',bool(''))
# api.grant(newaddress[0]['address'],'send')
# api.grant(newaddress[0]['address'],'receive')

sendasset=api.sendasset('18MCconQFj2EgqsvUWcn1uGXVvNBPjP9yHK5pv','KUDO',1000)
try:
	if sendasset.has_key('error'):
		errormsg=sendasset['error']['message']
		print({'result':'false','error':errormsg})	
except AttributeError:
	print({'result':'true','error':''})
# print(sendasset)
# print(newaddress)
# print(tryimport)