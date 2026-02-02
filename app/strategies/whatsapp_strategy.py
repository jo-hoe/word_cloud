import os
import re
import datetime
from typing import List
from app.strategies.base import InputSourceStrategy
from app.utils.file_utils import get_file_content as util_get_file_content, get_absolute_path as util_get_absolute_path


class WhatsAppMessage:
    def __init__(self, timestamp: datetime.datetime, username: str, message: str):
        self.timestamp = timestamp
        self.username = username
        self.message = message


class WhatsAppStrategy(InputSourceStrategy):
    # Embedded URL regex
    URL_REGEX = r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+"

    # Embedded content of app/whatsapp/whatsapp_message_regex.txt
    REGEX_PATTERN = r"""
    (?# contains the regex statement to parse whatsapp messages)
    (?# make sure re lib is configure with re.VERBOSE and re.MULTILINE)
    ^
    (?P<datetime>\d{1,2}\/\d{1,2}\/\d{2}[^-]+)\s+-\s+
    (?P<name>[^:]+):\s+
    (?P<message>[\s\S]+?)
    (?=^\d{1,2}\/\d{1,2}\/\d{2}[^-]|\Z)
    """

    REGEX_PATTERN_MEMBER_TIMESTAMP = "datetime"
    REGEX_PATTERN_MEMBER_MESSAGE = "message"
    REGEX_PATTERN_MEMBER_NAME = "name"
    WHATSAPP_DATE_PATTERN = "%x, %H:%M"

    @staticmethod
    def get_absolute_path(path: str) -> str:
        script_dir = os.path.dirname(__file__)
        return util_get_absolute_path(script_dir, path)

    @staticmethod
    def get_file_content(path: str) -> str:
        """
        Read text content from a file using shared file_utils, preserving original resolution behavior.
        """
        script_dir = os.path.dirname(__file__)
        return util_get_file_content(path, base_dir=script_dir)

    @staticmethod
    def remove_urls(text: str) -> str:
        urls = re.findall(WhatsAppStrategy.URL_REGEX, text)
        for url in urls:
            text = text.replace(url, "")
        return text

    @staticmethod
    def tokenize(words: str) -> List[str]:
        return re.sub(r"[^\w]", " ", words).split()

    @staticmethod
    def parse_datetime(string_representation: str) -> datetime.datetime:
        return datetime.datetime.strptime(
            string_representation, WhatsAppStrategy.WHATSAPP_DATE_PATTERN
        )

    def extract_texts_from_string(self, text: str) -> str:
        """
        Convenience method used for tests and simple inputs:
        Returns the provided text with WhatsApp-specific placeholders removed.
        """
        if text is None:
            return text
        return text.replace("<Media omitted>", "").replace("<Media omitted>", "")

    def extract_texts(self, input_source: str) -> List[str]:
        """
        Extract message texts from a WhatsApp exported chat backup file.
        Returns a list of message strings.
        """
        backup_text = self.get_file_content(input_source)
        return self._parse_messages_from_string(backup_text)

    def _parse_messages_from_string(self, input_string: str) -> List[str]:
        # Compile and parse messages using embedded regex
        pattern = re.compile(self.REGEX_PATTERN, flags=re.MULTILINE | re.VERBOSE)
        texts: List[str] = []
        for match in pattern.finditer(input_string):
            message = match.groupdict().get(self.REGEX_PATTERN_MEMBER_MESSAGE)
            if message is not None:
                texts.append(message.replace("<Media omitted>", ""))
        return texts
