import argparse

import Configurations
from DataProcessing.LMACProcessing import LMACContestMessagesProcessing
from Network.Discord import DiscordBotClient
from Services.AspectLogging import LogAspect


class Main:
    EXITCODE_OK: int = 0
    EXITCODE_ERROR: int = 1

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.description = 'Renders a markdown from all nominations made per contest in a specific Discord channel.'
        parser.add_argument(
            '-simulate',
            type=bool,
            help='Starts the tool in simulation mode. Sending messages is then disabled.',
            default=False,
            required=False
        )
        exit(self._main(vars(parser.parse_args())))

    def _main(self, arguments: dict):

        logger = LogAspect('BotMain')
        logger.logger().info('Started processing.')

        try:
            contestMessagesProcessor = LMACContestMessagesProcessing(
                contestDelimiterPattern=Configurations.BaseConfiguration.discordRoundDelimiterMessagePattern
            )

            discordClient = DiscordBotClient(
                sourceChannelId=Configurations.BaseConfiguration.discordSourceChannelId,
                messageProcessor=contestMessagesProcessor,
                sendMessage=Configurations.BaseConfiguration.discordFileMessageText,
                filename=Configurations.BaseConfiguration.discordFilename,
                simulate=arguments['simulate']
            )
            discordClient.run(Configurations.BaseConfiguration.discordBotToken)
        except Exception as e:
            logger.logger().error('Error ({message})'.format(message=str(e)))
            return Main.EXITCODE_ERROR

        logger.logger().info('Finished processing.')

        return Main.EXITCODE_OK


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Main()
