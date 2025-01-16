from locust import HttpUser, task, constant, events
from locust.runners import STATE_STOPPING, STATE_STOPPED, STATE_CLEANUP

class StressTestShortestPathUser(HttpUser):
    wait_time = constant(0.1)

    @task(1)
    def visit_index(self):
        self.client.get("/")
    
    @task(1)
    def get_shortest_path(self):
        data = {
            "start_word": "slighted",
            "end_word": "blighted"
        }
        self.client.get("/api/paths", params=data)

    @task(1)
    def download_json_paths(self):
        paths_mock = [{"nodes": ["A", "B", "C"], "relationships": [1, 2]}]
        self.client.post("/api/download/json", json={"paths": paths_mock}, headers={"Content-Type": "application/json"})

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    if environment.runner and environment.runner.state in [
        STATE_STOPPING,
        STATE_STOPPED,
        STATE_CLEANUP,
    ]:
        print("Stress test completed.")
