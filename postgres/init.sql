CREATE TABLE monitoring (
    id SERIAL PRIMARY KEY,
    document_id INT NOT NULL,
    number_of_files_read_in_batch INT,
    invoice_number VARCHAR(50),
    raw_text TEXT,
    shop VARCHAR(20),
    total NUMERIC(12, 2),
    currency VARCHAR(10),
    timestamp TIMESTAMP,
    raw_text_for_llm TEXT,
    rule_based_text TEXT,
    review_required BOOLEAN,
    llm_score FLOAT
);


CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    document_id INT NOT NULL,
    raw_text TEXT,
    invoice_number VARCHAR(100),
    shop VARCHAR(100),
    total NUMERIC(12, 2),
    currency VARCHAR(10),
    timestamp TIMESTAMP,
    item VARCHAR(255),
    price NUMERIC(12, 2)
);