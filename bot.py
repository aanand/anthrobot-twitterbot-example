#!/usr/bin/env python2
# -*- coding: utf-8 -*- #

from twitterbot import TwitterBot

from anthrobot import config, actions, characteristics

from extensions.sql_storage import SQLStorage

import random
import os
import logging


class Butt(config.Config):
    nouns = ["butt", "ass", "bum", "arse"]


class YourButt(TwitterBot):
    def bot_init(self):
        self.config['storage'] = SQLStorage(os.environ['DATABASE_URL'])

        self.config['api_key'] = os.environ['TWITTER_CONSUMER_KEY']
        self.config['api_secret'] = os.environ['TWITTER_CONSUMER_SECRET']
        self.config['access_key'] = os.environ['TWITTER_ACCESS_TOKEN']
        self.config['access_secret'] = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

        # use this to define a (min, max) random range of how often to tweet
        # e.g., self.config['tweet_interval_range'] = (5*60, 10*60) # tweets every 5-10 minutes
        self.config['tweet_interval_range'] = (10*60, 60*60)

        # only reply to tweets that specifically mention the bot
        self.config['reply_direct_mention_only'] = False

        # only include bot followers (and original tweeter) in @-replies
        self.config['reply_followers_only'] = True

        # fav any tweets that mention this bot?
        self.config['autofav_mentions'] = False

        # fav any tweets containing these keywords?
        self.config['autofav_keywords'] = []

        # follow back all followers?
        self.config['autofollow'] = False

    def on_scheduled_tweet(self):
        text = self.generate_tweet(max_len=140)

        if self._is_silent():
            self.log("Silent mode is on. Would've tweeted: {}".format(text))
            return

        self.post_tweet()

    def on_mention(self, tweet, prefix):
        prefix = prefix + ' '
        text = prefix + self.generate_tweet(max_len=140-len(prefix))

        if self._is_silent():
            self.log("Silent mode is on. Would've responded to {} with: {}".format(self._tweet_url(tweet), text))
            return

        self.post_tweet(text, reply_to=tweet)

    def on_timeline(self, tweet, prefix):
        pass

    def _is_silent(self):
        return int(os.environ.get('SILENT_MODE', '0')) != 0

    def generate_tweet(self, max_len):
        cfg = Butt()
        candidates = self.generate_candidates(cfg)
        candidates = [c for c in candidates if len(c) <= max_len]

        if len(candidates) == 0:
            raise Exception("No suitable candidates were found")

        return random.choice(candidates)

    def generate_candidates(self, cfg):
        if random.random() < float(os.environ.get('ACTION_PROBABILITY', '0.8')):
            tweets = self.search(cfg.action_seeds())
            generated_actions = actions.generate(cfg, [t.text for t in tweets])
            return ['*%s*' % a for a in generated_actions]
        else:
            tweets = self.search(cfg.characteristic_seeds())
            generated_characteristics = characteristics.generate(cfg, [t.text for t in tweets])
            return ['Im %s' % a for a in generated_characteristics]

    def search(self, seeds):
        query = ' OR '.join('"%s"' % s for s in seeds)
        return self.api.search(query, count=100, result_type='recent')

if __name__ == '__main__':
    stderr = logging.StreamHandler()
    stderr.setLevel(logging.DEBUG)
    stderr.setFormatter(logging.Formatter(fmt='%(levelname)8s: %(message)s'))

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(stderr)

    bot = YourButt()
    bot.run()
