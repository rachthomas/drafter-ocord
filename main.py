#import statements
from drafter import *
from dataclasses import dataclass
from bakery import assert_equal
import random

#website desc and setup
set_website_title("OCorD")
set_site_information(author="Rachel Thomas",
                     description="Manage party members to defeat a monster, choosing either OFFENSE, CUNNING or DEFENSE (OCorD) in a luck-based, rock-paper-scissors-like battling format.",
                     sources="Drafter documentation. No AI was used to code this project.",
                     planning=["CS1 Final Project 0 - Planning.pdf","CS1 Final Project 1 - Design.pdf"],
                     links=["https://github.com/rachthomas/drafter-ocord"]
                     )
hide_debug_information()
set_website_framed(False)

#dataclasses
@dataclass
class Party_Member:
    name: str
    number: int
    hp: int
    perk: str
    choice: str
    effect: str

@dataclass
class Monster:
    name: str
    hp: int
    choice: str
    effect: str

@dataclass
class State:
    turn: str
    selection: str
    party_stats: list[Party_Member]
    monster_stats: Monster
    attack_damage: int
    
#helper functions
def determine_face(member: Party_Member) -> str:
    """
    Chooses a png of a face to be displayed on the fight screen based on the party member's number and effect.
    Args:
        member (Party_Member): The party member (from the list of party_stats) to be given a face
    Returns:
        str: The name of the png file
    """
    if member.hp == 0:
        return "partymemberdead.png"
    if member.effect == "x":
        return "partymember" + str(member.number) + "neutral.png"
    if member.effect == "weak":
        return "partymember" + str(member.number) + "weak.png"
    if member.effect == "strong":
        return "partymember" + str(member.number) + "strong.png"
    return "partymember" + str(member.number) + "neutral.png"

def determine_textbox(state: State) -> str:
    """
    Selects what the textbox at the top of the page is going to say (depending on the current turn).
    Args:
        state (State): The current state of the website
    Returns:
        str: A message to display
    """
    if "ocord" in state.turn:
        return "Select an attack."
    if state.turn == "monster prepares":
        return state.monster_stats.name + " prepares to attack..."
    if state.turn == "monster choice":
        return state.monster_stats.name + " chose " + state.monster_stats.choice.upper() + "!"
    if "party attack" in state.turn:
        return state.party_stats[int(state.turn[-1])-1].name + " attacks! " + state.monster_stats.name + " takes " + str(state.attack_damage) + " damage!"
    if "monster attack" in state.turn:
        return state.monster_stats.name + " attacks! " + state.party_stats[int(state.turn[-1])-1].name + " takes " + str(state.attack_damage) + " damage!"
    return "This wasn't supposed to happen."

def determine_ocord_text(state: State) -> Row:
    """
    If the turn is ocord, places a selection arrow in the top textbox based if the user is selecting
    offense, cunning, or defense.
    Args:
        state (State): The current state of the website
    Returns:
        Row: The words "offense", "cunning", and "defense", padded, with an arrow pointing to the current selection
    """
    if "ocord" not in state.turn:
        return Row("")
    if state.selection == "offense":
        return Row("> OFFENSE","CUNNING","DEFENSE", style_padding="10px")
    if state.selection == "cunning":
        return Row("OFFENSE","> CUNNING","DEFENSE", style_padding="10px")
    if state.selection == "defense":
        return Row("OFFENSE","CUNNING","> DEFENSE", style_padding="10px")
    return Row("")

def determine_monster_face(state: State) -> str:
    """
    Chooses a png of a monster to be displayed on the fight screen based on the current turn.
    Args:
        state (State): The current state of the website
    Returns:
        str: The name of the png file
    """
    if "party attack" in state.turn:
        return "monsterhurt.png"
    if "monster attack" in state.turn or state.turn == "monster choice":
        return "monsterattack.png"
    else:
        return "monsterneutral.png"

def determine_border (state: State, num: int) -> str:
    """
    Highlights the border around the party member's box if the current turn is related to them.
    Args:
        state (State): The current state of the website
    Returns:
        str: The pixel size and color the border should be
    """
    if str(num) in state.turn:
        return "6px solid black"
    else:
        return "3px solid black"

#global constants
#for easier change later
BASE_DAMAGE = 10.0
    
#route functions
@route
def index (state: State) -> Page:
    """
    Builds the starting screen.
    Args:
        state (State): The current state of the website
    Returns:
        Page: The page of the screen (title, monster image, description, and button to move to setup)
    """
    return Page(state, [
        Header("OCorD"),
        "\n",
        Div(
        Image("monstereyes.png",1000,300)
            ),
        "\n",
        "A monster approaches..."
        "\n",
        Button("Assemble Party Members", "setup")
        ])

@route
def setup (state: State) -> Page:
    """
    Builds the setup screen.
    Args:
        state (State): The current state of the website
    Returns:
        Page: The page of the screen (textbox, monster image, party members (image, name and select perk fields),
              perk descriptions, and button to move to update names and perks)
    """
    return Page(state, [
        Div(
        "Name your Party Members and select their perks.",
        style_border="3px solid black",
        style_padding="10px"
            ),
        "\n",
        Div(
        Image("monstereyes.png",1000,300),
            ),
        "\n",
        Row(
        Div(
        "\n",
        Image("partymember1neutral.png",150,150),
                "\n",
        TextBox("name1", state.party_stats[0].name),
                "\n",
        SelectBox("perk1", ["x", "X-X", "(<3)", "\o/"], state.party_stats[0].perk),
        style_padding="10px",
        style_border="3px solid black"
            ),
        Div(
        "\n",
        Image("partymember2neutral.png",150,150),
                "\n",
        TextBox("name2", state.party_stats[1].name),
                "\n",
        SelectBox("perk2", ["x", "X-X", "(<3)", "\o/"], state.party_stats[1].perk),
        style_padding="10px",
        style_border="3px solid black"
            ),
        Div(
        "\n",
        Image("partymember3neutral.png",150,150),
                "\n",
        TextBox("name3", state.party_stats[2].name),
                "\n",
        SelectBox("perk3", ["x", "X-X", "(<3)", "\o/"], state.party_stats[2].perk),
        style_padding="10px",
        style_border="3px solid black"
            ),
        Div(
        "\n",
        Image("partymember4neutral.png",150,150),
        "\n",
        TextBox("name4", state.party_stats[3].name),
                "\n",
        SelectBox("perk4", ["x", "X-X", "(<3)", "\o/"], state.party_stats[3].perk),
        style_padding="10px",
        style_border="3px solid black"
            )
            ),
        "\n",
        "Perk Descriptions: \n x-x Lethality - Deal More Damage \n (<3) Sheltered - Take Less Damage \n \o/ Praised - 20% Chance to Ignore Damage Taken",
        "\n",
        Button("Fight!", "update_names_and_perks")
        ])

@route
def update_names_and_perks (state: State, name1: str, name2: str, name3: str, name4: str, perk1: str, perk2: str, perk3: str, perk4: str) -> Page:
    """
    Adds the user selected names and perks to the state, initializes the turn and selection,
    then calls for the fight page to be built.
    Args:
        state (State): The current state of the website
        names 1-4 (str): The names inputted in the party member's textbox
        perks 1-4 (str): The perks selected in the party member's dropdown
    Returns:
        Page: The fight screen with updated state
    """
    state.party_stats[0].name = name1
    state.party_stats[1].name = name2
    state.party_stats[2].name = name3
    state.party_stats[3].name = name4
    state.party_stats[0].perk = perk1
    state.party_stats[1].perk = perk2
    state.party_stats[2].perk = perk3
    state.party_stats[3].perk = perk4
    state.turn = "ocord1"
    state.selection = "offense"
    return fight(state)

@route
def fight (state: State) -> Page:
    """
    Builds the fight screen.
    Args:
        state (State): The current state of the website
    Returns:
        Page: The page of the screen (textbox, monster image, party members (image, name, perk, hp),
              and buttons to select and move between selections)
    """
    return Page (state, [
        Div(
        determine_textbox(state),
        determine_ocord_text(state),
        style_border="3px solid black",
        style_padding="10px"
            ),
        "\n",
        Div(
        Image(determine_monster_face(state),1000,300),
            ),
        "\n",
        Row(
        Div(
        state.party_stats[0].choice.upper(),
        "\n",
        Image(determine_face(state.party_stats[0]),150,150),
                "\n",
        state.party_stats[0].name + " " + state.party_stats[0].perk,
                "\n",
        "HP: " + str(state.party_stats[0].hp),
        style_padding="10px",
        style_border=determine_border(state,1)
            ),
        "   ",
        Div(
        state.party_stats[1].choice.upper(),
        "\n",
        Image(determine_face(state.party_stats[1]),150,150),
                "\n",
        state.party_stats[1].name + " " + state.party_stats[1].perk,
                "\n",
        "HP: " + str(state.party_stats[1].hp),
        style_padding="10px",
        style_border=determine_border(state,2)
            ),
        "   ",
        Div(
        state.party_stats[2].choice.upper(),
        "\n",
        Image(determine_face(state.party_stats[2]),150,150),
                "\n",
        state.party_stats[2].name + " " + state.party_stats[2].perk,
                "\n",
        "HP: " + str(state.party_stats[2].hp),
        style_padding="10px",
        style_border=determine_border(state,3)
            ),
        "   ",
        Div(
        state.party_stats[3].choice.upper(),
        "\n",
        Image(determine_face(state.party_stats[3]),150,150),
        "\n",
        state.party_stats[3].name + " " + state.party_stats[3].perk,
                "\n",
        "HP: " + str(state.party_stats[3].hp),
        style_padding="10px",
        style_border=determine_border(state,4)
            ),
        Div(
        Button("<","left"),
        Button(">", "right"),
        Button("Z","select"),
        style_padding="10px"
        )
        )
        ])

@route
def left (state: State) -> Page:
    """
    When the left arrow button is pressed during ocord,
    moves the selection arrow depending on if there is another option to the left.
    Args:
        state (State): The current state of the website
    Returns:
        Page: The fight screen with updated state
    """
    if "ocord" in state.turn:
        if state.selection == "offense":
            return fight(state)
        if state.selection == "cunning":
            state.selection = "offense"
            return fight(state)
        if state.selection == "defense":
            state.selection = "cunning"
            return fight(state)
    else:
        return fight(state)

@route
def right (state: State) -> Page:
    """
    When the right arrow button is pressed during ocord,
    moves the selection arrow depending on if there is another option to the right.
    Args:
        state (State): The current state of the website
    Returns:
        Page: The fight screen with updated state
    """
    if "ocord" in state.turn:
        if state.selection == "offense":
            state.selection = "cunning"
            return fight(state)
        if state.selection == "cunning":
            state.selection = "defense"
            return fight(state)
        if state.selection == "defense":
            return fight(state)
    else:
        return fight(state)

@route
def select (state: State) -> Page:
    """
    This is a long one; it changes the turn when the select button is pressed. This is how the user both selects
    their chosen ocord and to "move on" from the turn after they read the resulting text.
    Here are the turns of the game, in order:
    - (the party member's choices and effects are reset to x)
    - ocord1: party member one chooses ocord (if alive)
    - ocord2: party member two chooses ocord (if alive)
    - ocord3: party member three chooses ocord (if alive)
    - ocord4: party member four chooses ocord (if alive)
    - monster prepares: calls determine_effects *(see function)
    - monster choice: the monster reveals its choice of ocord
    - party attack1: party member one attacks the monster for damage (if alive) (see determine_and_apply_damage function)
    - party attack2: party member two attacks the monster for damage (if alive)
    - party attack3: party member three attacks the monster for damage (if alive)
    - party attack4: party member four attacks the monster for damage (if alive)
    - (if the monster is dead, show win screen)
    - monster attack1: monster attacks party member1 for damage (if they are alive)
    - monster attack2: monster attacks party member2 for damage (if they are alive)
    - monster attack3: monster attacks party member3 for damage (if they are alive)
    - monster attack4: monster attacks party member4 for damage (if they are alive)
    - (if all players are dead, show lose screen)
    - (wrap back to the top)
    
    Args:
        state (State): The current state of the website
    Returns:
        Page: Ultimately the fight screen (unless the monster's hp is zero, then returns win screen) (unless all
                the party members' hp is zero, then returns lose screen) with updated state
    """
    if state.turn == "ocord1":
        state.party_stats[0].choice = state.selection
        if not state.party_stats[1].hp == 0:
            state.turn = "ocord2"
        elif not state.party_stats[2].hp == 0:
            state.turn = "ocord3"
        elif not state.party_stats[3].hp == 0:
            state.turn = "ocord4"
        else:
            state.turn = "monster prepares"
        return fight(state)
    if state.turn == "ocord2":
        state.party_stats[1].choice = state.selection
        if not state.party_stats[2].hp == 0:
            state.turn = "ocord3"
        elif not state.party_stats[3].hp == 0:
            state.turn = "ocord4"
        else:
            state.turn = "monster prepares"
        return fight(state)
    if state.turn == "ocord3":
        state.party_stats[2].choice = state.selection
        if not state.party_stats[3].hp == 0:
            state.turn = "ocord4"
        else:
            state.turn = "monster prepares"
        return fight(state)
    if state.turn == "ocord4":
        state.party_stats[3].choice = state.selection
        state.turn = "monster prepares"
        return fight(state)
    if state.turn == "monster prepares":
        return determine_effects(state)
    if state.party_stats[0].hp == 0 and state.party_stats[1].hp == 0 and state.party_stats[2].hp == 0 and state.party_stats[3].hp == 0:
        state.party_stats[0].hp = 100
        state.party_stats[1].hp = 100
        state.party_stats[2].hp = 100
        state.party_stats[3].hp = 100
        state.monster_stats.hp = 400
        state.party_stats[0].choice = "x"
        state.party_stats[1].choice = "x"
        state.party_stats[2].choice = "x"
        state.party_stats[3].choice = "x"
        state.party_stats[0].effect = "x"
        state.party_stats[1].effect = "x"
        state.party_stats[2].effect = "x"
        state.party_stats[3].effect = "x"
        return lose(state)
    if state.monster_stats.hp == 0:
        state.party_stats[0].hp = 100
        state.party_stats[1].hp = 100
        state.party_stats[2].hp = 100
        state.party_stats[3].hp = 100
        state.monster_stats.hp = 400
        state.party_stats[0].choice = "x"
        state.party_stats[1].choice = "x"
        state.party_stats[2].choice = "x"
        state.party_stats[3].choice = "x"
        state.party_stats[0].effect = "x"
        state.party_stats[1].effect = "x"
        state.party_stats[2].effect = "x"
        state.party_stats[3].effect = "x"
        return win(state)
    if state.turn == "monster choice":
        if state.party_stats[0].hp == 0:
            if not state.party_stats[1].hp == 0:
                state.turn = "party attack2"
            elif not state.party_stats[2].hp == 0:
                state.turn = "party attack3"
            else:
                state.turn = "party attack4"
        else:
            state.turn = "party attack1"
        return determine_and_apply_damage(state)
    if state.turn == "party attack1":
        if state.party_stats[1].hp == 0:
            if not state.party_stats[2].hp == 0:
                state.turn = "party attack3"
            elif not state.party_stats[3].hp == 0:
                state.turn = "party attack4"
            else:
                state.turn = "monster attack1"
        else:
            state.turn = "party attack2"
        return determine_and_apply_damage(state)
    if state.turn == "party attack2":
        if state.party_stats[2].hp == 0:
            if not state.party_stats[3].hp == 0:
                state.turn = "party attack4"
            else:
                if not state.party_stats[0].hp == 0:
                    state.turn = "monster attack1"
                else:
                    state.turn = "monster attack2"
        else:
            state.turn = "party attack3"
        return determine_and_apply_damage(state)
    if state.turn == "party attack3":
        if state.party_stats[3].hp == 0:
            if not state.party_stats[0].hp == 0:
                state.turn = "monster attack1"
            elif not state.party_stats[1].hp == 0:
                state.turn = "monster attack2"
            else:
                state.turn = "monster attack3"
        else:
            state.turn = "party attack4"
        return determine_and_apply_damage(state)
    if state.turn == "party attack4":
        if not state.party_stats[0].hp == 0:
            state.turn = "monster attack1"
        elif not state.party_stats[1].hp == 0:
            state.turn = "monster attack2"
        elif not state.party_stats[2].hp == 0:
            state.turn = "monster attack3"
        else:
            state.turn = "monster attack4"
        return determine_and_apply_damage(state)
    if state.turn == "monster attack1":
        if not state.party_stats[1].hp == 0:
            state.turn = "monster attack2"
        elif not state.party_stats[2].hp == 0:
            state.turn = "monster attack3"
        elif not state.party_stats[3].hp == 0:
            state.turn = "monster attack4"
        else:
            state.turn = "ocord1"
        return determine_and_apply_damage(state)
    if state.turn == "monster attack2":
        if not state.party_stats[2].hp == 0:
            state.turn = "monster attack3"
        elif not state.party_stats[3].hp == 0:
            state.turn = "monster attack4"
        elif not state.party_stats[0].hp == 0:
            state.turn = "ocord1"
        else:
            state.turn = "ocord2"
        return determine_and_apply_damage(state)
    if state.turn == "monster attack3":
        if not state.party_stats[3].hp == 0:
            state.turn = "monster attack4"
        elif not state.party_stats[0].hp == 0:
            state.turn = "ocord1"
        elif not state.party_stats[1].hp == 0:
            state.turn = "ocord2"
        else:
            state.turn = "ocord3"
        return determine_and_apply_damage(state)
    if state.turn == "monster attack4":
        if not state.party_stats[0].hp == 0:
            state.turn = "ocord1"
        elif not state.party_stats[1].hp == 0:
            state.turn = "ocord2"
        elif not state.party_stats[2].hp == 0:
            state.turn = "ocord3"
        else:
            state.turn = "ocord4"
    state.party_stats[0].choice = "x"
    state.party_stats[1].choice = "x"
    state.party_stats[2].choice = "x"
    state.party_stats[3].choice = "x"
    state.party_stats[0].effect = "x"
    state.party_stats[1].effect = "x"
    state.party_stats[2].effect = "x"
    state.party_stats[3].effect = "x"
    state.selection = "offense"
    return fight(state)

@route
def determine_effects (state: State) -> Page:
    """
    Determines if each party member's ocord choice is weak, strong, or neutral against the monster's choice,
    then sets that to their effect.
    Offense beats Cunning, Cunning beats Defense, Defense beats Offense.
    Args:
        state (State): The current state of the website
    Returns:
        Page: The fight screen with updated state
    """
    choice_list = ["offense", "cunning", "defense"]
    state.monster_stats.choice = choice_list[random.randint(0,2)]
    monster_choice = state.monster_stats.choice
    for member in state.party_stats:
        if monster_choice == "offense" and member.choice == "cunning":
            member.effect = "weak"
        else:
            if monster_choice == "offense" and member.choice == "defense":
                member.effect = "strong"
            else:
                if monster_choice == "cunning" and member.choice == "offense":
                    member.effect = "strong"
                else:
                    if monster_choice == "cunning" and member.choice == "defense":
                        member.effect = "weak"
                    else:
                        if monster_choice == "defense" and member.choice == "offense":
                            member.effect = "weak"
                        else:
                            if monster_choice == "defense" and member.choice == "cunning":
                                member.effect = "strong"
                            else:
                                member.effect = "x"
    state.turn = "monster choice"
    return fight(state)

@route
def determine_and_apply_damage (state:State) -> Page:
    """
    Calculates damage based on effect and perks. Subtracts damage from either player or monster depending
    on the current turn (who is attacking who).
    Args:
        state (State): The current state of the website
    Returns:
        Page: The fight screen with updated state
    """
    damage = BASE_DAMAGE
    if "party attack" in state.turn:
        if state.party_stats[int(state.turn[-1])-1].effect == "strong":
            damage = damage * 1.5
        if state.party_stats[int(state.turn[-1])-1].effect == "weak":
            damage = damage / 1.5
        if state.party_stats[int(state.turn[-1])-1].perk == "X-X":
            damage = damage * 1.2
        state.monster_stats.hp -= round(damage)
        if state.monster_stats.hp <= 0:
            state.monster_stats.hp = 0
    if "monster attack" in state.turn:
        if state.party_stats[int(state.turn[-1])-1].effect == "strong":
            damage = damage / 1.5
        if state.party_stats[int(state.turn[-1])-1].effect == "weak":
            damage = damage * 1.5
        if state.party_stats[int(state.turn[-1])-1].perk == "(<3)":
            damage = damage / 1.2
        if state.party_stats[int(state.turn[-1])-1].perk == "\o/":
            if random.randint(1,10) < 3:
                damage = 0
        state.party_stats[int(state.turn[-1])-1].hp -= round(damage)
        if state.party_stats[int(state.turn[-1])-1].hp <= 0:
            state.party_stats[int(state.turn[-1])-1].hp = 0
    state.attack_damage = round(damage)
    return fight(state)

@route
def win (state: State) -> Page:
    """
    Builds the win screen.
    Args:
        state (State): The current state of the website
    Returns:
        Page: The page of the screen (title, monster image, description, and button to move to setup)
    """
    return Page(state, [
        Header("The monster was defeated!"),
        "\n",
        Div(
        Image("monsterdead.png",1000,300)
            ),
        "\n",
        "Play again?"
        "\n",
        Button("Assemble Party Members", "setup")
        ])

@route
def lose (state: State) -> Page:
    """
    Builds the lose screen.
    Args:
        state (State): The current state of the website
    Returns:
        Page: The page of the screen (title, monster image, description, and button to move to setup)
    """
    return Page(state, [
        Header("The party was defeated..."),
        "\n",
        Div(
        Image("monstereyes.png",1000,300)
            ),
        "\n",
        "Try again?"
        "\n",
        Button("Assemble Party Members", "setup")
        ])

#initializing dataclasses for starting state
starting_party =  [
                    Party_Member("Name1", 1, 100,"x","x","x"),
                    Party_Member("Name2", 2, 100,"x","x","x"),
                    Party_Member("Name3", 3, 100,"x","x","x"),
                    Party_Member("Name4", 4, 100,"x","x","x")
                  ]

starting_monster = Monster("??? Beast", 500, "x", "x")

#start server
start_server(State("start", "x", starting_party, starting_monster, "x"))
