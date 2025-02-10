# LOGINNETWORK

## Installation

```bash
uv sync
```

## Environment

### Environment Variables for Running Streamlit

```bash
cp .streamlit/example.secrets.toml .streamlit/secrets.toml
```

Enter your secrets in `.streamlit/secrets.toml`.

### Environment Variables for Running Tests

```bash
cp .env.example .env
```

Enter your secrets in `.env`.

## Usage

```bash
uv run streamlit run src/main.py
```

## Test

```bash
# Run once after git clone
uv pip install -e .
uv run pytest

# To run logic tests that do not have the 'test_' prefix:
uv run python rag_chatbot.py
```
