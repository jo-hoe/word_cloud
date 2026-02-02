import os
import re
import datetime
from typing import List
from app.strategies.base import InputSourceStrategy


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
        return os.path.join(script_dir, path)

    @staticmethod
    def get_file_content(path: str) -> str:
        """
        Read text content from a file. Tries multiple locations for relative paths:
        - As provided (current working directory)
        - Relative to this module's directory
        - Under project_root/test/
        """
        candidates = [path]
        if not os.path.isabs(path):
            script_dir = os.path.dirname(__file__)
            candidates.append(os.path.join(script_dir, path))
            project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
            candidates.append(os.path.join(project_root, "test", path))

        last_error = None
        for p in candidates:
            try:
                with open(p, "r", encoding="utf8", errors="ignore") as file:
                    return file.read()
            except FileNotFoundError as e:
                last_error = e
                continue

        # If all attempts failed, raise the last error
        if last_error:
            raise last_error
        raise FileNotFoundError(f"File not found: {path}")

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

    def extract_texts(self, input_source: str) -> List[str]:
        """
        Extract message texts from a WhatsApp exported chat backup file.
        Returns a list of message strings.
        """
        # Load backup text
        backup_text = self.get_file_content(input_source)

        # Compile and parse messages using embedded regex
        pattern = re.compile(self.REGEX_PATTERN, flags=re.MULTILINE | re.VERBOSE)
        texts: List[str] = []
        for match in pattern.finditer(backup_text):
            message = match.groupdict().get(self.REGEX_PATTERN_MEMBER_MESSAGE)
            if message is not None:
                texts.append(message.replace("<Media omitted>", ""))
        return texts
