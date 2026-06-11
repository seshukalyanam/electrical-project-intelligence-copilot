from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from src.utils.config import DATA_DIR, LOCAL_DB_DIR
from src.utils.helpers import read_json, utc_stamp


def load_catalog() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "shared" / "materials_catalog.csv")


def load_labor_rates() -> dict[str, Any]:
    return read_json(DATA_DIR / "shared" / "labor_rates.json", {})


def generate_estimate(project_id: str, category_filter: str | None = None) -> tuple[pd.DataFrame, dict[str, Any], Path]:
    catalog = load_catalog()
    labor_rates = load_labor_rates()
    quantities = read_json(DATA_DIR / project_id / "estimates" / "project_quantities.json", {})
    labor_rate = float(labor_rates.get("journeyman_hourly_rate", 82))
    rows = []
    for item in quantities.get("items", []):
        if category_filter and category_filter.lower() not in item["category"].lower():
            continue
        match = catalog[catalog["item_code"] == item["item_code"]]
        if match.empty:
            rows.append({**item, "warning": "Missing from materials catalog"})
            continue
        cat = match.iloc[0]
        qty = float(item["quantity"])
        unit_cost = float(cat["unit_cost"])
        labor_hours_per_unit = float(cat["labor_hours_per_unit"])
        total_labor_hours = qty * labor_hours_per_unit
        rows.append(
            {
                "Category": item["category"],
                "Item": cat["item_name"],
                "Quantity": qty,
                "Unit": cat["unit"],
                "Unit Cost": unit_cost,
                "Material Total": round(qty * unit_cost, 2),
                "Labor Hours/Unit": labor_hours_per_unit,
                "Total Labor Hours": round(total_labor_hours, 2),
                "Labor Cost": round(total_labor_hours * labor_rate, 2),
                "Total Cost": round(qty * unit_cost + total_labor_hours * labor_rate, 2),
                "Notes": item.get("notes", ""),
            }
        )
    df = pd.DataFrame(rows)
    output_dir = LOCAL_DB_DIR / "estimates"
    output_dir.mkdir(parents=True, exist_ok=True)
    out = output_dir / f"{project_id}_estimate_{utc_stamp()}.csv"
    df.to_csv(out, index=False)
    summary = {
        "material_total": round(float(df.get("Material Total", pd.Series(dtype=float)).sum()), 2),
        "labor_hours": round(float(df.get("Total Labor Hours", pd.Series(dtype=float)).sum()), 2),
        "labor_cost": round(float(df.get("Labor Cost", pd.Series(dtype=float)).sum()), 2),
        "total_cost": round(float(df.get("Total Cost", pd.Series(dtype=float)).sum()), 2),
        "assumptions": quantities.get("assumptions", []),
        "missing_data_warnings": quantities.get("missing_data_warnings", []),
    }
    return df, summary, out
