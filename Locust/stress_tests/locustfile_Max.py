from locust import HttpUser, task, constant, events
from locust.runners import STATE_STOPPING, STATE_STOPPED, STATE_CLEANUP

class StressTestLongestPathUser(HttpUser):
    wait_time = constant(0.1)

    @task(1)
    def visit_index(self):
        self.client.get("/")

    @task(2)
    def search_longest_path_steps(self):
        self.client.post("/search", data={
            "start_word": "slighted",
            "end_word": "blighted",
            "mode": "steps",
            "max_depth": 15
        })

    @task(2)
    def search_longest_path_weight(self):
        self.client.post("/search", data={
            "start_word": "slighted",
            "end_word": "blighted",
            "mode": "weight",
            "max_depth": 15
        })

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    if environment.runner and environment.runner.state in [
        STATE_STOPPING,
        STATE_STOPPED,
        STATE_CLEANUP,
    ]:
        print("Stress test completed.")
