#!/usr/bin/env python2
# -*- coding: utf-8 -*- #

from twitterbot import TwitterBot

from anthrobot import config, actions, characteristics

from extensions.sql_storage import SQLStorage

import arrow

import random
import os
import logging
import re


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
        self.config['tweet_interval_range'] = (1*60, 3*60*60)

        # only reply to tweets that specifically mention the bot
        self.config['reply_direct_mention_only'] = False

        # only include bot followers (and original tweeter) in @-replies
        self.config['reply_followers_only'] = False

        # fav any tweets that mention this bot?
        self.config['autofav_mentions'] = False

        # fav any tweets containing these keywords?
        self.config['autofav_keywords'] = []

        # follow back all followers?
        self.config['autofollow'] = False

        # ignore home timeline tweets which mention other accounts?
        self.config['ignore_timeline_mentions'] = False

        # max number of times to reply to someone within the moving window
        self.config['reply_threshold'] = 5

        # length of the moving window, in seconds
        self.config['recent_replies_window'] = 20*60

        # regex to check if we should reply to a timeline tweet
        self.config['timeline_pattern'] = r'\bbutts?\b'

        # probability of replying to a matching timeline tweet
        self.config['timeline_reply_probability'] = float(os.environ.get('TIMELINE_REPLY_PROBABILITY', '1.0'))

        # probability of tweeting an action, rather than a characteristic
        self.config['action_probability'] = float(os.environ.get('ACTION_PROBABILITY', '0.8'))

        self.config['silent_mode'] = (int(os.environ.get('SILENT_MODE', '0')) != 0)

    def on_scheduled_tweet(self):
        text = self.generate_tweet(max_len=140)

        if self._is_silent():
            self.log("Silent mode is on. Would've tweeted: {}".format(text))
            return

        self.post_tweet(text)

    def on_mention(self, tweet, prefix):
        if not self.check_reply_threshold(tweet, prefix):
            return

        self.reply_to_tweet(tweet, prefix)

    def on_timeline(self, tweet, prefix):
        if not re.search(self.config['timeline_pattern'], tweet.text, flags=re.IGNORECASE):
            return

        if not self.check_reply_threshold(tweet, prefix):
            return

        if random.random() > self.config['timeline_reply_probability']:
            self.log("Failed dice roll. Not responding to {}".format(self._tweet_url(tweet)))
            return

        self.reply_to_tweet(tweet, prefix)

    def reply_to_tweet(self, tweet, prefix):
        prefix = prefix + ' '
        text = prefix + self.generate_tweet(max_len=140-len(prefix))

        if self._is_silent():
            self.log("Silent mode is on. Would've responded to {} with: {}".format(self._tweet_url(tweet), text))
        else:
            self.post_tweet(text, reply_to=tweet)

        self.update_reply_threshold(tweet, prefix)

    def _is_silent(self):
        return self.config['silent_mode']

    def check_reply_threshold(self, tweet, prefix):
        self.trim_recent_replies()
        screen_names = self.get_screen_names(prefix)
        over_threshold = [sn for sn in screen_names if self.over_reply_threshold(sn)]

        if len(over_threshold) > 0:
            self.log("Over reply threshold for {}. Not responding to {}".format(", ".join(over_threshold), self._tweet_url(tweet)))
            return False

        return True

    def over_reply_threshold(self, screen_name):
        replies = [r for r in self.recent_replies() if screen_name in r['screen_names']]
        return len(replies) >= self.config['reply_threshold']

    def update_reply_threshold(self, tweet, prefix):
        screen_names = self.get_screen_names(prefix)

        self.recent_replies().append({
            'created_at': arrow.utcnow(),
            'screen_names': screen_names,
        })

        self.log("Updated recent_replies: len = {}".format(len(self.recent_replies())))

    def get_screen_names(self, prefix):
        return [sn.replace('@', '') for sn in prefix.split()]

    def trim_recent_replies(self):
        len_before = len(self.recent_replies())
        now = arrow.utcnow()
        self.state['recent_replies'] = [
            r for r in self.recent_replies()
            if (now - r['created_at']).seconds < self.config['recent_replies_window']
        ]
        self.log("Trimmed recent_replies: {} -> {}".format(len_before, len(self.recent_replies())))

    def recent_replies(self):
        if 'recent_replies' not in self.state:
            self.state['recent_replies'] = []
        return self.state['recent_replies']

    def generate_tweet(self, max_len):
        cfg = Butt()
        candidates = self.generate_candidates(cfg)
        candidates = [c for c in candidates if len(c) <= max_len]

        if len(candidates) == 0:
            raise Exception("No suitable candidates were found")

        return random.choice(candidates)

    def generate_candidates(self, cfg):
        if random.random() < self.config['action_probability']:
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
