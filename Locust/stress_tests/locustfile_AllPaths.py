from locust import HttpUser, task, constant, events
from locust.runners import STATE_STOPPING, STATE_STOPPED, STATE_CLEANUP

class StressTestUser(HttpUser):
    wait_time = constant(0.1)

    @task(1)
    def visit_index(self):
        response = self.client.get("/")
        if response.status_code == 200:
            self.client.post(
                "/",
                data={
                    "start_word": "blighted",
                    "end_word": "slighted",
                },
            )

    @task(2)
    def visit_display(self):
        self.client.get(
            "/display", params={"start_word": "blighted", "end_word": "slighted"}
        )

    @task(1)
    def visit_api_paths(self):
        self.client.get(
            "/api/paths",
            params={"start_word": "blighted", "end_word": "slighted"},
        )

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    if environment.runner and environment.runner.state in [
        STATE_STOPPING,
        STATE_STOPPED,
        STATE_CLEANUP,
    ]:
        print("Stress test completed.")
