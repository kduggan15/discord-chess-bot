# bot.py
import os

import discord
from dotenv import load_dotenv

import chess
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class chessGuild():
    def __init__(self):
        self.games = {}#{gameID->(board,white,black)} where board is a chess.Board(), and white and black are userIDs
        self.players = {}#{userID->gameID}, represents active players. Used to prevent users being in multiple games, and to interpret commands
        self.user_names = {}#{userID->userName}Maintains dictionary of userids and usernames
        self.match_queue = []

    #returns true if a game starts, else false
    #Add logging for matchmaking
    def matchmake(self)->bool:
        if len(self.match_queue) >=2:
            board = chess.Board()
            if random.randint(0,1):
                white = self.match_queue.pop(0)
                black = self.match_queue.pop(0)
            else:
                black = self.match_queue.pop(0)
                white = self.match_queue.pop(0)
            self.games[id(board)] = (board, white,black)
            self.players[white] = id(board)#each player points to the gameID they're playing on
            self.players[black] = id(board)
            return True
        else:
            return False
    #returns true if a game starts, else false
    def enqueue_player(self, user) -> str:
        if user.id not in self.players and user.id not in self.match_queue:# TODO: searches array which is slow
            self.user_names[user.id] = user.name
            self.match_queue.append(user.id)
            self.user_names[user.id] = user.name
            if self.matchmake():
                return self.ascii_board(user.id)
            else:
                return f'{user.name} has been added to the matchmaking queue. Challenge them with !c play'

    def legal_moves(self,userID):
        return str(self.games[self.players[userID]][0].legal_moves)[37:-1]#str(self.boards[message.guild.id].legal_moves)[37:-1]

    def make_move(self,userID, san_move):
        game = self.games[self.players[userID]]
        if game[0].is_game_over():
            return
        elif game[0].turn == chess.WHITE and game[1]==userID:
            move = game[0].parse_san(san_move) #try for parsing error
            game[0].push(move)
        elif game[0].turn == chess.BLACK and game[2]==userID:
            move = game[0].parse_san(san_move) #try for parsing error
            game[0].push(move)

    #Takes a userID and returns an ASCII representation of the board they're playing on
    #TODO: This does two things. Prints the board and cleans up the game. This should be decoupled
    #TODO: Say when in check
    def ascii_board(self, userID):
        game = self.games[self.players[userID]]
        b = f'`{game[0]}`'#TODO: what if player doesn't have a game
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
        if game[0].is_game_over():
            b+=f'\nGame over {game[0].result()}'
            #cleanup game
            del self.players[game[1]]
            if game[2] in self.players:
                del self.players[game[2]]
            del game
            return b
        elif game[0].turn:
            b+=f'\nWhite ({self.user_names[game[1]]}) to move.'
        else:
            b+=f'\nBlack ({self.user_names[game[2]]}) to move.'

        return b

    def resign_player(self, userID):
        if userID not in self.players:
            return "You are not in a match to resign from not in match"
        else:
            game = self.games[self.players[userID]]
            user_name = self.user_names[userID]
            #cleanup game:
            del self.players[game[1]]
            if game[2] in self.players:
                del self.players[game[2]]
            del game
            return f"{user_name} has resigned. Game over"



class chessClient(discord.Client):

    async def on_ready(self):
        self.chessGuilds={}
        print(f'{client.user} is connected to the following guilds:')
        for guild in client.guilds:
            self.chessGuilds[guild.id] = chessGuild() #Simple constructor for chessGuilds, could be read from a DB in the future
            print(f'\t{guild.name}({guild.id})')

    async def on_message(self, message):
        if message.author == client.user:
            return
        args = message.content.split(' ')
        if args[0] == '!c':
            if args[1] == 'play':
                response = self.chessGuilds[message.guild.id].enqueue_player(message.author)
                await message.channel.send(response)

            elif args[1] == 'legal-moves':
                response = self.chessGuilds[message.guild.id].legal_moves(message.author.id)
                await message.channel.send(response)

            elif args[1] == 'm' or args[1] == 'move':
                response='unknown error'
                try:
                    self.chessGuilds[message.guild.id].make_move(message.author.id, args[2])
                    #self.make_move(self.boards[message.guild.id], args[2])
                    response = self.chessGuilds[message.guild.id].ascii_board(message.author.id)#self.ascii_board(message.guild.id)
                except ValueError as error:
                    if 'invalid' in str(error):
                        response = 'Move expects valid algebraic notation. ie; Ne3, e4, Qxe2, etc.'
                    elif 'illegal' in str(error):
                        response = 'Illegal move. For a list of legal moves try !c legal-moves'
                except KeyError as error:
                    response = 'No active game. Join the queue with `!c play`'
                await message.channel.send(response)
            elif args[1] == 'h' or args[1] == 'help':
                response = 'Welcome to Chess Bot!\nTry `!c play` to get on the match queue.\n\nOnce in a game, make moves with `!c move [move]` or `!c m [move]`\nMoves are in algebraic notation, i.e. `!c m e4` to push a pawn or, `!c m Qxe4` to take the piece on e4 with the queen\n\nWhen the game ends, you can play again with `!c play`\n\nResign with `!c resign`'
                await message.channel.send(response)
            elif args[1]=='resign':
                response = self.chessGuilds[message.guild.id].resign_player(message.author.id)
                await message.channel.send(response)
            elif args[1]=='resign':
                response = self.chessGuilds[message.guild.id].resign_player(message.author.id)
                await message.channel.send(response)


client = chessClient()
client.run(TOKEN)
