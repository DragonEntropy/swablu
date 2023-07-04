import discord
import os
from dotenv import load_dotenv
import requests

load_dotenv()
client = discord.Client()

gen = 1
gen_dictionary = {1:"I", 2:"II", 3:"III", 4:"IV", 5:"V", 6:"VI", 7:"VII", 8:"VIII"}
gen_games = {1:"rb", 2:"gs", 3:"rs", 4:"dp", 5:"bw", 6:"xy", 7:"sm", 8:"ss"}
bulba_exceptions = {"mr mime":"mr._Mime", "Mime jr":"mime_Jr.", "mr rime":"mr._Rime"}

def validate(pokemon):
    try:
        api = "https://pokeapi.co/api/v2/pokemon/" + pokemon.replace(" ", "-").replace("'", "")
        r = requests.get(api).json()
        r["name"]
        return True
    except:
        return False

def reformat(data):
    return data.replace(" ", "-").replace("'", "").replace("%","")
    

@client.event
async def on_ready():
    print("Swablu has soared into the server!")

@client.event
async def on_message(message):
    global gen
    if message.content.startswith("&help"):
        await message.channel.send("""Below is the current list of commands of me!
        **&help** : Allows you to see all my available commands
        **&ability** *<ability name>* : Gives a brief descripton of an ability
        **&gen** *<generation number>* : Sets my generation
        **&learnset** *<pokemon name>* : Generates a bulbapedia link to the pokemon's learnset
        **&move** *<move name>* : Gives a thorough description of a move
        **&nature** *<nature name>* : Provides the effect of a nature
        **&nature list** : Provides a list of all natures and there effects
        **&pet** : ? ? ?
        **&smogon** *<pokemon name>* : Creates a smogon link to the pokemon's competitive overview
        **&stats** *<pokemon name>* : Provides the base stats of a pokemon
        **&type** *<pokemon name>* : Gives a pokemon's types
    """)

#Returns a description of an ability
    elif message.content.startswith("&ability "):
        ability = message.content[9:].lower()
        ability_f = reformat(ability)
        try:
            api = "https://pokeapi.co/api/v2/ability/" + ability_f
            r = requests.get(api).json()
            for i in range(0, 50):
                if r["effect_entries"][i]["language"]["name"] == "en":
                    description = r["effect_entries"][i]["short_effect"]
                    await message.channel.send("Below is a description of the ability **" + ability + "**: \n    *" + description + "*")
                    #print("Ability number " + str(i))
                    break
        except:
            await message.channel.send("This ability does not exist!")

#Allows the generation to be changed
    elif message.content.startswith("&gen "):
        try:
            generation = int(message.content[5:])
            if gen_dictionary.get(generation) != None:
                gen = generation
                await message.channel.send("The generation was switched to gen " + str(gen))
            else:
                await message.channel.send("This generation is not valid! (Generations must be from 1 to 8)")
        except:
            await message.channel.send("This generation is not valid! (Generations must be from 1 to 8)")

#Returns the bulbapedia link for the pokemon's learnset
    elif message.content.startswith("&learnset "):
        pokemon = message.content[10:].lower()
        if pokemon in bulba_exceptions:
            pokemon_f = bulba_exceptions.get(pokemon)
        else:
            pokemon_f = pokemon.replace(" ", "_")
        if validate(pokemon.replace(" ", "-").replace("'", "")):
            learnset_url = "https://bulbapedia.bulbagarden.net/wiki/{0}_(Pokémon)/Generation_{1}_learnset".format(pokemon_f, gen_dictionary.get(gen))
            await message.channel.send(pokemon_f.capitalize() + "'s learnset can be found through this link: \n" + learnset_url)
        else:
            await message.channel.send("This pokemon does not exist!")

#Returns a thorough description of a move
    elif message.content.startswith("&move "):
        move = message.content[6:].lower()
        move_f = reformat(move)
        try:
            api = "https://pokeapi.co/api/v2/move/" + move_f
            r = requests.get(api).json()
            damage_class = r["damage_class"]["name"]
            if damage_class == "status":
                power = 0
            else:
                power = r["power"]
                if power == None:
                    power = "varying"
            typing = r["type"]["name"]
            accuracy = r["accuracy"]
            pp = r["pp"]
            priority = r["priority"]
            if accuracy == None:
                accuracy = "infinite"
            effects = r["effect_entries"][0]["short_effect"]
            effect_chance = r["effect_chance"]
            target = r["target"]["name"].replace("-", " ").capitalize()
            output = """Below is a description of the move **{0}**: 
    It is a **{1}** move with type **{2}**
    Its power and accuracy are **{3}** and **{4}** respectively
    It has **{5}** pp and a priority of **{6}**
    The target of the move: {7}
    Move description: *{8}*""".format(move, damage_class, typing, power, accuracy, pp, priority, target, effects)
            await message.channel.send(output.replace("$effect_chance%", "**" + str(effect_chance) + "%**"))
        except:
            await message.channel.send("This move does not exist!")

#Returns the effect of a nature
    elif message.content.startswith("&nature "):
        nature = message.content[8:].lower()
        if nature == "list":
            output = "Below is a complete summary of each nature:"
            for i in range(1, 26):
                api = "https://pokeapi.co/api/v2/nature/" + str(i)
                r = requests.get(api).json()
                name = r["name"]
                if r["increased_stat"] == None:
                    output = output + "\n    **{0}** : No stat changes".format(name.capitalize())
                else:
                    increased = r["increased_stat"]["name"]
                    decreased = r["decreased_stat"]["name"]
                    output = output + "\n    **{0}** : Increased {1}, decreased {2}".format(name.capitalize(), increased, decreased)
        else:
            try:
                api = "https://pokeapi.co/api/v2/nature/" + nature
                r = requests.get(api).json()
                if r["increased_stat"] == None:
                    output = "**{0}** : No stat changes".format(nature.capitalize())
                else:
                    increased = r["increased_stat"]["name"]
                    decreased = r["decreased_stat"]["name"]
                    output = "**{0}** : Increased {1}, decreased {2}".format(nature.capitalize(), increased, decreased)            
            except:
                output = "This nature does not exist!"
        await message.channel.send(output.replace("-", " "))

#Pets the swablu
    elif message.content.startswith("&pet"):
        print("uwu")

#Returns a smogon link for the pokemon
    elif message.content.startswith("&smogon "):
        pokemon = message.content[8:].lower()
        pokemon_f = reformat(pokemon)
        if validate(pokemon):
            smogon_url = "https://www.smogon.com/dex/{0}/pokemon/{1}/".format(gen_games.get(gen), pokemon_f)
            await message.channel.send(pokemon.capitalize() + "'s competitive overview can be found through this link: \n" + smogon_url)
        else:
            await message.channel.send("This pokemon does not exist!")

#Returns the base stats of the pokemon
    elif message.content.startswith("&stats "):
        pokemon = message.content[7:].lower()
        pokemon_f = reformat(pokemon)
        try:
            api = "https://pokeapi.co/api/v2/pokemon/" + pokemon
            r = requests.get(api).json()
            stats = []
            for stat in range(6):
                base_stat =  r["stats"][stat]["base_stat"]
                stats.append(base_stat)
            await message.channel.send("""{0}'s base stats are:
    HP: **{1}**
    Attack: **{2}**
    Defence: **{3}**
    Special Attack: **{4}**
    Special Defence: **{5}**
    Speed: **{6}**""".format(pokemon.capitalize(), stats[0], stats[1], stats[2], stats[3], stats[4], stats[5]))
        except:
            await message.channel.send("This pokemon does not exist!")

#Returns the pokemon's type/types
    elif message.content.startswith("&type "):
        pokemon = message.content[6:].lower()
        pokemon_f = reformat(pokemon)
        try:
            api = "https://pokeapi.co/api/v2/pokemon/" + pokemon_f
            r = requests.get(api).json()
            if gen < 6:
                try:
                    type_set = r["past_types"][0]["types"]
                except:
                    type_set = r["types"]
            else:
                type_set = r["types"]
            type1 = type_set[0]["type"]["name"]
            try:
                type2 = type_set[1]["type"]["name"]
                await message.channel.send("{0}'s types are {1} and {2}".format(pokemon, type1, type2).capitalize())
            except:
                type2 = None
                await message.channel.send("{0}'s type is {1}".format(pokemon, type1).capitalize())
        except:
            await message.channel.send("This pokemon could not be found")

#Runs if an invalid command is provided
    elif message.content.startswith("&"):
        await message.channel.send("""It seems that you have either:
        *- Tried to use a command that I do not understand*
        *- Forgotten to add part of a command*
Try &help to see a list of available commands and their usages
        """)
    
client.run(os.getenv('TOKEN'))
