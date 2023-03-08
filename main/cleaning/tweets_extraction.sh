#!/bin/bash
# code contribution - Ridhi
# This shell script hydrates tweets using twarc library and a set of unique tweet ids
pip install --upgrade twarc
twarc2 configure
twarc2 hydrate ./tweet_ids_random.txt hydrated_tweets.json