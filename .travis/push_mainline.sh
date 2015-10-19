#!/bin/bash

[ "$TRAVIS_BRANCH" != "dev" ] && return 0

short_commit=$(git rev-parse --short HEAD)
git config --global user.email "builds@travis-ci.com"
git config --global user.name "Travis CI"
git fetch
git reset --hard
git checkout master --force
git merge --no-ff -m "Merged commit $short_commit of dev into master after successful build" dev
git push -q $GH_TOKEN@github.com:$TRAVIS_REPO_SLUG.git master