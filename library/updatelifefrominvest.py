'''update datalife.json when investstock.json and investetf.json has changed'''

class UpdateLifeFromInvest:
	def __init__(self, dataLife):
		self.data_life = dataLife


	def get_life_data_updated(self, invStock, invEtf):
		dataLife = self.data_life

		sto_cost = 0
		sto_divd = 0
		sto_prof = 0
		sto_curr = 0
		for key, val in invStock.items():
			sto_cost += val['life_tot_cost']
			sto_divd += val['life_tot_divd']
			sto_prof += val['life_tot_prof']
			sto_curr += val['year_end_valu']

		sto_gain = sto_curr - sto_cost + sto_divd + sto_prof
		sto_incr = 0
		if sto_cost != 0:
			sto_incr = sto_gain / sto_cost

		dataLife['stocks']['life_sto_cost'] = sto_cost
		dataLife['stocks']['life_sto_divd'] = sto_divd
		dataLife['stocks']['life_sto_prof'] = sto_prof
		dataLife['stocks']['life_sto_curr'] = sto_curr
		dataLife['stocks']['life_sto_gain'] = sto_gain
		dataLife['stocks']['life_sto_incr'] = sto_incr

		etf_cost = 0
		etf_divd = 0
		etf_prof = 0
		etf_curr = 0
		for key, val in invEtf.items():
			etf_cost += val['life_tot_cost']
			etf_divd += val['life_tot_divd']
			etf_prof += val['life_tot_prof']
			etf_curr += val['year_end_valu']

		etf_gain = etf_curr - etf_cost + etf_divd + etf_prof
		etf_incr = 0
		if etf_cost != 0:
			etf_incr = etf_gain / etf_cost

		dataLife['etfs']['life_etf_cost'] = etf_cost
		dataLife['etfs']['life_etf_divd'] = etf_divd
		dataLife['etfs']['life_etf_prof'] = etf_prof
		dataLife['etfs']['life_etf_curr'] = etf_curr
		dataLife['etfs']['life_etf_gain'] = etf_gain
		dataLife['etfs']['life_etf_incr'] = etf_incr

		return dataLife

	def get_life_data_updated_stock(self, invStock):
		dataLife = self.data_life

		sto_cost = 0
		sto_divd = 0
		sto_prof = 0
		sto_curr = 0
		for key, val in invStock.items():
			sto_cost += val['life_tot_cost']
			sto_divd += val['life_tot_divd']
			sto_prof += val['life_tot_prof']
			sto_curr += val['year_end_valu']

		sto_gain = sto_curr - sto_cost + sto_divd + sto_prof
		sto_incr = 0
		if sto_cost != 0:
			sto_incr = sto_gain / sto_cost

		dataLife['stocks']['life_sto_cost'] = sto_cost
		dataLife['stocks']['life_sto_divd'] = sto_divd
		dataLife['stocks']['life_sto_prof'] = sto_prof
		dataLife['stocks']['life_sto_curr'] = sto_curr
		dataLife['stocks']['life_sto_gain'] = sto_gain
		dataLife['stocks']['life_sto_incr'] = sto_incr

		return dataLife


	def get_life_data_updated_etf(self, invEtf):
		dataLife = self.data_life

		etf_cost = 0
		etf_divd = 0
		etf_prof = 0
		etf_curr = 0
		for key, val in invEtf.items():
			etf_cost += val['life_tot_cost']
			etf_divd += val['life_tot_divd']
			etf_prof += val['life_tot_prof']
			etf_curr += val['year_end_valu']

		etf_gain = etf_curr - etf_cost + etf_divd + etf_prof
		etf_incr = 0
		if etf_cost != 0:
			etf_incr = etf_gain / etf_cost

		dataLife['etfs']['life_etf_cost'] = etf_cost
		dataLife['etfs']['life_etf_divd'] = etf_divd
		dataLife['etfs']['life_etf_prof'] = etf_prof
		dataLife['etfs']['life_etf_curr'] = etf_curr
		dataLife['etfs']['life_etf_gain'] = etf_gain
		dataLife['etfs']['life_etf_incr'] = etf_incr

		return dataLife
