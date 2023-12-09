from main_objects import Player, Button, game_object
walls = []

wall2 = game_object(700,150, 200, 320, (181,159,60))
walls.append(wall2)
# wall = game_object(400,250, 150, 500, (181,159,60)) 
# walls.append(wall)


def find_y_down(my_player, wall):
    tempy = my_player.window_height - 80 - my_player.speed
    while tempy > 750:
        tempy -= my_player.speed
    my_y = wall.y + wall.height - tempy
    return my_y
def find_y_up(my_player,wall):
    tempy = 0
    while tempy < wall.y - my_player.height:
        tempy += my_player.speed
    my_y = tempy - wall.y + my_player.height + 3
    return my_y

def level_three(screen, event, my_player: Player):
    screen.fill((0,0,0))
    my_player.draw(screen)
    my_player.twoDmovement = True
    my_player.canjump = False

    for wall in walls:
        wall.draw(screen)
        y_diff_down = find_y_down(my_player, wall)
        y_diff_up = find_y_up(my_player, wall)
        if wall.object.colliderect(my_player.hitbox):
            if my_player.walkingdown and not my_player.y - y_diff_up in range(wall.y - my_player.height, wall.y + wall.height + 1):
                my_player.walldown = True
            if my_player.walkingup and not my_player.y + my_player.height + 1 in range(wall.y, wall.y + wall.height + 1):
                my_player.wallup = True
            if my_player.walkingright and not my_player.x - 1 in range(wall.x, wall.x + wall.width + 1) and my_player.y + my_player.height in range(wall.y, wall.y + wall.height + my_player.height + 1 - y_diff_down) and not my_player.walldown and not my_player.wallup:
                my_player.wallright = True
            if my_player.walkingleft and not (my_player.x + my_player.width + 1) in range(wall.x, wall.x + wall.width + 1) and my_player.y + my_player.height in range(wall.y, wall.y + wall.height + my_player.height + 1 - y_diff_down) and not my_player.walldown and not my_player.wallup:
                my_player.wallleft = True
        else:
            my_player.wallup = False
            my_player.walldown =  False
            my_player.wallleft = False
            my_player.wallright = False
    my_player.movement()
    my_player.hitbox.x = my_player.x
    my_player.hitbox.y = my_player.y 

# from main_objects import Player, Button, game_object
# walls = []
# wall = game_object(400,250, 50, 500, (181,159,60))
# walls.append(wall)
# def find_y(my_player, wall):
#     tempy = my_player.window_height - 80 - my_player.speed
#     while tempy > 750:
#         tempy -= my_player.speed
#     my_y = wall.y + wall.height - tempy
#     return my_y

# def level_three(screen, event, my_player: Player):
#     screen.fill((0,0,0))
#     my_player.draw(screen)
#     my_player.twoDmovement = True
#     my_player.canjump = False
#     for wall in walls:
#         y_diff = find_y(my_player, wall)
#         if wall.object.colliderect(my_player.hitbox):
#             if my_player.walkingright and not my_player.x - 1 in range(wall.x, wall.x + wall.width + 1) and my_player.y + 1 in range(wall.y, wall.y + wall.height + 1 - y_diff):
#                 my_player.wallright = True
#             if my_player.walkingleft and not (my_player.x + my_player.width + 1) in range(wall.x, wall.x + wall.width + 1) and my_player.y + 1 in range(wall.y, wall.y + wall.height + 1 - y_diff):
#                 my_player.wallleft = True
#             if my_player.walkingdown and not my_player.y - 1 in range(wall.y, wall.y + wall.height + 1):
#                 my_player.walldown = True
#             if my_player.walkingup and not my_player.y + my_player.height + 1 in range(wall.y, wall.y + wall.height + 1):
#                 my_player.wallup = True
#         else:
#             my_player.wallup = False
#             my_player.walldown =  False
#             my_player.wallleft = False
#             my_player.wallright = False

#     print(my_player.wallleft)
#     my_player.movement()
#     my_player.canjump = False
#     my_player.hitbox.x = my_player.x
#     my_player.hitbox.y = my_player.y 

#     for wall in walls:
#         wall.draw(screen)


