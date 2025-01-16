from locust import HttpUser, task, constant, events
from locust.runners import STATE_STOPPING, STATE_STOPPED, STATE_CLEANUP

class StressTestIsolatedNodesUser(HttpUser):
    wait_time = constant(0.1)

    @task(1)
    def visit_index(self):
        self.client.get("/")

    @task(2)
    def fetch_isolated_nodes(self):
        self.client.get("/isolated-nodes")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    if environment.runner and environment.runner.state in [
        STATE_STOPPING,
        STATE_STOPPED,
        STATE_CLEANUP,
    ]:
        print("Stress test completed.")
