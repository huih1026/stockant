import datetime

class Dividend:
	def __init__(self, invest):
		self.invest = invest


	def receive_divd_update(self, args):
		invest = self.invest

		today  = datetime.datetime.today()
		date   = today.date()

		if args['date'] > date:
			return invest, ''

		invest[args['symb']]['life_tot_divd'] += args['amnt']
		invest[args['symb']]['year_tot_divd'] += args['amnt']

		log_msg = str(args['date']) +  ', Divd  ***' + args['symb'] + '*** ' + str(invest[args['symb']]['year_tot_amnt']) + ' @ total amount: ' + str(args['amnt']) + '.\n'

		return invest, log_msg