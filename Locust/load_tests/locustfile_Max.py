from locust import HttpUser, task, between

class LongestPathUser(HttpUser):
    wait_time = between(1, 5)

    @task(1)
    def visit_index(self):
        self.client.get("/")

    @task(1)
    def search_longest_path_steps(self):
        self.client.post("/search", data={
            "start_word": "slighted",
            "end_word": "blighted",
            "mode": "steps",
            "max_depth": 15
        })

    @task(1)
    def search_longest_path_weight(self):
        self.client.post("/search", data={
            "start_word": "slighted",
            "end_word": "blighted",
            "mode": "weight",
            "max_depth": 15
        })