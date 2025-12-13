from lerobot.robots.so101_follower import SO101FollowerConfig, SO101Follower
from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig
from lerobot.datasets.utils import hw_to_dataset_features
from lerobot.policies.factory import make_pre_post_processors
from lerobot.policies.utils import build_inference_frame, make_robot_action
from lerobot.policies.smolvla.modeling_smolvla import SmolVLAPolicy
import torch
from time import sleep
from pathlib import Path
import time


class Robot:
    def __init__(self, dummy=False):
        if dummy:
            self.dummy = True
            return
        else:
            self.dummy = False

        calibration_dir = ""

        self.camera_cfg = {
            "top": OpenCVCameraConfig(index_or_path=2, width=640, height=480, fps=30),
            "side": OpenCVCameraConfig(index_or_path=4, width=640, height=480, fps=30),
            "up": OpenCVCameraConfig(index_or_path=6, width=640, height=480, fps=30),
        }

        self.robot_id = "tihado_follower"
        self.robot_port = "/dev/ttyACM1"

        self.device = torch.device("cuda")  # or "cuda" or "cpu"
        self.model_id = "lerobot/smolvla_base"

        self.robot_cfg = SO101FollowerConfig(
            port=self.robot_port,
            id=self.robot_id,
            cameras=self.camera_cfg,
            calibration_dir=Path(calibration_dir),
        )

        self.MAX_STEPS_SECONDS = 30

        self.robot = SO101Follower(self.robot_cfg)
        self.robot.connect(calibrate=False)
        self.robot_type = "so101_follower"
        self.action_features = hw_to_dataset_features(
            self.robot.action_features, "action"
        )
        self.obs_features = hw_to_dataset_features(
            self.robot.observation_features, "observation"
        )
        self.dataset_features = {**self.action_features, **self.obs_features}

        self.model = SmolVLAPolicy.from_pretrained(self.model_id)

        self.preprocess, self.postprocess = make_pre_post_processors(
            self.model.config,
            self.model_id,
            # This overrides allows to run on MPS, otherwise defaults to CUDA (if available)
            preprocessor_overrides={"device_processor": {"device": str(self.device)}},
        )

    def run(self, task):
        if self.dummy:
            print("Dummy mode: No action will be sent to the robot")
            sleep(5000)
            return

        start_time = time.time()
        # Threshold for considering an action as "no action" (all values close to zero)
        ACTION_THRESHOLD = 1e-6

        while True:
            if time.time() - start_time > self.MAX_STEPS_SECONDS:
                break

            obs = self.robot.get_observation()
            obs_frame = build_inference_frame(
                observation=obs,
                ds_features=self.dataset_features,
                device=self.device,
                task=task,
                robot_type=self.robot_type,
            )

            obs = self.preprocess(obs_frame)

            action = self.model.select_action(obs)
            action = self.postprocess(action)
            action = make_robot_action(action, self.dataset_features)

            # Check if there are no meaningful actions (all values are effectively zero)
            action_magnitude = sum(abs(v) for v in action.values())
            if action_magnitude < ACTION_THRESHOLD:
                print("No action detected - task may be complete. Breaking loop.")
                break

            self.robot.send_action(action)

        print("Task finished! Starting new task...")


if __name__ == "__main__":
    robot = Robot()
    robot.run("feed")
