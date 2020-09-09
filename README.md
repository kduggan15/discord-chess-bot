# Discord Chess Bot -- Play Chess With Your Friends on Discord!
## Using the bot
- Public bot invite link coming soon
- `!c play` to start matchmaking. Once another player types `!c play`, you will be matched
- Players are pseudorandomly assigned colors and the state of the board is represented as ASCII
- Enter your moves with `!c m [move]` where `[move]` is in algebraic notation. Such as `!c m e4` or `!c m Qxe4`
- You can type `!c legal-moves` for a list of legal moves in algebraic notation
- After each move, the board is printed again, until the game ends, at which point you can play again with `!c play`
## Running the bot on your own
- git clone https://github.com/kduggan15/discord-chess-bot.git
- It is recommended to make a virtualenv for python programs
- pip install virtualenv
- cd discord-chess-bot
- virtualenv . -p python3
- . bin/activate
- pip install -U discord.py
- pip install -U python-dotenv
- pip install -U python-chess
- create a file named `.env` in the same folder as main.py and put the line `DISCORD_TOKEN={YOUR_TOKEN}`
- Make sure this doesn't become public. That's what dotenv is for
- Finally, python3 main.py
