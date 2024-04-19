import os
import sys
import random
import torch
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.callbacks import CheckpointCallback
from sb3_contrib import MaskablePPO
from sb3_contrib.common.wrappers import ActionMasker

from snake_game_custom_wrapper_cnn import SnakeEnv

if torch.backends.mps.is_available():
    NUM_ENV = 32 * 2
else:
    NUM_ENV = 32

# Constants
MAX_SEED_VALUE = int(1e9)
MPS_LR = 5e-4
CUDA_LR = 2.5e-4
FINAL_LR = 2.5e-6
CLIP_START = 0.150
CLIP_END = 0.025

LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)

# Linear scheduler
def linear_schedule(initial_value: float, final_value: float = 0.0):
    assert initial_value > 0.0, "Initial value should be positive."

    def scheduler(progress):
        return final_value + progress * (initial_value - final_value)
    
    return scheduler

def make_env(seed=0):
    def _init():
        env = SnakeEnv(seed=seed)
        env = ActionMasker(env, SnakeEnv.get_action_mask)
        env = Monitor(env)
        env.seed(seed)
        return env
    return _init


def main():
    # Generate a list of random seeds for each environment.
    seed_set = set()
    while len(seed_set) < NUM_ENV:
        seed_set.add(random.randint(0, MAX_SEED_VALUE))

    # Create the Snake environment.
    env = SubprocVecEnv([make_env(seed=s) for s in seed_set])

    is_mps_available = torch.backends.mps.is_available()
    lr_schedule = linear_schedule(MPS_LR if is_mps_available else CUDA_LR, FINAL_LR)
    clip_range_schedule = linear_schedule(CLIP_START, CLIP_END)

    device = "mps" if is_mps_available else "cuda"
    batch_size = 512 * 8 if is_mps_available else 512
    save_dir = "trained_models_cnn_mps" if is_mps_available else "trained_models_cnn"

    model = MaskablePPO(
        "CnnPolicy",
        env,
        device=device,
        verbose=1,
        n_steps=2048,
        batch_size=batch_size,
        n_epochs=4,
        gamma=0.94,
        learning_rate=lr_schedule,
        clip_range=clip_range_schedule,
        tensorboard_log=LOG_DIR
    )

    os.makedirs(save_dir, exist_ok=True)

    checkpoint_interval = 15625
    checkpoint_callback = CheckpointCallback(save_freq=checkpoint_interval, save_path=save_dir, name_prefix="ppo_snake")

    # Writing the training logs from stdout to a file
    original_stdout = sys.stdout
    log_file_path = os.path.join(save_dir, "training_log.txt")
    with open(log_file_path, 'w') as log_file:
        sys.stdout = log_file
        model.learn(total_timesteps=int(1e8), callback=[checkpoint_callback])
        env.close()
    
    # Restore stdout
    sys.stdout = original_stdout

    # Save the final model
    model.save(os.path.join(save_dir, "ppo_snake_final.zip"))

if __name__ == "__main__":
    main()
