#!/usr/bin/env python2
# -*- coding: utf-8 -*- #

from twitterbot import TwitterBot

from anthrobot import config, actions

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
        self.config['reply_direct_mention_only'] = True

        # only include bot followers (and original tweeter) in @-replies
        self.config['reply_followers_only'] = True

        # fav any tweets that mention this bot?
        self.config['autofav_mentions'] = False

        # fav any tweets containing these keywords?
        self.config['autofav_keywords'] = []

        # follow back all followers?
        self.config['autofollow'] = False

    def on_scheduled_tweet(self):
        self.post_tweet(self._generate_action(max_len=140))

    def on_mention(self, tweet, prefix):
        prefix = prefix + ' '
        text = prefix + self._generate_action(max_len=140-len(prefix))
        self.post_tweet(text, reply_to=tweet)

    def on_timeline(self, tweet, prefix):
        pass

    def _generate_action(self, max_len):
        cfg = Butt()

        q = ' OR '.join('"%s"' % s for s in cfg.action_seeds())
        tweets = self.api.search(q=q, count=100, result_type='recent')

        candidates = actions.generate(cfg, [t.text for t in tweets])
        if len(candidates) == 0:
            raise Exception("No actions were found")

        for _ in range(5):
            text = '*%s*' % random.choice(candidates)
            if len(text) <= max_len:
                return text

        raise Exception("Failed to generate a short enough tweet")

if __name__ == '__main__':
    stderr = logging.StreamHandler()
    stderr.setLevel(logging.DEBUG)
    stderr.setFormatter(logging.Formatter(fmt='%(levelname)8s: %(message)s'))

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(stderr)

    bot = YourButt()
    bot.run()
