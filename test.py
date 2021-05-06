import datetime
import requests
import json
from library.updateinvest import UpdateInvest
from library.updatebench  import UpdateBench

def API_call(key, date):
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

	print(payload['startDate'])
	print(payload['endDate'])

	count = 1
	while count < 7:
		req = requests.get(url=url, params=payload)
		if req.status_code == 200:
			res = req.json()
			print(payload['startDate'])
			print(payload['endDate'])
			return res
		
		datee = date - datetime.timedelta(days=count)
		y, m, d = datee.year, datee.month, datee.day
		epoch = int(datetime.datetime(y, m, d, 0, 0).timestamp() * 1000)
		payload['startDate'] = epoch
		payload['endDate']   = epoch
		count += 1

	return {'empty': True}

	


def main():
	a = -0.3
	print(abs(a))

if __name__ == '__main__':
	main()