from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from qdrant_client.http.models import (
    PointStruct,
    PointIdsList,
)
from core.config import QDRANT_URL,QDRANT_API_KEY

client = QdrantClient(
    url=QDRANT_URL,api_key=QDRANT_API_KEY,check_compatibility=False
)


class VectorService:

    def __init__(self):
        self.client = client

        if not self.client.collection_exists("jobsvectors"):
            self.client.create_collection(
                collection_name="jobsvectors",
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE
                )
            )

        if not self.client.collection_exists("resumesvectors"):
            self.client.create_collection(
                collection_name="resumesvectors",
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE
                )
            )
        if not self.client.collection_exists("recommendationsvectors"):
            self.client.create_collection(
                collection_name="recommendationsvectors",
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE
                )
            )

    # ---------------- JOBS ----------------

    def store_job_embedding(self, job, embedding: list[float]):
        self.client.upsert(
            collection_name="jobsvectors",
            points=[
                PointStruct(
                    id=job.id,
                    vector=embedding,
                    payload={
                        "location": job.location,
                        "salary_range": job.salary_range,
                        "job_type": job.job_type,
                    }
                )
            ]
        )

    def remove_job_embedding(self, job_id: int):
        self.client.delete(
            collection_name="jobsvectors",
            points_selector=PointIdsList(
                points=[job_id]
            )
        )

    def search_vectors(
        self,
        query_vector: list[float],
        top_k: int
    ):
        return self.client.query_points(
            collection_name="jobsvectors",
            query=query_vector,
            limit=top_k
        )
    def get_job_vector(self, job_id: int):
        result = self.client.retrieve(
            collection_name="jobsvectors",
            ids=[job_id],
            with_vectors=True
        )

        if not result:
            return None

        return result[0]
    # ---------------- RESUMES ----------------

    def store_resume_embedding(
        self,
        user_id: int,
        embedding: list[float],
        job_role:str,
        years_of_experience:int,
        skills: list[str]
    ):
        result=self.client.upsert(
            collection_name="resumesvectors",
            points=[
                PointStruct(
                    id=user_id,
                    vector=embedding,
                    payload={
                        "job_role": job_role,
                        "experience": years_of_experience,
                        "skills": skills
                    }
                )
            ]
        )
    def store_recommendations(self, user_id: int,embedding: list[float]):
        result=self.client.upsert(
            collection_name="recommendationsvectors",
            points=[
                PointStruct(
                    id=user_id,
                    vector=embedding,
                    payload={
                        "user_id": user_id
                    }
                )
            ]
        )
    def remove_recommendations(self, user_id: int):
        self.client.delete(
            collection_name="recommendationsvectors",
            points_selector=PointIdsList(
                points=[user_id]
            )
        )
    def get_resume_data(self, user_id: int):
        result = self.client.retrieve(
            collection_name="resumesvectors",
            ids=[user_id]
        )

        if not result:
            return None

        return result[0].payload

    def get_resume_vector(self, user_id: int):
        result = self.client.retrieve(
            collection_name="resumesvectors",
            ids=[user_id],
            with_vectors=True
        )
    

        if not result:
            return None

        return result[0]

    def remove_resume_embedding(self, user_id: int):
        self.client.delete(
            collection_name="resumesvectors",
            points_selector=PointIdsList(
                points=[user_id]
            )
        )
    def search_resume_vectors(
        self,
        query_vector: list[float],
        top_k: int
    ):
        return self.client.query_points(
            collection_name="resumesvectors",
            query=query_vector,
            limit=top_k
        )
    def get_recommendation_vectors(self, user_id: int):
        result = self.client.retrieve(
            collection_name="recommendationsvectors",
            ids=[user_id],
            with_vectors=True
        )

        if not result:
            return None

        return result[0]