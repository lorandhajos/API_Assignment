#!/bin/bash

VOLUME_NAME="api_assignment_postgres_data"
BACKUP_NAME=$(date +"%Y%m%d-%H%M%S")

docker run --rm -v $VOLUME_NAME:/data -v $(pwd)/backup:/backup alpine tar czf /backup/$BACKUP_NAME.tar.gz -C /data .

echo "Backup completed. Archive stored in backup/$BACKUP_NAME.tar.gz"
