from locust import HttpUser, task, between

class ClusterDetectionUser(HttpUser):
    wait_time = between(1, 5)

    @task(1)
    def visit_index(self):
        self.client.get("/")

    @task(2)
    def run_louvain_algorithm(self):
        self.client.get("/api/clusters", params={"algorithm": "louvain"})

    @task(2)
    def run_wcc_algorithm(self):
        self.client.get("/api/clusters", params={"algorithm": "wcc"})

    @task(1)
    def display_louvain_cluster(self):
        self.client.get("/display", params={"algorithm": "louvain", "cluster": 86})

    @task(1)
    def display_wcc_cluster(self):
        self.client.get("/display", params={"algorithm": "wcc", "cluster": 4453})

    @task(1)
    def download_louvain_results(self):
        self.client.get("/api/download/all_results", params={"property": "community"})

    @task(1)
    def download_wcc_results(self):
        self.client.get("/api/download/all_results", params={"property": "component"})
