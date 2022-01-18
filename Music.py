import time
from threading import Thread, Lock
from tracemalloc import start

import discord
from discord.ext import commands
import youtube_dl

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = []
        self.mutex = Lock()
        
        # DAEMON
        self.interval = 1

        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            if len(self.queue) > 0:
                lastThread = self.queue.pop()
                lastThread.start()
                lastThread.join()
            time.sleep(self.interval)

    def play_song(self, ctx, source):
        self.mutex.acquire()
        try:
            ctx.voice_client.play(source)
            
            while ctx.voice_client.is_playing():
                pass
            
        finally:
            self.mutex.release()

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel")

        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_channel.disconnect()

    @commands.command()
    async def play(self, ctx, url):
        await self.join(ctx)

        try:
            ctx.voice_client.stop()

            FFMPEG_OPTIONS = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            YDL_OPTIONS = {'format': 'bestaudio'}

            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info['formats'][0]['url']
                source = await discord.FFmpegOpusAudio.from_probe(source=url2, **FFMPEG_OPTIONS)

                # PLAY
                thread = Thread(target=self.play_song, args=[ctx, source])
                self.queue.append(thread)
        except:
            print("Error")

    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send("Paused ⏸️")

    @commands.command()
    async def resume(self, ctx):
        await ctx.voice_client.resume()
        await ctx.send("Resumed ▶️")


def setup(client):
    client.add_cog(Music(client))
