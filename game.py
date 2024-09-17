#import subprocess
#subprocess.run(["", "", "",""])
from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.showbase import DirectObject
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import *
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import NodePath, TextureStage, Filename, LVecBase3f, OrthographicLens

import sys
import random


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.win.setClearColor((0.0, 0.5, 0.9, 1))  # RGB值，alpha默认为1
                # 设置渲染到屏幕的方式为正交投影，适合2D UI
  
        # 禁用鼠标
        self.disableMouse()

        #隐藏鼠标
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)

        #设定摄像机初始位置
        self.camera.setPos(0, 0, 100)

        # 载入环境模型
        self.environ = self.loader.loadModel("models/environment")

        # 设置环境模型的父实例
        self.environ.reparentTo(self.render)

        # 对模型进行比例及位置调整
        self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-8, 42, 0)

        # 通知任务管理器调用SpinCameraTask控制相机
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        # 载入熊猫角色
        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)

        # 动画循环
        self.pandaActor.loop("walk")

        # 创建四幕
        PosInterval1 = self.pandaActor.posInterval(13,
                                                   Point3(0, -10, 0),
                                                   startPos=Point3(0, 10, 0))
        PosInterval2 = self.pandaActor.posInterval(13,
                                                   Point3(0, 10, 0),
                                                   startPos=Point3(0, -10, 0))
        HprInterval1 = self.pandaActor.hprInterval(3,
                                                   Point3(180, 0, 0),
                                                   startHpr=Point3(0, 0, 0))
        HprInterval2 = self.pandaActor.hprInterval(3,
                                                   Point3(0, 0, 0),
                                                   startHpr=Point3(180, 0, 0))

        # 创建情节并运行四幕2
        self.pandaPace = Sequence(PosInterval1,
                                  HprInterval1,
                                  PosInterval2,
                                  HprInterval2,
                                  name="pandaPace")
        self.pandaPace.loop()

        #创建HUD
        global X1, X2, text, text2, L1, L2l, L2r
        text = OnscreenText(fg=(255, 255, 0, 255),
                            pos=(-0.1, -0.1), scale=0.1, mayChange=True)
        text2 = OnscreenText(pos=(-0.7, 0), scale=0.1, mayChange=True)
        DirectFrame(frameColor=(255, 255, 0, 255),
                    frameSize=(-0.04, 0.04, -0.002, 0.002), pos=(0, 0, 0))
        DirectFrame(frameColor=(255, 255, 0, 255),
                    frameSize=(-0.002, 0.002, -0.04, 0.04), pos=(0, 0, 0))
        X1 = DirectFrame(frameColor=(0, 0, 0, 255),
                         frameSize=(-0.04, 0.04, -0.002, 0.002), pos=(0, 0, 0))
        X2 = DirectFrame(frameColor=(0, 0, 0, 255),
                         frameSize=(-0.002, 0.002, -0.04, 0.04), pos=(0, 0, 0))
        DirectFrame(frameColor=(255, 255, 0, 255),
                    frameSize=(-0.5, -0.51, 0.5, -0.5), pos=(0, 0, 0))
        L1 = DirectFrame(frameColor=(255, 255, 0, 255), frameSize=(
            0.2, 0.11, 0.005, -0.005), pos=(0, 0, 0))
        L2l = DirectFrame(frameColor=(255, 255, 0, 255),
                          frameSize=(-0.1, -0.04, 0.002, -0.002), pos=(0, 0, 0))
        L2r = DirectFrame(frameColor=(255, 255, 0, 255), frameSize=(
            0.04, 0.1, 0.002, -0.002), pos=(0, 0, 0))
        DirectFrame(frameColor=(255, 255, 0, 255),
                    frameSize=(-0.1, 0.1, 0.002, -0.002), pos=(0, 0, 0.5))
        DirectFrame(frameColor=(255, 255, 0, 255),
                    frameSize=(-0.1, 0.1, 0.002, -0.002), pos=(0, 0, -0.5))

        # 定义旋转相机
    def spinCameraTask(self, task):
        (mouse, size) = (base.win.getPointer(0), self.get_size())
        (mx0, my0) = (size[0]-mouse.getX(), mouse.getY())
        (mx, my, hpr) = (mx0/160, my0/160, self.camera.getHpr())
        (rx, ry) = (mx-size[0]/320+hpr[0], my-size[1]/320+hpr[1])

        pos = self.camera.getPos()
        (lx, ly, lz) = (pos[0], pos[1], pos[2])
        (angle, angle2) = (hpr[0], hpr[1])
        distance = 0.2

        if angle < 0:
            while angle < 0:
                angle = angle+360
        else:
            angle = angle % 360

        if angle2 < 0:
            while angle2 < 0:
                angle2 = angle2+360
        else:
            angle2 = angle2 % 360

        distance2 = cos(angle2*pi/180)*distance

        if angle % 90 == 0:
            if angle == 0:
                (x, y) = (0, distance2)
            elif angle == 90:
                (x, y) = (distance2, 0)
            elif angle == 180:
                (x, y) = (0, -distance2)
            else:
                (x, y) = (-distance2, 0)
        else:
            if angle <= 45:
                x = sin(angle*pi/180)*distance2
                y = cos(angle*pi/180)*distance2
            elif angle < 90:
                angle = 90-angle
                x = cos(angle*pi/180)*distance2
                y = sin(angle*pi/180)*distance2
            elif angle <= 135:
                angle = angle-90
                x = cos(angle*pi/180)*distance2
                y = -sin(angle*pi/180)*distance2
            elif angle < 180:
                angle = 180-angle
                x = sin(angle*pi/180)*distance2
                y = -cos(angle*pi/180)*distance2
            elif angle <= 225:
                angle = angle-180
                x = -sin(angle*pi/180)*distance2
                y = -cos(angle*pi/180)*distance2
            elif angle < 270:
                angle = 270-angle
                x = -cos(angle*pi/180)*distance2
                y = -sin(angle*pi/180)*distance2
            elif angle < 315:
                angle = angle-270
                x = -cos(angle*pi/180)*distance2
                y = sin(angle*pi/180)*distance2
            else:
                angle = 360-angle
                x = -sin(angle*pi/180)*distance2
                y = cos(angle*pi/180)*distance2

        if angle2 % 90 == 0:
            if angle2 == 0 or angle2 == 90:
                z = distance
            else:
                z = 0
        else:
            if angle2 <= 45:
                z = sin(angle2*pi/180)*distance
            elif angle2 < 90:
                angle2 = 90-angle2
                z = cos(angle2*pi/180)*distance
            elif angle2 <= 135:
                angle2 = angle2-90
                z = cos(angle2*pi/180)*distance
            elif angle2 < 180:
                angle2 = 180-angle2
                z = sin(angle2*pi/180)*distance
            elif angle2 <= 225:
                angle2 = angle2-180
                z = -sin(angle2*pi/180)*distance
            elif angle2 < 270:
                angle2 = 270-angle2
                z = -cos(angle2*pi/180)*distance
            elif angle2 < 315:
                angle2 = angle2-270
                z = -cos(angle2*pi/180)*distance
            else:
                angle2 = 360-angle2
                z = -sin(angle2*pi/180)*distance

        if lz < -1:
            self.closeWindow(self.win)
            sys.exit()
        self.camera.setPos(-x+lx, y+ly, z+lz)
        self.camera.setHpr(rx, ry, 0)

        if ry >= 360:
            while ry >= 360:
                ry = ry-360
        elif ry < 0:
            while ry < 0:
                ry = ry+360
        if ry//180 == 0:
            ry = ry
        elif ry//180 == 1:
            ry = ry-360
        L2l.setPos(0, 0, ry/180)
        L2r.setPos(0, 0, ry/180)
        b = size[1]/2
        a = mouse.getX()/b-size[0]/size[1], 0, 1-mouse.getY()/b
        X1.setPos(a)
        X2.setPos(a)
        text['text'] = str(int(ry))
        text2['text'] = str(int(z+lz))
        if z+lz > 100:
            L1.setPos(-0.7, 0, 0.5)
            text2['pos'] = (-0.7, 0.48)
        else:
            L1.setPos(-0.7, 0, (z+lz)/100-0.5)
            text2['pos'] = (-0.7, (z+lz)/100-0.52)
        if z+lz < 11:
            text2['fg'] = (255, 0, 0, 255)
        elif z+lz < 31:
            text2['fg'] = (0, 255, 255, 255)
        else:
            text2['fg'] = (255, 255, 0, 255)

        return Task.cont

MyApp().run()
