from src.sources import *

def event_func(event, x, y, flags, param):
    pass

cv2.namedWindow(windowName)

the_game = game([27, 20], 25)
fob = fobject("src/data/block1.csv")

frame = 0
while (True):

    key = cv2.waitKey(1)
    frame += 1
    if frame % 120 == 0 :
        fob.pos[1] += 1
    print("Frame :", frame, end="\r")
    the_game.show_map = deepcopy(the_game.game_map)
    fob.draw_obj(the_game)
    if fob.check_block(the_game):
        the_game.game_map = the_game.show_map[:]
        fob = fobject("src/data/block{}.csv".format(random.randrange(1, 6)), color=255, pos=[1, 1])



    the_game.draw_game()
    cv2.imshow(windowName, the_game.img)
    the_game.img[:, :, :] = 0

    fob.move_control(the_game, key)

    if key == ord("q"):
        break

cv2.destroyAllWindows()
