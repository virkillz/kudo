from flask import Flask,jsonify, render_template,request, Response,redirect
from Savoir import Savoir
from flask_qrcode import QRcode
#from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError
import json
from functools import wraps
# from flask import request, Response
from flask_recaptcha import ReCaptcha
import requests
import sqlite3
import binascii


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
    'RECAPTCHA_ENABLED': True,
    'RECAPTCHA_SITE_KEY': "6LfntEYUAAAAAIeK8kIh8x5AjJ5NjebKM4hp17oA",
    'RECAPTCHA_SECRET_KEY': "6LfntEYUAAAAAL5GYAX1vZuagQVoxERr0oHLu-3n"
})

recaptcha = ReCaptcha()
recaptcha.init_app(app)
QRcode(app)

@app.route('/')
def starter():
	return render_template('home.html')

@app.route('/api/v1/kudosocial/getfeatured')
def getfeatured()
	return '{"result":[{"address":"1a1mP9mLQFmPc3wXwoQLLSaBEgxsbPqH56syBb","title":"Im awesome","content":"Something is wrong in our community"},{"address":"1a1mP9mLQFmPc3wXwoQLLSaBEgxsbPqH5fsyBb","title":"Im tired","content":"Something is wrong in our community"},{"address":"1a1mP9mLQFmPcewXwoQLLSaBEgxsbPqH56syBb","title":"Im tired","content":"Something is wrong in our community"},{"address":"1a1mP9mLQFmPc3wXwoQLLSaBEgxsbPqH56syBb","title":"Im tired","content":"Something is wrong in our community"}]}'

@app.route('/api/v1/kudosocial/getsocial/<count>/<start>')
def getsocial(count,start):
	api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)
	stream = api.liststreamitems('kudosocial',bool(1),int(count),int(start))
	return json.dumps(stream)

@app.route('/api/v1/kudosocial/post',methods = ['POST'])
def socialpost():
	key=request.form['key']
	value=request.form['value']
	addr=request.form['addr']
	privkey=request.form['privkey']

	#switch this in production for python3
	value=binascii.hexlify(value)
	# value=value.encode('utf-8')
	# value=value.hex()


	load = [{"for":"kudosocial","key":key,"data":str(value)}]
	# return load
	try:
		api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)
		coba=api.createrawsendfrom(addr,{},load)
		# return json.dumps(coba)
		if 'error' in coba:
			return jsonify({'result':'false','error':coba['error']['message']})	
		else:
			sign=api.signrawtransaction(coba,[],[privkey])
			if 'error' in sign:
				return jsonify({'result':'false','error':sign['error']['message']})	
			else:
				publish=api.sendrawtransaction(sign['hex'])
				return jsonify({'result':'success','trxid':publish})	
				# return jsonify({'result':'true','error':'','origin_address':addfrom,'destination_address':addto,'amount':amt,'trx_id':publish})
	except ConnectionError:
		return jsonify({'result':'false','error':'can\'t connect to node'})	



@app.route('/api/v1/getstream/<trxid>')
def getstream(trxid):
	try:
		api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)
		coba =api.getstreamitem('experimentdata',trxid)
		return json.dumps(coba)
	except ConnectionError:
		return jsonify({'result':'false','error':'can\'t connect to node'})		

@app.route('/api/v1/storestream',methods = ['POST'])
def storestream():
	key=request.form['key']
	value=request.form['value']
	addr=request.form['addr']
	privkey=request.form['privkey']

	#switch this in production for python3
	value=binascii.hexlify(value)
	# value=value.encode('utf-8')
	# value=value.hex()


	load = [{"for":"experimentdata","key":key,"data":str(value)}]
	# return load
	try:
		api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)
		coba=api.createrawsendfrom(addr,{},load)
		# return json.dumps(coba)
		if 'error' in coba:
			return jsonify({'result':'false','error':coba['error']['message']})	
		else:
			sign=api.signrawtransaction(coba,[],[privkey])
			if 'error' in sign:
				return jsonify({'result':'false','error':sign['error']['message']})	
			else:
				publish=api.sendrawtransaction(sign['hex'])
				return jsonify({'result':'success','trxid':publish})	
				# return jsonify({'result':'true','error':'','origin_address':addfrom,'destination_address':addto,'amount':amt,'trx_id':publish})
	except ConnectionError:
		return jsonify({'result':'false','error':'can\'t connect to node'})	


@app.route('/register/hackathon',methods = ['POST', 'GET'])
def registerhack():
	if request.method == 'GET':
		return render_template('registerhack.html')
	else:
		try:
			regid=request.form['regid']
			name=request.form['name']
			email=request.form['email']
			phone=request.form['phone']
			univ=request.form['university']
			interest=request.form['interest']
			kudoaddress=request.form['address']
			skill=request.form['skill']
			con = sqlite3.connect("database.db")
			cur = con.cursor()
			cur.execute("INSERT INTO hackathon (regid,name,kudoaddress,phone,email,programming_skill,university,blockchain_interest) VALUES (?,?,?,?,?,?,?,?)",(regid,name,kudoaddress,phone,email,skill,univ,interest) )
			con.commit()
			msg = "Record successfully added"
		except:
			con.rollback()
			msg = "error in insert operation"
		finally:
			return render_template('registerhack.html',errormsg=msg)
			con.close()

@app.route('/comingsoon')
def comingsoon():
	return render_template('comingsoon.html')

@app.route('/checkout/<token>')
def checkout(token):
	return render_template('qrtopay.html')

@app.route('/whitepaper')
def whitepaper():
	return render_template('whitepaper.html')

@app.route('/wallet/newaddress')
def newaddressqr():	
	return render_template('newaddress.html')

@app.route('/wallet/history',methods = ['POST', 'GET'])
def gethistory():	
	if request.method == 'GET':
		return render_template('history.html')
	else:
		return redirect("http://159.65.1.34/Ideachain/assetaddress/"+request.form['address']+"/60-265-65453")

@app.route('/wallet/showqr')
def showqr():
	try:
		api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)
		newaddress=api.createkeypairs()
		tryimport=api.importaddress(newaddress[0]['address'],'',bool(''))
		api.grant(newaddress[0]['address'],'send')
		api.grant(newaddress[0]['address'],'receive')
		# return jsonify({'result':'true','address':newaddress[0]['address'],'public_key':newaddress[0]['pubkey'],'private_key':newaddress[0]['privkey'],'error':''})
		keys={'addr':newaddress[0]['address'],'pubkey':newaddress[0]['pubkey'],'privkey':newaddress[0]['privkey']}
		return render_template('addressqr.html',keys=keys)
	except ConnectionError:
		return jsonify({'result':'false','error':'can\'t connect to node'})		

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

@app.route('/wallet/sendkudo',methods = ['POST', 'GET'])
def walletsendkudo():
	if request.method == 'GET':	
		return render_template('sendkudo.html')
	else:
		addfrom = request.form['origin']
		addto = request.form['destination']
		amt=request.form['amount']
		privkey=request.form['privkey']
	if is_int(amt)==False:
		return render_template('sendkudo.html',errormsg="Check your amount. It must be rounded number")
	try:
		api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)
		coba=api.createrawsendfrom(addfrom,json.loads('{"'+addto+'":{"KUDO":'+amt+'}}'))
		if 'error' in coba:
			return render_template('sendkudo.html',errormsg=coba['error']['message'])
		else:
			sign=api.signrawtransaction(coba,[],[privkey])
			if 'error' in sign:
				return render_template('sendkudo.html',errormsg=sign['error']['message'])
			else:
				publish=api.sendrawtransaction(sign['hex'])
				detail={"id":publish,"origin":addfrom,"destination":addto,"amount":amt}
				return render_template('transfersuccess.html',trx=detail)
				# return jsonify({'result':'true','error':'','origin_address':addfrom,'destination_address':addto,'amount':amt,'trx_id':publish})
	except ConnectionError:
		return render_template('sendkudo.html',errormsg="Cannot connect to the node")


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
					# return jsonify({'result':'false','error':'address can\'t be founded.'})
					return render_template('balanceresult.html',msg="Address cannot be founded.")
			return render_template('balanceresult.html',msg="Balance of "+address+" is "+str(balance)+ " Kudo")
			# return jsonify({'result':'true','address':address,'coin':'KUDO','balance':balance,'error':''})
		except ConnectionError:
			return render_template('balanceresult.html',msg="Can't connect to the node.")
			# return jsonify({'result':'false','error':'can\'t connect to node'})	
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


# BOHONGAN
@app.route('/payments/<anything>')
def payment(anything):
	return '{\
	"xchg_rate": null,\
    "tx_fee": null,\
    "token": "b846924b-def3-4ae6-8792-4742f7cde5c7",\
    "timeout": 600,\
    "tag": null,\
    "status": "pending",\
    "redirect_url": null,\
    "paid_at": null,\
    "orig_amount": null,\
    "currency": "xrb",\
    "created_at": "2018-02-20T09:46:17.512066Z",\
    "amount": "1",\
    "account": "xrb_34z3bezxdgmadkba85dt5eybb1n8bobuo1gxcm6a4admbk8frr5h66xcbtxp"\
}'


@app.route('/kudosocial/getfeatured')
def getfeatured():
	return '{"result":[{"address":"1a1vDdo2skGtYJr2M7TEFGMaUzPeXuMbkUnBTW","title":"Gregory","content":"Blockchain Atache"},{"address":"1a1mP9mLQFmPc3wXwoQLLSaBEgxsbPqH56syBb","title":"VirKill","content":"Blockchain coder"},{"address":"1RwwZka6bvzMqUzx1GGjP6af86KG6QH769BPY3","title":"Aung Ye Lin","content":"Kudo Pimp"}]}'

@app.route('/kudosocial/getlatesttalk')
def getlatesttalk():
	return '{"result":[{"address":"1a1vDdo2skGtYJr2M7TEFGMaUzPeXuMbkUnBTW","title":"Blockchain for Education","content":"So I got an Idea..."},{"address":"1a1mP9mLQFmPc3wXwoQLLSaBEgxsbPqH56syBb","title":"Kudo need to be available on exchange","content":"So I can buy..."},{"address":"1RwwZka6bvzMqUzx1GGjP6af86KG6QH769BPY3","title":"Can we allow advertising?","content":"So I can advertise"}]}'


# bohongan


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
