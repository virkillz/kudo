from flask import Flask,jsonify, render_template,request, Response
from Savoir import Savoir
from flask_qrcode import QRcode
#from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError
import json
from functools import wraps
# from flask import request, Response
from flask_recaptcha import ReCaptcha
import requests


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'edwinkepo' and password == 'aiusd738qhwkasn783ekaYhasd8qhedksDbs'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

rpcuser = 'multichainrpc'
rpcpasswd = 'CLF82NnCCsuJa1FMhU6fQuueoRWBDrA6SQDwD9mjNfed'
rpchost = '159.65.1.34'
rpcport = '4774'
chainname = 'ideachain'


app=Flask(__name__,static_url_path='/static')
app.config.update({
    'RECAPTCHA_ENABLED': False,
    'RECAPTCHA_SITE_KEY': "6LfntEYUAAAAAIeK8kIh8x5AjJ5NjebKM4hp17oA",
    'RECAPTCHA_SECRET_KEY': "6LfntEYUAAAAAL5GYAX1vZuagQVoxERr0oHLu-3n"
})

recaptcha = ReCaptcha()
recaptcha.init_app(app)
QRcode(app)

@app.route('/')
def starter():
	return render_template('home.html')

@app.route('/whitepaper')
def whitepaper():
	return render_template('whitepaper.html')

@app.route('/wallet/newaddress')
def newaddressqr():
	return render_template('newaddress.html')

@app.route('/wallet/showqr')
def showqr():
	return render_template('addressqr.html')

@app.route('/faucet',methods = ['POST', 'GET'])
def showfaucet():
	if request.method == 'GET':
		return render_template('faucet.html')
	else:		
		if recaptcha.verify():
			try:
				addr=request.form['address']
				api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)	
				sendasset=api.sendasset(addr,'KUDO',25)
				if 'error' in sendasset:
					errormsg=sendasset['error']['message']
					# return jsonify({'result':'false','error':errormsg})	
					return render_template('faucet.html',errormsg="Failed. "+errormsg)
				else:
					# return 'joy'
					# return jsonify({'result':'true','error':''})
					return render_template('faucet.html',errormsg="Succeed. Add 25 to "+addr)					
			except ConnectionError:
				# return jsonify({'result':'false','error':'can\'t connect to node'})
				return render_template('faucet.html',errormsg="Failed. Can't connect to the Node")					
			pass
		else:
			return render_template('faucet.html',errormsg="Wrong Captcha")
			pass

@app.route('/wallet/sendkudo')
def walletsendkudo():
	return render_template('sendkudo.html')


@app.route('/wallet/balance',methods = ['POST', 'GET'])
def balance():
	if request.method == 'GET':
		return render_template('balance.html')
	else:
		address=request.form['address']
		try:
			api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)
			test=api.getaddressbalances(address)
			balance=0
			for x in test:
				if ('name' in x) and (x['name']=='KUDO'):
					balance=x['qty']
				else:
					return jsonify({'result':'false','error':'address can\'t be founded.'})
			return jsonify({'result':'true','address':address,'coin':'KUDO','balance':balance,'error':''})
		except ConnectionError:
			return jsonify({'result':'false','error':'can\'t connect to node'})	
		# return render_template('balance.html')	

@app.route('/api/v1/getbalance/<addr>')
def getbalance(addr):
	try:
		api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)
		test=api.getaddressbalances(addr)
		balance=0
		for x in test:
			if ('name' in x) and (x['name']=='KUDO'):
				balance=x['qty']
			else:
				return jsonify({'result':'false','error':'address can\'t be founded.'})
		return jsonify({'result':'true','address':addr,'coin':'KUDO','balance':balance,'error':''})
	except ConnectionError:
		return jsonify({'result':'false','error':'can\'t connect to node'})

@app.route('/api/v1/createrandomaddress')
def newaddress():
	try:
		api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)
		newaddress=api.createkeypairs()
		tryimport=api.importaddress(newaddress[0]['address'],'',bool(''))
		api.grant(newaddress[0]['address'],'send')
		api.grant(newaddress[0]['address'],'receive')
		return jsonify({'result':'true','address':newaddress[0]['address'],'public_key':newaddress[0]['pubkey'],'private_key':newaddress[0]['privkey'],'error':''})
	except ConnectionError:
		return jsonify({'result':'false','error':'can\'t connect to node'})	

@app.route('/api/v1/faucet/<addr>')
def faucet10(addr):
	try:
		api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)	
		sendasset=api.sendasset(addr,'KUDO',25)
		if 'error' in sendasset:
			errormsg=sendasset['error']['message']
			return jsonify({'result':'false','error':errormsg})	
		else:
			# return 'joy'
			return jsonify({'result':'true','error':''})
	except ConnectionError:
		return jsonify({'result':'false','error':'can\'t connect to node'})	


@app.route('/api/v1/sendkudo/<addfrom>/<addto>/<amt>/<privkey>')
def sendkudo(addfrom,addto,amt,privkey):
	if is_int(amt)==False:
		return jsonify({'result':'false','error':'check your amount to be sent'})	
	try:
		api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)
		coba=api.createrawsendfrom(addfrom,json.loads('{"'+addto+'":{"KUDO":'+amt+'}}'))
		if 'error' in coba:
			return jsonify({'result':'false','error':coba['error']['message']})	
		else:
			sign=api.signrawtransaction(coba,[],[privkey])
			if 'error' in sign:
				return jsonify({'result':'false','error':sign['error']['message']})	
			else:
				publish=api.sendrawtransaction(sign['hex'])
				return jsonify({'result':'true','error':'','origin_address':addfrom,'destination_address':addto,'amount':amt,'trx_id':publish})
	except ConnectionError:
		return jsonify({'result':'false','error':'can\'t connect to node'})	

def is_int(amount):
	try:
		int(amount)
		return True
	except ValueError:
		return False


if __name__ == '__main__':
    app.run()
