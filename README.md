# cloud-gpt

## Projects

- **`cloud_gpt.etl`** — a small orders ETL pipeline (extract from CSV, validate/clean, load into SQLite). CLI: `python -m cloud_gpt.etl.pipeline <source_csv> <db_path>`.
- **`cloud_gpt.mcp_server`** — an MCP server exposing the ETL pipeline as tools (`run_orders_etl`, `list_orders`) for an LLM client to call.

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
