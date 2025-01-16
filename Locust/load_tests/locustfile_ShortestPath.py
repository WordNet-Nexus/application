from locust import HttpUser, task, between
import logging

class ShortestPathUser(HttpUser):
    wait_time = between(1, 5)

    @task(1)
    def visit_index(self):
        self.client.get("/")

    @task(1)
    def get_shortest_path(self):
        data = {
            "start_word": "slighted",
            "end_word": "blighted"
        }
        try:
            self.client.get("/api/paths", params=data)
        except Exception as e:
            logging.error(f"Error en la ruta /api/paths: {str(e)}")
            return {"error": "Internal Server Error"}, 500
        


    @task(1)
    def download_json_paths(self):
        paths_mock = [{"nodes": ["A", "B", "C"], "relationships": [1, 2]}]
        self.client.post("/api/download/json", json={"paths": paths_mock}, headers={"Content-Type": "application/json"})

