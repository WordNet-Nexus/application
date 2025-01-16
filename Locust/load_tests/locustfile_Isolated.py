from locust import HttpUser, task, between

class IsolatedNodesUser(HttpUser):
    wait_time = between(1, 5)

    @task(1)
    def visit_index(self):
        self.client.get("/")

    @task(2)
    def fetch_isolated_nodes(self):
        self.client.get("/isolated-nodes")

