import torch
from transformers import RobertaTokenizer, RobertaModel


def generate_embedding(code_string):
    # Use CodeBERT's tokenizer and model
    tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
    model = RobertaModel.from_pretrained("microsoft/codebert-base")

    # Tokenize the code
    inputs = tokenizer(code_string, return_tensors="pt",
                       truncation=True, max_length=512)

    # Generate embeddings
    with torch.no_grad():
        outputs = model(**inputs)
    # Use the last hidden state (default behavior) as the embedding.
    # In practice, you might average or pool the embeddings in various ways.
    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

    return embedding
