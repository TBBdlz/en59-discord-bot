import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='$', intents=intents)

initial_extensions: list = []

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    initial_extensions.append('cogs.' + filename[:-3])
print(initial_extensions)


"""
Discord bot functions
"""
@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')
  print('-----------------------------------------')
  
"""
main script
"""
if __name__ == '__main__':
  for extension in initial_extensions:
    client.load_extension(extension)
  keep_alive()
  try:
    client.run(os.environ['TOKEN'])
  except:
    os.system('kill 1')
