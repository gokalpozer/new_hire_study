# README

## Project Overview

This project performs sentiment and intent analysis on conversational data using a zero-shot classification approach. The model employed is the **facebook/bart-large-mnli**, which predicts sentiments and intents from input text and logs the results into a PostgreSQL database.

The application is designed to be run as a command-line tool with the command `run-my-project` and is implemented in Python, utilizing the BART model for text classification.

---

## Project Structure

```
my_project/
├── build/                      # Generated after running setup.py for distribution
├── dist/                       # Generated distribution packages
├── my_project.egg-info/        # Metadata for the package
├── src/
│   ├── main.py                 # Core script for running the application
│   ├── __init__.py             # Required for packaging
│   ├── insert.sql              # SQL script for creating the database table
├── config/
│   ├── settings.yaml           # Configuration file (model and database settings)
│   ├── __init__.py             # Required for packaging
├── data/
│   ├── iphone.json             # Sample conversational data
│   ├── __init__.py             # Required for packaging
├── resources/
│   ├── zero_shot_model.py      # Zero-shot classification implementation
│   ├── __init__.py             # Required for packaging
├── setup.py                    # Setup script for packaging and distribution
├── requirements.txt            # Dependency list
└── README.md                   # Project documentation (this file)
```

---

## Installation and Setup

### Prerequisites
- Python 3.8+
- PostgreSQL

### Steps
1. Clone the repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the database:
   - Ensure that PostgreSQL is running locally.
   - Update the `connection_string` in `config/settings.yaml` with your PostgreSQL credentials.
   - The database table will be automatically created when you run the program.
4. Build and install the package:
   ```bash
   python setup.py sdist bdist_wheel
   pip install dist/my_project-1.0-py3-none-any.whl
   ```

---

## Usage

Run the project using the following terminal command:
```bash
run-my-project
```

The program will:
1. Load the **facebook/bart-large-mnli** model.
2. Parse the conversational data from `data/iphone.json`.
3. Perform sentiment and intent analysis on each message.
4. Log the predictions into the PostgreSQL database.

---

## Key Components

### 1. `src/main.py`
Handles the primary workflow, including:
- Loading configuration and data.
- Initializing the `ZeroShotClassifier`.
- Performing sentiment and intent predictions.
- Logging results to the PostgreSQL database.

**Enhancement**: Sends both 'speaker' and 'message' in this format: `'speaker' + ': ' + 'message' to increase its performance on intent classification.


### 2. `src/insert.sql`
Defines the schema for the `logs` table:
```sql
CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    conversation_id INT,
    speaker VARCHAR(30),
    sentiment VARCHAR(50),
    intention VARCHAR(50),
    message VARCHAR(200)
);
```

### 3. `config/settings.yaml`
Contains configurations for:
- Model: `facebook/bart-large-mnli`
- Logging level: `INFO`
- Database connection string (e.g., `postgresql://username:password@localhost:5432/logs`)

### 4. `resources/zero_shot_model.py`
Implements the zero-shot classification using the Hugging Face `transformers` library.

### 5. `data/iphone.json`
A sample dataset of conversational exchanges used for analysis, created using ChatGPT.

```json
{
  "conversation": [
    {
      "speaker": "Salesman",
      "message": "Hello! Welcome to our store. How can I assist you today?"
    }
  ]
}
```

---

## Dependencies
The project requires the following Python packages:
- `transformers==4.38.0`
- `pyyaml==6.0`
- `aiofiles==23.1.0`
- `asyncpg==0.28.0`
- `tensorflow==2.13.0`
- `psycopg2==2.9.10`

Install them using:
```bash
pip install -r requirements.txt
```

---

## Notes
- This project uses a **local PostgreSQL database** for storing logs.
- The `ZeroShotClassifier` leverages the **facebook/bart-large-mnli** model for performing sentiment and intent analysis.
- Conversational data is provided in JSON format and should follow the structure of `data/iphone.json`.
- The table schema for logging results is defined in `src/insert.sql`.

---

## Author
Gökalp Özer
