from app.Match import Match
from app.categories.Mobility import Mobility
from app.clusters import clustering, get_cluster_nb, get_percentage_distances
from models.client.schemas import Client
from models.jober.schemas import Jober, JoberMatch
from models.jober.repository import get_all as get_all_jobers

from models.db import Base, SessionLocal, engine
from sqlalchemy.orm import Session
from joblib import Parallel, delayed

MIN_MATCH_PERCENTAGE = 60 
MIN_CLUSTER_MATCH_PERCENTAGE = 80


def sort_decreasing_percentages(matches: list[Match], jobers: list[Jober]):
	"""Get the jobers who matched, by decreasing match percentage

	Args:
		matches (list[Match]): The matchs between the given client and the jobers
		jobers (list[Jober]): The jobers that tried to match with the given client

	Returns:
		list[JoberMatch]: The jobers who matched, by decreasing match percentage
	"""
	sorted_jobers_matches: list[JoberMatch] = []


	for i in range(len(matches)):
		match = matches[i]
		jober = jobers[i]

		if (match == None or match.match_percentage < MIN_MATCH_PERCENTAGE): continue

		sorted_jobers_matches.append(
			JoberMatch(
				name = jober.name,
				surname = jober.surname,
				zip_code = jober.zip_code,
				city = jober.city.city,
				last_job = jober.last_job.job_name or '',
				gender = jober.gender,
				looking_for_job = jober.looking_for_job.job_name or '',
				availability1 = jober.availability1,
				availability2 = jober.availability2,
				salary = jober.salary,
				location_job = jober.location_job,
				company_size = jober.company_size,
				driver_license = jober.driver_license,
				tpe = jober.tpe,
				pme = jober.pme,
				eti = jober.eti,
				big_company = jober.big_company,
				skills1 = jober.skills1,
				skills2 = jober.skills2,
				skills3 = jober.skills3,
				contract_type1 = jober.contract_type1,
				contract_type2 = jober.contract_type2,
				contract_type3 = jober.contract_type3,
				contract_type_differences = jober.contract_type_differences,
				if_not_more_info = jober.if_not_more_info,
				teleworking = jober.teleworking,
				max_distance = jober.max_distance,
				ready_move_out = jober.ready_move_out,
				mobility = jober.mobility,
				id = jober.id,
				match_percentage = match.match_percentage,
				match_info = match.get_info()
		))

	sorted_jobers_matches.sort(key = lambda jober: jober.match_percentage, reverse = True)

	return sorted_jobers_matches



def get_best_match_client(client: Client):
	# Create clusters and get a list of distances between clusters (0 - 100)
	# 0 means that the two clusters are  very far away from each other (ie match at 0%)
	# On the other hand, 100 means that the two jobs match perfectly ie match at 100%
	normalized_clusters_centroids_distances = clustering()

	match_res: list[Match]

	# Get all jobers
	Base.metadata.create_all(bind=engine)
	db: Session = SessionLocal()
	jobers: list[Jober] = get_all_jobers(db)
	db.close()

	nb_client_cluster = get_cluster_nb(client.job_name.job_name) 

	def process(jober: Jober):

		#################### Filtering jobers ####################
		
		# Solely take those who are ready to move out or are within distance of the client job
		mobility = Mobility(client.location, jober.city, jober.max_distance, jober.ready_move_out)

		if (not(mobility.compare())): return None
		
		nb_jober_cluster = jober.last_job.cluster if (jober.last_job != None) else jober.looking_for_job.cluster
		# If client job and jober last_job | looking for job are in two very different clusters, pass
		if (get_percentage_distances(normalized_clusters_centroids_distances, nb_jober_cluster, nb_client_cluster) < MIN_CLUSTER_MATCH_PERCENTAGE):	
			return None	

		#################### Matching ####################
			
		match = Match(jober, client, normalized_clusters_centroids_distances)
		match.get_match_percentage()
		return match

	
	match_res = Parallel(n_jobs=-1)(delayed(process)(jober) for jober in jobers)

	# sort by match_percentage decreasing and return jobers from this list of matches
	return sort_decreasing_percentages(match_res, jobers)[:25]
	

