import sys
import json
import requests
import datetime
from library.displayyear  import DisplayYear
from library.displaylife  import DisplayLife
from library.displaybench import DisplayBench
from library.displayposi  import DisplayPositions
from library.trading      import Trading
from library.dividend     import Dividend
from library.updateinvest import UpdateInvest
from library.updateyearfrominvest import UpdateYearFromInvest
from library.updatelifefrominvest import UpdateLifeFromInvest
from flask 				 import Flask, render_template, request, flash, redirect, session, logging, url_for
from flask_wtf 			 import FlaskForm
from wtforms 			 import Form, validators, FloatField, SubmitField, DateField, RadioField, StringField, SelectField
from wtforms.validators  import DataRequired


app = Flask(__name__)


@app.route('/')
def index():

	curr_year = str(datetime.datetime.now().year)

	'''
	TO DO:
		this block check if current year not exist in file
		then need to add a new year block.
	'''

	# Get the data from benchmark
	with open('./data/benchmark.json') as rfile:
		bench_data = json.load(rfile)

	# Get the data from the year and life file to render the table
	with open('./data/datayear.json') as rfile:
		year_data = json.load(rfile)
	with open('./data/datalife.json') as rfile:
		life_data = json.load(rfile)

	# create Display object to extract infor
	# tot_year: [ [stocks], [etfs] ], tot_life same format
	inv_year = DisplayYear(year_data[curr_year])
	inv_life = DisplayLife(life_data[curr_year])
	ben_mark = DisplayBench(bench_data[curr_year])

	tot_year = inv_year.get_curr_year_inv()
	tot_life = inv_life.get_life_time_inv()
	tot_mark = ben_mark.get_bench_mark()
	
	return render_template('index.html', totyear=tot_year, totlife=tot_life, totMark=tot_mark)


@app.route('/position')
def position():

	with open('./data/investstock.json') as rfile:
		allstock = json.load(rfile)
	with open('./data/investetf.json') as rfile:
		alletf = json.load(rfile)

	curr_year = str(datetime.datetime.now().year)

	inv_sto = DisplayPositions(allstock[curr_year])
	inv_etf = DisplayPositions(alletf[curr_year])

	pos_sto = inv_sto.get_positions_inv()
	pos_etf = inv_etf.get_positions_inv()

	return render_template('position.html', ps=pos_sto, pe=pos_etf)


@app.route('/apiupdate')
def apiupdate():

	curr_year  = str(datetime.datetime.now().year)

	'''This block to call go to call API to get latest price, 
		then update the each symbol year_end_valu, to update
		corresponding values in file
	'''
	with open('./data/investstock.json') as rfile:
		inv_sto = json.load(rfile)
	with open('./data/investetf.json') as rfile:
		inv_etf = json.load(rfile)

	updateSto  = UpdateInvest(inv_sto[curr_year])
	updateEtf  = UpdateInvest(inv_etf[curr_year])
	update_sto = updateSto.get_invest_ending_updated()
	update_etf = updateEtf.get_invest_ending_updated()

	inv_sto[curr_year] = update_sto
	inv_etf[curr_year] = update_etf

	with open('./data/investstock.json', 'w') as wfile:
		json.dump(inv_sto, wfile, indent=4)
	with open('./data/investetf.json', 'w') as wfile:
		json.dump(inv_etf, wfile, indent=4)


	''' This block to update summary dateyear and datalife file 
		after invest got updated. then writes to file
	'''
	with open('./data/datayear.json') as rfile:
		data_year = json.load(rfile)
	with open('./data/datalife.json') as rfile:
		data_life = json.load(rfile)

	updateYear  = UpdateYearFromInvest(data_year[curr_year])
	updateLife  = UpdateLifeFromInvest(data_life[curr_year])
	update_year = updateYear.get_year_data_updated(update_sto, update_etf)
	update_life = updateLife.get_life_data_updated(update_sto, update_etf)

	data_year[curr_year] = update_year
	data_life[curr_year] = update_life

	with open('./data/datayear.json', 'w') as wfile:
		json.dump(data_year, wfile, indent=4)
	with open('./data/datalife.json', 'w') as wfile:
		json.dump(data_life, wfile, indent=4)

	msg = 'You have successfully api updated postions.'
	return render_template('message.html', msg=msg)


class InputForm(Form):
	# 'A' is the value, 'Buy' is the content to display on the web
	radio_tr = RadioField(choices=[('A','Buy'),('B', 'Sell')])
	radio_se = RadioField(choices=[('A', 'Stock'), ('B', 'ETF')]) 
	symbol   = StringField('Symbol', [DataRequired(message='Symbol is required!'), validators.Length(min=1, max=5)])
	quantity = FloatField('Quantity', [DataRequired()])
	amount   = FloatField('Amount', [DataRequired()])
	date     = DateField('Transaction Date')

@app.route('/trading', methods=['GET', 'POST'])
def trading():
	''' - collect the user trading buy-or-sell infor
	    - update the invest file, also api call to verify symbol and calculate last price
	    - update the year and life file as well
	    - update the log file
	    - 
	'''
	web_msg   = ''
	curr_year = datetime.datetime.today().year
	today     = datetime.datetime.today().date()

	form = InputForm(request.form)
	if request.method == 'POST' and form.validate():
		buy_or_sell = form.radio_tr.data
		sto_or_etfs = form.radio_se.data

		form_args = {}
		form_args['symb'] = form.symbol.data.upper()
		form_args['quan'] = form.quantity.data
		form_args['amnt'] = form.amount.data
		form_args['date'] = form.date.data

		with open('./data/datayear.json') as rfile:
			data_year = json.load(rfile)
		with open('./data/datalife.json') as rfile:
			data_life = json.load(rfile)

		# following is to update datayear & dataetf file
		updateYear = UpdateYearFromInvest(data_year[str(curr_year)])
		updateLife = UpdateLifeFromInvest(data_life[str(curr_year)])

		# pass investstock.json if radio choosen as stock
		if sto_or_etfs == 'A':
			with open('./data/investstock.json') as rfile:
				inv_stock = json.load(rfile)

			updateStock = Trading(inv_stock[str(curr_year)])
			if buy_or_sell == 'A':
				updated_sto, log_msg = updateStock.buy_and_update(form_args)
			else:
				updated_sto, log_msg = updateStock.sell_and_update(form_args)

			if log_msg != '':
				inv_stock[str(curr_year)] = updated_sto
				with open('./data/investstock.json', 'w') as wfile:
					json.dump(inv_stock, wfile, indent=4)

				updated_year = updateYear.get_year_data_updated_stock(updated_sto)
				updated_life = updateLife.get_life_data_updated_stock(updated_sto)

		else:
			with open('./data/investetf.json') as rfile:
				inv_etf = json.load(rfile)

			updateEtf= Trading(inv_etf[str(curr_year)])
			if buy_or_sell == 'A':
				updated_etf, log_msg = updateEtf.buy_and_update(form_args)
			else:
				updated_etf, log_msg = updateEtf.sell_and_update(form_args)

			# writes back to invest
			if log_msg != '':
				inv_etf[str(curr_year)] = updated_etf
				with open('./data/investetf.json', 'w') as wfile:
					json.dump(inv_etf, wfile, indent=4)

				# following is to update datayear & dataetf file
				updated_year = updateYear.get_year_data_updated_etf(updated_etf)
				updated_life = updateLife.get_life_data_updated_etf(updated_etf)


		# writes into the history log file
		web_msg = '| Warning: nothing has done, something goes wrong!'
		if log_msg != '':
			with open('./data/log', 'a') as logfile:
				logfile.write(log_msg)

			data_year[str(curr_year)] = updated_year
			data_life[str(curr_year)] = updated_life

			with open('./data/datayear.json', 'w') as wfile:
				json.dump(data_year, wfile, indent=4)
			with open('./data/datalife.json', 'w') as wfile:
				json.dump(data_life, wfile, indent=4)

			web_msg = '| Congrats: Update Finished!'

	return render_template('trading.html', form=form, msg=web_msg)


class DividendForm(Form):
	symb = StringField('Symbol', [DataRequired(message='Symbol is required!'), validators.Length(min=1, max=5)])
	amnt = FloatField('Amount', [DataRequired()])
	date = DateField('Received Date')

@app.route('/dividend', methods=['GET', 'POST'])
def dividend():
	curr_year = datetime.datetime.today().year

	form = DividendForm(request.form)

	web_msg = ''
	if request.method == 'POST' and form.validate():
		
		form_args = {}
		form_args['symb'] = form.symb.data.upper()
		form_args['amnt'] = form.amnt.data
		form_args['date'] = form.date.data

		with open('./data/investstock.json') as rfile:
			inv_stock = json.load(rfile)
		with open('./data/investetf.json') as rfile:
			inv_etf = json.load(rfile)

		with open('./data/datayear.json') as rfile:
			data_year = json.load(rfile)
		with open('./data/datalife.json') as rfile:
			data_life = json.load(rfile)

		# following is to update datayear & dataetf file
		updateYear = UpdateYearFromInvest(data_year[str(curr_year)])
		updateLife = UpdateLifeFromInvest(data_life[str(curr_year)])


		# if the user-given symb in invest_stock file
		if form_args['symb'] in inv_stock[str(curr_year)]:
			update_sto = Dividend(inv_stock[str(curr_year)])
			updated_sto, log_msg = update_sto.receive_divd_update(form_args)

			if log_msg != '':
				inv_stock[str(curr_year)] = updated_sto
				with open('./data/investstock.json', 'w') as wfile:
					json.dump(inv_stock, wfile, indent=4)

				updated_year = updateYear.get_year_data_updated_stock(updated_sto)
				updated_life = updateLife.get_life_data_updated_stock(updated_sto)

		elif form_args['symb'] in inv_etf[str(curr_year)]:
			update_etf = Dividend(inv_etf[str(curr_year)])
			updated_etf, log_msg = update_etf.receive_divd_update(form_args)

			if log_msg != '':
				inv_etf[str(curr_year)] = updated_etf
				with open('./data/investetf.json', 'w') as wfile:
					json.dump(inv_etf, wfile, indent=4)

				updated_year = updateYear.get_year_data_updated_etf(updated_etf)
				updated_life = updateLife.get_life_data_updated_etf(updated_etf)

		else:
			log_msg = ''

		# if msg is not empty, then writes to file, and update year and life file
		web_msg = '| Warning: dividend adding goes Wrong!'
		if log_msg != '':
			with open('./data/log', 'a') as logfile:
				logfile.write(log_msg)

			data_year[str(curr_year)] = updated_year
			data_life[str(curr_year)] = updated_life

			with open('./data/datayear.json', 'w') as wfile:
				json.dump(data_year, wfile, indent=4)
			with open('./data/datalife.json', 'w') as wfile:
				json.dump(data_life, wfile, indent=4)

			web_msg = '| Congrats: update Finished!'

	return render_template('dividend.html', form=form, msg=web_msg)




if __name__ == '__main__':
	app.secret_key='stockant123'
	app.run(debug=True)
