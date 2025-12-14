# Dataset Capture for LeRobot

![Dataset Visualization](./dataset.png)

This document describes how we capture datasets for training LeRobot policies using our 3-camera setup.

## Our dataset

We created 2 datasets for training the policy model:

- **[Dataset 1](https://huggingface.co/datasets/tiena2cva/tihado_mission_3)**: This dataset is used to train the policy model for the task of picking up the carrot and feeding it to the user.

- **[Dataset 2](https://huggingface.co/datasets/tiena2cva/tihado_mission_4)**: This dataset is used to train the policy model for the task of picking up the meat and feeding it to the user.

## Camera Setup

We use **3 cameras** positioned at different angles to provide comprehensive visual coverage of the robot's workspace:

![Camera Setup](./camera_setup.jpg)

1. **Front Camera**: in the robot arm (`camera3`)

   - Resolution: 640×480
   - Frame Rate: 30 FPS
   - Position: Front view of the robot arm

2. **Top Camera** (`camera1`)

   - Resolution: 640×480
   - Frame Rate: 30 FPS
   - Position: Overhead view of the workspace

3. **Side Camera** (`camera2`)

   - Resolution: 640×480
   - Frame Rate: 30 FPS
   - Position: Side view of the robot arm

## Hardware Configuration

- **Leader Arm** (Teleoperation): `/dev/ttyACM0`
- **Follower Arm** (Robot being controlled): `/dev/ttyACM1`
- **Robot Type**: SO101 Follower
- **Robot ID**: `tihado_follower`

## Dataset Capture Process

### Prerequisites

1. **Calibrate the robots** before recording:

   ```bash
   # Calibrate Follower
   lerobot-calibrate --robot.type=so101_follower --robot.port=/dev/ttyACM1 --robot.id=tihado_follower

   # Calibrate Leader
   lerobot-calibrate --teleop.type=so101_leader --teleop.port=/dev/ttyACM0 --teleop.id=tihado_leader
   ```

2. **Login to Hugging Face** (if pushing datasets):
   ```bash
   huggingface-cli login --token <token> --add-to-git-credential
   ```

### Recording Command

We use the `lerobot-record` command to capture demonstrations. The cameras are configured as follows:

```bash
lerobot-record \
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM1 \
    --robot.id=tihado_follower \
    --robot.cameras="{front: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30}, top: {type: opencv, index_or_path: 4, width: 640, height: 480, fps: 30}, side: {type: opencv, index_or_path: 6, width: 640, height: 480, fps: 30}}" \
    --teleop.type=so101_leader \
    --teleop.port=/dev/ttyACM0 \
    --teleop.id=tihado_leader \
    --dataset.repo_id="tiena2cva/tihado_mission_4" \
    --dataset.num_episodes=20 \
    --dataset.episode_time_s=30 \
    --dataset.reset_time_s=10 \
    --dataset.single_task="pickup the carrot and feed" \
    --dataset.root=/home/tihado/tihado-team13/so101_food_4/ \
    --display_data=true
```

### Recording Parameters

- **`--robot.cameras`**: Configures all 3 cameras (front, top, side) with their respective device indices and settings
- **`--dataset.num_episodes`**: Number of demonstration episodes to record
- **`--dataset.episode_time_s`**: Duration of each episode in seconds
- **`--dataset.reset_time_s`**: Time allowed for resetting the environment between episodes
- **`--dataset.single_task`**: Task description for the demonstrations
- **`--dataset.repo_id`**: Hugging Face repository ID for storing the dataset
- **`--display_data=true`**: Shows camera feeds and data during recording

## Teleoperation

During recording, the operator uses the **Leader Arm** (`/dev/ttyACM0`) to control the **Follower Arm** (`/dev/ttyACM1`). All three camera views are captured simultaneously along with the robot's actions, creating a multi-view dataset for training.

## Data Structure

The captured dataset includes:

- **Observations**: Multi-view camera images from all 3 cameras (front, top, side)
- **Actions**: Robot joint positions and movements recorded from the follower arm
- **Task descriptions**: Text descriptions of the task being demonstrated
- **Timestamps**: Temporal information for each frame

This multi-camera setup provides rich visual information from different perspectives, which helps the trained policies better understand spatial relationships and object positions in the workspace.
