import xml.etree.ElementTree as ET

def display_message(node):
    msg = node.find("message")
    if msg is not None:
        print("\nPNJ :", msg.text.strip())

def apply_game_properties(node):
    props = node.find("game_properties")
    if props is not None:
        for prop in props:
            print(f"[GAME] {prop.tag} = {prop.text.strip()}")

def apply_node(node):
    if node.tag == "conversation":
        start = node.find("start")
        print("PNJ :", start.text.strip())
        choices = node.findall("choice")
    else:
        display_message(node)
        apply_game_properties(node)
        choices = node.findall("choice")

    if not choices:
        print("\n[FIN DU DIALOGUE]")
        return

    while True:
        print()
        for i, choice in enumerate(choices, start=1):
            print(f"{i} - {choice.attrib['text']}")

        try:
            index = int(input("\n> ")) - 1
            if index < 0 or index >= len(choices):
                raise ValueError
        except ValueError:
            print("Choix invalide.")
            continue

        apply_node(choices[index])
        return

# --- Chargement du XML ---
tree = ET.parse("dtest.xml")
root = tree.getroot()

# --- Lancement du dialogue --
apply_node(root)

