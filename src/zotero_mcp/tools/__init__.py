"""Tool modules — importing this package registers all tools with the MCP app."""

from zotero_mcp.tools import (  # noqa: F401
    annotations,
    connectors,
    read_pdf,
    retrieval,
    search,
    write,
)

# Optional: Scite enrichment (requires ``pip install zotero-mcp-server[scite]``)
try:
    from zotero_mcp.tools import scite as scite  # noqa: F401
except ImportError:
    pass

# ---------------------------------------------------------------------------
# Lite mode: only keep essential tools to reduce system prompt size.
# Set ZOTERO_MCP_LITE=true to enable.
# ---------------------------------------------------------------------------
import os as _os

if _os.environ.get("ZOTERO_MCP_LITE", "").lower() in ("1", "true", "yes"):
    from zotero_mcp._app import mcp as _mcp

    _KEEP_TOOLS = {
        "zotero_search_items",
        "zotero_semantic_search",
        "zotero_get_item_metadata",
        "zotero_get_attachment_path",
        "zotero_get_collection_items",
        "zotero_search_collections",
        "zotero_create_note",
        "zotero_update_item",
    }

    import asyncio as _asyncio

    async def _prune_tools():
        all_tools = await _mcp.list_tools()
        for t in all_tools:
            if t.name not in _KEEP_TOOLS:
                try:
                    _mcp.local_provider.remove_tool(t.name)
                except Exception:
                    pass

    try:
        loop = _asyncio.get_running_loop()
        loop.create_task(_prune_tools())
    except RuntimeError:
        _asyncio.run(_prune_tools())
