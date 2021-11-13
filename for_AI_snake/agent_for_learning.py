import torch
import numpy as np
import random
from collections import deque
from AI_snake import Game_field, Game


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001