import random
import re
from abc import ABC

from beem import Hive
from beem.comment import Comment

from DataProcessing.Processing import MessagesProcessingBase


class LMACContestMessagesProcessing(MessagesProcessingBase, ABC):
    DEFAULT_IMAGE_URL: str = 'https://files.peakd.com/file/peakd-hive/quantumg/23tSh9ZCk2m46Yy9XQeQErkwL99fsdQjsxH9A6T4WKyi7BCDs3y4Q6pE3zMfDF4ggv5TS.png'

    _generatedText: str

    def __init__(self, contestDelimiterPattern: str):
        self._compiledContestDelimiterPattern = re.compile(contestDelimiterPattern)
        self._compiledPostLinkPattern = re.compile(r'https\:\/\/(?:peakd\.com|hive\.blog)\/[@a-z0-9_\-\/\.]+')
        self._compiledAuthorPermPattern = re.compile(r'@([a-z0-9_\-\.]+)/([a-z0-9_\-\.\/]+)')
        self._generatedText = ''
        self._hive = Hive()

    def processMessages(self, messages: list):
        random.shuffle(messages)

        for message in messages:
            if self._compiledContestDelimiterPattern.match(message.content) is not None or 'Round ' in message.content:
                return

            for link in self._getLinks(message.content):
                self._generatedText += '@{author}\n{url}\n{imageLink}\n\n'.format(
                    author=link['author'],
                    url=link['url'],
                    imageLink=link['imageLink'],
                )

    def _getLinks(self, messageBody: str) -> list:
        matches = self._compiledPostLinkPattern.finditer(messageBody)
        if not matches:
            print ('not found: ' + messageBody)
            return []

        links = []

        for match in matches:

            author, permlink = self._extractAuthorPerm(match.group())

            links.append({
                    'author': author,
                    'url': match.group(0),
                    'imageLink': self._loadHivePostImageLink(author, permlink)
                }
            )

        return links

    def getGeneratedText(self) -> str:
        return self._generatedText

    def _extractAuthorPerm(self, url: str):
        match = self._compiledAuthorPermPattern.findall(url)
        match=list(match[0])
        return match[0], match[1]

    def _loadHivePostImageLink(self, author: str, permlink: str) -> str:
        comment = Comment(
            '@{hiveAuthor}/{hivePermlink}'.format(hiveAuthor=author, hivePermlink=permlink),
            blockchain_instance=self._hive
        )
        if 'image' not in comment.json_metadata or len(comment.json_metadata['image']) == 0:
            return LMACContestMessagesProcessing.DEFAULT_IMAGE_URL

        return comment.json_metadata['image'][0]
