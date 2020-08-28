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

    def make_move(self, board, san_move):
        move = board.parse_san(san_move)#try for parsing error
        board.push(move)


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
            elif args[1] == 'legal-moves':
                response = str(self.boards[message.guild.id].legal_moves)[37:-1]
                await message.channel.send(response)
            elif args[1] == 'm' or args[1] == 'move':
                response="unknown error"
                try:
                    self.make_move(self.boards[message.guild.id], args[2])
                    response = self.ascii_board(message.guild.id)
                except ValueError as error:
                    if 'invalid' in str(error):
                        response = 'Move expects valid algebraic notation. https://en.wikipedia.org/wiki/Algebraic_notation_(chess)'
                    elif 'illegal' in str(error):
                        response = 'Illegal move. For a list of legal moves try !c legal-moves'
                except KeyError as error:
                    response = 'No active game. Create a game with !c new'
                await message.channel.send(response)



client = chessClient()
client.run(TOKEN)




client.run(TOKEN)
