from locust import HttpUser, task, constant, events
from locust.runners import STATE_STOPPING, STATE_STOPPED, STATE_CLEANUP

class StressTestNodeConnectionsUser(HttpUser):
    wait_time = constant(0.1)

    @task(1)
    def visit_index(self):
        self.client.get("/")

    @task(2)
    def get_specific_degree_nodes(self):
        self.client.get("/api/nodes/specific_degree", params={"degree": 3})

    @task(2)
    def get_degree_range_nodes(self):
        self.client.get("/api/nodes/degree_range", params={"min_degree": 2, "max_degree": 5})

    @task(2)
    def get_min_degree_nodes(self):
        self.client.get("/api/nodes/min_degree", params={"min_degree": 4})


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    if environment.runner and environment.runner.state in [
        STATE_STOPPING,
        STATE_STOPPED,
        STATE_CLEANUP,
    ]:
        print("Stress test completed.")
