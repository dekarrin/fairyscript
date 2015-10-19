#!/bin/bash

[ "$TRAVIS_BRANCH" != "dev" ] && return 0

git config --global user.email "builds@travis-ci.com"
git config --global user.name "Travis CI"
short_commit=$(git rev-parse --short HEAD)

# get entire repo
repo_temp="$(mktemp -d)"

GIT_MERGE_AUTOEDIT=no
git clone "https://github.com/$TRAVIS_REPO_SLUG" "$repo_temp"
cd "$repo_temp"
git checkout dev
git checkout master
git merge dev
git push -q "https://$GH_TOKEN@github.com/$TRAVIS_REPO_SLUG.git" master