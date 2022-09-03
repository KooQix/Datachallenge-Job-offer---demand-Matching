import json
import os

from resources.data_preprocessing import preprocessing


def scrap(job_name: str):
    # Scrap using js script. Result (as json) will be written into job_qualities.json
	if (job_name == None or job_name == ''): return None
	os.system(f"node services/web/scrap.js '{job_name}'")
 
	# Read data and return dictionary
	with open("services/web/job_qualities.json", "r") as f:
		res: dict = json.load(f)
		f.close()
		try:
			job_name = res["job_name"]
			if (job_name != None and job_name != ""):
				return res
			else: return None
		except Exception:
			return None
 
 
def preprocessing_data(job_name: str):
	# Scrap data and get it as dictionary
	preprocessed_job_name = preprocessing(job_name, False)

	job = scrap(preprocessed_job_name)

	if (job == None): return None

	data = job["data"]

	if (data == ""):
		# test partial words (Cariste rouleur doesn't find anything; cariste does)
		split = preprocessed_job_name.split(" ")
		if (len(split) > 1):
			i = 0
			while i < len(split) and data == "":
				job = scrap(split[i])
				data = job["data"]
				i += 1

		# Try masculine (Conditionneuse, doesn't find anything; Conditionneur does)
		if (data == ""):
			os.system(f"node services/web/scrap_masc.js '{preprocessed_job_name}'")

			# Read masc name
			with open("services/web/job_masc.json", "r") as f:
				job_masc: str = preprocessing(f.readline(), False)
				f.close()

				if job_masc != "":
					job = scrap(job_masc)
					data = job["data"]
			
	return preprocessing(data, True, [preprocessed_job_name])
