from pathlib import Path

def load_collision_layers(obj_name, root_dir): #function that returns the list of the paths of all the collision layers of an object
        collision_layers_dir = Path(root_dir + "\\images\\collision_layers")
        collision_layers_path = list(collision_layers_dir.iterdir())
        print(collision_layers_path)

        valid_collision_layers_path = []
        all_found = False
        layer_count = 0
        while not all_found:
            layer_name = f"{obj_name}_pos{layer_count}.png"
            layer_path = Path(collision_layers_dir / layer_name)
            if layer_path in collision_layers_path:
                valid_collision_layers_path.append(layer_path)
                layer_count +=1
            else:
                all_found = True

        return valid_collision_layers_path

collision_layers_path = load_collision_layers("vase", "D:/Ethan/Projets/Terceract-project/src/room/room_1/front_wall")
print(collision_layers_path)