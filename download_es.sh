#!/bin/bash

LIGHT_RED='\033[1;31m'
LIGHT_GREEN='\033[1;32m'
LIGHT_BLUE='\033[1;34m'
NO_COLOR='\033[0m'

# Create temporary folder
mkdir -p tmp

printf "${LIGHT_BLUE}Starting ElasticSearch download...\n${NO_COLOR}"
unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    *)          machine="UNKNOWN:${unameOut}"
esac

if [ $machine = "Linux" ] ; then
  # Download Elasticsearch archive
  wget -c -O tmp/elasticsearch.tar.gz https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.12.0-linux-x86_64.tar.gz
elif [ $machine = "Mac" ] ; then
  # Download Elasticsearch archive
  wget -c -O tmp/elasticsearch.tar.gz https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.12.0-darwin-x86_64.tar.gz
else
  printf "${LIGHT_REd}ERROR: Platform not supported${NO_COLOR}"
fi
printf "${LIGHT_GREEN}Elasticsearch download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting Elasticsearch archive extraction...\n${NO_COLOR}"
tar xf tmp/elasticsearch.tar.gz
mv elasticsearch-7.12.0 elasticsearch
printf "${LIGHT_GREEN}Elasticsearch archive extraction: DONE\n\n${NO_COLOR}"