import discord
from discord.ext import commands
from model import get_class
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='.', intents=intents)

@bot.command()
async def check(ctx):  
        if not ctx.message.attachments:
            await ctx.send("📎 Por favor envía una imagen.")
            return

        for attachment in ctx.message.attachments:
            await attachment.save(f"./{attachment.filename}")
        
            # obtener resultado del modelo
            label, conf = get_class(
                model_path="./keras_model.h5",
                labels_path="labels.txt",
                image_path=f"./{attachment.filename}"
            )

            if conf > 0.60: 
                # limpiar label
                label = label.strip()

                # embed bonito
                embed = discord.Embed(
                    title="🔍 Análisis de imagen",
                    color=discord.Color.green()
                )

                embed.add_field(
                    name="📌 Detectado",
                    value=f"**{label}**",
                    inline=False
                )

                embed.add_field(
                    name="📊 Confianza",
                    value=f"**{conf:.2%}**",
                    inline=False
                )

                embed.set_image(url=attachment.url)
                embed.set_footer(text="Bot IA")



                await ctx.send(embed=embed)

            else: 
                await ctx.send("La imagen no se entiende muy bien porfavor envia otra para estar mas seguro")    
                    
        



@bot.event
async def on_ready():
    print(f'Hemos inciado sesion como {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hola! Soy un bot -- {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def info(ctx):
    await ctx.send(f'Este server se creo el 2/3/2026')


bot.run("TOKEN")