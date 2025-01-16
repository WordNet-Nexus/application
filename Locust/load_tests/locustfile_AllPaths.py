from locust import HttpUser, task, between

class AllPathsUser(HttpUser):
    wait_time = between(1, 5)

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

