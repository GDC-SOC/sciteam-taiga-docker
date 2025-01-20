#!/bin/bash

# Update the system
echo "Updating the system..."
sudo apt update && sudo apt upgrade -y

# Install Docker
echo "Installing Docker..."
sudo apt install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker ubuntu

# Apply Docker group changes for the current session
echo "Applying Docker group changes..."
newgrp docker <<EOF

# Install Docker Compose
echo "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify Docker installation
echo "Verifying Docker installation..."
docker --version
docker-compose --version

# Install additional dependencies
echo "Installing additional dependencies..."
sudo apt install -y git curl jq

# Clone the Taiga repository
echo "Cloning the Taiga repository..."
if [ ! -d "~/taiga" ]; then
  git clone https://github.com/GDC-SOC/sciteam-taiga-docker.git ~/taiga
else
  echo "Taiga repository already exists, skipping clone."
fi
EOF

# Navigate to the repository directory
cd ~/taiga

# Group settings
newgrp docker

# Build the Taiga containers
# echo "Building Taiga Docker containers..."
# docker-compose build

# Notify the user
echo "Setup complete! Create .env file and then fun docker-compose build."