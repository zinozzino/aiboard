import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from kobert.pytorch_kobert import get_pytorch_kobert_model
from kobert.utils import get_tokenizer
from gluonnlp.data import BERTSPTokenizer, BERTSentenceTransform

import random
import json
import pdb

from classifier import *

token_max_len = 25
learning_rate = 1e-4
model_path = "model_e400.pt"

model = Classifier(token_max_len)
optimizer = optim.Adam(model.parameters(), learning_rate)

checkpoint = torch.load(model_path)
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
loss = checkpoint['loss']

tokenizer = Tokenizer()

model.eval()

tokens = tokenizer.convert("어떻게 질문을 이해하나요?")
ans_pred = model(tokens)
ans_rate, ans_ind = ans_pred.max(1)
#ans_rate > 3~5 -> then ans. else no ans.
print(ans_rate, ans_ind)
print(ans_pred)


