#### 1: Ensure that the parameters have been set using GUI.py before running this script ####
#### 2: Paste the file path of your "main" file on line 473 ####


import random
import bpy
import math
import os
import cv2
import imutils
import time



def Read_Params(main):

    lines = []
    data_file = open(main_folder + "Images/" + "parameters.txt")

    for line in data_file:
        lines.append(int(line.strip()))

    data_file.close

    #rewrite the file to contain info
    data_file_update = open(main_folder + "Images/" + "parameters.txt", "w")
    data_file_update.write(f"angle number = {lines[0]}\naxes = {lines[1]}\ndistance = {lines[2]}\ntexture = {lines[3]}\nbackground = {lines[4]}\nlighting = {lines[5]}\nResolution = {lines[6]}\nObject Position = {lines[7]}\n")
    
    return lines


def Clear_workspace():

    if "Cube" in bpy.data.objects:
        bpy.data.objects['Cube'].select_set(True)
        bpy.ops.object.delete() 

    if "Light" in bpy.data.objects:
        bpy.data.objects['Light'].select_set(True)
        bpy.ops.object.delete() 

    bpy.ops.object.select_all(action='DESELECT')


def delete_object(name):

    bpy.data.objects[name].select_set(True)
    
    bpy.ops.object.delete() 
            

def camera_to_object(object):
    
    #Select Camera Object
    bpy.data.objects[object].select_set(True)
    
    #Put object in frame from current camera position
    bpy.ops.view3d.camera_to_view_selected()
    bpy.data.cameras["Camera"].clip_end = 1000 
    bpy.data.cameras["Camera"].lens -= 3 
    
    #Deselect Camera Object
    bpy.ops.object.select_all(action='DESELECT')
          
        
def camera_setup(part):
    
    #Select Camera object
    Cam_object = bpy.data.objects['Camera']
    bpy.context.view_layer.objects.active = Cam_object

    #Set Camera to head on view
    bpy.data.cameras["Camera"].lens = 60
    bpy.context.object.rotation_euler[0] = -1.5708
    bpy.context.object.rotation_euler[1] = 3.14159
    bpy.context.object.rotation_euler[2] = 0
    
    #Deselect camera object
    bpy.ops.object.select_all(action='DESELECT')
    
    camera_to_object(part)
 

def open_file(part, location):
    
    #Load in object
    full_file_name= location + part + ".STL"
    bpy.ops.import_mesh.stl(filepath=(full_file_name))
    

    bpy.data.objects[part].select_set(True)
    
    #Centers
    bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
    
    #Smooths
    bpy.ops.object.shade_smooth(use_auto_smooth=True)
    
    bpy.ops.object.select_all(action='DESELECT')
    

def set_render_resolution(option):
    
    resolution = [100, (200/3), 50]

    if option <= (len(resolution)-1):
        bpy.context.scene.render.resolution_percentage = int(resolution[option])
    
    else:
        bpy.context.scene.render.resolution_x = 640
        bpy.context.scene.render.resolution_y = 640
        bpy.context.scene.render.resolution_percentage = 100

    
def save_image(name, location):

    file_save_location = location + name + ".png"
    
    bpy.context.scene.render.filepath = file_save_location
    
    bpy.ops.render.render(use_viewport=True, write_still=True,)


def rotate_camera_vert (object, rotations):
        
    Cam_object = bpy.data.objects['Camera']
    
    bpy.context.object.rotation_euler[0] += ((2*math.pi)/rotations)
    
    bpy.ops.object.select_all(action='DESELECT')
    
    camera_to_object(object)
        
            
def rotate_camera_horiz (object, rotations):
        
    Cam_object = bpy.data.objects['Camera']
    
    bpy.context.object.rotation_euler[2] += ((2*math.pi)/rotations)
    
    bpy.ops.object.select_all(action='DESELECT')
    
    camera_to_object(object)    
        

def camera_distance (max_distance, distances):

    distance_list = list(range(1, max_distance+1, int((max_distance+1)/distances)))
    
    offset_distance = random.choice(distance_list)
    
    return offset_distance


def HDRI_lighting(main_path, HDRI_file):

    ### Code fro adding HDRI -> Credit: "https://blender.stackexchange.com/questions/209584/using-python-to-add-an-hdri-to-world-node" ###
    
    C = bpy.context
    scn = C.scene
    node_tree = scn.world.node_tree
    tree_nodes = node_tree.nodes
    tree_nodes.clear()
    node_background = tree_nodes.new(type='ShaderNodeBackground')
    node_environment = tree_nodes.new('ShaderNodeTexEnvironment')
    node_environment.image = bpy.data.images.load(main_path + HDRI_file) 
    node_output = tree_nodes.new(type='ShaderNodeOutputWorld')   
    links = node_tree.links
    link = links.new(node_environment.outputs["Color"], node_background.inputs["Color"])
    link = links.new(node_background.outputs["Background"], node_output.inputs["Surface"])

    # Makes the loaded HDRI Dissapear in camera view
    bpy.context.scene.render.film_transparent = True

    return node_environment


def update_random_HDRI (main_path, node_background):

    HDRIs = get_images(main_path, ".exr")

    HDRI_background = random.choice(HDRIs)

    if HDRI_background in bpy.data.images:
        node_background.image = bpy.data.images[HDRI_background]
    
    else:
        node_background.image = bpy.data.images.load(main_path + HDRI_background) 


def create_material ():

    ## Delete reoccuring materials
    bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

    ## Create a new material
    material = bpy.data.materials.new(name="Part Material")
    material.use_nodes = True
    
    # Append material to object 
    object = bpy.data.objects[part_name]
    bpy.context.view_layer.objects.active = object
    object.data.materials.append(material)
    
    #Set default material
    material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.115, 0.115, 0.115, 1)
    material.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = 0.5
    material.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.1
    
    return material


def random_object_texture (material):

    material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (random.random(), random.random(), random.random(), 1)
    material.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = random.random()
    material.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = random.random()


def background_image_setup():

    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    links = tree.links

    for node in tree.nodes:
        tree.nodes.remove(node)
        
    image_node = tree.nodes.new('CompositorNodeImage')
    scale_node = tree.nodes.new('CompositorNodeScale')
    alpha_over_node = tree.nodes.new('CompositorNodeAlphaOver')
    render_layer_node = tree.nodes.new('CompositorNodeRLayers')
    file_output_node = tree.nodes.new('CompositorNodeComposite')

    # Scales image to dimensions set in the Render panel, my case 1280x720
    scale_node.space = "RENDER_SIZE" 

    # Scale background image
    links.new(image_node.outputs[0], scale_node.inputs[0])

    # Set background image as background image input to alpha node
    links.new(scale_node.outputs[0], alpha_over_node.inputs[1]) #1

    # Set rendered object as the foreground image to alpha node
    links.new(render_layer_node.outputs[0], alpha_over_node.inputs[2]) #2

    # Final image is the output image
    links.new(alpha_over_node.outputs[0], file_output_node.inputs[0])
    
    return image_node


def get_images(path, file_type):
    
    entries = os.listdir(path)
    final_entries = []

    for file in entries:
        if file_type in file:
            final_entries.append(file)
    
    return final_entries


def set_black_background(image_shortcut, path):
    
    if "Black_Background.jpg" in bpy.data.images:
        image_shortcut.image = bpy.data.images["Black_Background.jpg"]
    
    else:
        image_shortcut.image = bpy.data.images.load(path + "") 


def set_random_background(image_shortcut, path):
    
    images = get_images(path, ".jpg")

    background = random.choice(images)

    if background in bpy.data.images:
        image_shortcut.image = bpy.data.images[background]
    
    else:
        image_shortcut.image = bpy.data.images.load(path + background) 


def create_folders(image_folder, part_name):

    #Creates the files to save images and labels in
    os.mkdir(image_folder + part_name)
    os.mkdir(image_folder + part_name + "/" + part_name + " Images")
    os.mkdir(image_folder + part_name + "/" + part_name + " Labels")
    os.mkdir(image_folder + part_name + "/" + part_name + " Masks")

    location = image_folder + part_name + "/" + part_name 

    return location


def info_file (image_folder, count, part_name):
            
    data_file = open(image_folder + "Label_Info.txt", "a")
    data_file.write(f"{count} = {part_name}\n")
    data_file.close()


def random_polar():
    options = [1, -1]
    result = random.choice(options)
    return result


def take_pictures (main_folder, angles, axis, part, count, save_location, distance, max_distance, distances, object_texture, material, background, image_shortcut, image_location, include_HDRI, HDRI_node, position):    
    
    save_here = create_folders(save_location, part)
    
    if angles*axis <= 1500: #Reomve this limit when running in full!!

        for i in range(axis):      
                
                for n in range(angles):

                    ## including object texture
                    
                    if object_texture == 1:
                        random_object_texture (material)
                    
                    ## including background

                    if background == 1:
                        set_random_background(image_shortcut, image_location)
                    else:
                        set_black_background(image_shortcut, (main_folder + "Black_Background.jpg"))
                                        
                    ## including HDRI
                        
                    if include_HDRI == 1:
                        update_random_HDRI((main_folder + "HDRI Backgrounds/"), HDRI_node)
                    
                    if distance == 1:
                        
                        distance_offset = camera_distance (max_distance, distances) # will be any of [1, 11, 21, 31]
                        
                        bpy.data.cameras["Camera"].lens -= distance_offset 
                        
                        #This will automatically discount posision if distance is not selected. 
                        #Just need to test to make sure it works in this if statement

                        if position == 1:
                            
                            #changes the camere angle so that object appears non centerd

                            Cam_object = bpy.data.objects['Camera']
                            bpy.context.view_layer.objects.active = Cam_object

                            back = [1, 11, 21, 31]
                            rotations_x = [0, math.radians(3), math.radians(6.5), math.radians(13)]
                            rotations_y = [0, math.radians(1.5), math.radians(4), math.radians(8)]

                            rotate = back.index(distance_offset)   

                            x_rot = rotations_x[rotate]*random_polar()
                            y_rot = rotations_y[rotate]*random_polar()

                            bpy.context.object.rotation_euler[2] += x_rot
                            bpy.context.object.rotation_euler[0] += y_rot
                    
                            # Save origional image
                            save_image((part + "_" + str(count)), save_here + " Images/")

                            # save masked image
                            set_black_background(image_shortcut, (main_folder + "Black_Background.jpg"))
                            save_image((part + "_" + str(count)), (save_here + " Masks/"))
                            
                            bpy.context.object.rotation_euler[2] -= x_rot
                            bpy.context.object.rotation_euler[0] -= y_rot

                        else:

                            # Save origional image
                            save_image((part + "_" + str(count)), save_here + " Images/")

                            # save masked image
                            set_black_background(image_shortcut, (main_folder + "Black_Background.jpg"))
                            save_image((part + "_" + str(count)), (save_here + " Masks/"))


                        bpy.data.cameras["Camera"].lens += (distance_offset+3)
                        
                        rotate_camera_vert(part, angles)
                        
                        count += 1
                        
                    else:
                        
                        # Save origional image
                        save_image((part + "_" + str(count)), save_here + " Images/")

                        # Save mask image
                        set_black_background(image_shortcut, (main_folder + "Black_Background.jpg"))
                        save_image((part + "_" + str(count)), (save_here + " Masks/"))
                        
                        bpy.data.cameras["Camera"].lens += 3 
                        
                        rotate_camera_vert(part, angles)
                    
                        count += 1
                    
                rotate_camera_horiz(part, axis)
               
                bpy.data.cameras["Camera"].lens += 3
                
    delete_object(part_name)
                
    return save_here


def label_all_images(label_path, part_No):

    to_label = get_images(label_path + " Masks/", ".png")

    for image_name in to_label:

        image = cv2.imread(label_path + " Masks/" + image_name)

        # Retrieves the dimensions of the image ##
        (h, w, d) = image.shape

        ## applying binary colours to image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(image, 30, 255, cv2.THRESH_BINARY)[1]

        # Retrieve contours
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        # create lists to store contour coordinates
        x_coords = []
        y_coords = []

        for coord in range((len(contours[0]) - 1)):
            x_coords.append(contours[0][coord][0][0])
            y_coords.append(contours[0][coord][0][1])

        # retrieve max a min value of box:
        x_max = max(x_coords, default=w)
        x_min = min(x_coords, default=0)
        y_max = max(y_coords, default=h)
        y_min = min(y_coords, default=0)

        width = (x_max - x_min) / w
        height = (y_max - y_min) / h
        center = [(x_min / w) + (width / 2), (y_min / h) + (height / 2)]

        data_file = open(label_path + " Labels/" + image_name[:-4] + ".txt", "a")
        data_file.write(f"{part_No} {center[0]:.3f} {center[1]:.3f} {width:.3f} {height:.3f}")
        data_file.close()



##### setup code #####
        
# Start Timer
start_time = time.time()

#set count for images and parts
image_count = 1
part_count = 0

#### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Paste the location of the mail folder here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#####

main_folder = "/Users/mgbuck/Desktop/Blender Programming/"

#### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Paste the location of the mail folder here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#####

HDRI = "Default.exr"
parts = get_images(main_folder + "Parts/", ".STL")

Clear_workspace()

params = Read_Params(main_folder)

##### setup code #####


### Select HOW MANY ANGLES you would like to take the picture from (angles = angle_number*axil_number)

angle_number = params[0]

axil_number = params[1]


### Select distance = 1 if you would like to include randomised CAMERA DISTANCE

cam_distance = params[2]

max_distance = 40

distances = 4


### decide if you want to include random OBJECT MATERIAL

object_texture = params[3]

### decide if you want to include random BACKGROUND

background = params[4]

### decide if you want to include random HDRI LIGHTING

include_HDRI = params[5]

### selct resolution of render (1080p, 720p, 540p)

set_render_resolution(params[6])

## random object position

position = params[7]


##### Main Code #####

for part_name in parts:

    part_name = part_name[:-4]

    open_file(part_name, (main_folder + "Parts/"))

    camera_setup(part_name)

    material = create_material()

    HDRI_node = HDRI_lighting((main_folder + "HDRI Backgrounds/"), HDRI)

    image_shortcut = background_image_setup()

    # King Functions

    save_loc = take_pictures(main_folder, angle_number, axil_number, part_name, image_count, (main_folder + "Images/"), cam_distance, max_distance, distances, object_texture, material, background, image_shortcut, (main_folder + "Background Images/"), include_HDRI, HDRI_node, position) 

    print("--- %s seconds --- Image production time" % (time.time() - start_time))

    label_all_images(save_loc, part_count)

    info_file ((main_folder + "Images/"), part_count, part_name)

    part_count += 1

#Print the run time
print("--- %s seconds --- total time" % (time.time() - start_time))

##### Main Code #####
