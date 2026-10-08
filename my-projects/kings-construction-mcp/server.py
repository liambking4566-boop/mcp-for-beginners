"""Kings Construction & Property Solutions - first MCP server.

Gives an AI assistant three quoting tools, a rate-card resource and a
quote-email prompt. Built on the MCP Python SDK 2.x (MCPServer).
"""

import math
from typing import TypedDict

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Kings Construction")

GST_RATE = 0.10  # Australian GST

# Placeholder rates - replace with your real figures.
RATE_CARD = {
    "labour_per_hour": 85.00,
    "call_out_fee": 60.00,
    "default_markup_percent": 15.0,
    "paint_coverage_m2_per_litre": 12.0,
    "concrete_bag_20kg_yield_m3": 0.01,
}


class JobEstimate(TypedDict):
    labour: float
    materials_with_markup: float
    call_out_fee: float
    subtotal_ex_gst: float
    gst: float
    total_inc_gst: float


class ConcreteVolume(TypedDict):
    net_m3: float
    order_m3: float
    bags_20kg: int


class PaintQuantity(TypedDict):
    litres_exact: float
    litres_to_buy: int


@mcp.tool()
def job_estimate(
    labour_hours: float,
    materials_cost: float,
    hourly_rate: float = RATE_CARD["labour_per_hour"],
    markup_percent: float = RATE_CARD["default_markup_percent"],
    include_call_out: bool = True,
) -> JobEstimate:
    """Estimate a handyman/maintenance job price in AUD, including 10% GST.

    Markup is applied to materials only. Amounts are rounded to the cent.
    """
    if labour_hours < 0 or materials_cost < 0 or hourly_rate < 0 or markup_percent < 0:
        raise ValueError("Hours, costs, rate and markup must not be negative")

    labour = labour_hours * hourly_rate
    materials = materials_cost * (1 + markup_percent / 100)
    call_out = RATE_CARD["call_out_fee"] if include_call_out else 0.0
    subtotal = labour + materials + call_out
    gst = subtotal * GST_RATE
    return {
        "labour": round(labour, 2),
        "materials_with_markup": round(materials, 2),
        "call_out_fee": round(call_out, 2),
        "subtotal_ex_gst": round(subtotal, 2),
        "gst": round(gst, 2),
        "total_inc_gst": round(subtotal + gst, 2),
    }


@mcp.tool()
def concrete_volume(
    length_m: float, width_m: float, depth_mm: float, waste_percent: float = 10.0
) -> ConcreteVolume:
    """Concrete needed for a rectangular slab or footing, with a waste allowance."""
    if min(length_m, width_m, depth_mm) <= 0 or waste_percent < 0:
        raise ValueError("Dimensions must be positive and waste must not be negative")

    net = length_m * width_m * depth_mm / 1000
    total = net * (1 + waste_percent / 100)
    return {
        "net_m3": round(net, 3),
        "order_m3": round(total, 3),
        "bags_20kg": math.ceil(total / RATE_CARD["concrete_bag_20kg_yield_m3"]),
    }


@mcp.tool()
def paint_quantity(wall_area_m2: float, coats: int = 2) -> PaintQuantity:
    """Litres of paint for a wall area, rounded up to whole litres."""
    if wall_area_m2 <= 0 or coats < 1:
        raise ValueError("Area must be positive and coats at least 1")

    litres = wall_area_m2 * coats / RATE_CARD["paint_coverage_m2_per_litre"]
    return {"litres_exact": round(litres, 2), "litres_to_buy": math.ceil(litres)}


@mcp.resource("rates://standard")
def standard_rates() -> dict:
    """The current standard rate card used by the quoting tools."""
    return RATE_CARD


@mcp.prompt()
def quote_email(client_name: str, job_description: str) -> str:
    """Draft a professional quote email for a client."""
    return (
        f"Write a friendly, professional quote email from Kings Construction & "
        f"Property Solutions to {client_name} for this job: {job_description}. "
        f"Use the job_estimate tool to price it, show the GST-inclusive total, "
        f"state the quote is valid for 30 days, and keep it under 200 words."
    )


if __name__ == "__main__":
    mcp.run()
