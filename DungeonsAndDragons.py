"""
dnd_lite.py - Mini Dungeons & Dragons en Python (Texto, intento numero 2)

Mejoras en esta versión:
- Sistema de input para que el jugador elija acciones en combate.
- Pausa al final del juego para evitar que la ventana se cierre.
- Manejo de opciones inválidas (elige atacar por defecto).
"""

import random
import math
import textwrap

# -----------------------
# Utilidades: dados
# -----------------------
def roll(sides=20, n=1):
    """Tira n dados de 'sides' lados y devuelve lista de resultados."""
    return [random.randint(1, sides) for _ in range(n)]

def d(sides):
    return roll(sides)[0]

def roll_d20(mod=0, advantage=False, disadvantage=False):
    """Tira un d20 con opcional ventaja/desventaja y aplica modificador."""
    if advantage and disadvantage:
        advantage = disadvantage = False
    if advantage:
        r1, r2 = roll(20, 2)
        raw = max(r1, r2)
    elif disadvantage:
        r1, r2 = roll(20, 2)
        raw = min(r1, r2)
    else:
        raw = d(20)
    total = raw + mod
    return raw, total

# -----------------------
# Sistema de personajes
# -----------------------
ATTRIBUTES = ["Fuerza", "Destreza", "Constitución", "Inteligencia", "Sabiduría", "Carisma"]

def generate_attributes(method="standard"):
    """Genera atributos: 'standard' distribuye valores predefinidos; 'random' 4d6 drop lowest."""
    if method == "standard":
        values = [15, 14, 13, 12, 10, 8]
        random.shuffle(values)
        return dict(zip(ATTRIBUTES, values))
    else:
        vals = []
        for _ in range(6):
            rolls = roll(6, 4)
            rolls.sort()
            vals.append(sum(rolls[1:]))
        return dict(zip(ATTRIBUTES, vals))

def modifier(score):
    """Modificador tipo D&D: floor((score - 10) / 2) usando math.floor"""
    return math.floor((score - 10) / 2)

class Character:
    def __init__(self, name, cls, attrs=None):
        self.name = name
        self.cls = cls
        self.level = 1
        self.xp = 0
        self.attrs = attrs or generate_attributes()
        self.prof_bonus = 2
        self.max_hp = self.compute_max_hp()
        self.hp = self.max_hp
        self.ac = self.compute_ac()
        self.inventory = {"Poción de curación": 1}
        self.spell_slots = self.compute_spell_slots()
        self.weapon = self.default_weapon()
        self.available_spells = self.class_spells()
        self.actions = []
        self.update_actions()

    def compute_max_hp(self):
        con_mod = modifier(self.attrs["Constitución"])
        hit_die = {"Guerrero": 10, "Pícaro": 8, "Mago": 6}.get(self.cls, 8)
        return hit_die + con_mod

    def compute_ac(self):
        dex = modifier(self.attrs["Destreza"])
        if self.cls == "Guerrero":
            return 16 + min(dex, 2)
        elif self.cls == "Pícaro":
            return 12 + dex
        elif self.cls == "Mago":
            return 10 + dex
        return 10 + dex

    def compute_spell_slots(self):
        return 2 if self.cls == "Mago" else 0

    def default_weapon(self):
        weapons = {
            "Guerrero": {"name": "Espada larga", "dmg": "1d8", "weap_mod": "Fuerza"},
            "Pícaro": {"name": "Daga", "dmg": "1d4", "weap_mod": "Destreza"},
            "Mago": {"name": "Bastón", "dmg": "1d6", "weap_mod": "Fuerza"},
        }
        return weapons.get(self.cls, {"name": "Puños", "dmg": "1d3", "weap_mod": "Fuerza"})

    def class_spells(self):
        if self.cls == "Mago":
            return {
                "Bola de fuego (1d6)": {"slots": 1, "dmg": "1d6", "uses": 2},
                "Rayo (1d8)": {"slots": 1, "dmg": "1d8", "uses": 2}
            }
        return {}

    def update_actions(self):
        actions = ["Atacar", "Defender", "Usar poción", "Huir"]
        if self.cls == "Pícaro":
            actions.append("Ataque sigiloso")
        if self.cls == "Mago" and self.spell_slots > 0:
            actions.append("Lanzar hechizo")
        self.actions = actions

    def attack_roll(self, target_ac, advantage=False, disadvantage=False):
        weap = self.weapon
        stat_mod = modifier(self.attrs[weap["weap_mod"]])
        attack_mod = stat_mod + self.prof_bonus
        raw, total = roll_d20(mod=attack_mod, advantage=advantage, disadvantage=disadvantage)
        return {
            "raw": raw, "total": total,
            "hit": (total >= target_ac and raw != 1) or raw == 20,
            "critical": (raw == 20),
            "miss": (raw == 1),
            "mod": attack_mod
        }

    def damage_roll(self, dmg_str, critical=False):
        n, sides = map(int, dmg_str.split('d'))
        dmg = sum(roll(sides, n))
        if critical:
            dmg += sum(roll(sides, n))
        dmg += max(0, modifier(self.attrs[self.weapon["weap_mod"]]))
        return max(1, dmg)

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def gain_xp(self, amt):
        self.xp += amt
        thresholds = {2: 300, 3: 900, 4: 2700}
        for lvl, req in thresholds.items():
            if self.xp >= req and self.level < lvl:
                self.level_up()

    def level_up(self):
        self.level += 1
        self.prof_bonus = 2 + math.floor((self.level - 1) / 4)
        hit_die = {"Guerrero": 10, "Pícaro": 8, "Mago": 6}.get(self.cls, 8)
        gained = math.ceil((hit_die / 2) + modifier(self.attrs["Constitución"]))
        self.max_hp += gained
        self.hp = self.max_hp
        self.spell_slots = self.compute_spell_slots() + (1 if self.cls == "Mago" and self.level >= 3 else 0)
        self.update_actions()
        print(f"\n¡{self.name} sube a nivel {self.level}! HP +{gained} -> {self.max_hp}")

    def use_potion(self):
        if self.inventory.get("Poción de curación", 0) > 0:
            self.inventory["Poción de curación"] -= 1
            self.heal(8)
            print(f"{self.name} usa Poción de curación y recupera 8 PV.")
            return True
        print("No tienes pociones.")
        return False

    def choose_spell(self):
        for name, data in self.available_spells.items():
            if data.get("uses", 0) > 0:
                return name
        return None

    def cast_spell(self, name):
        spell = self.available_spells.get(name)
        if not spell or spell.get("uses", 0) <= 0 or self.spell_slots <= 0:
            print("No puedes lanzar ese hechizo.")
            return 0
        spell["uses"] -= 1
        self.spell_slots -= 1
        n, sides = map(int, spell["dmg"].split('d'))
        dmg = sum(roll(sides, n))
        print(f"{self.name} lanza {name} y hace {dmg} puntos de daño.")
        return dmg

    def is_alive(self):
        return self.hp > 0

    def status(self):
        return f"{self.name} (Nivel {self.level} {self.cls}) - HP: {self.hp}/{self.max_hp} - AC: {self.ac} - XP: {self.xp}"

# -----------------------
# Monstruos
# -----------------------
class Monster:
    def __init__(self, name, hp, ac, attack_dmg="1d6", xp_reward=50):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.ac = ac
        self.attack_dmg = attack_dmg
        self.xp_reward = xp_reward

    def is_alive(self):
        return self.hp > 0

    def attack_roll(self, target_ac):
        raw, total = roll_d20(mod=2)
        return {
            "raw": raw, "total": total,
            "hit": (total >= target_ac and raw != 1) or raw == 20,
            "critical": (raw == 20),
            "miss": (raw == 1),
            "mod": 2
        }

    def damage_roll(self):
        n, sides = map(int, self.attack_dmg.split('d'))
        return max(1, sum(roll(sides, n)))

    def status(self):
        return f"{self.name} - HP: {self.hp}/{self.max_hp} - AC: {self.ac}"

# -----------------------
# Combate
# -----------------------
def combat_round(player: Character, monster: Monster):
    print("\n--- Nuevo turno ---")
    print(player.status())
    print(monster.status())
    action = choose_player_action(player)

    if action == "Atacar":
        res = player.attack_roll(monster.ac)
        print(f"Tirada d20: {res['raw']} + mod {res['mod']} = {res['total']}")
        if res["miss"]:
            print("¡Fallo crítico!")
        elif res["hit"]:
            dmg = player.damage_roll(player.weapon["dmg"], critical=res["critical"])
            print(f"Golpeas a {monster.name} e infliges {dmg} de daño.")
            monster.hp -= dmg
        else:
            print("Fallas el ataque.")

    elif action == "Ataque sigiloso" and player.cls == "Pícaro":
        res = player.attack_roll(monster.ac, advantage=True)
        if res["hit"]:
            dmg = player.damage_roll(player.weapon["dmg"], critical=res["critical"]) + 3
            print(f"Ataque sigiloso: infliges {dmg} de daño.")
            monster.hp -= dmg

    elif action == "Defender":
        print(f"{player.name} se defiende (AC +4 este turno).")
        player.ac += 4

    elif action == "Usar poción":
        player.use_potion()

    elif action == "Lanzar hechizo" and player.cls == "Mago":
        spell = player.choose_spell()
        if spell:
            monster.hp -= player.cast_spell(spell)

    elif action == "Huir":
        if random.random() < 0.5:
            print("Huyes del combate.")
            return "fled"
        print("No logras huir.")

    if not monster.is_alive():
        print(f"\nHas derrotado a {monster.name}!")
        player.gain_xp(monster.xp_reward)
        return "won"

    mres = monster.attack_roll(player.ac)
    print(f"{monster.name} tira d20: {mres['raw']} + {mres['mod']} = {mres['total']}")
    if mres["hit"]:
        dmg = monster.damage_roll()
        player.hp -= dmg
        print(f"{monster.name} te golpea e inflige {dmg} de daño.")
    else:
        print(f"{monster.name} falla su ataque.")
    player.ac = player.compute_ac()
    if not player.is_alive():
        print(f"\n¡{player.name} ha caído!")
        return "lost"
    return "ongoing"

def choose_player_action(player: Character):
    print("\nAcciones disponibles:")
    for i, action in enumerate(player.actions, 1):
        print(f"{i}. {action}")
    choice = input("Elige acción (1-{}): ".format(len(player.actions)))
    try:
        return player.actions[int(choice) - 1]
    except:
        print("Opción inválida, atacas por defecto.")
        return "Atacar"

def simple_encounter(player: Character, monster: Monster):
    print(textwrap.fill(f"Te encuentras con {monster.name}!", width=70))
    state = "ongoing"
    while state == "ongoing":
        state = combat_round(player, monster)
    return state

def make_monster_for_level(level):
    monsters = {
        1: Monster("Lobo salvaje", hp=10, ac=12, attack_dmg="1d6", xp_reward=100),
        2: Monster("Bandido", hp=16, ac=13, attack_dmg="1d8", xp_reward=250),
        3: Monster("Ogro joven", hp=30, ac=15, attack_dmg="2d6", xp_reward=700)
    }
    return monsters.get(level, Monster("Troll", hp=45, ac=16, attack_dmg="2d8", xp_reward=1500))

def create_character_heuristic(name, cls_choice, attr_method="standard"):
    attrs = generate_attributes(attr_method)
    c = Character(name=name, cls=cls_choice, attrs=attrs)
    print("\n--- Personaje creado ---")
    print(c.status())
    print("Atributos:", c.attrs)
    return c

def campaign_run(player: Character, encounters=5):
    print(f"\nComienza la campaña de {encounters} encuentros.")
    for i in range(1, encounters+1):
        print(f"\n--- Encuentro {i} ---")
        monster = make_monster_for_level(min(player.level, 3))
        result = simple_encounter(player, monster)
        if result in ("fled", "lost"):
            break
        if random.random() < 0.4:
            player.inventory["Poción de curación"] = player.inventory.get("Poción de curación", 0) + 1
            print("Encuentras una Poción de curación en el botín.")
        print("Estado tras encuentro:", player.status())
    print("\nCampaña terminada.")
    print(player.status())
    print("Inventario:", player.inventory)

if __name__ == "__main__":
    random.seed()
    hero = create_character_heuristic(name="Aramil", cls_choice="Guerrero", attr_method="standard")
    campaign_run(hero, encounters=6)
    input("\nPresiona ENTER para salir...")
