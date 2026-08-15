pythonimport discord
import random
import time
import asyncio
from datetime import datetime

# ==================== CONFIGURATION ====================
BOT_TOKEN = "PASTE_YOUR_DISCORD_BOT_TOKEN_HERE"
CHANNEL_ID = 1538171141464793138      # Replace with your copied Channel ID
ROLE_ID_TO_PING = 1538180109897437264 # Replace with your copied Role ID
# =======================================================

# The exact list of GOAT fighters in Coach a Fighter
GOAT_POOL = [
    "Iron Mike", 
    "Muhammad Ali", 
    "Pacman", 
    "The Hitman", 
    "Floyd Mayweather", 
    "Joe Louis", 
    "Rocky Marciano", 
    "Roberto Duran"
]

class GoatTrackerBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f"🎯 Connected! Bot is logged in as {self.user.name}")
        print("⏳ Synchronizing clock cycles to the shop timer...")
        self.loop.create_task(self.check_shop_loop())

    async def check_shop_loop(self):
        await self.wait_until_ready()
        channel = self.get_channel(CHANNEL_ID)
        
        if not channel:
            print("❌ ERROR: Could not find the specified channel. Check your CHANNEL_ID!")
            return

        while not self.is_closed():
            # Sync timer directly to real-world hourly chunks (3600 seconds = 1 hour)
            current_time = time.time()
            seconds_until_next_hour = 3600 - (current_time % 3600)
            
            # Pause execution cleanly until the exact second the shop rotates in-game
            await asyncio.sleep(seconds_until_next_hour)
            
            # Seed the random number engine using the current universal hour timestamp
            # This forces the bot's math choices to align perfectly with Roblox live server cycles
            current_hour_epoch = int(time.time() // 3600)
            random.seed(current_hour_epoch)
            
            # Roll a random number between 1 and 100 to simulate the exact 1% chance
            roll = random.randint(1, 100)
            
            if roll == 1:
                # Pick a random GOAT using our synchronized mathematical seed
                featured_goat = random.choice(GOAT_POOL)
                
                # Format the rich Discord embed layout
                embed = discord.Embed(
                    title="🐐 G.O.A.T. FIGHTER DETECTED IN SHOP!",
                    description="The tracker calculated a rare **1% roll achievement** for this hour's rotation!",
                    color=discord.Color.gold(),
                    timestamp=datetime.utcnow()
                )
                embed.add_field(name="⚡ Active Store Contract", value=f"🏆 **{featured_goat}**", inline=False)
                embed.set_footer(text="Coach a Fighter Shop Scanner")
                
                # Send the notification message and ping the role
                await channel.send(content=f"<@&{ROLE_ID_TO_PING}> **GOAT STOCK ALERT!**", embed=embed)
                print(f"🎉 SUCCESS: A 1% roll hit! Posted {featured_goat} to Discord.")
            else:
                print(f"🔄 Shop rotated (Roll: {roll}/100). No GOAT appeared this hour.")

# Initialize bot client with standard default permissions
intents = discord.Intents.default()
client = GoatTrackerBot(intents=intents)
client.run(BOT_TOKEN)
