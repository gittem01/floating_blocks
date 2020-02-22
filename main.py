from src.sources import *
import simpleaudio as aud

the_game = game([25, 12], 24)
fob = fobject("src/data/{}".format(random.choice(os.listdir("src/data"))), color=255, pos=[the_game.game_size[1]//2, 0])
next = fobject("src/data/{}".format(random.choice(os.listdir("src/data"))), color=255, pos=[the_game.game_size[1]//2, 0])
sound = aud.WaveObject.from_wave_file("sounds/over.wav")

frame = 0

while (True):

    frame += 1
    #print("Frame :", frame, end="\r")

    key = cv2.waitKey(1)

    the_game.show_map = deepcopy(the_game.game_map)
    fob.draw_obj(the_game)
    next.draw_next(the_game)

    if fob.check_block(the_game):
        if key == ord("s") or frame % 60 == 0:

            the_game.game_map = the_game.show_map[:]
            the_game.line_clear()
            fob = next


            if fob.check_block(the_game):
                sound.play()
                x = 0
                while True:
                    key = cv2.waitKey(1)
                    if key == ord("q"):
                        break
                    x += 1
                    the_game.img[:, :, :] = 0
                    cv2.putText(the_game.img,'Game',(10,300), cv2.FONT_HERSHEY_SIMPLEX, 3,
                                (x % 256,128 + x % 128,0),2,cv2.LINE_AA)
                    cv2.putText(the_game.img,'Over',(40,500), cv2.FONT_HERSHEY_SIMPLEX, 3,
                                (x % 256,128 + x % 128,0),2,cv2.LINE_AA)
                    cv2.imshow(windowName, the_game.img)


            next = fobject("src/data/{}".format(random.choice(os.listdir("src/data"))), color=255, pos=[the_game.game_size[1]//2, 0])

    else:
        if frame % 120 == 0 and key != ord("s"):
            fob.pos[1] += 1
    fob.move_control(the_game, key)
    the_game.draw_game()
    cv2.imshow(windowName, the_game.img)
    the_game.img[:, :, :] = 0

    if key == ord("q"):
        break

cv2.destroyAllWindows()
