# Data package
**For the article *A Reference Architecture of Reinforcement Learning Frameworks.***

---
## About
The surge in reinforcement learning (RL) applications gave rise to diverse supporting technology, such as RL frameworks. However, the architectural patterns of these frameworks are inconsistent across implementations and there exist no reference architecture (RA) to form a common basis of comparison, evaluation, and integration.
To address this gap, we propose an RA for RL frameworks. By deconstructing and analyzing eighteen state-of-the-practice RL frameworks, we identify recurring architectural components and their relationships, and codify them in an RA. To validate our RA and demonstrate its utility, we reconstruct characteristic RL patterns and existing frameworks. Finally, we identify architectural trends, e.g., commonly used components, implementation strategies, and outline paths to improving RL frameworks.
Our work aids RL framework developers in designing and implementing RL services, and helps users in integrating RL components into their applications.

## Contents
- `/RA/reference_architecture.pdf` - The reference architecture (RA) of RL frameworks.
- `/data/data.xlsx` - Data extraction sheet of eighteen RL systems.
  - `Axial coding` - Identifies components and their relationships. 
  - `Selective coding` - Refines component groups and builds reference architecture. 
  - `Final RA` - Finalized reference architecture.
  - `RA-to-framework mapping` - A view on RA by mapping each RA component to its realization status in RL systems.

## Color coding
We use the following color codes in `Final RA`.
- $\color{Green}{\textsf{Green}}$ - Explicitly implemented component in the specific framework (i.e., standalone component) 
- $\color{Yellow}{\textsf{Yellow}}$ - Explicitly implemented component in the specific framework (i.e., functionality is present but merged into another component)
- $\color{Grey}{\textsf{Grey}}$ - Explicitly implemented component via an external third-party dependency
- $\color{Red}{\textsf{Red}}$ - Component not implemented in the specific framework

`RA-to-framework mapping` includes all components marked in green and yellow, representing both explicitly ($\color{Green}{\textsf{green}}$) and implicitly ($\color{Yellow}{\textsf{yellow}}$) implemented components.

## Sampled frameworks
| ID | Name | GitHub repository |
|---|---|---|
|F1| Gymnasium | https://github.com/Farama-Foundation/Gymnasium |
|F2| PettingZoo | https://github.com/Farama-Foundation/PettingZoo |
|F3| Unity ML-Agents | https://github.com/Unity-Technologies/ml-agents |
|F4| Isaac Gym | https://github.com/isaac-sim/IsaacGymEnvs |
|F5| Isaac Lab | https://github.com/isaac-sim/IsaacLab |
|F6| dm_control | https://github.com/google-deepmind/dm_control |
|F7| DeepMind Lab | https://github.com/google-deepmind/lab |
|F8| Arcade Learning Environment | https://github.com/Farama-Foundation/Arcade-Learning-Environment |
|F9| Jumanji | https://github.com/instadeepai/jumanji |
|F10| Stable Baselines3 | https://github.com/DLR-RM/stable-baselines3 |
|F11| RL Baselines3 Zoo | https://github.com/DLR-RM/rl-baselines3-zoo |
|F12| RLlib | https://github.com/ray-project/ray/tree/master/rllib | 
|F13| Acme | https://github.com/google-deepmind/acme |
|F14| MARLlib | https://github.com/Replicable-MARL/MARLlib |
|F15| BenchMARL | https://github.com/facebookresearch/BenchMARL |
|F16| Mava | https://github.com/instadeepai/Mava |
|F17| Dopamine | https://github.com/google/dopamine |
|F18| Tianshou | https://github.com/thu-ml/tianshou |
