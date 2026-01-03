from pathlib import Path

#This script will update all instances of the "XML_generator.py" script in the directory tree which it is run.
#Animation definitions will not be replaced, but any modified code after the

#######################################
#  Code for generating the animations #
#######################################

#comment block will be replaced. By default, the string "#  Code for generating the animations #" is used to specify
#the line after which the updated code will be inserted. Remove this from the specific files which you don't want to be effected.

REPLACE_STARTING_FROM = "#  Code for generating the animations #"

UPDATED_CODE = '''
GLOBAL_MIRROR_KEY = {0:0, 1:1, 2:2, 3:3, 4:4, 5:3, 6:2, 7:1}
VALID_OPTIONAL_ARGUMENTS = ["RushFrame", "HitFrame", "ReturnFrame", "CopyOf", "Omnidirectional", "GenerateAnimation", "StartingIndex"]
ROTATION_DIRECTIONS = [(0,1), (-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(1,0),(1,1)]  #Ordered clockwise starting from south.

#Vector operations.
def vec_add(vec1 : tuple, vec2 : tuple):
    return (vec1[0] + vec2[0], vec1[1] + vec2[1])

def vec_scalar(number : int, vec : tuple):
    return (number * vec[0], number * vec[1])

def flip_x(vec : tuple):
    return (vec[0] * -1, vec[1])

#A function for generating the omnidirectional offsets.
def vec_transform(vec : tuple, transform_index : int):
    return vec_add(vec_scalar(vec[0], ROTATION_DIRECTIONS[(transform_index+6) % 8]), vec_scalar(vec[1], ROTATION_DIRECTIONS[transform_index]))

#A function for handling the inputted data.
def extract_arguments(frame):
        frame_index = frame[0]
        frame_duration = frame[1]
        frame_offset = (0,0)
        shadow_offset = (0,0)
        is_mirrored = False

        if len(frame) > 2:
            third_argument = frame[2]
            if type(third_argument) == tuple: frame_offset = third_argument
            if type(third_argument) == bool: is_mirrored = third_argument

            if len(frame) > 3:
                fourth_argument = frame[3]
                if type(fourth_argument) == tuple: shadow_offset =  fourth_argument
                if type(fourth_argument) == bool: is_mirrored = fourth_argument

                if len(frame) > 4:
                    fifth_argument = frame[4]
                    if type(fifth_argument) == bool: is_mirrored = fifth_argument
                    
        return (frame_index, frame_duration, frame_offset, shadow_offset, is_mirrored)

#Functions for generating animations.

def generate_omnidirectional_animation(base_animation, omni_displacements):
    animation_data = []
    for i in range(8):
                animation = []
                for j in range(len(base_animation)):
                    frame_index, frame_duration, frame_offset, shadow_offset, is_mirrored = extract_arguments(base_animation[j])

                    if GLOBAL_MIRROR:
                        frame_index += INDEX_OFFSET * i
                        frame_rotation = (frame_index // INDEX_OFFSET) % 8
                        frame_column = frame_index % INDEX_OFFSET
                        frame_index = frame_column + INDEX_OFFSET * GLOBAL_MIRROR_KEY[frame_rotation]
                        if frame_rotation  in (5,6,7): is_mirrored = not is_mirrored
                    else:
                        frame_index += INDEX_OFFSET * i % (INDEX_OFFSET*8)

                    animation.append([
                        frame_index,
                        frame_duration,
                        vec_add(frame_offset, vec_transform(omni_displacements[j][0], i)),
                        vec_add(shadow_offset, vec_transform(omni_displacements[j][1], i)),
                        is_mirrored
                    ])
                animation_data.append(animation)
    return animation_data

def generate_rotate_animation(starting_index):
    animation_data = []
    for i in range(8):
        anim = []
        for j in range(9):
            rotation = (i + j) % 8
            if GLOBAL_MIRROR and rotation in (5,6,7):
                rotation = GLOBAL_MIRROR_KEY[rotation]
                anim.append([starting_index + INDEX_OFFSET * rotation, 2, True])
            else:
                anim.append([starting_index + INDEX_OFFSET * rotation, 2])
        animation_data.append(anim)
    return animation_data

def generate_double_animation(starting_index):
    animation_data = generate_omnidirectional_animation(
        [[starting_index,2], [starting_index,2], [starting_index,2], [starting_index,2], [starting_index,2], [starting_index,2], [starting_index,3], [starting_index,3],
         [starting_index,3], [starting_index,2], [starting_index,3], [starting_index,2], [starting_index,2], [starting_index,2], [starting_index,2], [starting_index,2]],
        [[(0,0), (0,0)], [(6,0),(6,0)], [(-6,0),(-6,0)], [(10,0),(10,0)], [(-10,0),(-10,0)], [(12,0),(12,0)], [(-12,0), (-12,0)], [(13,0),(13,0)], [(-13,0),(-13,0)],
         [(12,0),(12,0)], [(-12,0), (-12,0)], [(10,0),(10,0)], [(-10,0),(-10,0)], [(6,0),(6,0)], [(-6,0),(-6,0)], [(0,0), (0,0)]]
    )
    return animation_data

def generate_swing_animation(starting_index):
    animation_data = generate_rotate_animation(starting_index)
    for i in range(8):
        animation_data[i][1][1] = 1
        animation_data[i][4][1] = 3
        animation_data[i][7][1] = 1
        animation_data[i][8][1] = 1
    for i in (0,4,5,6,7):
        for k in range(9):
            rotated = vec_transform(AUTO_SWING_DISPLACEMENTS[k], i)
            animation_data[i][k].insert(2, rotated)
            animation_data[i][k].insert(2, rotated)
    for i in (1,2,3):
        animation_data[i].reverse()
        for k in range(9):
            mirrored = flip_x(animation_data[8-i][k][2])
            animation_data[i][k].insert(2, mirrored)
            animation_data[i][k].insert(2, mirrored)
    return animation_data

def generate_charge_animation(starting_index):
    animation_data = generate_omnidirectional_animation(
    [[starting_index,2], [starting_index,2], [starting_index,2], [starting_index,2], [starting_index,2],
     [starting_index,2], [starting_index,2], [starting_index,2], [starting_index,2], [starting_index,2]], 
    [[(0,0), (0,0)],[(-1,0), (-1,0)],[(0,0), (0,0)],[(-1,0), (-1,0)],[(0,0), (0,0)],[(-1,0), (-1,0)],
     [(0,0), (0,0)],[(-1,0), (-1,0)],[(0,0), (0,0)],[(-1,0), (-1,0)]]
    ) 
    return animation_data

def increment_index(animation_data, increment):
        for direction in animation_data:
            for frame in direction:
                frame[0] += increment

####################################
# Code for generating the XML file #
####################################
with open("FrameData.xml", "w") as file:
    file.write('<?xml version="1.0"?> \\n <AnimData />')
    
animations.sort(key = lambda anim : anim[1])

#Create the XML tree
tree = XML.parse("FrameData.xml")
root = tree.getroot()
XML.SubElement(root, "FrameWidth").text = str(SPRITE_WIDTH)
XML.SubElement(root, "FrameHeight").text = str(SPRITE_HEIGHT)
XML.SubElement(root, "ShadowSize").text = str(SHADOW_SIZE)
anims = XML.SubElement(root, "Anims")

for animation in animations:
    animation_name, animation_index, directions = animation[0], animation[1], animation[2]

    anim = XML.SubElement(anims, "Anim")
    XML.SubElement(anim, "Name").text = str(animation_name)
    XML.SubElement(anim, "Index").text = str(animation_index)

    #Process optional arguments.
    if len(animation) == 4:
        optional_arguments = animation[3]
        for argument in optional_arguments:
            if argument not in VALID_OPTIONAL_ARGUMENTS:
                print(f"The animation '{animation_index}' contains an invalid argument '{argument}'. Check for misspellings.")

        if "CopyOf" in optional_arguments:
            XML.SubElement(anim, "CopyOf").text = optional_arguments["CopyOf"]
            continue
        
        for argument, value in optional_arguments.items():
            if argument in ("RushFrame", "HitFrame", "ReturnFrame"):
                XML.SubElement(anim, argument).text = str(value)

        #Generate the animation from a template when specified.
        preset = optional_arguments.get("GenerateAnimation")
        if preset == "Double":
            start_index = directions.pop()
            directions += generate_double_animation(start_index)

        if preset == "Rotate":
            start_index = directions.pop()
            directions += generate_rotate_animation(start_index)

        if preset == "Swing":
            start_index = directions.pop()
            directions += generate_swing_animation(start_index)
        
        if preset == "Charge":
            start_index = directions.pop()
            directions += generate_charge_animation(start_index)
        

        #Generate the other directions when specified.
        if bool(optional_arguments.get("Omnidirectional")):
            omni_displacements = [[(0,0),(0,0)]] * len(directions[0])
            if len(directions) == 2:
                omni_displacements = directions.pop()
                for disp in omni_displacements:
                    if len(disp) == 0: disp += [(0,0),(0,0)] 
                    if len(disp) == 1: disp += [(0,0)]
            base_animation = directions.pop()

            directions += generate_omnidirectional_animation(base_animation, omni_displacements)

        if "StartingIndex" in optional_arguments:
            increment_index(directions, optional_arguments["StartingIndex"])
        
    sequences = XML.SubElement(anim, "Sequences")

    for direction in directions:
        sequence = XML.SubElement(sequences, "AnimSequence")

        for frame in direction:
            frame_index, frame_duration, frame_offset, shadow_offset, is_mirrored = extract_arguments(frame)
            frame_offset = vec_add(frame_offset, BASE_SPRITE_OFFSET)
            shadow_offset = vec_add(shadow_offset, BASE_SHADOW_OFFSET)

            frame = XML.SubElement(sequence, "AnimFrame")
            XML.SubElement(frame, "FrameIndex").text = str(frame_index)
            XML.SubElement(frame, "Duration").text = str(frame_duration)
            XML.SubElement(frame, "HFlip").text = str(int(is_mirrored))
            offsets1 = XML.SubElement(frame, "Sprite")
            offsets2 = XML.SubElement(frame, "Shadow")
            XML.SubElement(offsets1, "XOffset").text = str(frame_offset[0])
            XML.SubElement(offsets1, "YOffset").text = str(frame_offset[1])
            XML.SubElement(offsets2, "XOffset").text = str(shadow_offset[0])
            XML.SubElement(offsets2, "YOffset").text = str(shadow_offset[1])

#Add indent and write to a file.
XML.indent(root, "  ")
tree.write("FrameData.xml")
print("Generation successfull.")
'''
root = Path('.')

def update_script(script_path : Path):
    starting_part = []
    has_insertion_point = False
    with script_path.open() as generator_script:
        for line in generator_script:
            starting_part.append(line)
            if line.strip() == REPLACE_STARTING_FROM:
                starting_part.append("#######################################")
                has_insertion_point = True
                break

    if has_insertion_point:
        with script_path.open("w") as generator_script:
            generator_script.writelines(starting_part)
            generator_script.write(UPDATED_CODE)
            print(f"The script at {script_path} was updated successfully.")
    else:
        print(f"The script at {script_path} did not contain the line '{REPLACE_STARTING_FROM}' and will thus be skipped.")

def recursive_update(path : Path):
    for child in path.iterdir():
        if child.name == "XML_generator.py":
            update_script(child)
        if child.is_dir():
            recursive_update(child)

recursive_update(root)
print("Update successfull.")