#!/bin/bash

# This script rebases dev on the latest master and then merges dev to master.
# The new master is then pushed to GitHub.
#
# Master and dev will be kept even with each other, assuming that dev diverges
# only by changes that can be fast-forwarded (which should be the case if
# master is never committed to directly).

[ "$TRAVIS_BRANCH" != "dev" ] && return 0

git config --global user.email "builds@travis-ci.com"
git config --global user.name "Travis CI"
short_commit=$(git rev-parse --short HEAD)

# get entire repo
repo_temp="$(mktemp -d)"

export GIT_MERGE_AUTOEDIT=no
git clone "https://github.com/$TRAVIS_REPO_SLUG" "$repo_temp"
cd "$repo_temp"
git checkout master
git checkout dev
git rebase master
git checkout master
git merge dev
git push -q "https://$GH_TOKEN@github.com/$TRAVIS_REPO_SLUG.git" master
