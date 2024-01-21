#!/bin/bash

VOLUME_NAME="api_assignment_postgres_data"

echo "Make sure docker is stopped before restoring."

echo "Please enter the backup name:"
read BACKUP_NAME

docker run --rm -v $VOLUME_NAME:/var/lib/postgresql/data -v $(pwd)/backup:/backup alpine sh -c "cd /var/lib/postgresql/data/ && tar xvf /backup/$BACKUP_NAME"

echo "Restore completed."
