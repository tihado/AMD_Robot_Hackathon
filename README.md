# AMD_Robotics_Hackathon_2025_Tihado

## Team Information

**Team:** 13 - Tihado Team

**Members:**

- 🐍 Hồng Hạnh - [@honghanhh](https://github.com/honghanhh)
- 🐍 Việt Tiến - [@nvti](https://github.com/nvti)
- 🐍 Nhật Linh - [@Nlag](https://github.com/NLag)
- 🐍 Phương Nhi - [@pnhneeechuu](https://github.com/pnhneeechuu)

**Summary:**  
**EatAble** is a voice-controlled robotic assistant designed to empower people with **upper limb disabilities** to eat independently — restoring **dignity**, **freedom**, and **equality** through accessible AI and robotics.

At its core, EatAble allows a person to simply **say what they want to eat**, and the robot will find that item on the table and **gently feed them**.

For example:

> “I want to eat beef.”  
> ✅ Robot detects beef  
> ✅ Picks it up using robotic arm  
> ✅ Brings it to the user’s mouth

This project started with feeding, but the long-term vision is broader: **Creating a world where disability does not limit autonomy.**

[🎥 Watch the demo video](#)

---

## 1. Mission Description

### 🌍 Real-world application

Millions of people live with physical disabilities that make daily tasks — even eating — a challenge. For many, this means:

- Relying on others for basic needs
- Losing a sense of independence
- Feeling isolated in everyday life

**EatAble** is designed to help **restore independence and dignity** using affordable, real-time technology that can work at home, in hospitals, or in care centers.

> “We don’t just build robots.  
> We build freedom — one meal at a time.”

#### Use Cases:

- 👩‍🦽 Supporting people with upper limb disabilities
- 🧓 Assisting elderly individuals who struggle with mobility
- 🏥 Deploying in hospitals, rehabilitation centers, and care homes
- 🏠 Enabling independent living at home with affordable robotics

> **“From a meal... to a life of independence.”**  
> Because eating isn't just survival — it's about dignity.

---

## 2. Creativity

### 💡 What makes EatAble different?

- **🗣️ Truly Natural Interaction**  
  We don't rely on fixed commands. Users can speak naturally — "I'm hungry", "I feel like eating beef", or "Can I have some carrots?" — and the system **understands and responds**.

- **👁️ Multi-View Human-Like Perception**  
  Three cameras (top, side, up) allow the robot to understand the table like a human would — in depth, position, and context.

- **🧠 Vision-Language-Action Intelligence**  
  By using **SmolVLA**, a vision-language-action policy model, the system doesn’t just "see" — it **interprets** what to do based on what it sees and what the user wants.

- **❤️ Accessibility-First Design**  
  Built not as a luxury gadget, but as a **life-enabling tool** that can be deployed in real homes and care settings, using affordable hardware and real-time AI.

---

### 3. Technical implementations

#### Teleoperation / Dataset capture

**Approach:** The project utilizes the pre-trained `lerobot/smolvla_base` model, which was trained on teleoperated demonstrations. The SmolVLA model combines vision-language understanding with robotic control, enabling it to follow natural language instructions for manipulation tasks.

**Technical Details:**

- **Robot Platform:** SO-101 Follower robot (SO101Follower) from SO-101 Robotics
- **Camera Configuration:** Three OpenCV cameras (top, side, up views) at 640x480 resolution, 30 FPS
- **Action Space:** Robot action features extracted from hardware configuration
- **Observation Space:** Multi-view camera observations with task context

#### Training

**Model:** SmolVLA (Small Vision-Language-Action) Policy

- **Base Model:** `lerobot/smolvla_base` (pre-trained)
- **Framework:** LeRobot Hugging Face
- **Training Infrastructure:** AMD Instinct™ MI300X GPU support via AMD Developer Cloud

The SmolVLA model was pre-trained on teleoperated demonstrations, learning to map visual observations and language instructions to robotic actions. The model architecture combines:

- Vision encoder for processing multi-view camera inputs
- Language encoder for understanding task instructions
- Action decoder for generating robot control commands

#### Inference

**Inference Pipeline:**

1. **Voice Input:** User speaks natural language command (e.g., "I want to eat carrots")
2. **Speech Recognition:** Google Speech Recognition API converts audio to text
3. **Intent Understanding:** OpenAI GPT-4o-mini with structured output parsing determines action intent
4. **Task Execution:** Robot receives task instruction ("feed") and:
   - Captures multi-view observations from cameras
   - Builds inference frame with task context
   - Preprocesses observations for model input
   - SmolVLA model selects action based on visual observations and task
   - Postprocesses and sends action to robot
   - Monitors action magnitude for task completion
   - Continues until task complete or timeout (30 seconds)

**Hardware Configuration:**

- **Device:** CUDA-enabled GPU (AMD Instinct™ MI300X or compatible)
- **Robot Port:** `/dev/ttyACM1`
- **Robot ID:** `tihado_follower`
- **Max Task Duration:** 30 seconds per task

---

### 4. Ease of use

**How generalizable is your implementation across tasks or environments?**

- **Task Generalization:** The SmolVLA model can be extended to various manipulation tasks beyond feeding (e.g., object manipulation, assistance tasks) by providing different task instructions
- **Environment Adaptation:** Multi-view camera system provides robust perception across different table setups and lighting conditions
- **Language Flexibility:** Natural language interface allows users to express requests in various ways, with LLM handling intent understanding
- **Hardware Portability:** Implementation uses standard LeRobot framework, making it adaptable to different robot platforms that support the framework

**Flexibility and adaptability of the solution:**

- **Modular Architecture:** Separated voice assistant, robot control, and model inference components allow for easy modification and extension
- **Dummy Mode:** Supports testing without physical robot hardware
- **Configurable Parameters:** Camera indices, robot ports, and model parameters can be adjusted for different setups
- **Action Threshold Detection:** Automatic task completion detection prevents unnecessary robot movements

**Types of commands or interfaces needed to control the robot:**

- **Primary Interface:** Natural language voice commands
  - Examples: "I want to eat carrots", "feed me", "I'm hungry", "can you feed me?"
- **Voice Assistant Features:**
  - Conversational interaction with friendly responses
  - Automatic action triggering based on intent
  - Multilingual support (ElevenLabs multilingual voice model)
- **Exit Commands:** "exit", "quit", "goodbye" to stop the system

---

## Additional Links

<!-- - **Demo Video:** [Link to video of your robot performing the task](#) -->

- **Dataset:** [URL of your dataset in Hugging Face](#)
- **Model:** [URL of your model in Hugging Face](#) (Using `lerobot/smolvla_base`)
<!-- - **Blog Post:** [Link to a blog post describing your work](#) -->

---

## Code submission
