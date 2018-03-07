import json
import sys, operator

def loadJsonTwitter(filename):
    tweets = {}
    with open(filename, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            if tweet['from_user_id'] not in tweets:
                tweets[tweet['from_user_id']] = []
            tweets[tweet['from_user_id']].append(int(tweet['id']))
    return tweets

def loadClusterResults(filename):
    clusters = {} # tweet_id:cluster_id
    with open(filename, 'r') as f:
        for line in f:
            cluster_id, tweet_ids = line.strip().split(':')
            for tweet_id in tweet_ids.split(','):
                clusters[int(tweet_id)] = int(cluster_id)
    return clusters

def writeSensMatrixFile(tweets, clusters, filename):
    f = open(filename, 'w')
    for user_id in tweets:
        measured_variables = []
        for tweet_id in tweets[user_id]:
            measured_variables.append(clusters[tweet_id])
        measured_variables.sort()
        for cluster in measured_variables:
            data = str(user_id) + ',' + str(cluster) + '\n'
            f.write(data)
    f.close()