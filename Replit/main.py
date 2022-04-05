# image = http://media-cache-ak0.pinimg.com/736x/b1/53/27/b15327b45365045b2fa4462dbc61c00b.jpg

from random import randrange
import discord
from discord.ext import commands
import json
import os
# os.system("cls")
from keep_alive import keep_alive

atrchange = {"agi": "Agilidade",
             "car": "Carisma",
             "con": "Constituição",
             "for": "Força",
             "fur": "Furtividade",
             "int": "Inteligência",
             "pod": "Poder",
             "sab": "Sabedoria",
}

rpgslist = []
for filename in os.listdir("./"):
    if ".json" in filename:
        filename = filename.replace(".json", "")
        filename = filename.replace("Fichas", "")
        rpgslist.append(filename)

rpgatual = "Felipe"

bot = commands.Bot("$")

@bot.command(aliases=["ajuda"])
async def h(ctx):
    embed=discord.Embed(title="Comandos do Bot", color=0xffffff)
    embed.set_thumbnail(url="http://media-cache-ak0.pinimg.com/736x/b1/53/27/b15327b45365045b2fa4462dbc61c00b.jpg")
    # embed.add_field(name="", value="", inline=False)
    embed.add_field(name="$rpg [nome do rpg]", value="Sem nome = Vê o rpg atual | Com nome = Define o rpg atual", inline=False)
    embed.add_field(name="$rpgs", value="Vê rpgs existentes", inline=False)
    embed.add_field(name="$criar [nome]", value="Sem nome = Cria sua ficha do rpg | Com nome = Cria a ficha de um npc", inline=False)
    embed.add_field(name="$apelido [apelido]", value="Muda o apelido da sua ficha", inline=False)
    embed.add_field(name="$deletar [nome]", value="Deleta a ficha do rpg", inline=False)
    embed.add_field(name="$ficha [nome]", value="Sem nome = Vê sua ficha | Com nome = Vê a ficha de um npc", inline=False)
    embed.add_field(name="$fichas", value="Vê fichas existentes", inline=False)
    embed.add_field(name="$atr [nome]", value="Sem nome = Vê seus atributos | Com nome = Vê atributos de um npc", inline=False)
    embed.add_field(name="$atr [nome] [atributo] [valor]", value="Sem nome = Altera seus atributos | Com nome = Altera atributos de um npc", inline=False)
    embed.add_field(name="$d100 [nome] [atributo] [modificador]", value="Joga dados", inline=False)
    embed.add_field(name="$ds100 [numero de dados] [nome] [atributo] [modificador]", value="Joga dados [numero] vezes", inline=False)
    embed.add_field(name="$hp [nome]", value="Sem nome = Vê seu HP | Com nome = Vê HP de um npc", inline=False)
    embed.add_field(name="$hp [nome] [número]", value="Sem nome = Adiciona ou diminui o número do seu hp | Com nome = Adiciona ou diminui o número de HP de um npc", inline=False)
    embed.set_footer(text="$sug [escreva a sugestão que irá ser enviada para um arquivo a qual eu lerei e tentarei implementar o mais rapido possível]")
    await ctx.send(embed=embed)

@bot.command()
async def rpg(ctx, rpgname=""):
    global rpgatual
    rpgname = rpgname.capitalize()
    if rpgname != "":
        if rpgname in rpgslist:
            rpgatual = rpgname
            await ctx.send(f"**Rpg definido para {rpgatual}**")
            atualizarjson()
        else:
            await ctx.send("**Esse rpg ainda não existe no meu banco de dados**")
    else:
        await ctx.send(f"**Rpg atual é {rpgatual}**")

@bot.command()
async def rpgs(ctx):
    resultado = ", ".join(rpgslist)
    await ctx.send(f"**{resultado}**")

with open(f"./Fichas{rpgatual}.json", "r+", encoding="UTF-8") as json_file:
        data = json.load(json_file)

def atualizarjson():
    global data
    with open(f"./Fichas{rpgatual}.json", "r+", encoding="UTF-8") as json_file:
        data = json.load(json_file)

atualizarjson()

def load_ficha():
    pass


@bot.event
async def on_ready():
        print(f'{bot.user.display_name} está pronta!')

@bot.command()
async def clear(ctx, amount=5):
	await ctx.channel.purge(limit=(amount + 1),  check=lambda msg: not msg.pinned)

@bot.command()
async def atr(ctx, atributo=None, newnumber=None, nome=None):
    if atributo in atrchange.keys():
        atributo = atrchange[atributo]
    if newnumber in atrchange.keys():
        newnumber = atrchange[newnumber]
    if atributo:
        atributo = atributo.capitalize()
    if nome:
        nome = nome.capitalize()
    atualizarjson()
    if atributo == None:
        if ctx.author.name.capitalize() in data.keys():
            apelido = data[ctx.author.name.capitalize()]["Atributos"]["Apelido"]
            embed=discord.Embed(title=f"Atributos de {apelido}", color=int(data[ctx.author.name.capitalize()]["Atributos"]["Cor"], 16))
            embed.set_thumbnail(url=data[ctx.author.name.capitalize()]["Atributos"]["Imagem"])
            embed.add_field(name="💪│Força", value=data[ctx.author.name.capitalize()]["Atributos"]["Força"], inline=False)
            embed.add_field(name="💨│Agilidade", value=data[ctx.author.name.capitalize()]["Atributos"]["Agilidade"], inline=False)
            embed.add_field(name="🛡️│Constituição", value=data[ctx.author.name.capitalize()]["Atributos"]["Constituição"], inline=False)
            embed.add_field(name="🐲│Sabedoria", value=data[ctx.author.name.capitalize()]["Atributos"]["Sabedoria"], inline=False)
            embed.add_field(name="📚│Inteligência", value=data[ctx.author.name.capitalize()]["Atributos"]["Inteligência"], inline=False)
            embed.add_field(name="🥷🏿│Furtividade", value=data[ctx.author.name.capitalize()]["Atributos"]["Furtividade"], inline=False)
            embed.add_field(name="💘│Carisma", value=data[ctx.author.name.capitalize()]["Atributos"]["Carisma"], inline=False)
            embed.add_field(name="🎖️│Poder", value=data[ctx.author.name.capitalize()]["Atributos"]["Poder"], inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("**É necessário criar uma ficha primeiro! ($criar)**")
    elif newnumber == None:
        if atributo in data["modelo"]["Atributos"].keys():
            atributo = atributo.capitalize()
            await ctx.send(f"**Seu valor de {atributo} é " + str(data[ctx.author.name.capitalize()]["Atributos"][atributo]) + "**")
        else:
            nome = atributo
            if nome in data.keys():
                embed=discord.Embed(title=f"Atributos de {nome}", color=int(data[nome]["Atributos"]["Cor"], 16))
                embed.set_thumbnail(url=data[nome]["Atributos"]["Imagem"])
                embed.add_field(name="💪│Força", value=data[nome]["Atributos"]["Força"], inline=False)
                embed.add_field(name="💨│Agilidade", value=data[nome]["Atributos"]["Agilidade"], inline=False)
                embed.add_field(name="🛡️│Constituição", value=data[nome]["Atributos"]["Constituição"], inline=False)
                embed.add_field(name="🐲│Sabedoria", value=data[nome]["Atributos"]["Sabedoria"], inline=False)
                embed.add_field(name="📚│Inteligência", value=data[nome]["Atributos"]["Inteligência"], inline=False)
                embed.add_field(name="🥷🏿│Furtividade", value=data[nome]["Atributos"]["Furtividade"], inline=False)
                embed.add_field(name="💘│Carisma", value=data[nome]["Atributos"]["Carisma"], inline=False)
                embed.add_field(name="🎖️│Poder", value=data[nome]["Atributos"]["Poder"], inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send("**Essa ficha não existe**")
    elif nome==None:
        if newnumber[0].isdigit():
            atributo = atributo.capitalize()
            with open(f"./Fichas{rpgatual}.json", "r+", encoding="UTF-8") as json_file:
                dataatr = json.load(json_file)
                dataatr[ctx.author.name.capitalize()]["Atributos"][atributo] = newnumber
                json_file.seek(0) 
                json_file.write(json.dumps(dataatr))
                json_file.truncate()
                atributovalor = dataatr[ctx.author.name.capitalize()]["Atributos"][atributo]
                await ctx.send(f"**Seu valor de {atributo} foi atualizado para {atributovalor}**")
        else:
            newnumber = newnumber.capitalize()
            if newnumber in data["modelo"]["Atributos"].keys():
                atributo = atributo.capitalize()
                await ctx.send(f"**Valor de {newnumber} de {atributo} é " + str(data[atributo]["Atributos"][newnumber]) + "**")
            else:
                await ctx.send(f"**Esse atributo não existe**")
    else:
        newnumber = newnumber.capitalize()
        with open(f"./Fichas{rpgatual}.json", "r+", encoding="UTF-8") as json_file:
            dataatr = json.load(json_file)
            dataatr[atributo]["Atributos"][newnumber] = nome
            json_file.seek(0) 
            json_file.write(json.dumps(dataatr))
            json_file.truncate()
            atributovalor = dataatr[atributo]["Atributos"][newnumber]
            await ctx.send(f"**Valor de {newnumber} de {atributo} foi atualizado para {nome}**")
            

@bot.command()
async def apelido(ctx, nome=""):
    nome = nome.capitalize()
    with open(f"./Fichas{rpgatual}.json", "r+", encoding="UTF-8") as json_file:
            data = json.load(json_file)
            data[ctx.author.name.capitalize()]["Atributos"]["Apelido"] = nome
            json_file.seek(0) 
            json_file.write(json.dumps(data))
            json_file.truncate()
            await ctx.send(f"**Apelido definido**")
            apelido = data[ctx.author.name.capitalize()]["Atributos"]["Apelido"]
            hpinit = data[ctx.author.name.capitalize()]["Atributos"]["HP"]
            hpfinal = int(12 + (int(data[ctx.author.name.capitalize()]["Atributos"]["Constituição"])/5))
            apelido = f"{apelido} {hpinit}/{hpfinal}"
            await ctx.author.edit(nick=apelido)


@bot.command()
async def ficha(ctx, nome=None):
    atualizarjson()
    if nome:
        nome = nome.capitalize()
    if nome==None:
        with open(f"./Fichas{rpgatual}.json", encoding="UTF-8") as json_file:
            data = json.load(json_file)
        if ctx.author.name.capitalize() in data.keys():
            hpinit = data[ctx.author.name.capitalize()]["Atributos"]["HP"]
            hpfinal = int(12 + (int(data[ctx.author.name.capitalize()]["Atributos"]["Constituição"])/5))
            apelido = data[ctx.author.name.capitalize()]["Atributos"]["Apelido"]
            embed=discord.Embed(title=f"Ficha de {apelido}", color=int(data[ctx.author.name.capitalize()]["Atributos"]["Cor"], 16))
            embed.set_thumbnail(url=data[ctx.author.name.capitalize()]["Atributos"]["Imagem"])
            embed.add_field(name="❤️‍🔥│HP", value=f"{hpinit} / {hpfinal}", inline=False)
            embed.add_field(name="🏋️‍♂️│P.E", value=(data[ctx.author.name.capitalize()]["Atributos"]["Poder"]), inline=False)
            embed.add_field(name="🧠│Sanidade", value=data[ctx.author.name.capitalize()]["Atributos"]["Poder"], inline=False)
            embed.add_field(name="👟│Movimento", value=(int(data[ctx.author.name.capitalize()]["Atributos"]["Agilidade"])/10), inline=False)
            embed.add_field(name="💪│Peso Carregável", value=data[ctx.author.name.capitalize()]["Atributos"]["Força"], inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("**É necessário criar uma ficha primeiro! ($criar)**")
    else:
        with open(f"./Fichas{rpgatual}.json", encoding="UTF-8") as json_file:
            data = json.load(json_file)
        if nome in data.keys():
            hpinit = data[nome]["Atributos"]["HP"]
            hpfinal = int(12 + (int(data[nome]["Atributos"]["Constituição"])/5))

            embed=discord.Embed(title=f"Ficha de {nome}", color=int(data[nome]["Atributos"]["Cor"], 16))
            embed.set_thumbnail(url=data[nome]["Atributos"]["Imagem"])
            embed.add_field(name="❤️‍🔥│HP", value=f"{hpinit} / {hpfinal}", inline=False)
            embed.add_field(name="🏋️‍♂️│P.E", value=(data[nome]["Atributos"]["Poder"]), inline=False)
            embed.add_field(name="🧠│Sanidade", value=data[nome]["Atributos"]["Poder"], inline=False)
            embed.add_field(name="👟│Movimento", value=(int(data[nome]["Atributos"]["Agilidade"])/10), inline=False)
            embed.add_field(name="💪│Peso Carregável", value=data[nome]["Atributos"]["Força"], inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("**Essa ficha não existe**")

@bot.command()
async def fichas(ctx):
    atualizarjson()
    if ctx.author.name.capitalize() == "Asteriuz":
        nomesemod = {i:data[i] for i in data if i!='modelo'}
        resultado = ", ".join((str(key) for key, value in nomesemod.items()))
        await ctx.send(f"**{resultado}**")
    else:
        await ctx.send("**Permissão necessária**")

@bot.command()
async def d100(ctx, nome, atributo=None, mod=0): 
    if atributo in atrchange.keys():
        atributo = atrchange[atributo]
    if nome in atrchange.keys():
        nome = atrchange[nome]
    nome = nome.capitalize()
    if nome in data["modelo"]["Atributos"].keys():
        if atributo != None:
            mod = atributo
            mod = int(mod)
        atributo = nome
        if ctx.author.name.capitalize() in data.keys(): 
            x = randrange(1,101)
            if ctx.author.name == "alerochao":
                x = 1
            x = x + mod
            atr = int(data[ctx.author.name.capitalize()]["Atributos"][atributo.capitalize()])

            resultado = ""
            cor = ""
            if x <= (atr/10):
                resultado = "Extremo"
                cor = 0xff00dd
            elif x <= (atr/5):
                resultado = "Muito Bom"
                cor = 0x048302
            elif x <= (atr/2):
                resultado = "Bom"
                cor = 0x04ff00
            elif x <= atr:
                resultado = "Normal"
                cor = 0xfbff00
            else:
                resultado = "Fracasso"
                cor = 0xfe0606
            
            if mod != 0:
                embed=discord.Embed(title=f"{x} | {resultado}", description=f"{x - mod}+({mod})={x} | {atributo.capitalize()} - {atr}", color=cor)
            else:
                embed=discord.Embed(title=f"{x} - {resultado}", description=f"{atributo.capitalize()} - {atr}", color=cor)
            # em bed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("**É necessário criar uma ficha primeiro! ($criar)**")
    else:
        if nome in data.keys(): 
            x = randrange(1,101)
            x = x + mod
            atr = int(data[nome]["Atributos"][atributo.capitalize()])

            resultado = ""
            cor = ""
            if x <= (atr/10):
                resultado = "Extremo"
                cor = 0xff00dd
            elif x <= (atr/5):
                resultado = "Muito Bom"
                cor = 0x048302
            elif x <= (atr/2):
                resultado = "Bom"
                cor = 0x04ff00
            elif x <= atr:
                resultado = "Normal"
                cor = 0xfbff00
            else:
                resultado = "Fracasso"
                cor = 0xfe0606

            if mod != 0:
                embed=discord.Embed(title=f"{x} | {resultado}", description=f"{x - mod}+({mod})={x} | {atributo.capitalize()} - {atr}", color=cor)
            else:
                embed=discord.Embed(title=f"{x} - {resultado}", description=f"{atributo.capitalize()} - {atr}", color=cor)
            # embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("**É necessário criar uma ficha primeiro! ($criar)**")

@bot.command()
async def ds100(ctx, number, nome="", atributo=None, mod=0):
    if atributo in atrchange.keys():
        atributo = atrchange[atributo]
    if nome in atrchange.keys():
        nome = atrchange[nome]
    nome = nome.capitalize()
    if not number.isdigit():
        await ctx.send("**$ds100 é preciso mandar o número de dados primeiro! (Caso seja só um dado use $d100)**")
    elif nome in data["modelo"]["Atributos"].keys():
        if atributo != None:
            
            mod = atributo
            mod = int(mod)
        atributo = nome
        if ctx.author.name.capitalize() in data.keys():
            vezes = 0
            while int(number) > vezes:
                x = randrange(1,101)
                if ctx.author.name == "alerochao":
                    x = 1
                x = x + mod
                atr = int(data[ctx.author.name.capitalize()]["Atributos"][atributo.capitalize()])

                resultado = ""
                cor = ""
                if x <= (atr/10):
                    resultado = "Extremo"
                    cor = 0xff00dd
                elif x <= (atr/5):
                    resultado = "Muito Bom"
                    cor = 0x048302
                elif x <= (atr/2):
                    resultado = "Bom"
                    cor = 0x04ff00
                elif x <= atr:
                    resultado = "Normal"
                    cor = 0xfbff00
                else:
                    resultado = "Fracasso"
                    cor = 0xfe0606
                
                if mod != 0:
                    embed=discord.Embed(title=f"{x} | {resultado}", description=f"{x - mod}+({mod})={x} | {atributo.capitalize()} - {atr}", color=cor)
                else:
                    embed=discord.Embed(title=f"{x} - {resultado}", description=f"{atributo.capitalize()} - {atr}", color=cor)
                # em bed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                vezes += 1
    else:
        if nome in data.keys(): 
            vezes = 0
            while int(number) > vezes:
                x = randrange(1,101)
                x = x + mod
                atr = int(data[nome]["Atributos"][atributo.capitalize()])

                resultado = ""
                cor = ""
                if x <= (atr/10):
                    resultado = "Extremo"
                    cor = 0xff00dd
                elif x <= (atr/5):
                    resultado = "Muito Bom"
                    cor = 0x048302
                elif x <= (atr/2):
                    resultado = "Bom"
                    cor = 0x04ff00
                elif x <= atr:
                    resultado = "Normal"
                    cor = 0xfbff00
                else:
                    resultado = "Fracasso"
                    cor = 0xfe0606

                if mod != 0:
                    embed=discord.Embed(title=f"{x} | {resultado}", description=f"{x - mod}+({mod})={x} | {atributo.capitalize()} - {atr}", color=cor)
                else:
                    embed=discord.Embed(title=f"{x} - {resultado}", description=f"{atributo.capitalize()} - {atr}", color=cor)
                # embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                vezes+=1
        else:
            await ctx.send("**Atributo não existe ou é necessário criar uma ficha primeiro! ($criar)**")


@bot.command()
async def hp(ctx, nome="", arg="0"):
    arg = arg.lstrip("+")
    nome = nome.lstrip("+")
    if nome == "reset":
         with open(f"./Fichas{rpgatual}.json", "r+", encoding="UTF-8") as json_file:
                data = json.load(json_file)
                await ctx.send(f"**Seu HP foi resetado**")
                hpfinal = int(12 + (int(data[ctx.author.name.capitalize()]["Atributos"]["Constituição"])/5))
                data[ctx.author.name.capitalize()]["Atributos"]["HP"] = hpfinal
                json_file.seek(0) 
                json_file.write(json.dumps(data))
                json_file.truncate()
                apelido = data[ctx.author.name.capitalize()]["Atributos"]["Apelido"]
                apelido = f"{apelido} {hpfinal}/{hpfinal}"
                await ctx.author.edit(nick=apelido)
    elif nome == "" or nome.lstrip("-").isdigit():
        nome.lstrip("+")
        arg = nome 
        if arg == "0" or nome == "":
            with open(f"./Fichas{rpgatual}.json", "r+", encoding="UTF-8") as json_file:
                data = json.load(json_file)
                await ctx.send(f"**Seu HP é " + str(data[ctx.author.name.capitalize()]["Atributos"]["HP"]) + "**")
                hpinit = data[ctx.author.name.capitalize()]["Atributos"]["HP"]
                hpfinal = int(12 + (int(data[ctx.author.name.capitalize()]["Atributos"]["Constituição"])/5))
                apelido = data[ctx.author.name.capitalize()]["Atributos"]["Apelido"]
                apelido = f"{apelido} {hpinit}/{hpfinal}"
                await ctx.author.edit(nick=apelido)
        elif arg.lstrip("-").isdigit():
            with open(f"./Fichas{rpgatual}.json", "r+", encoding="UTF-8") as json_file:
                data = json.load(json_file)
                data[ctx.author.name.capitalize()]["Atributos"]["HP"] = data[ctx.author.name.capitalize()]["Atributos"]["HP"] + int(arg)
                hpinit = data[ctx.author.name.capitalize()]["Atributos"]["HP"]
                hpfinal = int(12 + (int(data[ctx.author.name.capitalize()]["Atributos"]["Constituição"])/5))
                apelido = data[ctx.author.name.capitalize()]["Atributos"]["Apelido"]
                apelido = f"{apelido} {hpinit}/{hpfinal}"
                await ctx.author.edit(nick=apelido)
                json_file.seek(0) 
                json_file.write(json.dumps(data))
                json_file.truncate()
                hp = data[ctx.author.name.capitalize()]["Atributos"]["HP"]
                await ctx.send(f"**Seu HP foi atualizado para {hp}**")
        else:
            await ctx.send(f"**Envie um número!**")
    else:
        if arg == "0":
             with open(f"./Fichas{rpgatual}.json", "r+", encoding="UTF-8") as json_file:
                data = json.load(json_file)
                nome = nome.capitalize()
                await ctx.send(f"**O HP de {nome} é " + str(data[nome]["Atributos"]["HP"]) + "**")
        elif arg.lstrip("-").isdigit():
            nome = nome.capitalize()
            with open(f"./Fichas{rpgatual}.json", "r+", encoding="UTF-8") as json_file:
                data = json.load(json_file)
                data[nome]["Atributos"]["HP"] = data[nome]["Atributos"]["HP"] + int(arg)
                json_file.seek(0) 
                json_file.write(json.dumps(data))
                json_file.truncate()
                hp = data[nome]["Atributos"]["HP"]
                await ctx.send(f"**O HP de {nome} foi atualizado para {hp}**")
        else:
            await ctx.send(f"**Envie um número!**")
        

@bot.command()
async def criar(ctx, nome=None):
    if nome:
        nome = nome.capitalize()
    if nome == None:
        with open(f"./Fichas{rpgatual}.json", "r+", encoding="UTF-8") as json_file:
            data = json.load(json_file)
        if ctx.author.name.capitalize() in data.keys():
            await ctx.send(f"**Essa ficha já existe**")
        else:
            with open(f"./Fichas{rpgatual}.json", "r+", encoding="UTF-8") as json_file:
                data = json.load(json_file)
                data[ctx.author.name.capitalize()] = {"Atributos":{"Apelido":ctx.author.name.capitalize(),"Força":"0","Agilidade":"0","Constituição":0,"Sabedoria":0,"Inteligência":0,"Furtividade":0,"Carisma":0,"Poder":"0","HP":0,"Cor":"0x000000","Imagem":str(ctx.author.avatar_url)}}
                json_file.seek(0) 
                json_file.write(json.dumps(data))
                json_file.truncate()
                await ctx.send(f"**Sua ficha foi criada**")
    else:
        with open(f"./Fichas{rpgatual}.json", "r+", encoding="UTF-8") as json_file:
            data = json.load(json_file)
        if nome in data.keys():
            await ctx.send(f"**Essa ficha já existe**")
        else:
            with open(f"./Fichas{rpgatual}.json", "r+", encoding="UTF-8") as json_file:
                    data = json.load(json_file)
                    data[nome] = {"Atributos":{"Apelido":ctx.author.name.capitalize(),"Força":"0","Agilidade":"0","Constituição":0,"Sabedoria":0,"Inteligência":0,"Furtividade":0,"Carisma":0,"Poder":"0","HP":0,"Cor":"0x000000","Imagem":"https://t5z6q4c2.rocketcdn.me/wp-content/uploads/2019/10/ponto-de-interrogacao-como-usar-dicas-e-exemplos-1024x512.jpg"}}
                    json_file.seek(0) 
                    json_file.write(json.dumps(data))
                    json_file.truncate()
                    await ctx.send(f"**Ficha de {nome} foi criada**")

@bot.command()
async def deletar(ctx, nome=None):
    if nome:
        nome = nome.capitalize()
    if nome == None:
        with open(f"./Fichas{rpgatual}.json", "r+", encoding="UTF-8") as json_file:
                data = json.load(json_file)
                del data[ctx.author.name.capitalize()]
                json_file.seek(0) 
                json_file.write(json.dumps(data))
                json_file.truncate()
                await ctx.send(f"**Sua ficha foi deletada**")
    else:
        with open(f"./Fichas{rpgatual}.json", "r+", encoding="UTF-8") as json_file:
                data = json.load(json_file)
                del data[nome]
                json_file.seek(0) 
                json_file.write(json.dumps(data))
                json_file.truncate()
                await ctx.send(f"**Ficha de {nome} foi deletada**")


@bot.command()
async def nickchange(ctx, name):
    await ctx.guild.me.edit(nick=name)

@bot.command()
async def sug(ctx, *, text):
    with open(f"./Suggestion.txt", "a", encoding="UTF-8") as sug_file:
        sug_file.write(f"\n\n{text}")
        await ctx.send("**Sugestão enviada!**")


keep_alive()

try:
    bot.run('OTM4OTg1MTYwOTA3NTYzMDQ4.YfyQEw.6KzdEUCRxda5rIuNUItueBJOfSs')
except:
    os.system("kill 1")
