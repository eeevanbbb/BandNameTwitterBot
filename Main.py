import argparse
import requests
import sys
import time

import twitter
import schedule

#Prepend time to all log output (http://stackoverflow.com/questions/4883789/adding-a-datetime-stamp-to-python-print)
old_out = sys.stdout
class new_out:
    nl = True

    def write(self, x):
        """Write function overloaded."""
        if x == '\n':
            old_out.write(x)
            self.nl = True
        elif self.nl:
            old_out.write('[%s] %s' % (time.ctime(), x))
            self.nl = False
        else:
            old_out.write(x)
sys.stdout = new_out()

class Tweeter(object):
    def __init__(self, config_file, generator):
        self.config_api(config_file)
        self.generator = generator

    def config_api(self, config_file):
        twitter_keys = {}
        try:
            with open(config_file) as f:
                for line in f:
                    name, var = line.split('=')
                    twitter_keys[name.strip()] = var.strip()
        except IOError as e:
            sys.exit('Could not find twitter config file at: ' + twitter_file + str(e))

        consumer_key = twitter_keys.get('consumer_key')
        consumer_secret = twitter_keys.get('consumer_secret')
        access_key = twitter_keys.get('access_key')
        access_secret = twitter_keys.get('access_secret')

        if consumer_key == None:
            sys.exit('No consumer_key found in: ' + twitter_file)
        elif consumer_secret == None:
            sys.exit('No consumer_secret found in: ' + twitter_file)
        elif access_key == None:
            sys.exit('No access_key found in: ' + twitter_file)
        elif access_secret == None:
            sys.exit('No access_secret found in: ' + twitter_file)
        else:
            self.twitter_api = twitter.Api(consumer_key=consumer_key,
                                           consumer_secret=consumer_secret,
                                           access_token_key=access_key,
                                           access_token_secret=access_secret)
        try:
            self.twitter_user = self.twitter_api.VerifyCredentials()
        except twitter.TwitterError as e:
            sys.exit('Could not verify twitter credentials.' + str(e))

        if self.twitter_user == None:
            sys.exit('Could not verify twitter credentials.')
        else:
            print('Twitter credentials verified successfully.')

    def tweet(self):
        tweet_text = self.generator.new_tweet()
        if tweet_text:
            try:
                self.twitter_api.PostUpdate(tweet_text)
                print('Tweeting: "%s"' % tweet_text)
            except TwitterError as e:
                print('WARNING: Unable to tweet: "' + tweet + '"' + str(e))
        else:
            print('WARNING: Generator failed to generate tweet text.')

    def schedule_hourly(self):
        schedule.every().hour.do(self.tweet)
        
    def begin_loop(self):
        while True:
            schedule.run_pending()
            time.sleep(10)

class BandNameGenerator(object):
    def new_tweet(self):
        r = requests.get('http://bands.evanb.io/band_name')
        response = r.json()
        if "name" in response:
            return response["name"]
        else:
            print('WARNING: Failed to get band name.')
            return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the bot.')
    parser.add_argument('--twitter', dest='twitter_file', type=str, default='twitter_config.txt', help='The file containing the Twitter keys, one per line with the format key_name=key_value (default: config/twitter.txt)')
    args = parser.parse_args()

    generator = BandNameGenerator()
    tweeter = Tweeter(args.twitter_file, generator)
    tweeter.schedule_hourly()

    tweeter.begin_loop()


