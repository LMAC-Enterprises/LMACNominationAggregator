class BaseConfiguration:
    discordSourceChannelId: int = 0
    discordBotToken: str = 'ABCDEFG-HIJKLMNOPQ-R1-S2'
    discordRoundDelimiterMessagePattern: str = r'^Nominations\.$'
    discordFileMessageText: str = 'Nominations.'
    discordFilename: str = 'nominations.txt'
