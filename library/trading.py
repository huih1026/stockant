''' BUY:
	1. init a new positon
		- Add a new block

	2. add more for a new position


	SELL:
	1. close-out a position
		- change the status

	2. subtract for a position
'''

import datetime
import requests

class Trading:
	def __init__(self, invest):
		self.invest = invest


	def API_call(self, key, startDate, endDate):

		api_key   = 'P2PAOODDY7FT4ATXTIRALITGBL5AMHKZ'
		pre_base  = r'https://api.tdameritrade.com/v1/marketdata/'
		post_base = r'/pricehistory'

		year_e, month_e, day_e = endDate.year, endDate.month, endDate.day
		year_s, month_s, day_s = startDate.year, startDate.month, startDate.day

		epoch_beg = int(datetime.datetime(year_s, month_s, day_s, 0, 0).timestamp() * 1000)
		epoch_end = int(datetime.datetime(year_e, month_e, day_e, 0, 0).timestamp() * 1000)

		url = url = pre_base + key + post_base
		payload = {
			'apikey': api_key,
			'periodType': 'month',
			'frequencyType':'daily',
			'startDate': epoch_beg,
			'endDate': epoch_end
		}

		'''if today is sitting in the weekend or holliday, will make start date one more
		   day before the current one.
		   make loop max 7 days, just to avoid infinite case if meet exceptions
		'''
		count = 1
		while count < 7:
			req = requests.get(url=url, params=payload)
			if req.status_code == 200:
				res = req.json()
				return res
			
			startDate = startDate - datetime.timedelta(days=count)
			y, m, d = startDate.year, startDate.month, startDate.day
			epoch_beg = int(datetime.datetime(y, m, d, 0, 0).timestamp() * 1000)
			payload['startDate'] = epoch_beg
			count += 1

		return {'empty': True}



	def buy_and_update(self, args):

		invest = self.invest

		# if symb is existing in the Market, return last-trading price to compute end_valu
		# if symb is not existing , the status code still 200, but {'empty': True}
		today  = datetime.datetime.today()
		date   = today.date()
		result = self.API_call(args['symb'], today, today)

		if args['date'] > date:
			return invest, ''

		if result['empty'] == True:
			return invest, ""

		price = result['candles'][0]['close']

		# check if this symb in the existing dictionary
		if args['symb'] not in invest:
			template = {
				"life_liv_stat": True,
				"life_avg_cost": 0.00,
	            "life_tot_cost": 0.00,
	            "life_tot_divd": 0.00,
	            "life_tot_prof": 0.0,
	            "year_beg_amnt": 0,
	            "year_add_amnt": 0,
	            "year_tot_amnt": 0,
	            "year_beg_cost": 00.00,
	            "year_add_cost": 0.00,
	            "year_tot_cost": 0.00,
	            "year_avg_cost": 0.00,
	            "year_tot_divd": 0.00,
	            "year_tot_prof": 0.00,
	            "year_end_valu": 0.00
			}
			invest[args['symb']] = template

		invest[args['symb']]['year_add_amnt'] = invest[args['symb']]['year_add_amnt'] + args['quan']
		invest[args['symb']]['year_add_cost'] = invest[args['symb']]['year_add_cost'] + args['amnt']

		invest[args['symb']]['year_tot_amnt'] = invest[args['symb']]['year_add_amnt'] + invest[args['symb']]['year_beg_amnt']
		invest[args['symb']]['year_tot_cost'] = invest[args['symb']]['year_add_cost'] + invest[args['symb']]['year_beg_cost']

		invest[args['symb']]['life_tot_cost'] = invest[args['symb']]['life_tot_cost'] + args['amnt']

		if invest[args['symb']]['year_tot_amnt'] != 0:
			invest[args['symb']]['life_avg_cost'] = invest[args['symb']]['life_tot_cost'] / invest[args['symb']]['year_tot_amnt']

		if invest[args['symb']]['year_tot_amnt'] != 0:
			invest[args['symb']]['year_avg_cost'] = invest[args['symb']]['year_tot_cost'] / invest[args['symb']]['year_tot_amnt']

		invest[args['symb']]['year_end_valu'] = price * invest[args['symb']]['year_tot_amnt']

		log = str(args['date']) +  ', BUY  ***' + args['symb'] + '*** ' + str(args['quan']) + ' @ total amount: ' + str(args['amnt']) + '.\n'

		return invest, log

			
	def sell_and_update(self, args):
		'''	1. When sell a symb, avg cost wont be changed.
			2. If close-out this symb, live_stat will be changed to false, not alive.
			3. Next year, not alive should also be tranferred into new year, because life_divd and prof will be counted 
			   towards to the total profit and divd.
			4. If a symb enters into invest file, it will stay for ever.
			5. Inactive symbs will not be showing on the postion screen, but their prof and divd will be counted.=
		'''

		invest = self.invest

		# type wrong symb on the website
		if args['symb'] not in invest:
			return invest, ""

		# you sell more than you currently have
		if invest[args['symb']]['year_tot_amnt'] < args['quan']:
			return invest, ""

		today  = datetime.datetime.today()
		date   = today.date()
		result = self.API_call(args['symb'], today, today)

		if args['date'] > date:
			return invest, ''

		if result['empty'] == True:
			return invest, ""

		price = result['candles'][0]['close']

		invest[args['symb']]['year_add_amnt'] -= args['quan']
		invest[args['symb']]['year_tot_amnt'] = invest[args['symb']]['year_add_amnt'] + invest[args['symb']]['year_beg_amnt']

		invest[args['symb']]['year_add_cost'] -= invest[args['symb']]['year_avg_cost'] * args['quan']

		invest[args['symb']]['life_tot_cost'] -= invest[args['symb']]['life_avg_cost'] * args['quan']
		invest[args['symb']]['year_tot_cost'] -= invest[args['symb']]['year_avg_cost'] * args['quan']

		invest[args['symb']]['life_tot_prof'] = (args['amnt'] / args['quan'] - invest[args['symb']]['life_avg_cost']) * args['quan']
		invest[args['symb']]['year_tot_prof'] = (args['amnt'] / args['quan'] - invest[args['symb']]['year_avg_cost']) * args['quan']

		invest[args['symb']]['year_end_valu'] = price * invest[args['symb']]['year_tot_amnt']

		log = str(args['date']) +  ', SELL ***' + args['symb'] + '*** ' + str(args['quan']) + ' @ total amount: ' + str(args['amnt']) + '.\n'

		if invest[args['symb']]['year_tot_amnt'] == 0:
			invest[args['symb']]['life_liv_stat'] = False

			# just in case it is not exactly 0 value, zero the proper values
			invest[args['symb']]['life_tot_cost'] = 0.00
			invest[args['symb']]['life_avg_cost'] = 0.00

			invest[args['symb']]['year_beg_amnt'] = 0.00
			invest[args['symb']]['year_add_amnt'] = 0.00
			invest[args['symb']]['year_tot_amnt'] = 0.00

			invest[args['symb']]['year_beg_cost'] = 0.00
			invest[args['symb']]['year_add_cost'] = 0.00
			invest[args['symb']]['year_tot_cost'] = 0.00
			
			invest[args['symb']]['year_avg_cost'] = 0.00
			invest[args['symb']]['year_end_valu'] = 0.00

		return invest, log
