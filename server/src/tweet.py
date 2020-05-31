
import json
import tweepy
from predict import predict


consumer_key = consumer_secret = access_token = access_token_secret = ""
with open('tweet_cred.json', "r") as f:
    data = json.load(f)
    print(data)

    consumer_key = data['consumer_key']
    consumer_secret = data['consumer_secret']
    access_token = data['access_token']
    access_token_secret = data['access_token_secret']
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def rate_tweet( status):
    tweetFetched = api.get_status(status,  tweet_mode='extended')

    tweet_json = tweetFetched._json

    user_name = tweetFetched.user.screen_name
    for key in tweet_json:
        pass
        #print(key)

    replies = []

    for tweet in tweepy.Cursor(api.search, q='to:{}'.format(user_name),since_id=tweet_json['id'], max_id=None, tweet_mode='extended').items(900):
        
        if hasattr(tweet, 'in_reply_to_status_id_str'):
            if (tweet.in_reply_to_status_id_str==tweet_json['id_str']):
                replies.append(tweet.full_text)
                #print(tweet.full_text)
            
            

    tweet_score = predict([tweetFetched.full_text], 1) 
    replies_score = predict(replies, tweet_score)
    replies_pure_score = predict(replies, 1, allow_print= False)
    print(replies)
    print(len(replies))
    print("tweet score: ", tweet_score)
    print("reply to tweet postivity rating: " + str(replies_score))
    print("reply postivity rating: " + str(replies_pure_score))

    return replies_pure_score

    
