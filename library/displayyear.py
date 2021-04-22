
class DisplayYear:
	def __init__(self, yeardata):
		# yeardata contains stocks and etfs, separate them
		self.stocks = yeardata['stocks']
		self.etfs   = yeardata['etfs']


	def get_curr_year_inv(self):
		# [ [stocks], [etfs], [total] ]
		invest = []
		stocks = []
		stocks.append('Stocks')
		stocks.append(round(self.stocks['year_sto_cost'], 2))
		stocks.append(round(self.stocks['year_sto_addi'], 2))

		add_per_sto = 0
		if self.stocks['year_sto_cost'] - self.stocks['year_sto_addi'] != 0:
			add_per_sto = self.stocks['year_sto_addi'] / (self.stocks['year_sto_cost'] - self.stocks['year_sto_addi'])
		
		stocks.append(round(add_per_sto, 4))
		stocks.append(round(self.stocks['year_sto_divd'], 2))
		stocks.append(round(self.stocks['year_sto_prof'], 2))
		stocks.append(round(self.stocks['year_sto_curr'], 2))
		stocks.append(round(self.stocks['year_sto_gain'], 2))
		stocks.append(round(self.stocks['year_sto_incr'], 4))
		invest.append(stocks)

		etfs = []
		etfs.append('ETFs')
		etfs.append(str(round(self.etfs['year_etf_cost'], 2)))
		etfs.append(str(round(self.etfs['year_etf_addi'], 2)))

		add_per_etf = 0
		if self.etfs['year_etf_cost'] - self.etfs['year_etf_addi'] != 0:
			add_per_etf = self.etfs['year_etf_addi'] / (self.etfs['year_etf_cost'] - self.etfs['year_etf_addi'])
		
		etfs.append(round(add_per_etf, 4))
		etfs.append(round(self.etfs['year_etf_divd'], 2))
		etfs.append(round(self.etfs['year_etf_prof'], 2))
		etfs.append(round(self.etfs['year_etf_curr'], 2))
		etfs.append(round(self.etfs['year_etf_gain'], 2))
		etfs.append(round(self.etfs['year_etf_incr'], 4))
		invest.append(etfs)

		total = []
		total.append('Total')
		tot_cost = self.stocks['year_sto_cost'] + self.etfs['year_etf_cost']
		tot_addi = self.stocks['year_sto_addi'] + self.etfs['year_etf_addi']
		total.append(round(tot_cost, 2))
		total.append(round(tot_addi, 2))

		perc_tot = 0
		if tot_cost - tot_addi != 0:
			perc_tot = tot_addi / (tot_cost - tot_addi)

		total.append(round(perc_tot, 4))
		total.append(round(self.stocks['year_sto_divd'] + self.etfs['year_etf_divd'], 2))
		total.append(round(self.stocks['year_sto_prof'] + self.etfs['year_etf_prof'], 2))
		total.append(round(self.stocks['year_sto_curr'] + self.etfs['year_etf_curr'], 2))
		total.append(round(self.stocks['year_sto_gain'] + self.etfs['year_etf_gain'], 2))

		incr = 0
		if self.stocks['year_sto_cost'] + self.etfs['year_etf_cost'] != 0:
			incr = (self.stocks['year_sto_gain'] + self.etfs['year_etf_gain']) / (self.stocks['year_sto_cost'] + self.etfs['year_etf_cost'])
		total.append(round( incr, 4))
		
		invest.append(total)

		return invest;