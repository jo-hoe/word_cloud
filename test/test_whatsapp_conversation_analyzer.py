import unittest

from app.whatsapp_conversation_analyzer import WhatsAppConversationAnalyzer
from app.whatsapp_message import WhatsAppMessage

TEST_BACKUP_FILE_TXT = "test_backup_file.txt"


class TestWhatsAppConversationAnalyzer(unittest.TestCase):

    def test_get_file_content(self):
        data = WhatsAppConversationAnalyzer.get_file_content(TEST_BACKUP_FILE_TXT)

        self.assertGreater(len(data), 0)

    def test_backup_text_to_messages(self):
        messages = WhatsAppConversationAnalyzer.backup_text_to_messages(TEST_BACKUP_FILE_TXT)

        self.assertEqual(len(messages), 5)

    def test_backup_text_to_messages(self):
        text_with_url = "https://www.in.com/p/Bq/?utm=i&i=1\n text https://goo.gl/m/8"
        text = WhatsAppConversationAnalyzer.remove_urls(text_with_url)

        self.assertTrue("http" not in text)

    def test_get_word_count(self):
        messages = []
        messages.append(WhatsAppMessage(None, "", "🥯"))
        messages.append(WhatsAppMessage(None, "", "hello"))
        messages.append(WhatsAppMessage(None, "", "Hello World"))
        messages.append(WhatsAppMessage(None, "", "HelloWorld"))

        message_frequence = WhatsAppConversationAnalyzer.get_word_count(messages)

        self.assertEqual(len(message_frequence), 3)

    def test_get_top_words(self):
        word_fequence = WhatsAppConversationAnalyzer.get_top_words(TEST_BACKUP_FILE_TXT)

        self.assertEqual("often", word_fequence[0][0])


if __name__ == '__main__':
    unittest.main()
