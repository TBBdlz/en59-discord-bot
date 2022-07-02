from discord.ext import commands
from discord.utils import get

class Greetings(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.command()
  async def hello(self, ctx):
    await ctx.send('Hello, I your engineering helper!')

  @commands.Cog.listener()
  async def on_member_join(self, member):
    channel = self.client.get_channel(989117642113712133)
    await channel.send(f'Hello {member} welcome to EN59 discord server!')
    role = get(member.guild.roles, name='unknown 👽')
    await member.add_roles(role)

def setup(client):
  client.add_cog(Greetings(client))
  