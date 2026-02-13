# Data package
**For the article *A Reference Architecture of Reinforcement Learning Frameworks.***

---
## About
The surge in reinforcement learning (RL) applications gave rise to diverse supporting technology, such as RL frameworks. However, the architectural patterns of these frameworks are inconsistent across implementations and there exist no reference architecture (RA) to form a common basis of comparison, evaluation, and integration.
To address this gap, we propose an RA of RL frameworks. Through a grounded theory approach, we analyze 18 state-of-the-practice RL frameworks and by that, we identify recurring architectural components and their relationships, and codify them in an RA. To demonstrate our RA, we reconstruct characteristic RL patterns. Finally, we identify architectural trends, e.g., commonly used components, and outline paths to improving RL frameworks.

## Content description
- `01-reference architecture` - Contains the reference architecture (RA) of RL frameworks.
  - `reference-architecture.pdf` - The pdf version of complete RA.
  - `reference-architecture.png` - The png version of complete RA.
  - `reference-architecture-sources.vsd` - Visual Paradigm sources for the architectural figures in the article.
- `02-data` - Contains data used for GT and analysis.
  - `01-framework-metadata.xlsx` - Includes sampled framework metadata.
  - `02-gt-artifacts.xlsx` - Includes GT coding stages.
    - `axial-coding` - Identifies components and their relationships. 
    - `selective-coding` - Refines component groups and builds reference architecture.
    - `final-RA` - Finalized RA.
  - `03-final-RA.xlsx` - Includes finalized RA mapped to frameworks.
    - `final-RA-to-framework-summary` - Mapping frameworks with implementation status.
    - `final-RA-to-framework-detail` - Mapping frameworks with detailed information, e.g., link, code snippets, and explanation.
- `03-analysis` - Contains Python analysis scripts to obtain the results in the 04-results folder.
  - `table_generator.py` - Generates tables I-VI in the publication.
  - `statistics_generator.py` - Generates statistical calculations.
- `04-results` - Contains the plots and statistics that are used in the publication. For details, see [`04-results/statistics/README.md`](04-results/statistics/README.md).

## Reproduction of analysis
- Install the required Python packages by running `pip install -r ./03-analysis/requirements.txt` from the root folder.
- For tables, run `python ./03-analysis/table_generator.py` from the root folder and follow the instructions. 
Results will be generated into `04-results/tables` folders.
- For statistics, run `python ./03-analysis/statistics_generator.py` from the root folder and follow the instructions. 
Results  will be generated into `04-results/statistics` in a textual format.

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

## Final RA
<img src="01-reference%20architecture/reference-architecture.png">
