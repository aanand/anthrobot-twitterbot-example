import unittest
from anthrobot import actions
from anthrobot.config import Config


class Cat(Config):
    nouns = ["cat", "kitty"]


class ActionsTest(unittest.TestCase):
    tweets = [
        u'RT @lonelypetal: may be triggering but my cat is kissing my scars http://t.co/s58Zm2wCWJ',
        u"RT @idarahim_: \u201c@lonelypetal: may be triggering but my cat is kissing my scars http://t.co/RfFFkOYzti\u201d reasons why i'd date a cat",
        u'RT @lonelypetal: may be triggering but my cat is kissing my scars http://t.co/s58Zm2wCWJ',
        u'My cat just gave me a head massage\U0001f44c\U0001f60f #amazing',
        u"RT @MYSADCAT: My cat is sad because he only came here to do 2 things: get sad &amp; eat some Wanky Veg, &amp; he's almost out of Wanky Veg. http://\u2026",
        u"RT @MYSADCAT: My cat is sad because he only came here to do 2 things: get sad &amp; eat some Wanky Veg, &amp; he's almost out of Wanky Veg. http://\u2026",
        u'my cat is crazy!',
        u'@jongdaecin yES ONIICHAN SHOULD BE!1!1 oniichan treat me some pizza jsy nae? giggles ~*~* screams but your kitty is the cutest-',
        u'@Char_Stokely sweet dreams,   whats your Pussies name ?  sweetie. My Cat is Skye .   xx',
        u'RT @lonelypetal: may be triggering but my cat is kissing my scars http://t.co/s58Zm2wCWJ',
        u'think that my cat is being pathetic for going on hunger strike.. just because my mums left him to go on holiday. #prayforalfie',
        u'My kitty is awesome',
        u'RT @MYSADCAT: My cat is sad because he spoke to a nice ladycat today &amp; only realised later his tongue had been out the whole time. http://t\u2026',
        u'RT @MYSADCAT: My cat is sad because his love for you will still be strong after the boys of summer have gone. http://t.co/fjKt1uCg0R',
        u'My cat is sleeping next to me',
        u'My cat is such a little shit he climbed onto my head turned around then bit my eat',
        u"My cat is KNOCKING. Meowing. Scratching the carpet. It huuuurts :'(",
        u'My cat is knocking at my door. My heart is breaking.',
        u'@verepeer aww - your kitty is lovely! photo stalking ;p also a boy?',
        u'El si que sabe... #instaphoto #my #cat #is #sleeping #very #nice http://t.co/U8vpyojEzK',
        u"My cat is yowling downstairs non-stop, my ability to hear from that far away implies I'm not deaf.",
        u'No YOUR cat is spoiled... and that is definitely NOT Buxton mineral water she is drinking. http://t.co/t18P15bci9',
        u'Do you think your cat is the next Picasso, Van Gogh, Keith Harring?  Then you will love this app available on... http://t.co/cI9Tpu6XHB',
        u'Would have still been sleep but my cat is an attention whore n woke me up for nothing this morning. Rude bastard.',
        u'i miss you my kitty just chattin with the group or they will hang me lol :D',
        u'My cat is so fat, lmao.',
        u"RT @TheCiscoKidder: My cat is like a tiny politician. Every morning he launches a huge campaign to get fed and he's a complete asshole.",
    ]

    def setUp(self):
        self.config = Cat()

    def test_generate(self):
        generated_actions = actions.generate(self.config, self.tweets)
        self.assertEqual(set(generated_actions), set([
            u'knocks at ur door',
            u'is pathetic for going on hunger strike',
            u'yowls downstairs non',
            u'knocks',
            u'kisses ur scars',
            u'sleeps next to u'
        ]))

    def test_going_to(self):
        generated_actions = actions.generate(self.config, [
            u'my cat is going to kill me',
            u'my cat is going to the doctor',
        ])
        self.assertEqual(set(generated_actions), set([
            u'kills u',
            u'goes to the doctor',
        ]))
