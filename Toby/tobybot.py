import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import os
import pandas
import random
import time
import datetime
from dotenv import load_dotenv
import download_sheets
import blackjack

intents = discord.Intents.default()
intents.members = True

load_dotenv()
#client = commands.Bot(command_prefix = '$')
client = discord.Client(intents=intents)
TOKEN = 

email = 'blexbotdiscord@gmail.com'
password = 

version = "1.0"
version_desc = "Toby is born!"

start_time = time.time()

@client.event
async def on_ready():
    ts = datetime.datetime.now()
    print("["+str(ts)+"] "+f'{client.user} is online!')
    await client.get_channel(130405215294717952).send("Type $Toby help for commands.")
        #time.sleep(40000)
    
#new member joined
@client.event
async def on_member_join(member):
    ts = datetime.datetime.now()
    print("["+str(ts)+"] "+ member.name+" joined the server. Rank: Member")
    await client.get_channel(130405215294717952).send("Welcome to the Jungle **" + member.name +"**. Go stand over there with the rest.")
    role = discord.utils.get(member.server.roles, name="Member")
    await client.add_roles(member, role)

@client.event
async def on_message(message): 
  df = pandas.read_csv('Toby_Responses.csv')
  df1 = pandas.read_csv('Toby_Commands.csv')

  if message.author == client.user:
    return

  #help command
  if str(message.content) == "$Toby help":
      commands = ["$Toby interactions", "$Toby voices", "$Toby uptime",
                  "$Toby disconnect","$Toby roll dice","$Toby version", "$Toby blackjack"]
      output = ""
      for i in commands:
          output += i+"\n"
      await message.channel.send(str(output))
      ts = datetime.datetime.now()
      print("["+str(ts)+"] "+str(message.author)+" $Toby help")
      
  #basic interactions in chat
  if str(message.content) in df['Key'].values:
    x = random.randint(1,6)
    resp = df.at[df[df['Key'] == str(message.content)].index[0], str(x)]
    await message.channel.send(str(resp))
    ts = datetime.datetime.now()
    print("["+str(ts)+"] "+str(message.author)+" "+str(message.content))
     
  #help function for interactions
  if str(message.content) == "$Toby interactions":
    interactions = ""
    for i in df['Key'].values:
      interactions += i+"\n"
    await message.channel.send("Interact with me! Say a phrase below.\n"+interactions)
    ts = datetime.datetime.now()
    print("["+str(ts)+"] "+str(message.author)+" $Toby interactions")
  
  #commands for playing audio
  if str(message.content) in df1['Key'].values:
      ts = datetime.datetime.now()
      print("["+str(ts)+"] "+str(message.author)+" "+str(message.content))
      if (message.author.voice):
          channel = message.author.voice.channel
          
          voice = discord.utils.get(client.voice_clients, guild=message.guild)
          if voice == None:
              voice = await channel.connect()
              ts = datetime.datetime.now()
              print("["+str(ts)+"] Toby joining voice channel")
              
          source_string = df1.at[df1[df1['Key'] == str(message.content)].index[0], '1']
          
          if os.path.exists(source_string):
              source = FFmpegPCMAudio(source_string)
              player = voice.play(source)
          else:
              print("No such audio file")
      else:
          await message.channel.send("Must be in voice channel to do that")
          
          
  #help function for interactions
  if str(message.content) == "$Toby voices":
      interactions = ""
      for i in df1['Key'].values:
          interactions += i+"\n"
      await message.channel.send("Interact with me! Type a command below while in a voice channel.\n"+interactions)
      ts = datetime.datetime.now()
      print("["+str(ts)+"] "+str(message.author)+" $Toby voices")
      
  #disconnect toby from vc
  if str(message.content) == "$Toby disconnect":
      await message.guild.voice_client.disconnect()
      ts = datetime.datetime.now()
      print("["+str(ts)+"] "+str(message.author)+" $Toby disconnect")
      ts = datetime.datetime.now()
      print("["+str(ts)+"] Toby left the voice channel")
      
  #uptime for toby
  if str(message.content) == "$Toby uptime":
      uptime = round(time.time() - start_time)
      await message.channel.send(str(uptime) + " seconds")
      ts = datetime.datetime.now()
      print("["+str(ts)+"] "+str(message.author)+" $Toby uptime")
      ts = datetime.datetime.now()
      print("["+str(ts)+"] "+"Uptime: "+ str(uptime))

  #roll a dice
  if str(message.content) == "$Toby roll dice":
      number = random.randint(1,6)
      await message.channel.send(str(number))
      ts = datetime.datetime.now()
      print("["+str(ts)+"] "+str(message.author)+" $Toby roll dice")
      ts = datetime.datetime.now()
      print("["+str(ts)+"] They rolled a ",number)
      
  #Black_Jack game DOESNT WORK
  if str(message.content) == ("$Toby blackjack play"):
      og = message.author
      if (blackjack.player_score == 0):
          await message.channel.send("Insuffiencient Funds. Your balance is $0.")
          return
      await message.channel.send("WELCOME TO BLACKJACK! Current balance is: "+ blackjack.player_score +".\nToby's hand: [" + str(blackjack.dealer_hand[0])+", *Hidden*]\nYour hand: " + str(blackjack.player_hand) + " for a total of " + str(total(blackjack.player_hand)) +"\n Bet: $100\nDo you want to [H]it or [S]tand")
      quit = False
      blackjack.game(str(message.author))
      while not quit:
          message = await bot.wait_for("message", message.author=og)
          hits = ['h', 'H', 'hit', 'Hit', 'HIT']
          stands = ['s', 'S', 'stand', 'Stand', 'STAND']
          
          if (message.content in hits):
              blackjack.hit(blackjack.player_hand)
              if total(blackjack.player_hand)>21:
                  await message.channel.send("Your hand: " + str(blackjack.player_hand) + " for a total of " + str(total(blackjack.player_hand)) +"\n You busted.\n -$100")
                  quit=True
              await message.channel.send("Your hand: " + str(blackjack.player_hand) + " for a total of " + str(total(blackjack.player_hand)))

          if (message.content in stands):
            print("You chose to Stand")
            print ("Toby's hand: " + str(dealer_hand)+" for a total of "+str(total(dealer_hand))+"\n")
            if total(dealer_hand) >= total(player_hand):
                quit=True
            while total(dealer_hand)<17:
                print("Toby Hits")
                hit(dealer_hand)
                print ("Toby's hand: " + str(dealer_hand)+" for a total of "+str(total(dealer_hand))+"\n")
                if total(dealer_hand)>21:
                    quit=True
            score(dealer_hand,player_hand)
            quit=True
      
      ts = datetime.datetime.now()
      print("["+str(ts)+"] "+str(message.author)+" $Toby blackjack play")
      ts = datetime.datetime.now()
      print("["+str(ts)+"] "+str(message.author)+" $Toby blackjack play")
      
      
  #Toby version
  if str(message.content) == "$Toby version":
      await message.channel.send(str(version)+"- "+version_desc)
      ts = datetime.datetime.now()
      print("["+str(ts)+"] "+str(message.author)+" $Toby version")
      ts = datetime.datetime.now()
      print("["+str(ts)+"] Version: "+version+" "+version_desc)
      
  #Blackjack COMING SOON

client.run(TOKEN)
