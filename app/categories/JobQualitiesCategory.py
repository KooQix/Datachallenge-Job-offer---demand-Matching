from app.categories.Category import Category
from models.job.schemas import Job

from app.clusters import get_cluster_nb, get_percentage_distances


class JobQualitiesCategory(Category):
	job_client: Job

	last_job_jober: Job
	looking_for_job_jober: Job

	normalized_clusters_distances: list[list[float]]


	def __init__(self, 
			weight: int, 
			normalized_clusters_distances: list[list[float]],  
			job_client: Job, 
			last_job_jober: Job, 
			looking_for_job_jober: Job
		):
		self.weight = weight
		self.normalized_clusters_distances = normalized_clusters_distances
		self.job_client = job_client
		self.last_job_jober = last_job_jober
		self.looking_for_job_jober = looking_for_job_jober


	def compare(self):
		# Get cluster nb for each job
		if (self.job_client == None): return 0
		
		nb_cluster_job_client = get_cluster_nb(self.job_client.job_name)
		nb_cluster_job_jober = get_cluster_nb(self.last_job_jober.job_name if (self.last_job_jober != None) else self.looking_for_job_jober.job_name)
		
		self.match_percentage = get_percentage_distances(self.normalized_clusters_distances, nb_cluster_job_jober, nb_cluster_job_client)

		if (self.looking_for_job_jober.job_name != self.job_client.job_name):
			self.match_percentage /= 1.2

		if (self.last_job_jober == None):
			self.match_percentage /= 1.4

		return self.match_percentage 


	def to_dict(self):
		return {"job_qualities_category": self.match_percentage}




		

	