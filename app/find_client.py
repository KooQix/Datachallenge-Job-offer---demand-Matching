from app.Match import Match
from app.categories.Mobility import Mobility
from app.clusters import clustering, get_cluster_nb, get_percentage_distances
from models.client.schemas import Client, ClientMatch
from models.jober.schemas import Jober
from models.client.repository import get_all as get_all_clients


from models.db import Base, SessionLocal, engine
from sqlalchemy.orm import Session

from joblib import Parallel, delayed

MIN_MATCH_PERCENTAGE = 60 
MIN_CLUSTER_MATCH_PERCENTAGE = 80


def sort_decreasing_percentages(matches: list[Match], clients: list[Client]):
	"""Get the clients who matched, by decreasing match percentage

	Args:
		matches (list[Match]): The matchs between the given client and the clients
		clients (list[Client]): The clients that tried to match with the given client

	Returns:
		list[ClientMatch]: The clients who matched, by decreasing match percentage
	"""
	sorted_clients_matches: list[ClientMatch] = []
		
	for i in range(len(matches)):
		match = matches[i]
		client = clients[i]

		if (match == None or match.match_percentage < MIN_MATCH_PERCENTAGE): continue

		sorted_clients_matches.append(
			ClientMatch(
				multi = client.multi,
				contract_type = client.contract_type,
				contract_type_differences = client.contract_type_differences,
				if_not_more_info = client.if_not_more_info,
				worktime = client.worktime,
				salary = client.salary,
				location = client.location.city,
				driver_license = client.driver_license,
				company_size = client.company_size,
				other_license = client.other_license,
				skills1 = client.skills1,
				skills2 = client.skills2,
				skills3 = client.skills3,
				teleworking = client.teleworking,
				travel = client.travel,
				required_resume = client.required_resume,
				name = client.name,
				surname = client.surname,
				company_name = client.company_name,
				hq_location = client.hq_location,
				siret = client.siret,
				naf = client.naf,
				job_name = client.job_name.job_name,
				id = client.id,
				match_percentage = match.match_percentage,
				match_info = match.get_info()
			)
		)

	
	sorted_clients_matches.sort(key = lambda client: client.match_percentage, reverse = True)
	return sorted_clients_matches




def get_best_match_jober(jober: Jober):
	# Create clusters and get a list of distances between clusters (0 - 100)
	# 0 means that the two clusters are  very far away from each other (ie match at 0%)
	# On the other hand, 100 means that the two jobs match perfectly ie match at 100%
	normalized_clusters_centroids_distances = clustering()

	match_res: list[Match]

	# Get all clients
	Base.metadata.create_all(bind=engine)
	db: Session = SessionLocal()
	clients: list[Client] = get_all_clients(db)
	db.close()

	nb_jober_cluster = get_cluster_nb(jober.last_job.job_name) if (jober.last_job != None) else get_cluster_nb(jober.looking_for_job.job_name)

	def process(client: Client):
		
		#################### Filtering clients ####################
		
		# Solely take those who are ready to move out or are within distance of the client job
		mobility = Mobility(client.location, jober.city, jober.max_distance, jober.ready_move_out)
		if (not(mobility.compare())): return None

			
		# If client job and jober last_job | looking for job are in two very different clusters, pass
		if (get_percentage_distances(normalized_clusters_centroids_distances, client.job_name.cluster, nb_jober_cluster) < MIN_CLUSTER_MATCH_PERCENTAGE):	
			return None	

		#################### Matching ####################
		

		match = Match(jober, client, normalized_clusters_centroids_distances)
		match.get_match_percentage()
		return match

	match_res = Parallel(n_jobs=-1)(delayed(process)(client) for client in clients)


	# sort by match_percentage decreasing and return jobers from this list of matches
	return sort_decreasing_percentages(match_res, clients)[:25]
	

