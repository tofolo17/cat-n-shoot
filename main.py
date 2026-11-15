"""Cat-n-shoot: platform shooter controlled only by the mouse.

Prototype for the One Button Game Jam (June 2020).
"""

import os
import sys
from random import randint, choice

import pygame as pg
from pygame import mixer

from Functions import (
    animation_frames,
    bg_moving,
    blit_arrow,
    change_action,
    change_img_conditional,
    load_animation,
    load_map,
    move,
    screen_text,
    un_bug_collided_bg,
)

# Assets use relative paths: run from the script's folder
os.chdir(os.path.dirname(os.path.abspath(__file__)))

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Centering

pg.init()  # Starting Pygame

# Size of the screen and title
win_size = [900, 600]
# Fullscreen alternative:
# pg.display.Info().current_w - 5, pg.display.Info().current_h - 40
screen = pg.display.set_mode(size=win_size)
pg.display.set_caption('Cat N Shoot')
display = pg.Surface((600, 400))  # drawn small, then scaled up
clock = pg.time.Clock()

# Map variables
level_map = load_map('mapfile')
full_block = pg.image.load('Images/block_1.png')
half_block = pg.image.load('Images/block_2.png')
half_block_vertical = pg.image.load('Images/block_3.png')
half_block_right = pg.image.load('Images/block_4.png')
half_block_left = pg.image.load('Images/block_5.png')
half_support_right = pg.image.load('Images/block_6.png')
half_support_left = pg.image.load('Images/block_7.png')
glass = pg.image.load('Images/block_8.png')
chimney = pg.image.load('Images/block_9.png')
antenna = pg.image.load('Images/block_10.png')

# Dictionary that stores information about animations
# (each number is how many frames that image stays on screen)
animation_database = {
    'idle': load_animation('Animations/idle', [5, 5, 5, 5]),
    'run': load_animation('Animations/run', [5, 5, 5, 5, 5, 5, 5, 5]),
    'jump': load_animation('Animations/jump', [5, 5]),
    'shoot': load_animation('Animations/shoot', [5, 5, 5, 5]),
    'walkshoot': load_animation(
        'Animations/walkshoot', [5, 5, 5, 5, 5, 5, 5, 5]
    ),
    'jumpshoot': load_animation('Animations/jumpshoot', [5, 5, 5, 5]),
    'superjump': load_animation('Animations/superjump', [5, 5, 5, 5]),
    'superjumpshoot': load_animation(
        'Animations/superjumpshoot', [5, 5, 5, 5]
    ),
}


# Main loop
def game_loop():
    # Loop variables
    game_exit = moving_left = moving_right = False
    true_scroll = [0, 0]

    # Sound variables
    mixer.music.load('Musics/bgmusic.mp3')
    mixer.music.play(-1, 0, 5000)
    mixer.music.set_volume(0.05)
    running_sound = mixer.Sound('Musics/running.mp3')
    footstep_sound = mixer.Sound('Musics/footsteps.mp3')
    laser_sound = mixer.Sound('Musics/laser.mp3')
    reload_sound = mixer.Sound('Musics/reload.mp3')
    jump_sound = mixer.Sound('Musics/jump.mp3')
    rocket_jump_sound = mixer.Sound('Musics/rocket_jump.mp3')
    rocket_charger_sound = mixer.Sound('Musics/rocket_charger.mp3')
    rocket_ready = mixer.Sound('Musics/ready_rocket.mp3')
    landing_sound = mixer.Sound('Musics/landing.mp3')

    # Sound delimiters - Can be improved
    replay_jump_sound = replay_super_jump_sound = False
    replay_charger_sound = second_plus_rocket_use = False
    ready_rocket_sound_delimiter = footstep_sound_delimiter = 1
    running_sound_limiter = 1
    landing_sound_delimiter = 0

    # Shooting variables
    shoot = False
    bullets, shoot_pos = [], []
    n_of_bullets = time_to_shoot = time_to_recharge = 0
    bullet_img = pg.image.load('Images/bullet.png')

    # Physics
    vertical_momentum = air_timer = speed_timer = charge_timer = 0
    turbo_timer = dt = jump_timer = 0
    permitted_vm = [0, 0.3, 0.6, 0.8999999999999999, 1.2, 1.5]
    stars_speed = 0.3
    time_to_use = 8

    # Opacity variables
    right_arrow_opacity = left_arrow_opacity = upper_arrow_opacity = 70
    up_right_arrow_opacity = up_left_arrow_opacity = super_arrow_opacity = 70

    # Arrow variables
    arrow = pg.image.load('Images/seta.png').convert_alpha()
    img_arrow_n = 5

    # Character variables
    player_rect = pg.Rect(100, 100, 25, 30)
    player_frame = image_offset = 0
    player_action = 'idle'
    player_flip = super_jump_mode = False

    # Background layers
    x_building1 = x_building2 = x_building3 = 0
    background = pg.image.load('Images/bg.png')
    buildings1 = pg.image.load('Images/layer1.png')
    buildings2 = pg.image.load('Images/layer2.png')
    buildings3 = pg.image.load('Images/layer3.png')
    stars = []
    for n in range(45):
        stars.append([randint(0, 600), randint(0, 140)])

    # Converting numbers of mapfile to blocks
    def displaying_tile(
        block_name, w, h, n_block, corrector_x, corrector_y, collide=0
    ):
        if tile == f'{n_block}':
            display.blit(
                block_name,
                (
                    x * 16 + scroll[0] - corrector_x,
                    y * 16 + scroll[1] + corrector_y,
                ),
            )
            if not collide:
                tile_rect.append(pg.Rect(x * 16, y * 16, w, h))

    # While the game is open...
    while not game_exit:

        display.fill((0, 0, 0))  # Filling the screen with something
        display.blit(background, (0, 0))  # Gradient background

        # Camera
        true_scroll[0] -= ((player_rect.x + true_scroll[0]) - 230) / 12
        true_scroll[1] -= ((player_rect.y + true_scroll[1]) - 250) / 12
        scroll = true_scroll.copy()
        scroll[0] = int(true_scroll[0])
        scroll[1] = int(true_scroll[1])

        # Movement of buildings
        bg_moving(
            x_building3, buildings3, 140 + scroll[1] / 8, display, win_size[0]
        )
        bg_moving(
            x_building2, buildings2, 140 + scroll[1] / 6, display, win_size[0]
        )
        bg_moving(
            x_building1, buildings1, 165 + scroll[1] / 4, display, win_size[0]
        )

        # Adding stars
        for star in stars:
            pg.draw.line(
                display,
                (255, 255, 255),
                (star[0], star[1]),
                (star[0], star[1]),
            )
            star[0] -= stars_speed
            if star[0] < 0:
                star[0] = 600
                star[1] = randint(0, 140)

        # Map construction
        tile_rect = []
        y = 0
        for layer in level_map:
            x = 0
            for tile in layer:
                displaying_tile(full_block, 16, 16, 1, 0, 0)
                displaying_tile(half_block, 16, 4, 2, 0, 0)
                displaying_tile(half_block_vertical, 4, 16, 3, 6, 0)
                displaying_tile(half_block_right, 16, 4, 4, 0, 0)
                displaying_tile(half_block_left, 16, 4, 5, 0, 0)
                displaying_tile(half_support_right, 16, 16, 6, 0, 0)
                displaying_tile(half_support_left, 16, 16, 7, 0, 0)
                displaying_tile(glass, 16, 16, 8, 0, 0)
                displaying_tile(chimney, 10, 10, 9, 0, 7, True)
                displaying_tile(antenna, 84, 96, 'a', 0, -76, True)
                x += 1
            y += 1

        # Character movement
        player_movement = [0, 0]
        if speed_timer > 0.8 and vertical_momentum in permitted_vm:
            speed_boost = 3
            if running_sound_limiter < 2:
                footstep_sound.stop()
                running_sound.play(-1)
                running_sound.set_volume(0.05)
                running_sound_limiter += 1
        else:
            running_sound.stop()
            running_sound_limiter = 1
            speed_boost = 2
        if moving_right:
            player_movement[0] += speed_boost
            player_flip = False
            speed_timer += dt
            stars_speed = 0.4
            x_building1 -= 0.5
            x_building2 -= 0.3
            x_building3 -= 0.15
        elif moving_left:
            player_movement[0] -= speed_boost
            player_flip = True
            speed_timer += dt
            stars_speed = 0.2
            x_building1 += 0.5
            x_building2 += 0.3
            x_building3 += 0.15
        else:
            stars_speed = 0.3
            speed_timer = 0
        player_movement[1] += vertical_momentum
        vertical_momentum += 0.3
        if vertical_momentum > 7:
            vertical_momentum = 7

        # Motion-based animations - Can be optimized
        if moving_left or moving_right:
            if (
                footstep_sound_delimiter < 2
                and vertical_momentum in permitted_vm
            ):
                if speed_boost == 2:
                    footstep_sound.play(-1)
                    footstep_sound.set_volume(0.05)
                footstep_sound_delimiter += 1
            elif vertical_momentum not in permitted_vm:
                footstep_sound.stop()
                footstep_sound_delimiter = 1
            if shoot and time_to_recharge < 0:
                if air_timer <= 5:
                    player_action, player_frame = change_action(
                        player_action, player_frame, 'walkshoot'
                    )
            elif air_timer > 5:
                if turbo_timer > 0.75 or turbo_timer == 0:
                    player_action, player_frame = change_action(
                        player_action, player_frame, 'jump'
                    )
                else:
                    player_action, player_frame = change_action(
                        player_action, player_frame, 'superjump'
                    )
            else:
                player_action, player_frame = change_action(
                    player_action, player_frame, 'run'
                )
        else:
            footstep_sound_delimiter = running_sound_limiter = 1
            running_sound.stop()
            footstep_sound.stop()
            if shoot and time_to_recharge < 0:
                if air_timer <= 5:
                    player_action, player_frame = change_action(
                        player_action, player_frame, 'shoot'
                    )
            elif air_timer > 5:
                if turbo_timer > 0.75 or turbo_timer == 0:
                    player_action, player_frame = change_action(
                        player_action, player_frame, 'jump'
                    )
                else:
                    player_action, player_frame = change_action(
                        player_action, player_frame, 'superjump'
                    )
            else:
                player_action, player_frame = change_action(
                    player_action, player_frame, 'idle'
                )
        if shoot and time_to_recharge < 0:
            if air_timer > 5:
                if (
                    not super_jump_mode
                    or turbo_timer > 0.75
                    or turbo_timer == 0
                ):
                    player_action, player_frame = change_action(
                        player_action, player_frame, 'jumpshoot'
                    )
                else:
                    player_action, player_frame = change_action(
                        player_action, player_frame, 'superjumpshoot'
                    )

        player_rect, collisions = move(
            player_rect, player_movement, tile_rect
        )  # Relating the player and the map

        # Do not let the screen move when the player collides with the wall.
        x_building1, x_building2, x_building3 = un_bug_collided_bg(
            x_building1,
            x_building2,
            x_building3,
            collisions['right'],
            collisions['left'],
        )

        # Keeps the character colliding with the floor
        if collisions['bottom']:
            air_timer = vertical_momentum = 0
            super_jump_mode = False
        else:
            air_timer += 1

        # Transition between the stored frames
        player_frame += 1
        if player_frame >= len(animation_database[player_action]):
            player_frame = 0
        player_img_id = animation_database[player_action][player_frame]
        player_img = animation_frames[player_img_id]
        display.blit(
            pg.transform.flip(player_img, player_flip, False),
            (
                player_rect.x + scroll[0] + image_offset,
                player_rect.y + scroll[1],
            ),
        )

        # Adding arrows
        rocket_arrow = pg.image.load(
            f'Images/superarrow_{img_arrow_n}.png'
        ).convert_alpha()
        blit_arrow(50, 200, 180, left_arrow_opacity, arrow, display)
        blit_arrow(482, 70, 45, up_right_arrow_opacity, arrow, display)
        blit_arrow(50, 70, 135, up_left_arrow_opacity, arrow, display)
        blit_arrow(279, 70, 90, upper_arrow_opacity, arrow, display)
        blit_arrow(492, 200, 0, right_arrow_opacity, arrow, display)
        blit_arrow(279, 300, 90, super_arrow_opacity, rocket_arrow, display)

        # One-button controls: the mouse position on the screen decides
        # the movement (right/left thirds walk, top band jumps, bottom
        # fifth charges the rocket jump) and the click shoots.
        x, y = pg.mouse.get_pos()  # Getting mouse coordinates
        # X movement
        if x > (2 / 3 * win_size[0]) and (y > win_size[1] / 6):
            moving_left = False
            moving_right = True
            right_arrow_opacity = 100
        elif x < win_size[0] / 3 and (y > win_size[1] / 6):
            moving_right = False
            moving_left = True
            left_arrow_opacity = 100
        else:
            moving_right = moving_left = False
            right_arrow_opacity = left_arrow_opacity = 70
            upper_arrow_opacity = up_right_arrow_opacity = 70
            up_left_arrow_opacity = super_arrow_opacity = 70

        jump_timer += dt
        # Y movement
        if (y < win_size[1] / 3) and (y > win_size[1] / 6) and air_timer < 8:
            if replay_jump_sound:
                jump_sound.play()
                jump_sound.set_volume(0.05)
                replay_jump_sound = False
            if collisions['top']:
                vertical_momentum = -1
            elif collisions['bottom'] and jump_timer > 1.2:
                vertical_momentum = -6
                jump_timer = 0
                collisions['top'] = True
                replay_jump_sound = True
        elif collisions['bottom']:
            upper_arrow_opacity = up_left_arrow_opacity = 70
            up_right_arrow_opacity = 70

        # Super jump
        if y > 4 * win_size[1] / 5:
            charge_timer += dt
            if vertical_momentum in permitted_vm and time_to_use >= 8:
                if replay_charger_sound:
                    rocket_charger_sound.play()
                    rocket_charger_sound.set_volume(0.01)
                    replay_charger_sound = False
                super_arrow_opacity = 125
                player_rect.x += choice([-1.25, 1, -0.5, 0, 0.5, 1, 1.25])
            if charge_timer > 1:
                rocket_charger_sound.stop()
                super_jump_mode = replay_super_jump_sound = True
                second_plus_rocket_use = True
                vertical_momentum = -12
                charge_timer = time_to_use = ready_rocket_sound_delimiter = 0
        else:
            replay_charger_sound = True
            rocket_charger_sound.stop()
            charge_timer = 0
        if replay_super_jump_sound:
            rocket_jump_sound.play(maxtime=950)
            rocket_jump_sound.fadeout(900)
            rocket_jump_sound.set_volume(0.05)
            replay_super_jump_sound = False
        if super_jump_mode:
            turbo_timer += dt
        else:
            turbo_timer = 0

        # Analyzing the opacity of the arrows
        if vertical_momentum not in permitted_vm:
            upper_arrow_opacity = 100
            landing_sound_delimiter = 1
        else:
            if 0 < landing_sound_delimiter < 2:
                landing_sound.play()
                landing_sound.set_volume(0.05)
                landing_sound_delimiter += 1
        if upper_arrow_opacity == 100 and right_arrow_opacity == 100:
            up_right_arrow_opacity = 100
        elif upper_arrow_opacity == 100 and left_arrow_opacity == 100:
            up_left_arrow_opacity = 100
        else:
            up_left_arrow_opacity = 70
        if time_to_use >= 8:
            if ready_rocket_sound_delimiter < 2:
                if second_plus_rocket_use:
                    rocket_ready.play()
                    rocket_ready.set_volume(0.05)
                ready_rocket_sound_delimiter += 1
            time_to_use = 8
            img_arrow_n = 5
        else:
            img_arrow_n = change_img_conditional(
                time_to_use, [0, 2, 4, 6, 8], 1
            )
            charge_timer = 0

        # Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_exit = True
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and time_to_recharge < 0:
                    if player_flip:
                        image_offset = -5
                    shoot = True
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    image_offset = 0
                    shoot = False

        time_to_recharge -= dt  # Time to shoot
        # Bullets
        # 15 shots per magazine, then 2 seconds to reload
        if shoot and time_to_recharge < 0:
            player_movement[0] = 100
            time_to_shoot += dt
            if len(bullets) == 0:
                initial_bullet = 0
            else:
                initial_bullet = 0.15
            while time_to_shoot > initial_bullet:
                laser_sound.play()
                laser_sound.set_volume(0.05)
                laser_sound.fadeout(1000)
                bullets.append([player_rect.x, player_rect.y])
                shoot_pos.append([player_flip])
                time_to_shoot = 0
                n_of_bullets += 1
                if n_of_bullets > 14:
                    reload_sound.play()
                    reload_sound.set_volume(0.05)
                    time_to_recharge = 2
                    n_of_bullets = image_offset = 0
        for bullet in bullets:
            pos = bullets.index(bullet)
            if not shoot_pos[pos][0]:
                bullet[0] += 15
                x_start_shoot = 10
                angle = 0
            else:
                bullet[0] -= 15
                x_start_shoot = 0
                angle = 180
            display.blit(
                pg.transform.rotate(bullet_img, angle),
                (
                    bullet[0] + x_start_shoot + scroll[0],
                    bullet[1] + 15 + scroll[1],
                ),
            )
            if (
                bullet[0] > player_rect.x + 300 + arrow.get_width()
                or bullet[0] < player_rect.x - 300 - arrow.get_width()
            ):
                bullets.remove(bullet)
                shoot_pos.remove(shoot_pos[pos])
        screen_text(
            f'{15 - n_of_bullets} / 15', 540, 370, (255, 255, 255), 20, display
        )

        # Character's death (falling for about 2 seconds)
        if air_timer > 120:
            game_exit = True

        # Screen and FPS update
        screen.blit(pg.transform.scale(display, win_size), (0, 0))
        pg.display.update()
        time_to_use += dt
        dt = clock.tick(60) / 1000


if __name__ == '__main__':
    game_loop()
    pg.quit()
    sys.exit()
