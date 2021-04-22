class DisplayPositions:
	def __init__(self, positions):
		self.positions = positions

	def get_positions_inv(self):
		invest = []
		for key, val in self.positions.items():

			# skip the inactive symbols
			if val['life_liv_stat'] == False:
				continue

			symb = []
			symb.append(key)
			symb.append(round(val['year_tot_amnt'], 2))
			symb.append(round(val['year_tot_cost'], 2))
			symb.append(round(val['year_tot_divd'], 2))
			symb.append(round(val['year_tot_prof'], 2))
			symb.append(round(val['year_end_valu'], 2))

			gain = val['year_end_valu'] - val['year_tot_cost'] + val['year_tot_divd'] + val['year_tot_prof']
			incr = 0
			if val['year_tot_cost'] != 0:
				incr = gain / val['year_tot_cost']

			symb.append(round(gain, 2))
			symb.append(round(incr, 4))

			invest.append(symb)

		return invest
			