
### README.md

---



## Description

This application uses Python to extract data from various sources and load it into a Neo4j database. It is designed to be run in a Docker container for easy setup and deployment.
This contains a simple class that extracts data from a few different file types and creates Dict's The remaining is a structure to load the data into a Neo4j database and follow the applictaion model

## Getting Started

### Dependencies

- Docker
- Docker Compose (optional, for simplified multi-container setup)
- Python 3.8
- Neo4j (for local development or separate container deployment)

### Installing

- Clone this repository.
- Ensure Docker and Docker Compose (if using) are installed on your system.

## Running the Application


### Running Separately

If you prefer to run Neo4j and the Python application separately, you can do so by executing each container independently.

1. **Start Neo4j container:**

   ```bash
   docker run \
       --name neo4j \
       -p7474:7474 -p7687:7687 \
       -d \
       -v $HOME/neo4j/data:/data \
       -v $HOME/neo4j/logs:/logs \
       -v $HOME/neo4j/import:/var/lib/neo4j/import \
       -v $HOME/neo4j/plugins:/plugins \
       --env NEO4J_AUTH=neo4j/password \
       neo4j:latest
   ```

2. **Build and run the Python application container:**

   ```bash
   docker build -t py-neo4j-app .
   docker run -p 4000:80 --net=host py-neo4j-app
   ```

   Ensure that the environment variables in the `docker run` command match the settings of your Neo4j container.

## Usage

After starting the application using either method, access the Python app at `http://localhost:4000` and the Neo4j browser interface at `http://localhost:7474`.

