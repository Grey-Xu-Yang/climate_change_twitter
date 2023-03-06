#!/bin/bash
# code contribution - Ridhi
pip install --upgrade twarc
twarc2 configure
twarc2 hydrate ./tweet_ids_random.txt hydrated_tweets.json