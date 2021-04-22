
class DisplayLife:
	def __init__(self, lifedata):
		self.stocks = lifedata['stocks']
		self.etfs   = lifedata['etfs']

	def get_life_time_inv(self):
		# [ [stocks], [etfs], [total] ]
		invest = []
		stocks = []
		stocks.append('Stocks')
		stocks.append(str(round(self.stocks['life_sto_cost'], 2)))
		stocks.append(str(round(self.stocks['life_sto_divd'], 2)))
		stocks.append(str(round(self.stocks['life_sto_prof'], 2)))
		stocks.append(str(round(self.stocks['life_sto_curr'], 2)))
		stocks.append(str(round(self.stocks['life_sto_gain'], 2)))
		stocks.append(str(round(self.stocks['life_sto_incr'], 4)))
		invest.append(stocks)

		etfs = []
		etfs.append('ETFs')
		etfs.append(str(round(self.etfs['life_etf_cost'], 2)))
		etfs.append(str(round(self.etfs['life_etf_divd'], 2)))
		etfs.append(str(round(self.etfs['life_etf_prof'], 2)))
		etfs.append(str(round(self.etfs['life_etf_curr'], 2)))
		etfs.append(str(round(self.etfs['life_etf_gain'], 2)))
		etfs.append(str(round(self.etfs['life_etf_incr'], 4)))
		invest.append(etfs)

		total = []
		total.append('Total')
		total.append(str(round(self.stocks['life_sto_cost'] + self.etfs['life_etf_cost'], 2)))
		total.append(str(round(self.stocks['life_sto_divd'] + self.etfs['life_etf_divd'], 2)))
		total.append(str(round(self.stocks['life_sto_prof'] + self.etfs['life_etf_prof'], 2)))
		total.append(str(round(self.stocks['life_sto_curr'] + self.etfs['life_etf_curr'], 2)))
		total.append(str(round(self.stocks['life_sto_gain'] + self.etfs['life_etf_gain'], 2)))

		incr = 0
		if self.stocks['life_sto_cost'] + self.etfs['life_etf_cost'] != 0:
			incr = (self.stocks['life_sto_gain']  + self.etfs['life_etf_gain']) / (self.stocks['life_sto_cost'] + self.etfs['life_etf_cost'])
		total.append(str(round(incr, 4)))

		invest.append(total)

		return invest;