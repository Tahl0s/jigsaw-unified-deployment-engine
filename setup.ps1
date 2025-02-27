# Define the repository and folder path
$repoUrl = "https://github.com/Tahl0s/jigsaw-unified-deployment-engine.git"
$repoDir = "jigsaw-unified-deployment-engine"

# Check if the repo directory exists
if (-Not (Test-Path $repoDir)) {
    Write-Host "Cloning the repository..."
    git clone $repoUrl
} else {
    Write-Host "Repository already exists. Pulling latest changes..."
    Set-Location -Path $repoDir
    git pull
    Set-Location -Path ..
}

# Check if docker-compose.yml exists in the repo
if (-Not (Test-Path "$repoDir\docker-compose.yml")) {
    Write-Host "docker-compose.yml is missing in the repo!"
    exit 1
}

# Move into the repository folder
Set-Location -Path $repoDir

# Build and start the Docker containers
Write-Host "Starting Docker Compose..."
docker-compose up -d --build
