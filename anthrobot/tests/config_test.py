import unittest
from anthrobot.config import Config


class ConfigTest(unittest.TestCase):
    def test_action_seeds(self):
        self.assertEqual(Cat().action_seeds(), [
            "your cat is",
            "your cat just",
            "your kitty is",
            "your kitty just",
            "my cat is",
            "my cat just",
            "my kitty is",
            "my kitty just",
        ])

    def test_characteristic_seeds(self):
        self.assertEqual(Cat().characteristic_seeds(), [
            "cat is so",
            "cat is really",
            "kitty is so",
            "kitty is really",
        ])


class Cat(Config):
    nouns = ["cat", "kitty"]
