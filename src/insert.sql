CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    conversation_id INT,
    speaker VARCHAR(30),
    sentiment VARCHAR(50),
    intention VARCHAR(50),
    message VARCHAR(200)
);