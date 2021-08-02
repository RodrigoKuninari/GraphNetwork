# Graph Network

Graph Network is a project built using Python, Neo4J and Docker designed to analyse the possible relationships between a group of people.

## Installation

Use Docker to run the Graph Network.

```bash
docker-compose up
```

## Usage

To verify if the server is up:

```python
curl -v "http://localhost"
```

To return the friends of a person:

```python
curl -v "http://localhost/network?name=Ally"
```

## Discussion Notes
Graph Network was an interesting project to do. It was my first time working with Docker and Graph Database, so, I learned a lot during the entire process.