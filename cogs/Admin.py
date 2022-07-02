import discord
from discord.ext import commands
from replit import db
from discord.utils import get

"""
functions use to extract data
"""


def refactor_stu_id(student_id: str) -> tuple:
    proper_stu_id: str = ''
    valid: bool = True
    if student_id[:3] != '653':
      return False, ''
    if len(student_id) == 10:
        for char in student_id:
            if not char.isdigit():
                print(f'{char} is not digit')
                valid = False
                break
        proper_stu_id = f'{student_id[:9]}-{student_id[-1]}'
    elif len(student_id) == 11:
        for char in student_id.replace('-', ''):
            if not char.isdigit():
                valid = False
                break
        proper_stu_id = student_id
    else:
        valid = False

    return valid, proper_stu_id


class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, user: discord.Member, *, role: discord.Role):

        if role in user.roles:
            await ctx.send(f'{user.mention} already has the role, {role}')
        else:
            await user.add_roles(role)
            print(user)
            print(role)
            await ctx.send(f'Added {role} to {user.mention}')

    @addrole.error
    async def role_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permission to use this command.')

    @commands.Cog.listener()
    async def on_message(self, message):
        msg: str = message.content
        if msg.startswith('$verify'):
            channel = self.client.get_channel(989594313077977129)
            if 'exist_names' not in db.keys():
                db['exist_names'] = []
            exist_names = db['exist_names']
            if 'exist_ids' not in db.keys():
                db['exist_ids'] = []
            exist_ids = db['exist_ids']
            # user can verify only in verify channel
            if message.channel != channel:
                message.channel.send('You can only verify on verify channel.')
                return
            print(msg)
            if len(msg.split()) == 4:
                msg_list: list[str] = msg.split()
                raw_stu_id = msg_list[1]
                name = ' '.join(msg_list[2:])
                valid, stu_id = refactor_stu_id(raw_stu_id)
                if not valid:
                    await channel.send('รหัสนักศึกษาไม่ถูกต้อง! กรุณาตรวจสอบรหัสนักศึกษาของท่านแล้วกรอกใหม่...')
                else:  # student id is correct
                    try:
                        # this code check if name_index and student index correct or not
                        name_index = db['names'].index(name)
                        stu_id_index = db['student_ids'][name_index]
                    except ValueError:
                        await channel.send('รหัสนักศึกษากับชื่อเต็มไม่ตรงกัน!!! โปรดตรวจสอบข้อมูลให้ดี หากมีปัญหาให้ mention หาพี่สโมสร ENSU ได้เลยนะครับบ!!!')
                    else:
                        user = message.author
                        role = get(user.guild.roles, name="EN59")
                        unk_role = get(user.guild.roles, name='unknown 👽')
                        print(user)
                        mention = user.mention
                        if role in user.roles:
                            await channel.send(f'{mention} already has the role, {role}')
                        else:
                            if name in exist_names:
                                await channel.send('ไม่สามารถลงบัญชีซ้ำกันได้ หากมีปัญหาการใช้งานโปรด mention ENSU')
                                return
                            exist_names.append(name)
                            exist_ids.append(stu_id)
                            db['exist_names'] = exist_names
                            db['exist_ids'] = exist_ids
                            await user.add_roles(role)
                            await user.remove_roles(unk_role)
                            print(user)
                            print(role)
                            response = f'Added role {role} to {user}.'
                            await channel.send(response)

            else:
                guide_msg = """น้องๆ สามารถ verify ได้คำสั่งนี้เลยครับบ `$verify <student_id> <firstname> <lastname>`""" + \
                    '\nเช่น `$verify 653040174-2 เอก ฮาร์ตร็อคเกอร์`'
                await channel.send(guide_msg)


def setup(client):
    client.add_cog(Admin(client))
