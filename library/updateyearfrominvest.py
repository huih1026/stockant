'''update datayear.json when investstock.json and investetf.json has changed'''

class UpdateYearFromInvest:
	def __init__(self, dataYear):
		self.data_year = dataYear

	def get_year_data_updated(self, invStock, invEtf):
		dataYear = self.data_year

		sto_cost = 0
		sto_divd = 0
		sto_prof = 0
		sto_curr = 0
		sto_addi = 0
		for key, val in invStock.items():
			sto_addi += val['year_add_cost']
			sto_cost += val['year_tot_cost']
			sto_divd += val['year_tot_divd']
			sto_prof += val['year_tot_prof']
			sto_curr += val['year_end_valu']
			
		sto_gain = sto_curr - sto_cost + sto_divd + sto_prof
		sto_incr = 0
		if sto_cost != 0:
			sto_incr = sto_gain / sto_cost

		dataYear['stocks']['year_sto_addi'] = sto_addi
		dataYear['stocks']['year_sto_cost'] = sto_cost
		dataYear['stocks']['year_sto_divd'] = sto_divd
		dataYear['stocks']['year_sto_prof'] = sto_prof
		dataYear['stocks']['year_sto_curr'] = sto_curr
		dataYear['stocks']['year_sto_gain'] = sto_gain
		dataYear['stocks']['year_sto_incr'] = sto_incr


		etf_cost = 0
		etf_divd = 0
		etf_prof = 0
		etf_curr = 0
		etf_addi = 0
		for key, val in invEtf.items():
			etf_addi += val['year_add_cost']
			etf_cost += val['year_tot_cost']
			etf_divd += val['year_tot_divd']
			etf_prof += val['year_tot_prof']
			etf_curr += val['year_end_valu']

		etf_gain = etf_curr - etf_cost + etf_divd + etf_prof
		etf_incr = 0
		if etf_cost != 0:
			etf_incr = etf_gain / etf_cost

		dataYear['etfs']['year_etf_addi'] = etf_addi
		dataYear['etfs']['year_etf_cost'] = etf_cost
		dataYear['etfs']['year_etf_divd'] = etf_divd
		dataYear['etfs']['year_etf_prof'] = etf_prof
		dataYear['etfs']['year_etf_curr'] = etf_curr
		dataYear['etfs']['year_etf_gain'] = etf_gain
		dataYear['etfs']['year_etf_incr'] = etf_incr

		return dataYear

	def get_year_data_updated_stock(self, invStock):
		dataYear = self.data_year

		sto_cost = 0
		sto_divd = 0
		sto_prof = 0
		sto_curr = 0
		sto_addi = 0
		for key, val in invStock.items():
			sto_addi += val['year_add_cost']
			sto_cost += val['year_tot_cost']
			sto_divd += val['year_tot_divd']
			sto_prof += val['year_tot_prof']
			sto_curr += val['year_end_valu']
			
		sto_gain = sto_curr - sto_cost + sto_divd + sto_prof
		sto_incr = 0
		if sto_cost != 0:
			sto_incr = sto_gain / sto_cost

		dataYear['stocks']['year_sto_addi'] = sto_addi
		dataYear['stocks']['year_sto_cost'] = sto_cost
		dataYear['stocks']['year_sto_divd'] = sto_divd
		dataYear['stocks']['year_sto_prof'] = sto_prof
		dataYear['stocks']['year_sto_curr'] = sto_curr
		dataYear['stocks']['year_sto_gain'] = sto_gain
		dataYear['stocks']['year_sto_incr'] = sto_incr

		return dataYear



	def get_year_data_updated_etf(self, invEtf):
		dataYear = self.data_year

		etf_cost = 0
		etf_divd = 0
		etf_prof = 0
		etf_curr = 0
		etf_addi = 0
		for key, val in invEtf.items():
			etf_addi += val['year_add_cost']
			etf_cost += val['year_tot_cost']
			etf_divd += val['year_tot_divd']
			etf_prof += val['year_tot_prof']
			etf_curr += val['year_end_valu']

		etf_gain = etf_curr - etf_cost + etf_divd + etf_prof
		etf_incr = 0
		if etf_cost != 0:
			etf_incr = etf_gain / etf_cost

		dataYear['etfs']['year_etf_addi'] = etf_addi
		dataYear['etfs']['year_etf_cost'] = etf_cost
		dataYear['etfs']['year_etf_divd'] = etf_divd
		dataYear['etfs']['year_etf_prof'] = etf_prof
		dataYear['etfs']['year_etf_curr'] = etf_curr
		dataYear['etfs']['year_etf_gain'] = etf_gain
		dataYear['etfs']['year_etf_incr'] = etf_incr

		return dataYear