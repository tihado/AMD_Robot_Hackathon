# Camera Dev
Camera Robot Arm : /dev/video2
Camera Top: /dev/video4
Camera Side : /dev/video6
Leader Arm : /dev/ttyACM0
Follower Arm : /dev/ttyACM1

# Calibrate Follower
``` bash
lerobot-calibrate --robot.type=so101_follower --robot.port=/dev/ttyACM1 --robot.id=tihado_follower
```
# Calibrate Leader
``` bash
lerobot-calibrate --teleop.type=so101_leader --teleop.port=/dev/ttyACM0 --teleop.id=tihado_leader
```

# MIDDLE POSITION
  |O===O=o<
  ||
  ||
  |O
==O|
# MIDDLE POSITION

## Set display if executing from SSH
``` bash
export $DISPLAY=":0"
```

# Control
```bash
lerobot-teleoperate --robot.type=so101_follower --robot.port=/dev/ttyACM1 --robot.id=tihado_follower --teleop.type=so101_leader --teleop.port=/dev/ttyACM0 --teleop.id=tihado_leader
```

# Control with camera
```bash
lerobot-teleoperate --robot.type=so101_follower --robot.port=/dev/ttyACM1 --robot.id=tihado_follower --robot.cameras="{front: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30}, top: {type: opencv, index_or_path: 4, width: 640, height: 480, fps: 30}, side: {type: opencv, index_or_path: 6, width: 640, height: 480, fps: 30}}" --teleop.type=so101_leader --teleop.port=/dev/ttyACM0 --teleop.id=tihado_leader --display_data=true
```

# Login to Hugging Face
```bash
huggingface-cli login --token <token> --add-to-git-credential
```

# Record
```bash
lerobot-record \
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM1 \
    --robot.id=tihado_follower \
    --robot.cameras="{front: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30}, top: {type: opencv, index_or_path: 4, width: 640, height: 480, fps: 30}, side: {type: opencv, index_or_path: 6, width: 640, height: 480, fps: 30}}" \
    --teleop.type=so101_leader \
    --teleop.port=/dev/ttyACM0 \
    --teleop.id=tihado_leader \
    --dataset.repo_id="tiena2cva/tihado_mission_1" \
    --dataset.num_episodes=5 \
    --dataset.episode_time_s=20 \
    --dataset.reset_time_s=10 \
    --dataset.single_task="pickup the proterin bar and place it on the paper" \
    --dataset.root=${HOME}/so101_dataset1/
    --display_data=true
```

# Train
```bash
lerobot-train \
  --dataset.repo_id="tiena2cva/tihado_mission_1" \
  --policy.type=act \
  --output_dir=outputs/train/act_so101_test \
  --job_name=act_so101_test \
  --policy.device=cuda \
  --wandb.enable=true \
  --policy.repo_id="tiena2cva/tihado_mission_1"
```

```bash
lerobot-train \
  --dataset.repo_id=tiena2cva/tihado_mission_1 \
  --batch_size=64 \
  --steps=1000 \
  --output_dir=outputs/train/tihado_mission_1 \
  --job_name=tihado_mission_1 \
  --policy.repo_id=tiena2cva/tihado_mission_1 \
  --policy.device=cuda \
  --policy.type=act \
  --policy.push_to_hub=true \
  --wandb.enable=true
```

# Inference Asycn
``` bash
python -m lerobot.async_inference.robot_client \
    --server_address=127.0.0.1:8080 \ # SERVER: the host address and port of the policy server
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM1 \
    --robot.id=tihado_follower \
    --robot.cameras="{front: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30}, top: {type: opencv, index_or_path: 4, width: 640, height: 480, fps: 30}, side: {type: opencv, index_or_path: 6, width: 640, height: 480, fps: 30}}" \ # POLICY: the cameras used to acquire frames, with keys matching the keys expected by the policy
    --task="pickup the proterin bar and place it on the paper" \ # POLICY: The task to run the policy on (`Fold my t-shirt`). Not necessarily defined for all policies, such as `act`
    --policy_type=act \ # POLICY: the type of policy to run (smolvla, act, etc)
    --pretrained_name_or_path=tiena2cva/tihado_mission_1 \ # POLICY: the model name/path on server to the checkpoint to run (e.g., lerobot/smolvla_base)
    --policy_device=cuda \ # POLICY: the device to run the policy on, on the server
    --debug_visualize_queue_size=True # CLIENT: whether to visualize the queue size at runtime
```
```bash
python -m lerobot.async_inference.policy_server --host=127.0.0.1 --port=8080
```

```bash
python -m lerobot.async_inference.robot_client --server_address=127.0.0.1:8080 --robot.type=so101_follower --robot.port=/dev/ttyACM1 --robot.id=tihado_follower --robot.cameras="{front: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30}, top: {type: opencv, index_or_path: 4, width: 640, height: 480, fps: 30}, side: {type: opencv, index_or_path: 6, width: 640, height: 480, fps: 30}}" --task="pickup the proterin bar and place it on the paper" --policy_type=act --pretrained_name_or_path=tiena2cva/tihado_mission_1 --policy_device=cuda --debug_visualize_queue_size=true --actions_per_chunk=50 --chunk_size_threshold=0.5 --aggregate_fn_name=weighted_average
```
