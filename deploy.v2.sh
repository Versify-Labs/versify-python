# This script can be called from the command line to deploy the services to the
# server. It is also called by the deploy.sh script in the root of the project.

# Example: sh deploy.sh automation dev
# Example: sh deploy.sh automation dev AutomationService-RunTask

# Get the deployment arguments
SERVICE_NAME=$1
STAGE=$2
FUNCTION_NAME=$3

# Get the locations of necessary files
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_DIR=$DIR/vongo
SERVICE_DIR=$DIR/services/$SERVICE_NAME-service

# Lock the pipenv and copy the requirements to the service
echo "Copying requirements to $SERVICE_DIR"
cd $APP_DIR
pipenv requirements > requirements.txt
cp requirements.txt $SERVICE_DIR/requirements.txt
cd $DIR

# Copy the app directory to the service
echo "Copying app to $SERVICE_DIR"
cp -r $APP_DIR/app $SERVICE_DIR/app
cd $DIR

# Deploy the service
cd $SERVICE_DIR
if [ "$FUNCTION_NAME" ]
then
    echo "Deploying function $FUNCTION_NAME to stage $STAGE"
    sls deploy function -f $FUNCTION_NAME
else
    echo "Deploying $SERVICE_NAME to $STAGE"
    sls deploy --stage $STAGE
fi

# Remove the app directory from the service
echo "Removing app from $SERVICE_DIR"
rm -rf $SERVICE_DIR/app

# Return to the original directory
cd $DIR