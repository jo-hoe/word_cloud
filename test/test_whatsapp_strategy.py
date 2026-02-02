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

    def test_extract_texts_removes_media_placeholder(self):
        strategy = WhatsAppStrategy()
        texts = strategy.extract_texts(TEST_BACKUP_FILE_TXT)
        for t in texts:
            self.assertNotIn("<Media omitted>", t)

    def test_word_counts_from_texts(self):
        texts = ["🥯", "hello", "Hello World", "HelloWorld"]
        counts = word_counts_from_texts(
            texts=texts,
            min_word_length=3,
            blocklist_words=set(),
            blocklist_regex=[],
        )
        self.assertEqual(len(counts), 3)

    def test_top_word_from_backup(self):
        strategy = WhatsAppStrategy()
        texts = strategy.extract_texts(TEST_BACKUP_FILE_TXT)
        counts = word_counts_from_texts(
            texts=texts,
            min_word_length=3,
            blocklist_words=set(),
            blocklist_regex=[],
        )
        top_word = sorted(counts.items(), key=lambda x: x[1], reverse=True)[0][0]
        self.assertEqual("often", top_word)


if __name__ == '__main__':
    unittest.main()