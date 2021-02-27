import io
import PIL.Image as Image

import cv2

import os
import threading
from ppadb.client import Client
import numpy as np
import time
from lib import get_text_in_image, find_in_image, make_render, actions, cmd


class Bot4Bot():
    def __init__(self):
        adb = Client(host='127.0.0.1', port=5037)
        devices = adb.devices()
        if len(devices) == 0:
            print('no device attached')
            quit()
    
        self.device = devices[0]
        app = 'com.pixonic.wwr'
        
        if self.get_screen_res()[0] == 1200:
            self.base = self.handle_dir(f'{self.get_screen_res()[0]}_{self.get_screen_res()[1]}')

        while app not in (test:=self.device.shell(f'dumpsys activity | grep top-activity')):
            self.device.shell(f'monkey -p {app} -v 500')
            time.sleep(5)

        

    def handle_dir(self, directory):
        path = os.path.join('data', directory) 
        try: 
            os.makedirs(path, exist_ok = True) 
            # print("Directory '%s' created successfully" % directory) 
        except OSError as error: 
            print("Directory '%s' can not be created" % directory)

        return path

    def get_screen_res(self):
        wms = self.device.shell(f'wm size')
        if 'Override size' in wms:
            if '720x1520' in wms:
                screen_size = 720, 1520
            else:
                screen_size = 1080, 2280
        elif 'Physical size' in wms:
            if '720x1520' in wms:
                screen_size = 720, 1520
            else:
                screen_size = 1200, 1920
        return screen_size

    def capture(self, do="save", name='screen.png'):
        if do == "save":
            image = self.device.screencap()
            path = os.path.join(self.base, name)
            with open(path, 'wb') as f:
                f.write(image)
            image = open(path, 'r')
            return image
        elif do == "object":
            return Image.open(io.BytesIO(self.device.screencap()))
        elif do == "array":
            return np.array(Image.open(io.BytesIO(self.device.screencap())))
        else:
            print ("no option selected")

    def find_point(self, place=actions.menu["battle"], live=False):
        path = os.path.join(self.base, place)
        scr = os.path.join(self.base, 'screen.png')
        if live == True:
            self.capture(do="save")
            click = find_in_image.find(real=scr, get=path)
            # print(click)
        else:
            click = find_in_image.find(real=scr, get=path)
            # print(click)
        return click

    def find_points(self, place=actions.menu["battle"], live=False, render=False):
        path = os.path.join(self.base, place)
        scr = os.path.join(self.base, 'screen.png')


        origin = np.array(Image.open(io.BytesIO(cmd.run_adb('exec-out screencap -p', clean=False))))



        if live == True:
            self.capture(do="save")
            
            click = find_in_image.finding(real=origin, get=path, render=render)
            # print(click)
        else:
            click = find_in_image.finding(real=origin, get=path, render=render)
            # print(click)
        return click

    def input_touch(self, place):
        print(place)
        self.device.shell(f'input tap {place[0]} {place[1]}')

    def input_swipe(self, place, place_to):
        self.device.shell(f'input touchscreen swipe {place[0]} {place[1]} {place_to[0]} {place_to[1]} {int(600)}')

    def go_back(self):
        # input keyevent KEYCODE_WAKEUP
        self.device.shell(f'input keyevent 4')
        # self.device.shell(f'input keyevent ')
        print("back")

    def click_point(self, place=actions.menu["battle"], method= "tap"):
        click = self.find_points(place, live=True, render=False)
        if click is not None:
            if method == "tap":
                self.device.shell(f'input tap {click[0]} {click[1]}')
            else:
                self.device.shell(f'input touchscreen swipe {click[0]} {click[1]} {click[0]} {click[1]} {int(2.5)}')
        else:
            print("Got None")
            return None

    def find_text(self):
        click = get_text_in_image.text()
        # self.device.shell(f'input touchscreen swipe {click[0]} {click[1]} {click[0]} {click[1]} {int(2)}')
        return click

    # def stream(self):
    #     origin = np.array(Image.open(io.BytesIO(cmd.run_adb('exec-out screencap -p', clean=False))))
    #     re

        # return self.device.shell('screenrecord --bit-rate=16m --output-format=h264 --size 1920x1080 -').dtype

    def render(self):
        #count down
        # for i in list(range(4))[::-1]:
        #     print(i+1)
        #     time.sleep(1)
        last_time = time.time()
        init = True
        while init == True:
            # origin = np.array(Image.open(io.BytesIO(self.device.screencap())))
            origin = np.array(Image.open(io.BytesIO(cmd.run_adb('exec-out screencap -p', clean=False))))
            # print('loop took {} seconds'.format(time.time()-last_time))
            # last_time = time.time()
            views=[
                make_render.window('output', cv2.cvtColor(origin, cv2.COLOR_BGR2RGB)),
                # window('output2', cv2.cvtColor(origin, cv2.COLOR_BGR2RGB))
                ]
            if len(now := [views.remove(x) for x in views if x == 'close']) == 1:
                print('closing a view')
                init = False

    def check_menu(self):
        time.sleep(2)
        self.capture()
        menu = [
            self.find_points(actions.menu["battle"]),
            self.find_points(actions.menu["upgrade"]) or self.find_points(actions.menu["upgrade1"]),

            self.find_points(actions.menu["tasks"]),
            # self.find_points(actions.menu["market"]),
            self.find_points(actions.menu["workshop"]),

            testing.find_points(actions.menu["gold"]),
            testing.find_points(actions.menu["silver"]),
            # testing.find_points(actions.menu["power"]),
            testing.find_points(actions.menu["platnum"]),
        ]
        if len([f for f in menu if f is not None]) >= 4:
            return True
        else:
            return False

    def check_end(self):
        self.capture()
        menu = [
            self.find_points(actions.end["end"]),
        ]
        if len([f for f in menu if f is not None]) >= 4:
            return True
        else:
            return False
    
    def check_start(self):
        startup = [
            self.find_points(actions.menu["update"], live=True),
        ]
        if startup[0]:
            return True
        else:
            return False

    def start_upgrade(self):
        print("start upgrade")
        if self.find_points(actions.menu["upgrade"], live=True):
            self.click_point(actions.menu["upgrade"])
            time.sleep(5)
            if self.find_points(actions.upgrade["upgradesilver"], live=True):
                self.click_point(actions.upgrade["upgradesilver"])
                time.sleep(5)
            if self.find_points(actions.globals["exit"], live=True):
                self.click_point(actions.globals["exit"])

    def speed_up_upgrade(self):
        print("speed up upgrade")
        
        if self.find_points(actions.menu["upgrade1"], live=True):
            self.click_point(actions.menu["upgrade1"])
            time.sleep(5)
            if self.find_points(actions.menu["watch2"], live=True):
                self.click_point(actions.menu["watch2"])
                time.sleep(35)
                old = self.capture(do='array')
                if self.find_points(actions.menu["close"], live=True):
                    self.click_point(actions.menu["close"])
                else:
                    self.go_back()
                    time.sleep(5)
                    if self.capture(do='array').all() == old.all():
                        place = [
                            self.get_screen_res()[1]-35,
                            25
                        ]
                        self.input_touch(place)
                        print('Used Input')
                        time.sleep(5)
            if self.find_points(actions.globals["exit"], live=True):
                self.click_point(actions.globals["exit"])
    
    def loop_upgrade(self):
        print("looping upgrade")
        while self.find_points(actions.menu["upgrade1"], live=True):
            self.click_point(actions.menu["upgrade1"])
            time.sleep(5)
            if self.find_points(actions.menu["watch2"], live=True):
                self.click_point(actions.menu["watch2"])
                time.sleep(35)
                old = self.capture(do='array')
                if self.find_points(actions.menu["close"], live=True):
                    self.click_point(actions.menu["close"])
                else:
                    time.sleep(5)
                    if self.capture(do='array').all() == old.all():
                        place = [
                            self.get_screen_res()[1]-35,
                            25
                        ]
                        self.input_touch(place)
                        print('Used Input')
                        time.sleep(5)
        else:
            
            print("Ending Upgrade Loop")
            return 'end'
            


    def go_to_menu(self):
        print("trying to go to main menu")
        if not self.check_menu():
            if self.find_points(actions.menu["back"], live=True):
                self.click_point(actions.menu["back"])
            elif self.find_points(actions.menu["home"], live=True):
                self.click_point(actions.menu["home"])
            time.sleep(5)

    def operations_claim(self):
        print("trying to claim operations")
        if self.find_points(actions.menu["operations"], live=True):
            self.click_point(actions.menu["operations"])
            time.sleep(10)
            if self.find_points(actions.menu["claim"], live=True):
                self.click_point(actions.menu["claim"])
            time.sleep(5)
            self.go_to_menu()

    def swipe_right(self):
        y,x = self.get_screen_res()
        place = x/2, y/2
        place_to = x/2+x/5, y/2
        print(place)
        print(place_to)
        self.input_swipe(place, place_to)

    def swipe_left(self):
        y,x = self.get_screen_res()
        place = x/2, y/2
        place_to = x/2-x/5, y/2
        print(place)
        print(place_to)
        self.input_swipe(place, place_to)

    def swipe_up(self):
        y,x = self.get_screen_res()
        place = x/2-50, y/3*2
        place_to = x/2+50, y/2-y/5
        print(place)
        print(place_to)
        self.input_swipe(place, place_to)
    
    def swipe_down(self):
        y,x = self.get_screen_res()
        place = x/2-50, y/3
        place_to = x/2+50, y/2+y/5
        print(place)
        print(place_to)
        self.input_swipe(place, place_to)


if __name__ == "__main__":
    testing = Bot4Bot()
    if testing.find_points(actions.menu['battle']):
        testing.click_point(actions.menu['battle'])
    # testing.render()
    # while True:
    #     if not testing.check_menu():
    #         if testing.find_points(actions.globals['exit']):
    #             testing.click_point(actions.globals['exit'])
    #         else:
    #             try:
    #                 testing.go_back()
    #             except:
    #                 if self.find_points(actions.menu["back"], live=True):
    #                     self.click_point(actions.menu["back"])
    #                 elif self.find_points(actions.menu["home"], live=True):
    #                     self.click_point(actions.menu["home"])
    #     else:
    #         # testing.collect():

    #         if test:= testing.loop_upgrade():
    #             if test == 'end':
    #                 testing.start_upgrade()
    
    # while testing.find_points(actions.menu['tasks']):

    # testing.capture()

    # while not testing.check_menu():
    #     time.sleep(1)
    #     testing.go_back()
    # else:
    #     if testing.find_points(actions.menu['tasks'], live=True):
    #         testing.click_point(actions.menu["tasks"])
    #     time.sleep(5)
    #     testing.swipe_up()
    #     # testing.swipe_down()
    #     testing.swipe_up()
    #     # testing.swipe_down()
    #     testing.swipe_up()
    #     # testing.swipe_down()
    #     testing.swipe_up()
    #     # testing.swipe_down()

    # testing.stream()

    # if testing.find_points(actions.menu['exit'], live=True):
    #     testing.click_point(actions.menu["exit"])



        # if testing.check_menu():
        #     # testing.operations_claim()
        #     testing.start_upgrade()
        #     testing.run_upgrade()
        


    # testing.go_to_menu()
    
    # testing.find_points(actions.menu["watch2"], live=True, render=True)

    # testing.find_points(actions.menu["close"], live=True)    

    # while testing.find_points(actions.menu["watch1"], live=True):
    #     testing.click_point(actions.menu["watch1"])
    #     time.sleep(40)
    #     old = testing.capture(do='array')
    #     testing.go_back()
    #     if testing.capture(do='array')==old:
    #         place = [
    #             testing.get_screen_res()[1]-35,
    #             25
    #         ]
    #         testing.input_touch(place)
                
    # testing.click_point(actions.menu["close"])
    # time.sleep(5)

    # def watch_upgrade():
        # if testing.find_points(actions.menu["watch1"], live=True):
        #     testing.click_point(actions.menu["watch1"])

    # print(testing.find_points(actions.menu["workshop"], live=True))
    # print(testing.find_points(actions.menu["gold"], live=True))
    # print(testing.find_points(actions.menu["platnum"], live=True))
    # print(testing.find_points(actions.menu["silver"], live=True))
    
    # print(testing.find_points(actions.menu["platnum"], live=True))
    # print(testing.find_points(actions.menu["silver"], live=True))
    
    # print(testing.base)
    # print(testing.get_screen_res())

    
    # print(testing.check_menu())
    