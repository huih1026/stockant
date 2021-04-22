''' This class get latest price for each stock,
	then update the 'year_end_valu' and gain.
'''

import datetime
import requests

class UpdateInvest:
	def __init__(self, positions):
		self.posi = positions


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


	def get_invest_ending_updated(self):

		today = datetime.datetime.today()
		positions = self.posi

		for key, val in positions.items():

			# make the start date and ending date same for latest price
			result = self.API_call(key, today, today)

			# "FNILX" usually late for price update, then just skip
			if result['empty'] == True:
				continue

			price  = result['candles'][0]['close']
			val['year_end_valu'] = val['year_tot_amnt'] * price

		return positions
