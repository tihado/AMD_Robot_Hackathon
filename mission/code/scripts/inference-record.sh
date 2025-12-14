rm -rf '/home/tihado/.cache/huggingface/lerobot/tiena2cva/eval_tihado_model_3_test_1'
sudo chmod 666 /dev/ttyACM*
sleep 1
lerobot-record \
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM1 \
    --robot.id=tihado_follower \
    --robot.cameras="{camera3: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30}, camera1: {type: opencv, index_or_path: 4, width: 640, height: 480, fps: 30}, camera2: {type: opencv, index_or_path: 6, width: 640, height: 480, fps: 30}}" \
    --dataset.repo_id="tiena2cva/eval_tihado_model_3_test_1" \
    --dataset.single_task="pickup the carrot and feed" \
    --policy.path="tiena2cva/tihado_model_3" \
    --teleop.type=so101_leader \
    --teleop.port=/dev/ttyACM0 \
    --teleop.id=tihado_leader \
    --display_data=true \
    --dataset.num_episodes=1