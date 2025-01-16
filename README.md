# Wordnet-nexus: Word Graph Construction and Distributed Architecture

<div align="justify">
  
In this repository, you will find the source code for building a scalable and distributed architecture for processing and analyzing word-based graphs, leveraging AWS cloud services and DevOps practices. The system is designed to construct graphs from word datasets, where each word is a node, and edges connect words that differ by only one letter. This microservices-based application consists of the following modules:

- **Crawler**: Downloads books from Project Gutenberg and stores them in an AWS S3 bucket.
- **DatalakeBuilder**: Processes the books from S3, extracts words, computes their frequencies, and stores the results in a MongoDB database.
- **GraphDrawer**: Retrieves word frequencies from MongoDB, builds the graph, and saves it in a Neo4j database.
- **API Service**: Provides multiple APIs with dedicated web interfaces for tasks such as finding shortest paths, identifying clusters, detecting isolated nodes, and analyzing connections in the graph.
- **Architecture Module**: Contains scripts to define and deploy the distributed architecture on AWS and the memory that describes it.
- **Locust**: Includes Python scripts for performance testing of the web services using Locust.

In addition to the above, the tests are documented in their corresponding modules.

This architecture demonstrates efficient scaling for large datasets, robust API interaction, and insights into graph-based problems, showcasing practical applications in data science.

<img src="resources/Cloud Architecture.png" alt="Image for Dark Mode">

<h2>1) <b>How to run</b> </h2>
  
To deploy the full architecture, simply run the script that defines it as follows. Ensure that your AWS credentials are properly set as environment variables before proceeding.

```
./Architecture/init.sh
```

This script performs the following actions:

- Sets up the **VPC environment**, creating a Virtual Private Cloud (VPC) along with public and private subnets.
- Deploys various components of the architecture:
  - **Datalake Server**: Installs MongoDB in the private subnet.
  - **Datamart Server**: Installs Neo4j in the private subnet.
  - **Crawler Server**: Deploys the crawler in the public subnet to fetch data.
  - **Build Datalake**: Processes and prepares the datalake in MongoDB.
  - **Path Server API**: Deploys an API server to handle path-related requests in the private subnet.
  - **Build Datamart**: Sets up the datamart in Neo4j.
  - **Node Server API**: Deploys an API server for node-specific queries in the private subnet.
  - **Lambda Functions**: Deploys Lambda-based API services.
  - **NGINX Proxy Server**: Configures NGINX as a proxy server in the public subnet.

At the end of the deployment process, the script outputs an **Elastic IP Address**, which can be used to access the web application hosted on the NGINX proxy server.

```
http://<Elastic-IP>
```

<h2>Credits</h2>

- [Susana Suárez](https://github.com/susanasrez)
- [Mara Pareja](https://github.com/marapareja17)