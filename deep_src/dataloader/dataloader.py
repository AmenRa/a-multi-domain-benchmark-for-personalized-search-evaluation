from torch.utils.data import Dataset
import random


class TripletData(Dataset):
    def __init__(self, data, corpus):
        self.data = data
        self.data_ids = list(self.data.keys())
        self.corpus = corpus
        
    def __len__(self):
        return len(self.data_ids)
    
    def __getitem__(self, idx):
        query_id = self.data_ids[idx]
        query_data = self.data[query_id]
        query_text = query_data['text']
        
        # pos document
        pos_sample = random.choice(query_data['relevant_docs'])
        pos_text = self.corpus[pos_sample]
        
        # neg document
        neg_sample = random.choice(query_data['bm25_docs'])
        neg_text = self.corpus[neg_sample]
        
        return query_text, pos_text, neg_text        
