import torch
from transformers import RobertaTokenizer, RobertaModel

# Instantiate CodeBERT's tokenizer and model outside the function
tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
model = RobertaModel.from_pretrained("microsoft/codebert-base")


def generate_embedding(code_string):
    # Tokenize the code
    inputs = tokenizer(code_string, return_tensors="pt",
                       truncation=True, max_length=512)

    # Generate embeddings
    with torch.no_grad():
        outputs = model(**inputs)
    # Use the last hidden state (default behavior) as the embedding.
    embedding = outputs.last_hidden_state.mean(
        dim=1).squeeze().numpy().tolist()

    return embedding
