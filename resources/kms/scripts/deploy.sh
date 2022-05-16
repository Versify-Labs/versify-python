# Apply pending updates
sudo yum update

# Search for Docker package
sudo yum search docker

# Get version information
sudo yum info docker

# Install docker, run
sudo yum install docker

# Enable docker service at AMI boot time
sudo systemctl enable docker.service

# Start the Docker service
sudo systemctl start docker.service

# Grant the correct permissions
sudo chmod 666 /var/run/docker.sock

# Pull the tatum kms image
docker pull tatumio/tatum-kms

# Navigate to the home directory
cd $HOME

# Create a .env file in the $HOME directory with the following parameters:
touch .env
nano .env
TATUM_API_KEY=XXXXX-YOUR-API-KEY
TATUM_KMS_PASSWORD=XXXXPASSWORD

# Map Volume: map your home folder to map docker volume to local storage. refer to docker volume mapping for more details https://docs.docker.com/storage/volumes/
docker run -it --env-file .env -v $HOME:/root/.tatumrc tatumio/tatum-kms --help

# Store the private key to an account
docker run -it --env-file .env -v $HOME:/root/.tatumrc tatumio/tatum-kms --testnet storemanagedprivatekey MATIC

# TEST MODE ONLY -> Take a look at the generated wallet
docker run -it --env-file .env -v $HOME:/root/.tatumrc tatumio/tatum-kms --testnet export

# Enable daemon mode
docker run -d --env-file .env -v $HOME:/root/.tatumrc tatumio/tatum-kms daemon --chain MATIC --testnet 

# TEST: Send MATIC to the new address

# TEST: Send an API request to the tatum API (via lambda function)