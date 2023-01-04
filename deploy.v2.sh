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
VERSIFY_DIR=$DIR/vongo/app
SERVICE_DIR=$DIR/services/$SERVICE_NAME-service
SERVICE_VERSIFY_DIR=$SERVICE_DIR/app

echo "Copying versify module to $SERVICE_VERSIFY_DIR"
cp -r $VERSIFY_DIR $SERVICE_VERSIFY_DIR
cd $SERVICE_DIR

if [ "$FUNCTION_NAME" ]
then
    echo "Deploying function $FUNCTION_NAME to stage $STAGE"
    sls deploy function -f $FUNCTION_NAME
else
    echo "Deploying $SERVICE_NAME to $STAGE"
    sls deploy --stage $STAGE
fi

# Remove the versify module from the service
rm -rf $SERVICE_VERSIFY_DIR

# Return to the original directory
cd $DIR