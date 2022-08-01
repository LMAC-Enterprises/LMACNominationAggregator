import discord as discord
from discord import Intents, File

from DataProcessing.Processing import MessagesProcessingBase
from Services.AspectLogging import LogAspect


class DiscordBotClient(discord.Client):
    _sourceChannelId: int
    _messageProcessor: MessagesProcessingBase
    _filename: str
    _sendMessage: str
    _simulate: bool
    _logger: LogAspect

    def __init__(self, sourceChannelId: int, messageProcessor: MessagesProcessingBase, sendMessage: str, filename: str, simulate: bool):
        super().__init__(intents=discord.Intents.default())
        self._sourceChannelId = sourceChannelId
        self._messageProcessor = messageProcessor
        self._filename = filename
        self._sendMessage = sendMessage
        self._simulate = simulate
        self._logger = LogAspect('DiscordClient')

    async def on_ready(self):
        channel = self.get_channel(self._sourceChannelId)
        messages = await channel.history(limit=25).flatten()

        self._onChannelHistoryReceived(messages)
        await self._onFinishAllBotOperations()
        await self.close()

    def _onChannelHistoryReceived(self, messages: list):
        self._messageProcessor.processMessages(messages)

    async def _onFinishAllBotOperations(self):
        textToSend = self._messageProcessor.getGeneratedText()
        if len(textToSend) == 0:
            self._logger.logger().info('No links found.')
            return

        if self._simulate:
            print('Text to send: ' + textToSend)
            return

        with open(self._filename, 'w') as text_file:
            text_file.write(textToSend)

        channel = self.get_channel(self._sourceChannelId)
        with open(self._filename, 'r') as text_file:
            await channel.send(content='Nominations.', file=File(fp=text_file, filename=self._filename))
