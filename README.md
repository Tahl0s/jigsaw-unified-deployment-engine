# J.U.D.E - Jigsaw Unified Deployment Engine - WIP
**#ai #devops #opensource #cloud**

J.U.D.E is a project focused on creating a locally hosted AI-powered engine for automating server management, monitoring, and alerting while remaining scalable.

![Screenshot 2025-02-26 002618](https://github.com/user-attachments/assets/2cd0be2e-da27-49ad-812e-338dfa0af260)

Managing servers efficiently can be a challenge, and automation is key to handling complex infrastructure. **J.U.D.E (Jigsaw Unified Deployment Engine)** is designed to be an AI-driven solution for streamlining server management, monitoring, and alerting. With a locally hosted, containerized approach, J.U.D.E covers everything from security to adaptability, all while reducing operational overhead.

## Features Implemented So Far
- **Model Baseline & Browser Framework**
- **Ollama Running Inside Flask**
- **Locally Hosted**: No external API dependencies, ensuring security and privacy.
- **Short-Term Memory**: Maintains session context for improved interactions.
- **Long-Term Memory**: Persistent knowledge storage and retrieval.
- **Intelligent Knowledge Auto-Removal**: Efficient management of obsolete data.
- **Personality Index**: Configurable personality-based responses.
- **Reference-Based Reasoning**: Utilizing context and prior interactions to improve accuracy.
- **Access to Network Time**: For reasoning based on real-world timestamps.

## Current Planned Future Enhancements
- **API Integration**: For external systems and services.
- **MFA for Interface & SSH**: Enhancing security for remote access and automated deployments.
- **Advanced Alerting & Monitoring**: Automated incident response and remediation.
- **Containerized Deployments**: Optimizing Docker environments for portability and scalability.

## Why J.U.D.E?
The goal of J.U.D.E is to streamline the sometimes mundane administrative tasks involved in:
- Actively monitoring and applying patches based on pre-defined knowledge articles.
- Automating server management using tools like Ansible.
- Managing the lifecycle of VMs, and more.

By automating these tasks, J.U.D.E reduces the operational overhead and increases efficiency for systems administrators and DevOps teams.

## The Current State of Things
As of writing this, **J.U.D.E** is currently in the core refinement stage. The API is being expanded to support external services, and the core logic is being refined to ensure a solid, stable framework.

### Next Milestones:
- Implementing advanced token-based OAuth for secure authentication.
- Expanding API support to integrate with other services and tools.

## Setup Instructions

### Prerequisites:
- **Docker**: Ensure Docker is installed on your machine or server.
- **Docker Compose**: For multi-container Docker applications.

### Auto-Installer:

### Windows

```bash
setup.ps1
```
### Linux

```bash
chmod +x setup.sh
./setup.sh
```

### Manual Install:

### 1. Clone the Repository
Clone this repository to your local machine:

```bash
git clone https://github.com/Tahl0s/jigsaw-unified-deployment-engine.git
cd /jigsaw-unified-deployment-engine
```

### 2. Build and Run the Application
You can use Docker Compose to build and run the application:

```bash
docker-compose up --build
```

This command will:
- Build the Docker images defined in the `Dockerfile`.
- Start the services (Flask app, Nginx, etc.) as defined in the `docker-compose.yml` file.

### 3. Environment Variables
You may need to adjust the environment variables for the Flask app or add any secret keys for MFA or OAuth integrations in the `.env` file.

### 4. Access the Application
Once everything is up and running, access the application via your browser:

- **Flask App**: `http://localhost:5000`
- **Nginx (Proxy)**: `http://localhost:80`

### 5. Updating the Application
Whenever you push updates to the GitHub repository, the application will automatically pull the latest code during the CI/CD deployment process. Alternatively, you can manually rebuild the containers with:

```bash
docker-compose down
docker-compose up --build
```

## Contributing
Feel free to contribute to this project by submitting issues, pull requests, or suggestions. It’s an open-source initiative, and your input is highly appreciated!

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
