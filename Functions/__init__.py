import pygame as pg


# Loading the map (each character of mapfile.txt is a tile; 0 = empty)
def load_map(path):
    file = open(path + '.txt', 'r')
    data = file.read()
    file.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


animation_frames = {}  # Animation frames


# Checking the animations of the folders and placing them in lists.
def load_animation(path, frame_durations):
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pg.image.load(img_loc).convert()
        animation_image.set_colorkey((0, 114, 188))  # blue = transparent
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data


# Transition between frames
def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame


# Testing collision
def collision_test(rect, tiles):
    hit_list = []
    for each_tile in tiles:
        if rect.colliderect(each_tile):
            hit_list.append(each_tile)
    return hit_list


# Detecting collisions and movement
def move(rect, movement, tiles):
    collision_types = {
        'top': False,
        'bottom': False,
        'right': False,
        'left': False,
    }
    rect.x += int(movement[0])
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        if movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += int(movement[1])
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        if movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


# Adding opaque images
def blit_arrow(x_a, y_a, angle_a, opacity_a, obj, window):
    obj.set_alpha(opacity_a)
    window.blit(pg.transform.rotate(obj, angle_a), (x_a, y_a))


# Parallax
def bg_moving(x_bg, bg_layer, h, window, w_width):
    rel_x = x_bg % bg_layer.get_rect().width
    window.blit(bg_layer, (rel_x - bg_layer.get_rect().width, h))
    if rel_x < w_width:
        window.blit(bg_layer, (rel_x, h))


# Do not let the screen move when the player collides with the wall.
# (Undoes the parallax step; returns the new positions, since floats
# are not changed in place.)
def un_bug_collided_bg(x1, x2, x3, right, left):
    if right:
        x1 += 0.5
        x2 += 0.3
        x3 += 0.15
    if left:
        x1 -= 0.5
        x2 -= 0.3
        x3 -= 0.15
    return x1, x2, x3


# Change the flame arrow image
def change_img_conditional(component, values: list, def_result):
    i = 0
    while i < len(values) and component < values[-1]:
        if values[i] <= component < values[i + 1]:
            image_n = def_result + i
            return image_n
        i += 1


# Adding texts
def screen_text(text, x_coord, y_coord, color, size, window, r=0):
    msg = pg.font.SysFont('verdana', size - 10).render(str(text), True, color)
    window.blit(msg, msg.get_rect(center=(int(x_coord), int(y_coord))))
    if r:
        return msg.get_rect(center=(x_coord, y_coord))
