import datetime
import requests
import json
from library.updateinvest import UpdateInvest

def API_call(key, startDate, endDate):

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

	count = 1
	while count < 7:
		req = requests.get(url=url, params=payload)
		if req.status_code == 200:
			res = req.json()['candles']
			return res
		
		startDate = startDate - datetime.timedelta(days=count)

		print('test count: ', count)
		print('startDate: ', startDate)

		y, m, d = startDate.year, startDate.month, startDate.day
		epoch_beg = int(datetime.datetime(y, m, d, 0, 0).timestamp() * 1000)
		payload['startDate'] = epoch_beg
		count += 1

	return 0.00


def updateInvestmentBegin():
	with open('./data/investetf.json') as rf:
		inv_stock = json.load(rf)

	thisYear = datetime.datetime.today().year

	stock2021 = inv_stock[str(thisYear)]

	for key, val in stock2021.items():
		price = API_call(key)

		val['year_beg_cost'] = price * val['year_beg_amnt']
		val['year_tot_cost'] = val['year_beg_cost'] + val['year_add_cost']

		val['life_tot_cost'] = val['year_tot_cost']

		if val['year_tot_amnt'] != 0:
			val['year_avg_cost'] = val['year_tot_cost'] / val['year_tot_amnt']

		val['life_avg_cost'] = val['year_avg_cost']
		val['life_tot_divd'] = val['year_tot_divd']
		val['life_tot_prof'] = val['year_tot_prof']

	inv_stock[str(thisYear)] = stock2021

	with open('./data/investetf.json', 'w') as wf:
		json.dump(inv_stock, wf, indent=4)

	print('i am done')

def updateInvestmentEnd():
	with open('./data/investetf.json') as rf:
		inv_stock = json.load(rf)

	thisYear = datetime.datetime.today().year

	stock2021 = inv_stock[str(thisYear)]

	for key, val in stock2021.items():
		price = API_call(key)

		val['year_end_valu'] = price * val['year_tot_amnt']


	inv_stock[str(thisYear)] = stock2021

	with open('./data/investetf.json', 'w') as wf:
		json.dump(inv_stock, wf, indent=4)

	print('i am done')

def test():
	a = True
	b = 'kevin'
	return a, ""


def main():

	date = datetime.datetime.today().year

	print(date)
	
	


if __name__ == '__main__':
	main()