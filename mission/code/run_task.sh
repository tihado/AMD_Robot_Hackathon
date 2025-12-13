#!/usr/bin/env bash
set -euo pipefail

TASK="$1"

POLICY_PATH="lerobot/smolvla_base"
ROBOT_PORT="/dev/ttyACM1"
DURATION="30"

ROBOT_TYPE="so101_follower"
FPS="30"
ROBOT_ID="tihado_follower"
ROBOT_CAMERAS='{top: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30}, side: {type: opencv, index_or_path: 4, width: 640, height: 480, fps: 30}, up: {type: opencv, index_or_path: 6, width: 640, height: 480, fps: 30}}'
DATASET_SINGLE_TASK="$TASK"
DATASET_REPO_ID='tiena2cva/tihado_mission_test_1'
DATASET_EPISODE_TIME_S='30'
DATASET_NUM_EPISODES='5'
DATASET_PUSH_TO_HUB='false'


lerobot-record \
  --robot.type="${ROBOT_TYPE}" \
  --robot.port="${ROBOT_PORT}" \
  --policy.path="${POLICY_PATH}" \
  --dataset.fps "${FPS}" \
  --robot.id="${ROBOT_ID}" \
  --robot.cameras="${ROBOT_CAMERAS}" \
  --dataset.single_task="${DATASET_SINGLE_TASK}" \
  --dataset.repo_id="${DATASET_REPO_ID}" \
  --dataset.episode_time_s="${DATASET_EPISODE_TIME_S}" \
  --dataset.num_episodes="${DATASET_NUM_EPISODES}" \
  --dataset.push_to_hub="${DATASET_PUSH_TO_HUB}"