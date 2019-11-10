import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from kobert.pytorch_kobert import get_pytorch_kobert_model
from kobert.utils import get_tokenizer
from gluonnlp.data import BERTSPTokenizer, BERTSentenceTransform

import random

from database import Database

learning_rate = 1e-4
bert_len = 768
hidden = 7680

class ClassifierModel(nn.Module):

    def __init__(self, ans_len):
        super().__init__()

        self.linear1 = nn.Linear(bert_len, hidden)
        self.active = nn.Tanh()
        self.dropout = nn.Dropout(0.1)
        self.linear2 = nn.Linear(hidden, ans_len+1)

    def forward(self, x):
        x = self.linear1(x)
        x = self.active(x)
        x = self.dropout(x)
        x = self.linear2(x)
        return x


class Tokenizer():

    def __init__(self):
        self.token_max_len = 100

        self.kobert_model, vocab = get_pytorch_kobert_model()
        tok_path = get_tokenizer()
        tokenizer = BERTSPTokenizer(tok_path, vocab)
        self.transformer = BERTSentenceTransform(tokenizer, self.token_max_len)

    def convert(self, sentence):
        input_id, _, _ = self.transformer([sentence, ""])
        input_tensor = torch.LongTensor([input_id])
        with torch.no_grad():
            all_encoder_layer, pooled_output = self.kobert_model(input_tensor)

        #return pooled_output
        return all_encoder_layer[-1][0][0].unsqueeze(0)

class Classifier():
    
    def __init__(self, ans_max=0, path=None):
        if path is None :
            #create new Model
            self.answer_max = ans_max #get from databse.
            self.model = ClassifierModel(self.answer_max)
            self.optimizer = optim.Adam(self.model.parameters(), learning_rate)
            self.loss_fn = nn.CrossEntropyLoss()
            self.epoch = 0

        else : 
            #load models from data
            data = torch.load(path)
            self.answer_max = data['answer_max']
            
            self.model = ClassifierModel(self.answer_max)
            self.model.load_state_dict(data['model_state_dict'])

            self.optimizer = optim.Adam(self.model.parameters(), learning_rate)
            self.optimizer.load_state_dict(data['optimizer_state_dict'])
            
            self.loss_fn = nn.CrossEntropyLoss()
            self.loss = data['loss']

            self.epoch = data['epoch']
            print("{} epoch model loaded".format(self.epoch))
        
        self.tokenizer = Tokenizer()
        
    def save(self, path):
            torch.save({
                'answer_max' : self.answer_max,
                'model_state_dict' : self.model.state_dict(),
                'optimizer_state_dict' : self.optimizer.state_dict(),
                'loss' : self.loss,
                'epoch' : self.epoch
            }, path)

    def train(self, epoch, data):
        cor_num = []

        for e in range(self.epoch, self.epoch + epoch):
            #shuffle list
            random.shuffle(data)
            cor = 0
            running_loss = 0
            self.model.train()
            for q in data:
                tokens = self.tokenizer.convert(q['question'])
                ans = torch.LongTensor([q['answer_no']])
                ans_pred = self.model(tokens)
            
                self.loss = self.loss_fn(ans_pred, ans)
                running_loss += self.loss.item()

                self.optimizer.zero_grad()
                self.loss.backward()
                self.optimizer.step()
            
            print("LOSS : {}".format(running_loss/len(data)))
        
            self.model.eval()
            for q in data:
                tokens = self.tokenizer.convert(q['question'])
                ans_pred = self.model(tokens)
                _, ans_ind = ans_pred.max(1)
                if q['answer_no'] == ans_ind :
                    cor += 1

            print("RESULT : correct : {}/{}".format(cor, len(data)))
            cor_num.append(cor)
        
        self.epoch += epoch
        print(cor_num)

    def classify(self, question):
        tokens = self.tokenizer.convert(question)
        
        #change to eval mode.
        self.model.eval()
        ans_pred = self.model(tokens)
        ans_value, ans_ind = ans_pred.max(1)
        
        print(ans_pred)
        print(ans_value, ans_ind)

        return ans_ind.item()