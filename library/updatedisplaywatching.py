import datetime
import requests


# this class 
class UpdateDisplayWatching:
	def __init__(self, dataWatch):
		self.data = dataWatch


	# api call date format: DATE datatype, not string.
	# def API_call(self, key, startDate):

	def API_call(self, key, date):

		api_key   = 'P2PAOODDY7FT4ATXTIRALITGBL5AMHKZ'
		pre_base  = r'https://api.tdameritrade.com/v1/marketdata/'
		post_base = r'/pricehistory'

		year, month, day = date.year, date.month, date.day
		epoch = int(datetime.datetime(year, month, day, 0, 0).timestamp() * 1000)

		url = pre_base + key + post_base
		payload = {
			'apikey': api_key,
			'periodType': 'month',
			'frequencyType':'daily',
			'startDate': epoch,
			'endDate': epoch
		}

		count = 1
		while count < 7:
			req = requests.get(url=url, params=payload)
			if req.status_code == 200:
				res = req.json()
				return res
			
			date = date - datetime.timedelta(days=count)
			y, m, d = date.year, date.month, date.day
			epoch = int(datetime.datetime(y, m, d, 0, 0).timestamp() * 1000)
			payload['startDate'] = epoch
			payload['endDate'] = epoch
			count += 1

		return {'empty': True}


	def get_six_month_date(self):
		today = datetime.datetime.today()
		year  = today.year
		month = today.month - 6
		day  = today.day
		if month == 0:
			year  = year-1
			month = 12
		elif month < 0:
			year = year-1
			month = month+12

		str_date = str(year) + '-' + str(month) + '-' + str(day)
		ret = datetime.datetime.strptime(str_date, '%Y-%m-%d')
		return ret


	def update_watching(self):
		data  = self.data
		today = datetime.datetime.today()

		# convert 12/31 last year to datetime.datetime.Date datatype.
		year = str(today.year-1)
		last_day_str = year + '-12-31'
		last_day_dat = datetime.datetime.strptime(last_day_str, '%Y-%m-%d')

		date_six_mon = self.get_six_month_date()

		for key, val in data.items():

			# make the start date and ending date same for latest price
			result = self.API_call(key, today)

			# "FNILX" usually late for price update, then just skip
			if result['empty'] == False:
				val['most_curr_pric']  = result['candles'][0]['close']

			if val['most_curr_pric'] > val['life_high_valu']:
				val['life_high_valu'] = val['most_curr_pric']

			# get the price for last day of last year for Y-T-D ratio
			last_day_obj = self.API_call(key, last_day_dat)
			if last_day_obj['empty'] == False:
				last_day_price = last_day_obj['candles'][0]['close']
			else:
				last_day_price = val['most_curr_pric']

			# get the price for six month ago for six_month_performance
			six_month_obj = self.API_call(key, date_six_mon)
			if six_month_obj['empty'] == False:
				six_month_price = six_month_obj['candles'][0]['close']
			else:
				six_month_price = val['most_curr_pric']

			val['life_6mon_pric'] = six_month_price
			val['year_begi_pric'] = last_day_price
			
		return data

	def display_watching(self):
		data = self.data

		table = []
		for key, val in data.items():
			rows = []
			rows.append(key)

			gain_from_2011 = (val['most_curr_pric'] - val['year_begi_2011']) / val['year_begi_2011']
			gain_from_2016 = (val['most_curr_pric'] - val['year_begi_2016']) / val['year_begi_2016']
			gain_from_2020 = (val['most_curr_pric'] - val['year_begi_2020']) / val['year_begi_2020']
			gain_from_curr = (val['most_curr_pric'] - val['year_begi_pric']) / val['year_begi_pric']
			gain_from_6mon = (val['most_curr_pric'] - val['life_6mon_pric']) / val['life_6mon_pric']

			off_to_high = abs(val['most_curr_pric'] - val['life_high_valu']) / val['life_high_valu']

			rows.append(round(val['life_divd_curr'], 4))
			rows.append(round(val['life_expe_rati'], 4))
			rows.append(round(val['life_mgmt_rati'], 4))
			rows.append(round(val['life_high_valu'], 4))
			rows.append(val['high_valu_date'])
			rows.append(round(val['most_curr_pric'], 2))
			rows.append(round(off_to_high, 4))

			rows.append(round(gain_from_2011, 4))
			rows.append(round(gain_from_2016, 4))
			rows.append(round(gain_from_2020, 4))
			rows.append(round(gain_from_6mon, 4))
			rows.append(round(gain_from_curr, 4))

			table.append(rows)

		return table

