import unittest

from app.strategies.whatsapp_strategy import WhatsAppStrategy
from app.analyzer import word_counts_from_texts

TEST_BACKUP_FILE_TXT = "test_backup_file.txt"


class TestWhatsAppStrategy(unittest.TestCase):
    def test_get_file_content(self):
        data = WhatsAppStrategy.get_file_content(TEST_BACKUP_FILE_TXT)
        self.assertGreater(len(data), 0)

    def test_extract_texts(self):
        strategy = WhatsAppStrategy()
        texts = strategy.extract_texts(TEST_BACKUP_FILE_TXT)
        self.assertEqual(len(texts), 5)

    def test_remove_urls_removes_http(self):
        text_with_url = "https://www.in.com/p/Bq/?utm=i&i=1\n text https://goo.gl/m/8"
        text = WhatsAppStrategy.remove_urls(text_with_url)
        self.assertTrue("http" not in text)

    def test_emoji_in_text(self):
        text_with_emoji = "Hello 🥯 world!"
        strategy = WhatsAppStrategy()
        text = strategy.extract_texts_from_string(text_with_emoji)
        self.assertIn("🥯", text)

    def test_emoji_does_not_count_against_character_limit(self):
        text_with_emoji = "Hi 🥯"
        strategy = WhatsAppStrategy()
        texts = [text_with_emoji]
        counts = word_counts_from_texts(
            texts=texts,
            min_word_length=2,
            blocklist_words=set(),
            blocklist_regex=[],
        )
        self.assertIn("hi", counts)
        self.assertIn("🥯", counts)

    def test_extract_texts_removes_media_placeholder(self):
        strategy = WhatsAppStrategy()
        texts = strategy.extract_texts(TEST_BACKUP_FILE_TXT)
        for t in texts:
            self.assertNotIn("<Media omitted>", t)

    def test_word_counts_from_texts(self):
        texts = ["hi", "hello", "Hello World", "HelloWorld"]
        counts = word_counts_from_texts(
            texts=texts,
            min_word_length=4,
            blocklist_words=set(),
            blocklist_regex=[],
        )

        expected_counts = {
            "hello": 2,
            "world": 1,
            "helloworld": 1,
        }

        self.assertEqual(counts, expected_counts,
                         f"Expected {expected_counts}, got {counts}")

    def test_top_word_from_backup(self):
        strategy = WhatsAppStrategy()
        texts = strategy.extract_texts(TEST_BACKUP_FILE_TXT)
        counts = word_counts_from_texts(
            texts=texts,
            min_word_length=3,
            blocklist_words=set(),
            blocklist_regex=[],
        )
        top_word = sorted(
            counts.items(), key=lambda x: x[1], reverse=True)[0][0]
        self.assertEqual("often", top_word)


if __name__ == '__main__':
    unittest.main()
