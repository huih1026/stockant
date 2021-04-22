
class DisplayBench:
	def __init__(self, benchDate):
		self.bench = benchDate

	def get_bench_mark(self):
		bench = self.bench
		data  = []
		data.append('S&P 500')

		data.append(str(round(bench['life_beg'], 2)))
		data.append(str(round(bench['year_beg'], 2)))

		data.append(str(round(bench['life_max'], 2)))
		data.append(str(round(bench['year_cur'], 2)))

		# get the percent diff from high
		per_to_high = (bench['life_max'] - bench['year_cur']) / bench['year_cur']
		data.append(str(round(per_to_high, 4)))

		year_incr_rate = (bench['year_cur'] - bench['year_beg']) / bench['year_beg']
		life_incr_rate = (bench['year_cur'] - bench['life_beg']) / bench['life_beg']

		data.append(str(round(year_incr_rate, 4)))
		data.append(str(round(life_incr_rate, 4)))

		return data;