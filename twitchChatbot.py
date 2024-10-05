import os
import pygame
import time
from google.cloud import texttospeech_v1
from twitchio.ext import commands
import random

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "ttsBotServiceAccount.json"
client = texttospeech_v1.TextToSpeechClient()

pygame.mixer.init()

follow_sound = pygame.mixer.Sound("followerJingle.wav")
chatbot_online_sound = pygame.mixer.Sound("StartupJingleChill.wav")

language_names = ["en-AU-Polyglot-1",
         "en-AU-Standard-B",
         "en-AU-Standard-C",
         "en-AU-Standard-D",
         "en-IN-Standard-A",
         "en-IN-Standard-B",
         "en-IN-Standard-C",
         "en-IN-Standard-D",
         "en-GB-Standard-A",
         "en-GB-Standard-B",
         "en-GB-Standard-C",
         "en-GB-Standard-D",
         "en-GB-Standard-F",
         "en-US-Journey-D",
         "en-US-Journey-F",
         "en-US-Polyglot-1",
         "en-US-Standard-A",
         "en-US-Standard-B",
         "en-US-Standard-C",
         "en-US-Standard-D",
         "en-US-Standard-E",
         "en-US-Standard-F",
         "en-US-Standard-G",
         "en-US-Standard-H",
         "en-US-Standard-I",
         "en-US-Standard-J"]
language_codes = ["en-AU",
                  "en-AU",
                  "en-AU",
                  "en-AU",
                  "en-AU",
                  "en-IN",
                  "en-IN",
                  "en-IN",
                  "en-IN",
                  "en-GB",
                  "en-GB",
                  "en-GB",
                  "en-GB",
                  "en-GB",
                  "en-US",
                  "en-US",
                  "en-US",
                  "en-US",
                  "en-US",
                  "en-US",
                  "en-US",
                  "en-US",
                  "en-US",
                  "en-US",
                  "en-US"]

def check_profile(username):
    profiles = open("profiles.txt", 'r')
    
    file = profiles.read()
    
    if username in file:
        profiles.close()
        return True
    else:
        profiles.close()
        return False
    
def create_profile(username):
    langNum = random.randint(0, 24)
    profiles = open("profiles.txt", 'a')
    lang_code = language_codes[langNum]
    lang_name = language_names[langNum]
    profiles.write("\n" + username + "@" + lang_code + "@" + lang_name)
    print("new profile created")
    output_list = [username, lang_code, lang_name]
    return output_list
    profiles.close()
    
def get_profile(username):
    profiles = open("profiles.txt", 'r')
    
    line = profiles.readline()
    while line != '':
        print("parse")
        if username in line:
            print(line)
            elements = line.strip().split("@")
            return elements
        else:
            line = profiles.readline()
    return ['', '', '']

def profiler(username):
    profiles = open("profiles.txt", 'r')
    
    has_profile = False
    
    line = profiles.readline()
    while line != '':
        if username in line:
            # profile already exists
            has_profile = True
            print(line)
            elements = line.split("@")
            print(elements[0])
            print(elements[1])
            print(elements[2])
        line = profiles.readline()
    
    # print(has_profile)
    
    if not has_profile:
        langNum = random.randint(0, 25)
        profiles.close()
        profiles = open("profiles.txt", "a")
        profiles.write("\n" + username + "@" + language_codes[langNum] + "@" + language_names[langNum])
        print("new profile created")
        
    profiles.close()

sample_text = "Testing 12"

synthesis_input = texttospeech_v1.SynthesisInput(text = sample_text)

voice1 = texttospeech_v1.VoiceSelectionParams(
    name='en-US-Standard-A',
    language_code='en-US'
)

audio_config = texttospeech_v1.AudioConfig(
    audio_encoding=texttospeech_v1.AudioEncoding.MP3
)

response = client.synthesize_speech(
    input = synthesis_input,
    voice = voice1,
    audio_config=audio_config
)

def read_message(author, message):
    
    has_profile = check_profile(author)
    print(has_profile)
    
    if has_profile:
        profile = get_profile(author)
        print("yes profile")
        print(profile)
        voice1.name = profile[2]
        voice1.language_code = profile[1]
    else:
        profile = create_profile(author)
        print("no profile")
        print(profile)
        voice1.name = profile[2]
        voice1.language_code = profile[1]
    
    message = message[:150]
    what_to_read = author + " says: " + message
    synthesis_input = texttospeech_v1.SynthesisInput(text = what_to_read)
    
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice1,
        audio_config=audio_config
    )
    
    with open('message.mp3', 'wb') as output1:
        output1.write(response.audio_content)
    
    pygame.mixer.music.load('message.mp3')
    pygame.mixer.music.play()
    
    busy = True
    while busy == True:
        if pygame.mixer.music.get_busy() == False:
            busy = False
    
    os.remove('message.mp3')
    
class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=os.environ.get('OMNI_TWITCH_API_KEY'), prefix='?', initial_channels=["omnicorum"])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        chatbot_online_sound.play()

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        output = message.author.name + " writes: " + message.content
        print(output)
        
        read_message(message.author.name, message.content)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f'Hello {ctx.author.name}!')

bot = Bot()
bot.run()