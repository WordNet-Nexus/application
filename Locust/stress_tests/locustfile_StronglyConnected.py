from locust import HttpUser, task, constant, events
from locust.runners import STATE_STOPPING, STATE_STOPPED, STATE_CLEANUP

class StressTestClusterDetectionUser(HttpUser):
    wait_time = constant(0.1)

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
        """Simula mostrar un cluster específico utilizando Louvain."""
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

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    if environment.runner and environment.runner.state in [
        STATE_STOPPING,
        STATE_STOPPED,
        STATE_CLEANUP,
    ]:
        print("Stress test completed.")
