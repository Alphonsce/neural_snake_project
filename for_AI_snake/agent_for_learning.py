import torch
import torch.nn as nn
import numpy as np
import random
from collections import deque
from AI_snake import AI_Game
import training_model


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001