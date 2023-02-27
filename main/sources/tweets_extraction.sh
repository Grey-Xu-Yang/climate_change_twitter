#!/bin/bash
pip install --upgrade twarc
twarc2 configure
twarc2 hydrate ./tweet_ids_random.txt tweets_hydrated.json
