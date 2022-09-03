import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import euclidean_distances

from models.db import Base, SessionLocal, engine
from models.job.entity import JobEntity
from models.job.repository import get_cluster, set_cluster
from sqlalchemy.orm import Session
from models.job.repository import get_all
from models.job.schemas import Job

from joblib import Parallel, delayed

drop_cols = ["updated_at", "created_at"]




def get_all_jobs():
	# Get every job in database
	Base.metadata.create_all(bind=engine)
	db: Session = SessionLocal()
	_jobs: list[JobEntity] = get_all(db)
	db.close()

	jobs: list[Job] = []
	for job in _jobs:
		jobs.append(job.to_dict())
	return jobs



def set_clusters(df: pd.DataFrame):
	"""Set cluster number in the database

	Args:
		df (pd.DataFrame): The resulting dataframe, after clustering
	"""
	Base.metadata.create_all(bind=engine)
	db: Session = SessionLocal()
	for row in df.iterrows():
		row = row[1]
		nb_cluster = int(row["cluster"])
		job_id = int(row["id"])
		set_cluster(job_id, nb_cluster, db)

	db.close()





def normalize_distances(centroids: list[list[float]]):
	def get_distance_clusters(centroids: list[list[float]], cluster_1: int, cluster_2: int):
		"""Get the distance between 2 cluster centers

		Args:
			cluster_1 (int): Number of the first cluster
			cluster_2 (int): Number of the second cluster

		Returns:
			float | int: Return the distance between the two clusters
		"""
		if (cluster_1 >= len(centroids) or cluster_2 >= len(centroids)): return -1

		if (cluster_1 == cluster_2): return 0

		return euclidean_distances(np.array([centroids[cluster_1]]), np.array([centroids[cluster_2]]))[0][0]

	
	distances = []

	#################### Fill the distances matrix ####################
		
	_max_distance = -1
	_min_distance = 0 # Same cluster
	for i in range(len(centroids)):
		cluster_distances = []
		for j in range(i, len(centroids)):
			dist = get_distance_clusters(centroids, i, j)
			if (dist > _max_distance): _max_distance = dist
			cluster_distances.append(dist)
		
		distances.append(cluster_distances)


	#################### Normalize matrix (0 - 100) ####################

	# max distance = 0% match
	# min distance (0) = 100% match

	for i in range(len(distances)):
		for j in range(len(distances[i])):
			distances[i][j] = 100 - (distances[i][j] - _min_distance) * 100 / (_max_distance - _min_distance) 

	return distances




def clustering():
	""" 
		Create job clusters, based on the required qualities of the job (scrapped when the job has been created)
		
		Once clustering done, set cluster number for each job
		
		Finally, return the clusters centroids
	"""
	def calculate_WSS(points, kmax):

			def process(k: int):
				kmeans = KMeans(n_clusters = k, init="random", n_init=300, max_iter=2000).fit(points)
				centroids = kmeans.cluster_centers_
				pred_clusters = kmeans.predict(points)
				curr_sse = 0

				# calculate square of Euclidean distance of each point from its cluster center and add to current WSS
				for i in range(points.get_shape()[0]):
					curr_center = centroids[pred_clusters[i]]
					curr_sse += (points[i, 0] - curr_center[0]) ** 2 + (points[i, 1] - curr_center[1]) ** 2
				
				return curr_sse

			sse = Parallel(n_jobs=-1)(delayed(process)(k) for k in range(1, kmax+1))

			return sse

	def get_better_k(k_list: list, errors: list):
		stop = 9e-3
		i = 1
		
		while (i < len(k_list) - 3) and ((abs(errors[i] - errors[i + 1]) > stop) or (abs(errors[i + 1] - errors[i + 2]) > stop) or (abs(errors[i + 2] - errors[i + 3]) > stop)):

			i += 1

		return i + 3 if (i < len(k_list) - 3) else -1



	jobs: list[Job] = get_all_jobs()
	
	k_max = int(len(jobs) / 5) + 5
	df = pd.DataFrame.from_dict(jobs).drop(drop_cols, axis=1)
	info_jobs = df["info"]

	vectorizer = TfidfVectorizer(use_idf=False)
	features = vectorizer.fit_transform(info_jobs)

	# Get best k, eg the optimized number of clusters
	errors = calculate_WSS(features, k_max)
	k_list = [k for k in range(1, k_max+1)]
	k = get_better_k(k_list, errors)
	while (k == -1):
		k = get_better_k(k_list, errors)

	model = KMeans(n_clusters=k, init="random", n_init=300, max_iter=2000)
	model.fit(features)
	centroids: list[list[float]] = model.cluster_centers_

	# Add cluster to the dataframe
	df["cluster"] = model.labels_

	# Set cluster number to each job in the database
	set_clusters(df)

	return normalize_distances(centroids)



def get_percentage_distances(normalized_clusters_distances: list[list[float]], cluster_1: int, cluster_2: int):
	"""Get the match percentage between cluster_1 and cluster_2

	Args:
		cluster_1 (int): Number of the first cluster
		cluster_2 (int): Number of the second cluster

	Returns:
		int: Return the match percentage between cluster_1 and cluster_2
	"""
	_min = min(cluster_1, cluster_2)
	_max = max(cluster_1, cluster_2)
	return int(normalized_clusters_distances[_min][_max - _min])


def get_cluster_nb(job_name: str):
	"""Get the cluster number of job_name, in the database

	Args:
		job_name (str): 

	Returns:
		int: Return the cluster number 
	"""
	Base.metadata.create_all(bind=engine)
	db: Session = SessionLocal()
	nb_cluster = get_cluster(job_name, db)
	db.close()
	return nb_cluster