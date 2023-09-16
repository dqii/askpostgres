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
    repo_name TEXT NOT NULL, -- e.g., postgresql
    document_type TEXT NOT NULL, -- e.g., docs, code, mailing list
    repo_path TEXT, -- e.g., src/backend/commands/async.c
    url TEXT NOT NULL, -- e.g., https://github.com/postgres/postgres/blob/master/src/backend/commands/async.c
    contents TEXT NOT NULL,
    embedding REAL[]
);
