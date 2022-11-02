import discord
from discord import app_commands 
import cloudscraper as cs

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False 

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync() 
            self.synced = True
        print(f"We have logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)

scraper = cs.create_scraper() 

@tree.command(name = 'real_mines', description='mines predictor') #guild specific slash command
async def slash2(interaction: discord.Interaction, auth : str):

    r = scraper.get('https://api.bloxflip.com/games/mines/history', headers={"x-auth-token": auth}, params={ 'size': '1','page': '0',}  ) 
    
    
    uuid = (r.json()['data'][0]['uuid']) 

    mines_location = (r.json()['data'][0]['mineLocations']) #most recent mines location, we will use this to make a guess or a "prediction"

    clicked_spots = (r.json()['data'][0]['uncoveredLocations']) 

    grid = ['❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌'] 

    for x in mines_location: #make each bomb postion show up on grid
        grid[x] = 'X' #change the bomb posititons to differnt character

    for x in clicked_spots: #loop through every time u clicked and make it convert to grid
        grid[x] = 'O' #change the clicked positions to differnt character


    grid = ['❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌','❌'] 

    roundId = int(''.join(filter(str.isdigit, uuid))) 

    roundNum = int(str(roundId)[:2]) #get the first two numbers out of the round id
    grid[int(roundNum / 4)] = '✔️' 
    grid[int(roundNum / 5)] = '✔️' 
    grid[int(roundNum / 7)] = '✔️' 

    em = discord.Embed(description=f"```{grid[0]+grid[1]+grid[2]+grid[3]+grid[4]}"+ "\n" + f"{grid[5]+grid[6]+grid[7]+grid[8]+grid[9]}" + "\n" + f"{grid[10]+grid[11]+grid[12]+grid[13]+grid[14]}"+ \
        "\n" + f"{grid[15]+grid[16]+grid[17]+grid[18]+grid[19]}" + "\n" + f"{grid[20]+grid[21]+grid[22]+grid[23]+grid[24]}```", color=0x0025ff)

    await interaction.response.send_message(embed=em)

client.run('bot token')
