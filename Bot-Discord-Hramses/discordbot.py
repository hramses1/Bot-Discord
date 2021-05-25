from os.path import abspath
from typing import List
import discord
from discord import channel
from discord import client
from discord.voice_client import VoiceClient
from discord import guild
from discord import widget
from discord.enums import Status
from discord.errors import PrivilegedIntentsRequired
from discord.ext import commands, tasks
from urllib import parse, request
from discord.utils import get
import re
import youtube_dl
import os
import shutil
from random import choice
# --------------------------------------------------------
bot = commands.Bot(command_prefix='>', description="Esto es un bot de invocacion")
# --------------------------------------------------------
@bot.event
async def on_ready():
    # -------------------------------
    canal = channel.VoiceChannel
    if not canal:           
        voz = get(bot.voice_clients,guild=guild)
        await voz.disconnect()
    # -------------------------------
    await bot.change_presence(activity= discord.Game(name="Ingresa >"))
    print("BOT ONLINE")
# --------------------------------------------------------
@tasks.loop(seconds=20)
async def status(ctx):
    await client.change_presence(activity=discord.Game(choice(status)))

# --------------------------------------------------------
@bot.command(name='ping',help='This command return the latency')
async def ping(ctx):
    await ctx.send(f'**pong!** Latency: {round(bot.latency * 1000)}ms')
# --------------------------------------------------------
@bot.command(pass_context=True)
async def ven(ctx):
    canal = ctx.message.author.voice.channel
    if not canal:
        await ctx.send('No estas conectado a un canal de VOZ')
        return
    voz = get(bot.voice_clients,guild=ctx.guild)
    if voz and voz.is_connected():
        await voz.move_to(canal)
    else:
        voz= await canal.connect()
# --------------------------------------------------------
@bot.command(pass_context=True)
async def vete(ctx):
    canal = ctx.message.author.voice.channel
    voz = get(bot.voice_clients,guild=ctx.guild)
    await voz.disconnect()
# --------------------------------------------------------
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
# --------------------------------------------------------
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        # loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


client = commands.Bot(command_prefix='?')

status = ['Jamming out to music!', 'Eating!', 'Sleeping!']

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='general')
    await channel.send(f'Welcome {member.mention}!  Ready to jam out? See `?help` command for details!')
@bot.command(pass_context=True)
async def play1(ctx,*, search):
    # --------------------------------------------------------
    try:
        canal = ctx.message.author.voice.channel
    except:
        await ctx.send('No estas conectado a un canal de VOZ')
        return
    voz = get(bot.voice_clients,guild=ctx.guild)
    if voz and voz.is_connected():
        await voz.move_to(canal)
    else:
        voz= await canal.connect()
    # --------------------------------------------------------
    query_string= parse.urlencode({'search_query':search})
    html_content = request.urlopen('https://www.youtube.com/results?' + query_string)
    search_results = re.findall( r"watch\?v=(\S{11})", html_content.read().decode())
    await ctx.send("https://www.youtube.com/watch?v="+search_results[0])
# --------------------------------------------------------
    def revisar_lista():
        LR_en_Archivo=os.path.isdir("./Lista")
        if LR_en_Archivo is True:
            DIR = os.path.abspath(os.path.realpath("Lista"))
            tamaño = len(os.listdir(DIR))
            C_Activa=tamaño-1
            try:
                C_primera=os.listdir(DIR)[0]
            except:
                print("No hay canciones\n")
                listar.clear()
                return
            locatizacion_principal = os.path.dirname(os.path.realpath(__file__))
            C_localizacion = os.path.abspath(os.path.realpath("Lista")+"\\"+C_primera)
            if tamaño !=0:
                print("Cancion Lista, Se reproducira en breve")
                print(f"Canciones en la Lista: {C_Activa}")
                C_Encontrada= os.path.isfile("cancion.mp3")
                if C_Encontrada:
                    os.remove("cancion.mp3")
                    shutil.move(C_localizacion,locatizacion_principal)
                    for file in os.listdir("./"):
                        if file.endswith(".mp3"):
                            os.rename(file,'cancion.mp3')
                    voice.play(discord.FFmpegPCMAudio("cancion.mp3"),after=lambda e:revisar_lista())
                    voice.source=discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume= 20
                else:
                    listar.clear()
                    return
            else:
                listar.clear()
                print("No se agrego la cancion a la lista")
    
    if not canal:           
        canal = ctx.message.author.voice.channel
        voz = get(bot.voice_clients,guild=ctx.guild)
        await voz.disconnect()
# --------------------------------------------------------
    C_Encontrada= os.path.isfile("cancion.mp3")
    try:
        if C_Encontrada:
            os.remove("cancion.mp3")
            listar.clear()
            print("removido archivo antiguo")
    except PermissionError:
        print("se ha intentado eliminar un archivo pero este se encuentra Reproduccion")
        await ctx.send("ERROR: Cancion aun se esta reproduciendo")
        return
    LR_en_Archivo = os.path.isdir("./Lista")
    try:
        LR_Carpeta="./Lista"
        if LR_en_Archivo is True:
            print("Removida la carpeta Antigua")
            shutil.rmtree(LR_Carpeta)
    except:
        print("No hay carpeta")
    await ctx.send("En breve se reproducira la cancion")
    voice=get(bot.voice_clients,guild=ctx.guild)
    ydl_op={
        'format':'bestaudio/best',
        'quiet': True,
        'postprocessors':[{
            'key':'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality':'192',       
        }],
    }
    with youtube_dl.YoutubeDL(ydl_op)as ydl:
        print("Descargando cancion\n")
        link= search_results[0]
        ydl.download([link])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name2 = file
            print(f"Rembrando archivo: {file}\n")
            os.rename(file,"cancion.mp3")
    voz=get(bot.voice_clients,guild=ctx.guild)
    voz.play(discord.FFmpegPCMAudio("cancion.mp3"), after=lambda e: revisar_lista())
    voz.source=discord.PCMVolumeTransformer(voz.source)
    voz.source.volume= 20

    nombre= name2.rsplit("-",2)
    await ctx.send(f"Reproduciendo: {nombre[0]}\n")
# --------------------------------------------------------
@bot.command(pass_context=True)
async def awanta(ctx):
    voz=get(bot.voice_clients,guild=ctx.guild)

    if voz and voz.is_playing():
        print("Musica Pausada")
        voz.pause()
        await ctx.send("Musica Pausada")
    else:
        print("No se esta reproduciendo, Pausa erronea")
        await ctx.send("No se esta reproduciendo, Pausa erronea")
# --------------------------------------------------------
@bot.command(pass_context=True)
async def continua(ctx):
    voz=get(bot.voice_clients,guild=ctx.guild)

    if voz and voz.is_paused():
        print("Reproduciendo nuevamente")
        voz.resume()
        await ctx.send("Reproduciendo Nuevamente")
    else:
        print("No se escuentra Pausada ninguna musica")
        await ctx.send("No se escuentra Pausada ninguna musica")
# --------------------------------------------------------
@bot.command(pass_context=True)
async def stop(ctx):
    voz=get(bot.voice_clients,guild=ctx.guild)
    if voz and voz.is_playing():
        print("Musica detenida")
        voz.stop()
        await ctx.send("Musica Detenida")
    else:
        print("No se esta reproduciendo")
        await ctx.send("Musica Detenida")
# --------------------------------------------------------

# --------------------------------------------------------
listar={}
@bot.command(pass_context=True)
async def lista(ctx,*,search):
    # --------------------------------------------------------
    query_string= parse.urlencode({'search_query':search})
    html_content = request.urlopen('https://www.youtube.com/results?' + query_string)
    search_results = re.findall( r"watch\?v=(\S{11})", html_content.read().decode())
    # await ctx.send("https://www.youtube.com/watch?v="+search_results[0])
    # --------------------------------------------------------
    cancion_lista = os.path.isdir("./Lista")
    if cancion_lista is False:
        os.mkdir("Lista")
    DIR = os.path.abspath(os.path.realpath("Lista"))
    Lista_num = len(os.listdir(DIR))
    Lista_num+=1
    AgragarLista=True
    while AgragarLista:
        if Lista_num in listar:
            Lista_num=+1
        else:
            AgragarLista = False
            listar[Lista_num]= Lista_num

    Lista_path=os.path.abspath(os.path.realpath("Lista") + f"\cancion{Lista_num}.%(ext)s")
    
    ydl_op = {
        'format': 'bestaudio/best',
        'quiet':True,
        'outtmpl':Lista_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality':'192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_op) as ydl:
        print("Descargar cancion")
        link= search_results[0]
        ydl.download([link])
    await ctx.send("Añadida la cancion nro "+str(Lista_num)+" a la lista de Reproduccion")
    print("Cancion añadida")
# --------------------------------------------------------
@bot.command(name='play', help='This command plays music')
async def play(ctx,*, url):

    query_string= parse.urlencode({'search_query':url})
    html_content = request.urlopen('https://www.youtube.com/results?' + query_string)
    search_results = re.findall( r"watch\?v=(\S{11})", html_content.read().decode())
    # await ctx.send("https://www.youtube.com/watch?v="+search_results[0])

    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(search_results[0], loop=client.loop)
        voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('**Now playing:** {}'.format(player.title))

@tasks.loop(seconds=20)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))
bot.run('TOKEN')


