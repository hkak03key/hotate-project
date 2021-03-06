#!/bin/bash

PJ_NAME=hotate-project
SA_NAME=deploy
BUCKET_NAME=$PJ_NAME-terraform

SA_FULLNAME=$SA_NAME@$PJ_NAME.iam.gserviceaccount.com

gsutil mb -p $PJ_NAME -l us-west1 gs://$BUCKET_NAME/

gcloud services enable iam.googleapis.com # 実行ユーザが所属するprojectのserviceを有効にする必要がある

gcloud iam service-accounts create $SA_NAME --display-name $SA_NAME --project $PJ_NAME
gcloud projects add-iam-policy-binding $PJ_NAME --member serviceAccount:$SA_FULLNAME --role roles/owner
gcloud iam service-accounts keys create `cd $(dirname $0) && pwd`/../terraform/gcp_service_key.json --iam-account $SA_FULLNAME --project $PJ_NAME

# cloudresourcemanager.googleapis.comは手動で有効にする必要がある
gcloud services enable cloudresourcemanager.googleapis.com --project $PJ_NAME
