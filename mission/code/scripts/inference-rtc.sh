python /home/tihado/lerobot/examples/rtc/eval_with_real_robot.py \
    --policy.path=tiena2cva/tihado_mission_1 \
    --policy.device=cuda \
    --rtc.enabled=true \
    --rtc.execution_horizon=8 \
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM1 \
    --robot.id=tihado_follower \
    --robot.cameras="{front: {type: opencv, index_or_path: 8, width: 640, height: 480, fps: 30}, top: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30}, side: {type: opencv, index_or_path: 4, width: 640, height: 480, fps: 30}}" \
    --task="pickup meat and feed" \
    --duration=120 
    