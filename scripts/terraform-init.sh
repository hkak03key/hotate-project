#!/bin/sh

terraform init -backend-config="bucket=`cat gcp_service_key.json | jq -r .project_id`-terraform"
