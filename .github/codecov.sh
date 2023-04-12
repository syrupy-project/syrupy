#!/bin/bash

# From https://github.com/decidim/decidim (AGPL-3.0)

EVENT_PAYLOAD_FILE=$1

PR_ID=`jq ".number // .check_run.pull_requests[0].number" $EVENT_PAYLOAD_FILE`
GIT_SHA=`jq -r ".pull_request.head.sha // .check_run.head_sha // .after" $EVENT_PAYLOAD_FILE`

if [ $PR_ID = "null" ]; then
    bash <(curl -s https://codecov.io/bash) -C $GIT_SHA -s $ARTIFACT_DIR
else
    bash <(curl -s https://codecov.io/bash) -C $GIT_SHA -P $PR_ID -s $ARTIFACT_DIR
fi
