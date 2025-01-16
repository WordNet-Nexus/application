from locust import HttpUser, task, constant, events
from locust.runners import STATE_STOPPING, STATE_STOPPED, STATE_CLEANUP

class StressTestTopConnectedNodesUser(HttpUser):
    wait_time = constant(0.1)

    @task(1)
    def visit_index(self):
        self.client.get("/")

    @task(2)
    def get_top_connected_nodes(self):
        self.client.get("/top-connected-nodes", params={"limit": 10, "min_length": 5})

    @task(1)
    def search_word_connections(self):
        self.client.post("/search-word", data={"word": "fasted"})


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    if environment.runner and environment.runner.state in [
        STATE_STOPPING,
        STATE_STOPPED,
        STATE_CLEANUP,
    ]:
        print("Stress test completed.")
