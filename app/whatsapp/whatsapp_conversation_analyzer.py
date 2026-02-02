import datetime
import os
import re
from typing import List

from app.whatsapp_message import WhatsAppMessage

URL_REGEX = '(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+'

REGEX_PATTERN_FILE = "whatsapp_message_regex.txt"
REGEX_PATTERN_MEMBER_TIMESTAMP = "datetime"
REGEX_PATTERN_MEMBER_MESSAGE = "message"
REGEX_PATTERN_MEMBER_NAME = "name"

WHATSAPP_DATE_PATTERN = '%x, %H:%M'


class WhatsAppConversationAnalyzer:

    @staticmethod
    def parse_datetime(string_representation: str) -> datetime:
        return datetime.datetime.strptime(string_representation, WHATSAPP_DATE_PATTERN)

    @staticmethod
    def get_file_content(path: str) -> str:
        data = ""

        with open(path, 'r', encoding='utf8', errors='ignore') as file:
            data = file.read()

        return data;

    @staticmethod
    def get_backlisted_words(blocklist_word_file: str) -> List[str]:
        # create absolute file path to ensure that file is loaded from same folder as this script
        absolute_path = WhatsAppConversationAnalyzer.get_absolute_path(blocklist_word_file)
        words = WhatsAppConversationAnalyzer.get_file_content(absolute_path)
        return WhatsAppConversationAnalyzer.tokenize(words)

    @staticmethod
    def get_absolute_path(path: str) -> str:
        script_dir = os.path.dirname(__file__)
        return os.path.join(script_dir, path)

    @staticmethod
    def remove_urls(text: str) -> str:
        urls = re.findall(URL_REGEX, text)

        for url in urls:
            text = text.replace(url, "")

        return text

    @staticmethod
    def backup_text_to_messages(path: str) -> List[WhatsAppMessage]:
        regex_pattern = WhatsAppConversationAnalyzer.get_file_content(REGEX_PATTERN_FILE)

        # load backup file
        backup_text = WhatsAppConversationAnalyzer.get_file_content(path)

        messages = []
        pattern = re.compile(regex_pattern, flags=re.MULTILINE | re.VERBOSE)

        for match in pattern.finditer(backup_text):
            name = match.groupdict().get(REGEX_PATTERN_MEMBER_NAME)
            message = match.groupdict().get(REGEX_PATTERN_MEMBER_MESSAGE)
            timestamp_string = match.groupdict().get(REGEX_PATTERN_MEMBER_TIMESTAMP)
            timestamp = WhatsAppConversationAnalyzer.parse_datetime(timestamp_string)

            messages.append(WhatsAppMessage(timestamp, name, message))

        return messages

    @staticmethod
    def tokenize(words: str) -> List[str]:
        return re.sub("[^\w]", " ", words).split()

    @staticmethod
    def get_word_count(whatsapp_messages: List[WhatsAppMessage]) -> []:
        word_frequence = {}

        for whatsapp_messages in whatsapp_messages:
            # remove media content
            temp_message = whatsapp_messages.message.replace("<Media omitted>", "")
            # remove links
            temp_message = WhatsAppConversationAnalyzer.remove_urls(temp_message)
            # clean upper and lower case
            temp_message = temp_message.lower()
            # tokenize
            words = WhatsAppConversationAnalyzer.tokenize(temp_message)

            blacklisted_words = WhatsAppConversationAnalyzer.get_backlisted_words()

            for word in words:
                # omit words with a low number of characters
                # omit to long word
                # (45 characters is the longest word in a major dictionary
                # https://en.wikipedia.org/wiki/Longest_word_in_English)
                word_length = len(word)
                if word_length <= 2 or word_length > 45:
                    continue

                if word in blacklisted_words:
                    continue

                if word not in word_frequence:
                    word_frequence[word] = 1
                else:
                    word_frequence[word] += 1

        sorted_by_value = sorted(word_frequence.items(), key=lambda kv: kv[1], reverse=True)

        return sorted_by_value

    @staticmethod
    def get_top_words(path: str) -> []:
        messages = WhatsAppConversationAnalyzer.backup_text_to_messages(path)
        return WhatsAppConversationAnalyzer.get_word_count(messages)
