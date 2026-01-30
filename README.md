import random
import time

def slow_print(text):
    """Makes text appear slowly like a retro game."""
    print(text)
    
    time.sleep(1)

def play_game():
    # --- GAME SETUP (Variables) ---
    player_hp = 100
    player_max_hp = 100
    potions = 3
    
    dragon_hp = 150
    dragon_name = "Smaug the Terrible"

    print("========================================")
    print("⚔️  WELCOME TO DRAGON SLAYER  ⚔️")
    print("========================================")
    slow_print(f"A wild {dragon_name} appears!")
    slow_print("Prepare for battle...\n")

    # --- THE GAME LOOP ---
    # This runs continuously until the player or dragon dies
    while player_hp > 0 and dragon_hp > 0:
        
        # 1. DISPLAY STATS
        print(f"\n--- STATUS ---")
        print(f"Player HP: {player_hp}/{player_max_hp} | Potions: {potions}")
        print(f"Dragon HP: {dragon_hp}")
        print("--------------")

        # 2. PLAYER'S TURN (Input)
        print("Choose your action:")
        print("1. Sword Attack (Reliable damage)")
        print("2. Fireball Magic (Risky: High damage or Miss)")
        print("3. Drink Potion (Heal 30 HP)")
        
        choice = input("Your move (1/2/3): ")

        # 3. PLAYER LOGIC
        damage_dealt = 0
        
        if choice == '1':
            damage_dealt = random.randint(10, 20)
            print(f"You slashed the dragon for {damage_dealt} damage!")
        
        elif choice == '2':
            # 40% chance to miss magic
            hit_chance = random.randint(1, 100)
            if hit_chance > 40:
                damage_dealt = random.randint(25, 50)
                print(f"CRITICAL HIT! Fireball hits for {damage_dealt} damage!")
            else:
                print("Your fireball missed! The dragon laughs at you.")
        
        elif choice == '3':
            if potions > 0:
                heal_amount = 30
                player_hp += heal_amount
                # Ensure HP doesn't go above Max
                if player_hp > player_max_hp:
                    player_hp = player_max_hp
                potions -= 1
                print(f"You drank a potion. Health restored to {player_hp}.")
            else:
                print("You reached for a potion... but the bag is empty! Turn lost!")
        
        else:
            print("You stumbled and did nothing! (Invalid Input)")

        # Apply damage to Dragon
        dragon_hp -= damage_dealt

        # Check if Dragon is dead
        if dragon_hp <= 0:
            break # Exit the loop immediately

        # 4. ENEMY'S TURN (AI)
        slow_print(f"\n{dragon_name} is attacking...")
        
        # The dragon attacks based on randomness
        dragon_move = random.randint(1, 3)
        dragon_damage = 0

        if dragon_move == 1:
            dragon_damage = random.randint(5, 15)
            print(f"The dragon bit you! You take {dragon_damage} damage.")
        elif dragon_move == 2:
            dragon_damage = random.randint(10, 25)
            print(f"Fire Breath! It burns! You take {dragon_damage} damage.")
        else:
            print(f"The dragon missed its attack! You got lucky.")

        player_hp -= dragon_damage

    # --- GAME OVER SCREEN ---
    print("\n========================================")
    if player_hp > 0:
        print("🏆 VICTORY! You have slain the dragon!")
        print(f"You survived with {player_hp} HP.")
    else:
        print("💀 GAME OVER. The dragon eats you for dinner.")
    print("========================================")

# This line actually starts the game
play_game();
