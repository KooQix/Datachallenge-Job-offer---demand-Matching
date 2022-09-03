
import sys
sys.path.append(f"{sys.path[0]}/../../")

from models.jober.schemas import JoberCreate
from models.client.schemas import ClientCreate

from models.client.CompanySize import CompanySize

from pandas import read_csv
from models.client.repository import create as client_create
from models.jober.repository import create as jober_create
from models.db import Base, SessionLocal, engine
from sqlalchemy.orm import Session
Base.metadata.create_all(bind=engine)
db: Session = SessionLocal()


file_clients = "models/gen/data/DATA_CLIENT.csv"
file_jobers = "models/gen/data/DATA_JOBEUR.csv"

client_drop_cols = ["un site internet"]
jober_drop_cols = ["Si vous avez un profil Linkedin ou un e-CV, coller le lien URL :", "Si vous avez un site internet, blog ou portfolio coller le lien URL", "Permis PL", "Caces 1", "Caces 2", "Caces 3", "Voitures", "Autre transports"]




	#################### Clients ####################
 
print("\n\t#### Clients ####\n")
df_clients = read_csv(file_clients).drop(client_drop_cols, axis=1)
# print(df_clients)

def add_client(row_client: list):

	# Looking for several jobers 
	row_client[1] = row_client[1].lower().replace(' ', '') == 'oui'
	# worktime, % to int
	row_client[5] = row_client[5].replace(' ', '').replace('%', '')
	# driver_license
	row_client[8] = row_client[8].lower() == "permis de conduire" or row_client[8].lower() == "voiture"

	# Company size: TPE = 1, PME = 2, ETI = 3, BIG_COMPANY = 4
	company_size = str(row_client[9]).split(' ')[0].lower()
	
	if (company_size == "tpe"):
		row_client[9] = int(CompanySize.TPE._value_)
	elif (company_size == "pme"):
		row_client[9] = int(CompanySize.PME._value_)
	elif (company_size == "eti"):
		row_client[9] = int(CompanySize.ETI._value_)
	elif (company_size == "grand"):
		row_client[9] = int(CompanySize.BIG_COMPANY._value_)
	else:
		return
	
	# Other driver licenses
	row_client[10] = row_client[10].lower().replace(' ', '') == 'oui'
	# Required resume
	row_client[16] = row_client[16].replace(' ', '').lower() == 'oui'
 
	client = ClientCreate(
    	job_name = row_client[0], 
     	multi = row_client[1], 
		contract_type = row_client[2], 
		contract_type_differences = row_client[3], 
		if_not_more_info = row_client[4], 
		worktime = row_client[5], 
		salary = row_client[6], 
		location = row_client[7], 
		driver_license = row_client[8], 
		company_size = row_client[9], 
		other_license = row_client[10], 
		skills1 = row_client[11], 
		skills2 = row_client[12], 
		skills3 = row_client[13], 
		teleworking = row_client[14], 
		travel = row_client[15], 
		required_resume = row_client[16], 
		name = row_client[17], 
		surname = row_client[18], 
		company_name = row_client[19], 
		hq_location = row_client[20], 
		siret = row_client[21], 
		naf = row_client[22]
	)
	print(f"\n{client}")
	try:
		client_create(client, db)
	except Exception as e:
		print(f"An error occurred while creating client: {e}")
	


# Add db
for row in df_clients.iterrows():
	row = row[1]
	add_client(list(row))




	#################### Jobers ####################


print("\n\t#### Jobers ####\n")

df_jobers = read_csv(file_jobers).drop(jober_drop_cols, axis=1)
# print(df_jobers)

def add_jober(row_jober: list):

	# Availability1 & 2
	row_jober[7] = row_jober[7].replace(' ', '').replace('%', '')
	row_jober[8] = row_jober[8].replace(' ', '').replace('%', '')
	for i in [12, 13, 14, 15, 16, 23, 24, 30]:
		row_jober[i] = str(row_jober[i]).lower().replace(' ', '') == 'oui'

	# skills1 & 2 might be NaN
	row_jober[18] = '' if (str(row_jober[18]) == "nan") else row_jober[18]
	row_jober[19] = '' if (str(row_jober[19]) == "nan") else row_jober[19]
	
	# distance1, 2,3,4 => 26, 27, 28, 29
	max_distance = 20
	if (str(row_jober[29]).lower().replace(' ', '') == 'oui'):
		max_distance = 65
	elif (str(row_jober[28]).lower().replace(' ', '') == 'oui'):
		max_distance = 60
	elif (str(row_jober[27]).lower().replace(' ', '') == 'oui'):
		max_distance = 40

	jober = JoberCreate(
    	name = row_jober[0], 
		surname = row_jober[1], 
		zip_code = row_jober[2], 
		city = row_jober[3], 
		last_job = row_jober[4], 
		gender = row_jober[5], 
		looking_for_job = row_jober[6], 
		availability1 = row_jober[7], 
		availability2 = row_jober[8], 
		salary = row_jober[9], 
		location_job = row_jober[10], 
		company_size = row_jober[11], 
		driver_license = row_jober[12], 
		tpe = row_jober[13], 
		pme = row_jober[14], 
		eti = row_jober[15], 
		big_company = row_jober[16], 
		skills1 = row_jober[17], 
		skills2 = row_jober[18], 
		skills3 = row_jober[19], 
		contract_type1 = row_jober[20], 
		contract_type2 = row_jober[21], 
		contract_type3 = row_jober[22], 
		contract_type_differences = row_jober[23], 
		if_not_more_info = row_jober[24], 
		teleworking = row_jober[25], 
		max_distance = max_distance,
		ready_move_out = row_jober[30], 
		mobility = row_jober[31]
	)
	print(f"\n{jober}")
	try:
		jober_create(jober, db)
	except Exception as e:
		print(f"An error occurred while creating jober: {e}")



# Add db
for row in df_jobers.iterrows():
	row = row[1]
	add_jober(list(row))
 

# Finally, close db
db.close()
print("\n\n\t#### Database has been populated! ####\n")