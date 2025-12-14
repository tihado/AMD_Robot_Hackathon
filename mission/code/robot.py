from lerobot.robots.so101_follower import SO101FollowerConfig, SO101Follower
from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig
from lerobot.datasets.utils import hw_to_dataset_features
from lerobot.policies.factory import make_pre_post_processors
from lerobot.policies.utils import build_inference_frame, make_robot_action
from lerobot.policies.smolvla.modeling_smolvla import SmolVLAPolicy
from lerobot.policies.act.modeling_act import ACTPolicy
import torch
from time import sleep
from pathlib import Path
import time
from typing import Literal
import subprocess


class Robot:
    def __init__(self, dummy=False, use_command=False):
        if dummy:
            self.dummy = True
            return
        else:
            self.dummy = False

        self.task_mapping = {
            "feed": "pickup carrot and feed",
        }

        self.use_command = use_command
        if self.use_command:
            return

        calibration_dir = (
            "/home/tihado/.cache/huggingface/lerobot/calibration/robots/so101_follower"
        )

        self.camera_cfg = {
            "camera3": OpenCVCameraConfig(
                index_or_path=2, width=640, height=480, fps=30
            ),  # front
            "camera1": OpenCVCameraConfig(
                index_or_path=4, width=640, height=480, fps=30
            ),  # top
            "camera2": OpenCVCameraConfig(
                index_or_path=6, width=640, height=480, fps=30
            ),  # side
        }

        self.robot_id = "tihado_follower"
        self.robot_port = "/dev/ttyACM1"

        self.device = torch.device("cuda")  # or "cuda" or "cpu"
        self.model_id = "tiena2cva/tihado_model_3.1"
        self.model_type = "smolvla"  # or "act"

        self.robot_cfg = SO101FollowerConfig(
            port=self.robot_port,
            id=self.robot_id,
            cameras=self.camera_cfg,
            calibration_dir=Path(calibration_dir),
        )

        self.MAX_STEPS_SECONDS = 45
        self.MIN_STEPS_SECONDS = 10

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

        if self.model_type == "smolvla":
            self.model = SmolVLAPolicy.from_pretrained(self.model_id)
        elif self.model_type == "act":
            self.model = ACTPolicy.from_pretrained(self.model_id)
        else:
            raise ValueError(f"Invalid model type: {self.model_type}")

        self.preprocess, self.postprocess = make_pre_post_processors(
            self.model.config,
            self.model_id,
            # This overrides allows to run on MPS, otherwise defaults to CUDA (if available)
            preprocessor_overrides={"device_processor": {"device": str(self.device)}},
        )

        # For checking if the robot is moving
        self.action_diff_queue = []
        self.action_diff_threshold = 1.5
        self.action_diff_queue_size = 50

    def run(self, task: Literal["feed"]):
        if self.dummy:
            print("Dummy mode: No action will be sent to the robot")
            sleep(5000)
            return

        task_description = self.task_mapping[task]
        if not task_description:
            print(f"Invalid task: {task}")

            return

        if self.use_command:
            # use subprocess to run the command and wait for it to finish
            subprocess.run(["bash", "run_task.sh", task_description], check=True)
            print("Task finished! Starting new task...")
            return

        start_time = time.time()

        last_action = None
        self.action_diff_queue = []

        while True:
            if time.time() - start_time > self.MAX_STEPS_SECONDS:
                break

            obs = self.robot.get_observation()
            obs_frame = build_inference_frame(
                observation=obs,
                ds_features=self.dataset_features,
                device=self.device,
                task=task_description,
                robot_type=self.robot_type,
            )

            obs = self.preprocess(obs_frame)

            action = self.model.select_action(obs)
            action = self.postprocess(action)
            action = make_robot_action(action, self.dataset_features)

            # Check if robot is moving
            is_moving = self.is_robot_move(last_action, action)

            if not is_moving and time.time() - start_time > self.MIN_STEPS_SECONDS:
                print(
                    f"No movement detected in {self.action_diff_queue_size} steps. Breaking loop."
                )
                break

            self.robot.send_action(action)
            last_action = action

        print("Task finished! Starting new task...")

    def is_robot_move(self, last_action: dict | None, action: dict) -> bool:
        """
        Check if robot is moving by comparing current action with last action.
        Uses a rolling average over the last 50 steps to smooth out noise.
        Returns True if robot is moving, False otherwise.
        """
        if last_action is None:
            return True  # First iteration, assume moving

        sum_difference = 0
        # compare every value in the action dictionary
        for key, value in action.items():
            sum_difference += abs(last_action[key] - value)

        self.action_diff_queue.append(sum_difference)

        # Need at least 50 samples before making a decision
        if len(self.action_diff_queue) < self.action_diff_queue_size:
            return True  # Assume moving during warm-up period

        # Check if average movement over last 50 steps exceeds threshold
        avg_difference = sum(self.action_diff_queue) / len(self.action_diff_queue)
        is_moving = avg_difference > self.action_diff_threshold

        # Maintain queue size at 50 (remove oldest element)
        self.action_diff_queue.pop(0)

        return is_moving


if __name__ == "__main__":
    robot = Robot(use_command=False)
    robot.run("feed")
