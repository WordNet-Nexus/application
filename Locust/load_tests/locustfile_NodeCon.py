from locust import HttpUser, task, between

class NodeConnectionsUser(HttpUser):
    wait_time = between(1, 5)

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
