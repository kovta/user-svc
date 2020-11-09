#!/bin/bash

# Enables job control
set -m

# Enables error propagation
set -e

# Run the server and send it to the background
/entrypoint.sh couchbase-server &

# Check if couchbase server is up
check_db() {
  curl --silent http://127.0.0.1:8091/pools > /dev/null
  echo $?
}

# Variable used in echo
i=1
# Echo with
log() {
  echo "[$i] [$(date +"%T")] $@"
  i=`expr $i + 1`
}

# Wait until it's ready
until [[ $(check_db) = 0 ]]; do
  >&2 log "Waiting for Couchbase Server to be available ..."
  sleep 1
done

## Setup index and memory quota - Only needed for first startup
#log "$(date +"%T") Init cluster ........."
#couchbase-cli init-cluster -c 127.0.0.1 --cluster-username Administrator --cluster-password password \
#  --cluster-name userservice --cluster-ramsize 1024 --cluster-index-ramsize 512 --services data,index,query,fts \
#  --index-storage-setting default

couchbase-cli setting-cluster -c 127.0.0.1 -u Administrator -p password --cluster-username Administrator --cluster-password password \
  --cluster-name userservice --cluster-ramsize 1024 --cluster-index-ramsize 512 \

# Create the buckets - Only needed for first startup
#log "$(date +"%T") Create buckets ........."
#couchbase-cli bucket-create -c 127.0.0.1 --username Administrator --password password --bucket-type couchbase --bucket-ramsize 250 --bucket users
#couchbase-cli bucket-create -c 127.0.0.1 --username Administrator --password password --bucket-type couchbase --bucket-ramsize 250 --bucket users_test

# Create user
log "$(date +"%T") Create users ........."
couchbase-cli user-manage -c 127.0.0.1:8091 -u Administrator -p password --set --rbac-username sysadmin --rbac-password password \
 --rbac-name "sysadmin" --roles admin --auth-domain local
couchbase-cli user-manage -c 127.0.0.1:8091 -u Administrator -p password --set --rbac-username users --rbac-password password \
 --rbac-name "users" --roles bucket_full_access[*] --auth-domain local
couchbase-cli user-manage -c 127.0.0.1:8091 -u Administrator -p password --set --rbac-username users_test --rbac-password users_test_pass \
 --rbac-name "users" --roles bucket_full_access[*] --auth-domain local

# Need to wait until query service is ready to process N1QL queries
log "$(date +"%T") Waiting ........."
sleep 20

# Create users indexes
echo "$(date +"%T") Create users indexes ........."
cbq -u Administrator -p password -s "CREATE PRIMARY INDEX idx_primary ON \`users\`;"
cbq -u Administrator -p password -s "CREATE INDEX idx_type ON \`users\`(_type);"

cbq -u Administrator -p password -s "CREATE PRIMARY INDEX idx_primary ON \`users_test\`;"
cbq -u Administrator -p password -s "CREATE INDEX idx_type ON \`users_test\`(_type);"

fg 1