import logging
from threading import Thread
import time

import client_
from panda_env.PandaWithIK import Env


class controller():
    def __init__(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s %(levelname)-4s %(message)s',
                            datefmt='%m-%d %H:%M',)
        self.env = Env("./src/", debug=False)
        self.Plist = [
            Thread(target=self.penv, args=())
        ]
        self.human_pose = None

    def run(self):
        # self.env.run()
        logging.info("Start thread")
        for p in self.Plist:
            p.start()
        logging.info("Run main Thread")
        self.env.run()
        logging.info("End thread, joining thread")
        for p in self.Plist:
            p.join()

    def penv(self):
        """
        This is the function which maintain the panda3d environemt
        """
        logging.info("Start running ENV")
        while self.env.running:
            for i in range(5):
                self.human_pose = client_.generate_dict_with_ones(i)
                self.env.update_pos_target(self.human_pose)
                time.sleep(1)
            break
        logging.info("Stop running, Closing all process...")


def main():
    env = controller()
    env.run()


if __name__ == "__main__":
    main()
