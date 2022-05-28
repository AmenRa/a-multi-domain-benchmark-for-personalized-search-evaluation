import torch
from torch import einsum, nn
from torch.nn.functional import relu
from torch.nn import functional as F

class TripletMarginLoss(nn.Module):
    """
    Triplet Margin Loss function.
    """

    def __init__(self, margin=1.0):
        super(TripletMarginLoss, self).__init__()
        self.margin = margin

    def forward(
        self,
        anchors,
        positives,
        negatives,
    ):
        positive_embedding_scores = einsum("xz,xz->x", anchors, positives)
        negative_embedding_scores = einsum("xz,xz->x", anchors, negatives)

        loss = relu(
            self.margin - positive_embedding_scores + negative_embedding_scores
        ).mean()

        return loss

class BiEncoder(nn.Module):
    def __init__(self, query_model, doc_model, tokenizer, device):
        super(BiEncoder, self).__init__()
        self.query_model = query_model.to(device)
        self.doc_model = doc_model.to(device)
        self.tokenizer = tokenizer
        self.device = device
        
    def query_encoder(self, sentences):
        encoded_input = self.tokenizer(sentences, padding=True, truncation=True, return_tensors='pt').to(self.device)
        embeddings = self.query_model(**encoded_input)
        return F.normalize(self.mean_pooling(embeddings, encoded_input['attention_mask']), dim=-1)

    def doc_encoder(self, sentences):
        encoded_input = self.tokenizer(sentences, padding=True, truncation=True, return_tensors='pt').to(self.device)
        embeddings = self.doc_model(**encoded_input)
        return F.normalize(self.mean_pooling(embeddings, encoded_input['attention_mask']), dim=-1)
    
    def forward(self, triplet_texts):
        query_embedding = self.query_encoder(triplet_texts[0])
        pos_embedding = self.doc_encoder(triplet_texts[1])
        neg_embedding = self.doc_encoder(triplet_texts[2])
        
        return query_embedding, pos_embedding, neg_embedding
    
    @staticmethod
    def mean_pooling(model_output, attention_mask):
        token_embeddings = model_output[0] #First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
