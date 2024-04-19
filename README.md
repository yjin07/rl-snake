# Optimization of the Classic Snake Game using Reinforcement Learning

This project encompasses the script for the classic game "Snake" and an artificial intelligence agent that can autonomously play the game. The AI agent is developed using deep reinforcement learning, featuring two models: one based on a Multi-Layer Perceptron (MLP) and another on a Convolutional Neural Network (CNN). The CNN model demonstrates superior performance with higher average scores.

The primary code directory, `main/`, houses `logs/` for storing terminal outputs and training data curves (viewable via Tensorboard); `trained_models_cnn/` and `trained_models_mlp/` contain the weights of the CNN and MLP models at various training phases, accessible during tests in `test_cnn.py` and `test_mlp.py` to evaluate the performance of the agents.

The `utils/` directory includes essential scripts: `check_gpu_status/` to verify GPU accessibility for PyTorch; `compress_code.py` compacts the code into a single line, removing all indentation and line breaks, enhancing its compatibility with GPT-4 for coding suggestions (GPT-4 processes code without requiring conventional formatting).

## Running Guide
This project utilizes Python and primarily engages external libraries such as [Pygame](https://www.pygame.org/news)、[OpenAI Gym](https://github.com/openai/gym)、[Stable-Baselines3](https://stable-baselines3.readthedocs.io/en/master/). Python 3.8.16 is the recommended version, and Anaconda is suggested for setting up the environment. These instructions are verified on a Mac system.

```bash
# Create and activate a conda environment named SnakeAI with Python 3.8.16
conda create -n SnakeAI python=3.8.16
conda activate SnakeAI

# [Optional] Install a full PyTorch version to enable GPU training
conda install pytorch=2.0.0 torchvision pytorch-cuda=11.8 -c pytorch -c nvidia

# [Optional] Verify GPU functionality with PyTorch
python .\utils\check_gpu_status.py

# Install required libraries
pip install -r requirements.txt
```

### Running Tests
Run the Snake game directly using [Pygame](https://www.pygame.org/news) from the `main/` directory:
```bash
cd [project root]/snake-ai/main
python .\snake_game.py
```
After setting up the environment, test the AI agents using `test_cnn.py` or `test_mlp.py`:
```bash
cd [project root]/snake-ai/main
python test_cnn.py
python test_mlp.py
```

### Training Models
To retrain the models:
```bash
cd [project root]/snake-ai/main
python train_cnn.py
python train_mlp.py
```

### Viewing Training Curves
Tensorboard provides detailed curve graphs of the training:
```bash
cd [project root]/snake-ai/main
tensorboard --logdir=logs/
```

Access `http://localhost:6006/` to interact with the training data visualizations.

