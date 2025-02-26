import discord    #to interact with discord api
from discord.ext import commands    # to create commands
import pandas as pd
import matplotlib.pyplot as plt


TOKEN = "YOUR_BOT_TOKEN"    # bot token

# Enable necessary intents
intents = discord.Intents.default()
intents.message_content = True  # allow access to read massages
intents.guilds = True    # allow access to server details
intents.members = True  # allow access to server members details
bot = commands.Bot(command_prefix='!', intents=intents)    # bot listen to all the commands starts with !


messages_df = pd.DataFrame(columns=['User', 'Channel', 'Message'])    # create a dataframe to store messages

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    data = []
    for guild in bot.guilds:    # loop through all the servers the bot is in
        for channel in guild.text_channels:    # loop through all the  channels in the server
            try:
                async for message in channel.history(limit=100):  # Fetch last 100 messages
                    data.append([message.author.name, channel.name, message.content])
            except discord.errors.Forbidden:
                print(f"⚠️ Missing access to {channel.name}. Skipping...")

    global messages_df
    messages_df = pd.DataFrame(data, columns=['User', 'Channel', 'Message'])
    print("✅ Message history loaded!")

# Function to calculate and visualize message metrics
def calculate_metrics(df):
    if df.empty:
        return None  # Return None if no data

    user_counts = df['User'].value_counts()    # counts massages per user
    channel_counts = df['Channel'].value_counts()    # counts massages per channel

    plt.figure(figsize=(10, 6))

    plt.subplot(1, 2, 1)
    user_counts.plot(kind='bar', color='skyblue')
    plt.title('Messages per User')
    plt.xticks(rotation=45)

    plt.subplot(1, 2, 2)
    channel_counts.plot(kind='bar', color='lightcoral')
    plt.title('Messages per Channel')
    plt.xticks(rotation=45)

    plt.tight_layout()

    image_path = "analytics.png"
    plt.savefig(image_path)  # Save the image
    plt.close()  # Close the plot
    return image_path

# Discord bot command to display analytics
@bot.command(name='analytics')
async def analytics(ctx):
    image_path = calculate_metrics(messages_df)  # Generate image

    if image_path:
        with open(image_path, "rb") as f:
            await ctx.send("📊 Here is the message analytics report:", file=discord.File(f))
    else:
        await ctx.send("❌ No message data available for analytics.")

# Run the bot
bot.run(TOKEN)
