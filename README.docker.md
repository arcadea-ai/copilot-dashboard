# Deploying GitHub Copilot Dashboard with Docker

This guide provides step-by-step instructions for building and running the **GitHub Copilot Dashboard** using Docker.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your machine.
- A **GitHub API Key** (refer to the main project README for generation instructions).
- A `.env` file with the required environment variables. (refer to the main project README for `.env` file setup).

---

## 1. Build the Docker Image

Run the following command from the root directory of the project:

```
docker build -t copilot-dashboard .
```
## Docker Image Creation Process

This command will:

- Use the Dockerfile to create an image.
- Install all necessary dependencies.
- Set up the working environment.


# Run the Container
Using Environment Variables (Recommended)
```
docker run -p 8501:8501 --env-file <path/to/.env> copilot-dashboard
```
or manually pass the GitHub API key:
```
docker run -p 8501:8501 -e GITHUB_API_KEY=your_token_here copilot-dashboard
```
This will:
- Map the container’s port 8501 to the host machine.
- Load environment variables from .env or pass them manually.

## Accessing the Application
Once the container is running, open:
```
http://localhost:8501
```


