
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from kobert.pytorch_kobert import get_pytorch_kobert_model
from kobert.utils import get_tokenizer
from gluonnlp.data import BERTSPTokenizer, BERTSentenceTransform

import random
import json

bert_len = 768
hidden = 7680

class Classifier(nn.Module):

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
        

if __name__ == "__main__":
    tokenizer = Tokenizer()
    #read questions.
    with open('q.json') as json_file:
        jsons = json.load(json_file)
    questions = jsons['rows']
    ans_len = 25

    

    eye = torch.eye(ans_len)
    model = Classifier(ans_len)
    cor_num = []

    learning_rate = 1e-4
    optimizer = optim.Adam(model.parameters(), learning_rate)
    loss_fn = nn.CrossEntropyLoss()

    checkpoint = torch.load("model_e400.pt")
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    loss = checkpoint['loss']
    
    for e in range(50):
        #shuffle list
        random.shuffle(questions)
        cor = 0
        running_loss = 0
        model.train()
        for q in questions:
            tokens = tokenizer.convert(q['question'])
            ans = torch.LongTensor([q['answer_no']])
            ans_pred = model(tokens)
        
            loss = loss_fn(ans_pred, ans)
            running_loss += loss.item()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        
        print("LOSS : {}".format(running_loss/len(questions)))
    
        model.eval()
        for q in questions:
            tokens = tokenizer.convert(q['question'])
            ans_pred = model(tokens)
            _, ans_ind = ans_pred.max(1)
            if q['answer_no'] == ans_ind :
                cor += 1

        print("RESULT : correct : {}/{}".format(cor, len(questions)))
        cor_num.append(cor)

    print(cor_num)
    torch.save({
        'model_state_dict' : model.state_dict(),
        'optimizer_state_dict' : optimizer.state_dict(),
        'loss' : loss
    }, "model.pt")
