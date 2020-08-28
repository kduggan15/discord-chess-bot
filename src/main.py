# bot.py
import os

import discord
from dotenv import load_dotenv

import chess

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class chessClient(discord.Client):

    def ascii_board(self, id):
        b = f'`{self.boards[id]}`'
        b = b.replace('P','♟︎')
        b = b.replace('R','♜')
        b = b.replace('N','♞')
        b = b.replace('B','♝')
        b = b.replace('Q','♛')
        b = b.replace('K','♚')

        b = b.replace('p','♙')
        b = b.replace('r','♖')
        b = b.replace('n','♘')
        b = b.replace('b','♗')
        b = b.replace('q','♕')
        b = b.replace('k','♔')
        return b

    async def on_ready(self):
        self.boards={}
        guild = client.guilds[0]
        print(f'{client.user} is connected to the following guilds:')
        for guild in client.guilds:
            print(f'\t{guild.name}({guild.id})')

    async def on_message(self, message):
        if message.author == client.user:
            return
        args = message.content.split(' ')
        if args[0] == '!c':
            if args[1] == 'new':
                print(f"New game started on {message.guild}")
                self.boards[message.guild.id] = chess.Board()
                response = self.ascii_board(message.guild.id)
                await message.channel.send(response)
            elif self.boards[message.guild.id].parse_san(args[1]) in self.boards[message.guild.id].legal_moves:
                self.boards[message.guild.id].push_san(args[1])
                response = self.ascii_board(message.guild.id)
                await message.channel.send(response)



client = chessClient()
client.run(TOKEN)




client.run(TOKEN)
