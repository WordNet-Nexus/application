from locust import HttpUser, task, between

class TopConnectedNodesUser(HttpUser):
    wait_time = between(1, 5)

    @task(1)
    def visit_index(self):
        self.client.get("/")

    @task(2)
    def get_top_connected_nodes(self):
        self.client.get("/top-connected-nodes", params={"limit": 10, "min_length": 5})

    @task(1)
    def search_word_connections(self):
        self.client.post("/search-word", data={"word": "fasted"})

