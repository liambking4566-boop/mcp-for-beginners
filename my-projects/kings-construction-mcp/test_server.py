"""End-to-end test: starts server.py over stdio and calls it like an AI client would."""

import json
import sys
from pathlib import Path

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = StdioServerParameters(
    command=sys.executable, args=[str(Path(__file__).with_name("server.py"))]
)


@pytest.mark.anyio
async def test_server_end_to_end():
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = {t.name for t in (await session.list_tools()).tools}
            assert tools == {"job_estimate", "concrete_volume", "paint_quantity"}

            est = await session.call_tool(
                "job_estimate", {"labour_hours": 4, "materials_cost": 200}
            )
            data = est.structured_content
            # 4h x $85 = 340, 200 + 15% = 230, call-out 60 -> 630 + GST 63
            assert data["subtotal_ex_gst"] == 630.0
            assert data["total_inc_gst"] == 693.0

            slab = await session.call_tool(
                "concrete_volume", {"length_m": 3, "width_m": 2, "depth_mm": 100}
            )
            assert slab.structured_content["net_m3"] == 0.6
            assert slab.structured_content["order_m3"] == 0.66

            paint = await session.call_tool("paint_quantity", {"wall_area_m2": 40})
            assert paint.structured_content["litres_to_buy"] == 7

            bad = await session.call_tool("paint_quantity", {"wall_area_m2": -5})
            assert bad.is_error

            rates = await session.read_resource("rates://standard")
            assert json.loads(rates.contents[0].text)["labour_per_hour"] == 85.0

            prompt = await session.get_prompt(
                "quote_email", {"client_name": "Sam", "job_description": "fix gate"}
            )
            assert "Sam" in prompt.messages[0].content.text


@pytest.fixture
def anyio_backend():
    return "asyncio"
