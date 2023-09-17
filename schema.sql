CREATE TABLE users (
    id SERIAL PRIMARY KEY,
);

CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    repo_name TEXT NOT NULL, -- e.g., postgresql, llama_index
    document_type TEXT NOT NULL, -- e.g., docs, code, mailing list
    url TEXT NOT NULL, -- e.g., https://github.com/postgres/postgres/blob/master/src/backend/commands/async.c
    contents TEXT NOT NULL,
    embedding REAL[]
);

CREATE INDEX documents_index ON documents USING hnsw (embedding);

CREATE TABLE chunks (
    id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id),
    contents TEXT NOT NULL,
    embedding REAL[]
);

CREATE INDEX chunks_index ON chunks USING hnsw (embedding);

SET enable_seqscan = OFF;