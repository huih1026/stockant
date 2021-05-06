import datetime
import requests

class UpdateBench:
	def __init__(self, data):
		self.bench = data


	def get_benchmark_updated(self):
		data = self.bench

		api_key   = 'P2PAOODDY7FT4ATXTIRALITGBL5AMHKZ'
		pre_base  = r'https://api.tdameritrade.com/v1/marketdata/'
		post_base = r'/pricehistory'

		startDate = datetime.datetime.today()
		endDate   = datetime.datetime.today()

		year_e, month_e, day_e = endDate.year, endDate.month, endDate.day
		year_s, month_s, day_s = startDate.year, startDate.month, startDate.day

		epoch_beg = int(datetime.datetime(year_s, month_s, day_s, 0, 0).timestamp() * 1000)
		epoch_end = int(datetime.datetime(year_e, month_e, day_e, 0, 0).timestamp() * 1000)

		url = url = pre_base + r'$SPX.X' + post_base
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
				break
			
			startDate = startDate - datetime.timedelta(days=count)
			y, m, d = startDate.year, startDate.month, startDate.day
			epoch_beg = int(datetime.datetime(y, m, d, 0, 0).timestamp() * 1000)
			payload['startDate'] = epoch_beg
			payload['endDate'] = epoch_beg
			count += 1

		if res['empty'] == True:
			return data

		price  = res['candles'][0]['close']
		data['year_cur'] = price

		return data