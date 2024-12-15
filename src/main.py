import json
import yaml
import asyncio
from resources.zero_shot_model import ZeroShotClassifier
import os
import aiofiles
import importlib.resources
import time


async def log_to_db(connection_string, data):
    import asyncpg
    import importlib.resources

    conn = await asyncpg.connect(connection_string)

    # Use importlib.resources to access the insert.sql file
    try:
        with importlib.resources.open_text('src', 'insert.sql') as f:
            create_table_query = f.read()
    except FileNotFoundError:
        raise FileNotFoundError("The file insert.sql does not exist in the package.")

    # Check if the 'logs' table exists
    table_check_query = "SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'logs')"
    table_exists = await conn.fetchval(table_check_query)

    if not table_exists:
        # If the table doesn't exist, create it
        await conn.execute(create_table_query)

    # Retrieve the last conversation_id from the logs table
    last_id_query = "SELECT MAX(conversation_id) FROM logs"
    last_conversation_id = await conn.fetchval(last_id_query)
    if last_conversation_id is None:
        last_conversation_id = 0  # Start with 0 if no data exists in the table

    # Increment to get the new conversation_id
    new_conversation_id = last_conversation_id + 1

    # Insert each row into the logs table with the new conversation_id
    for row in data:
        await conn.execute(
            """
            INSERT INTO logs (conversation_id, speaker, sentiment, intention, message)
            VALUES ($1, $2, $3, $4, $5)
            """,
            new_conversation_id,
            row["speaker"],
            row["sentiment"],
            row["intention"],
            row["message"],
        )
    await conn.close()


async def main():
    try:
        # Method 1: Using importlib.resources
        with importlib.resources.open_text('config', 'settings.yaml') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        # Fallback method: try absolute path
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'settings.yaml')
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

    # Initialize Classifier
    model_name = config["model"]["name"]
    classifier = ZeroShotClassifier(model_name)

    # Load Conversation Data
    try:
        with importlib.resources.open_text('data', 'iphone.json') as f:
            conversation = json.load(f)
    except FileNotFoundError:
        # Fallback method with absolute path
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'iphone.json')
        with open(data_path, "r") as f:
            conversation = json.load(f)

    start_time = time.time()

    candidate_labels = ["positive", "negative", "neutral"]
    intents = ["buy", "upgrade", "information", "greeting", "confirm", "decline", "choose"]

    results = []
    for step in conversation["conversation"]:
        text = step["message"]
        sentiment = classifier.predict(text, candidate_labels)
        intent = classifier.predict(text, intents)
        results.append({
            "speaker": step["speaker"],
            "sentiment": sentiment["labels"][0],
            "intention": intent["labels"][0],
            "message": text
        })
    end_time = time.time()
    print(f"Prediction Time: {end_time - start_time:.2f} seconds")

    # Log Results
    await log_to_db(config["database"]["connection_string"], results)
    print("Processed and logged results successfully!")


def run():
    # Explicitly run the async main function
    asyncio.run(main())


# This allows both direct script running and package entry point execution
if __name__ == "__main__":
    run()
