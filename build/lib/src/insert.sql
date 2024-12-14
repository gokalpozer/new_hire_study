CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    conversation_id INT,
    speaker VARCHAR(30),
    sentiment VARCHAR(30),
    intention VARCHAR(30),
    message VARCHAR(200)
);