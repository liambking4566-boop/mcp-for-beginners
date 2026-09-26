# Kings Construction MCP Server

A first MCP server, built while working through
[Module 03 – First Server](../../03-GettingStarted/01-first-server/README.md).
Instead of the lesson's `add`/`subtract` demo, it gives an AI assistant real
quoting tools for Kings Construction & Property Solutions.

## What it exposes

| Type     | Name              | What it does                                                      |
| -------- | ----------------- | ----------------------------------------------------------------- |
| Tool     | `job_estimate`    | Labour + materials (with markup) + call-out fee + 10% GST in AUD  |
| Tool     | `concrete_volume` | m³ for a slab/footing, with waste allowance and 20 kg bag count    |
| Tool     | `paint_quantity`  | Litres of paint for a wall area and number of coats               |
| Resource | `rates://standard`| The rate card the tools use                                       |
| Prompt   | `quote_email`     | Drafts a client quote email using `job_estimate`                  |

> The rates in `RATE_CARD` (`server.py`) are placeholders. Replace them with
> your real labour rate, call-out fee and markup before using it for quotes.

## Run it

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m pytest -q             # end-to-end test over stdio
```

Try it interactively with the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector python server.py
```

## Connect it to Claude Desktop

Add this to `claude_desktop_config.json`, using the full paths on your machine:

```json
{
  "mcpServers": {
    "kings-construction": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/kings-construction-mcp/server.py"]
    }
  }
}
```

Then ask Claude: *"Quote a job: 4 hours labour and $200 of materials."*

## Note on SDK version

This uses the MCP Python SDK **2.x**, where `FastMCP` was renamed to
`MCPServer` (`from mcp.server.mcpserver import MCPServer`). The lesson's
solution code still uses `from mcp.server.fastmcp import FastMCP`, which only
works with `mcp<2`.
