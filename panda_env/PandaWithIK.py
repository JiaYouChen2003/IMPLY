import sys
import os
import logging
import json
from inverse_kinematics.CCDIK.camera_control import CameraControl
from inverse_kinematics.CCDIK.utils import *
from inverse_kinematics.CCDIK.ik_actor import IKActor
from inverse_kinematics.CCDIK.ik_chain import IKChain
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.task import Task

sys.path.append("./")
PATH = 'panda_env'


class Env(ShowBase):
    def __init__(self, src="../src/", model="waiter", debug=True):
        super().__init__(self)
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-4s %(message)s',
                            datefmt='%m-%d %H:%M',)
        self.DebugMode = debug

        logging.info("Loading model")
        self.running = True
        self.path = src + model
        self.model = Actor(os.path.join(self.path, "model.fbx"))
        self.root = render.attach_new_node("Root")
        self.ik_actor = IKActor(
            self.model, os.path.join(self.path, "texture.jpg"))
        self.ik_actor.reparent_to(self.root)
        logging.info("Success loading model")

        logging.info("Setup IK chain")

        logging.info("Loading Config")
        self.path = PATH
        with open(os.path.join(self.path, "Panda_config.json"), "r") as read_config:
            config = json.load(read_config)
        self.target_list = config["target_list"]
        self.base_dict = config["base_dict"]
        self.chain_list_dict = config["chain_list_dict"]
        self.joint_constrain = config["joint_constrain"]

        dir_map = {
            "x": LVector3f.unit_x(),
            "y": LVector3f.unit_y(),
            "z": LVector3f.unit_z(),
        }

        self.ik_chain = dict()
        self.ik_target = dict()
        for target in self.target_list:
            joint_names = self.chain_list_dict[target]
            self.ik_chain[target] = self.ik_actor.create_ik_chain(joint_names)
            if self.DebugMode:
                self.ik_chain[target].debug_display(line_length=0.5)
            tar = create_point(thickness=10)
            self.ik_target[target] = render.attach_new_node(tar)

            for name in joint_names:
                if name in self.joint_constrain:
                    constrain_type, constrain_tup = self.joint_constrain[name]
                    dir, (MIN, MAX) = constrain_tup
                    if constrain_type == "ball":
                        self.ik_chain[target].set_ball_constraint(name,
                                                                  min_ang=math.pi*MIN, max_ang=math.pi*MAX)
                    elif constrain_type == "hinge":
                        self.ik_chain[target].set_hinge_constraint(name, dir_map[dir],
                                                                   min_ang=math.pi*MIN, max_ang=math.pi*MAX)
                    elif constrain_type == "static":
                        self.ik_chain[target].set_static(name)

            self.ik_chain[target].set_target(self.ik_target[target])
        logging.info("Finish setup IK chain")

        self.task_mgr.add(self.move_target, "MoveTarget")
        self.task_mgr.add(self.head_rotate, "HeadRotate")
        self.joint_target = dict()

        logging.info("Setup camera")
        self.camera_setup()

        self.dx, self.dy, self.dz = 0, 0, 0
        if self.DebugMode:
            self.debug_setup()
            self.ik_actor.actor.ls()
        logging.info("Finish Panda all Setup Process")

    def camera_setup(self, ):
        self.set_frame_rate_meter(True)
        self.accept('escape', self.close_panda)
        self.disableMouse()
        self.cam_control = CameraControl(camera, self.mouseWatcherNode)
        self.taskMgr.add(self.cam_control.move_camera, "MoveCameraTask")
        self.accept("wheel_down", self.cam_control.wheel_down)
        self.accept("wheel_up", self.cam_control.wheel_up)

    def close_panda(self):
        self.running = False
        sys.exit()

    def update_pos_target(self, update_dict):
        if update_dict is not None:
            for joint_name, pos in update_dict.items():
                self.joint_target[joint_name] = pos
        return Task.cont

    def head_rotate(self, task):
        if "HEAD" in self.joint_target:
            degree = self.joint_target["HEAD"]
            x, y, z = self.joint_target["HEAD"]
            degree = math.atan2(y, x)
            logging.debug(degree)
            self.ik_actor.actor.controlJoint(None, "modelRoot", "neck_01").setHpr(
                0, -2*math.degrees(degree), 0)
        return Task.cont

    def move_target(self, task):
        for target in self.target_list:
            joint_tar = (self.dx, self.dy, self.dz)
            if not self.DebugMode and target in self.joint_target:
                joint_tar = self.nor2real(self.joint_target[target], target)
            self.ik_target[target].setPos(joint_tar)
            self.ik_chain[target].update_ik()
        return Task.cont

    def get_len(self, vec):
        return math.sqrt(sum(i**2 for i in vec))

    def rotate(self, vec, angle):
        px, py, _ = vec
        qx = px * math.cos(angle) - py * math.sin(angle)
        qy = px * math.sin(angle) + py * math.cos(angle)
        return qx, qy

    def vec_to_world(self, vec, bas, ref, Con=1):
        thetab = math.atan2(bas[1], bas[0])
        x, y = self.rotate(vec, thetab)
        x *= Con * self.get_len(bas)
        y *= -Con * self.get_len(bas)
        z = vec[-1] * self.get_len(bas)
        tar = LVector3f(x, y, z) + ref
        return tar

    def nor2real(self, normal, target):
        S, T, R, Con = self.base_dict[target]
        S = self.ik_actor.actor.exposeJoint(None, "modelRoot", S).getPos()
        T = self.ik_actor.actor.exposeJoint(None, "modelRoot", T).getPos()
        R = self.ik_actor.actor.exposeJoint(None, "modelRoot", R).getPos()
        bas = S - T
        ret = self.vec_to_world(normal, bas, S, Con)
        return ret

    def debug_setup(self,):
        # Debug Function
        self.accept("arrow_up", self.yn)
        self.accept("arrow_up-repeat", self.yn)
        self.accept("arrow_down", self.yp)
        self.accept("arrow_down-repeat", self.yp)
        self.accept("arrow_left", self.xp)
        self.accept("arrow_left-repeat", self.xp)
        self.accept("arrow_right", self.xn)
        self.accept("arrow_right-repeat", self.xn)
        self.accept(".", self.zp)
        self.accept(".-repeat", self.zp)
        self.accept(",", self.zn)
        self.accept(",-repeat", self.zn)
        self.accept("enter", self.rst)

    def rst(self, ): self.dx = self.dy = self.dz = 0
    def xp(self, ): self.dx += 10
    def xn(self, ): self.dx -= 10
    def yp(self, ): self.dy += 10
    def yn(self, ): self.dy -= 10
    def zp(self, ): self.dz += 10
    def zn(self, ): self.dz -= 10


def main():
    env = Env()
    env.run()


if __name__ == "__main__":
    main()
