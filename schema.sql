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

-- NOTE: Document type can be docs, code
-- TODO: Support document types - mailing list.
CREATE TABLE postgres_documents (
    id SERIAL PRIMARY KEY,
    document_type TEXT NOT NULL,
    repo_path TEXT,
    url TEXT NOT NULL,
    contents TEXT NOT NULL,
    embedding REAL[]
);
