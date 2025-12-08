# Replication package
**For the article *A Reference Architecture of Reinforcement Learning Systems.***

---
## About
The surge in reinforcement learning (RL) applications gave rise to diverse supporting technology, such as RL environments and frameworks. However, the architectural patterns of these systems are inconsistent across implementations and there exist no reference architecture (RA) to form a common basis of comparison, evaluation, and integration.
To address this gap, we propose an RA for RL. By deconstructing and analyzing eighteen state-of-the-practice RL environments and frameworks, we identify recurring architectural components and their relationships, and codify them in an RA. To validate our RA and demonstrate its utility, we reconstruct characteristic RL patterns and some existing frameworks. Finally, we identify architectural trends, e.g., commonly used components, implementation strategies, and outline paths to improving RL frameworks. Our work aids RL framework developers in designing and implementing RL services, and helps users in integrating RL components into their applications.

## Sampled systems
| Name | GitHub repository |
|---|---|
| Gymnasium | https://github.com/Farama-Foundation/Gymnasium |
| PettingZoo | https://github.com/Farama-Foundation/PettingZoo |
| Unity ML-Agents | https://github.com/Unity-Technologies/ml-agents |
| Isaac Gym | https://github.com/isaac-sim/IsaacGymEnvs |
| Isaac Lab | https://github.com/isaac-sim/IsaacLab |
| dm_control | https://github.com/google-deepmind/dm_control |
| DeepMind Lab | https://github.com/google-deepmind/lab |
| Arcade Learning Environment | https://github.com/Farama-Foundation/Arcade-Learning-Environment |
| Jumanji | https://github.com/instadeepai/jumanji |
| Stable Baselines3 | https://github.com/DLR-RM/stable-baselines3 |
| RL Baselines3 Zoo | https://github.com/DLR-RM/rl-baselines3-zoo |
| RLlib | https://github.com/ray-project/ray/tree/master/rllib | 
| Acme | https://github.com/google-deepmind/acme |
| MARLlib | https://github.com/Replicable-MARL/MARLlib |
| BenchMARL | |
| Mava | |
| Dopamine | |
| Tianshou | |


## Contents
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
