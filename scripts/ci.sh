#!/usr/bin/env bash

clear
# project_slug, takes the form: <project_type>/<org_name>/<repo_name>

projectType='github'
orgName='hasii2011'
repoName='pyut'

project_slug="${projectType}/${orgName}/${repoName}"

echo "${project_slug}"
# curl -u ${CIRCLECI_TOKEN}: https://circleci.com/api/v2/me

curl -u ${CIRCLECI_TOKEN}: -X POST --header "Content-Type: application/json" -d '{
  "branch": "master"
}' https://circleci.com/api/v2/project/${project_slug}/pipeline
