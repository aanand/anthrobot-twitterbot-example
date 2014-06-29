class Config(object):
    action_articles = ["your", "my"]
    action_verbs = ["is", "just"]

    characteristic_verbs = ["is"]
    characteristic_adverbs = ["so", "really"]

    @property
    def nouns(self):
        raise Exception("Config subclass must implement `nouns'")

    def action_seeds(self):
        return [
            " ".join([a, n, v]).strip()
            for a in self.action_articles
            for n in self.nouns
            for v in self.action_verbs
        ]

    def characteristic_seeds(self):
        return [
            " ".join([n, v, av]).strip()
            for n in self.nouns
            for v in self.characteristic_verbs
            for av in self.characteristic_adverbs
        ]

    def reject_tweet(self, tweet):
        return False
