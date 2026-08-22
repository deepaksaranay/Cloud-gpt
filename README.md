# cloud-gpt

## Projects

- **`cloud_gpt.etl`** — a small orders ETL pipeline (extract from CSV, validate/clean, load into SQLite). CLI: `python -m cloud_gpt.etl.pipeline <source_csv> <db_path>`.
- **`cloud_gpt.mcp_server`** — an MCP server exposing the ETL pipeline as tools (`run_orders_etl`, `list_orders`) for an LLM client to call.
- **`cloud_gpt.physics_api`** — a FastAPI service that answers physics questions by looking up the best-matching Wikipedia (Wikimedia) article and returning its summary. Run: `cloud-gpt-physics-api`.

## Setup

```bash
pip install -e ".[dev]"
pytest
```

## Running the MCP server

```bash
cloud-gpt-mcp-server
```

Point an MCP client (e.g. Claude Desktop/Code) at it with a config entry such as:

```json
{
  "mcpServers": {
    "cloud-gpt-orders": {
      "command": "cloud-gpt-mcp-server"
    }
  }
}
```

## Running the physics API

```bash
cloud-gpt-physics-api
```

Starts a FastAPI server on `http://127.0.0.1:8000`. `POST /ask` with `{"question": "..."}` to get an answer
sourced from Wikipedia; questions with no recognizable physics term are rejected with `422`, and a question
with no matching Wikipedia article returns `404`.

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Newton'"'"'s second law of motion?"}'
```
