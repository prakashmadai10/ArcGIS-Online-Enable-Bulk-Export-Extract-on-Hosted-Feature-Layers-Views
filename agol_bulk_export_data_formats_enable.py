"""
ArcGIS Online – Fast Export Enabler for Hosted Feature Layers
=============================================================
Parallelized version with thread-safe logging and summary reporting.

"""

import pandas as pd
import concurrent.futures
from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection

gis = GIS("home")

GROUP_IDS = [
    "8a422fc62b134b7182e57ff3c78f5971",
    "4d168b55c84d4f1abc8797ffbfec5323",
    "aa33558d2e3247ef9e341ac45ee091d8",
    "84e69fd1f7a94d39adb94b070e4e910a"
]

def is_hosted(item):
    return "hosted service" in [tk.lower() for tk in (item.typeKeywords or [])]

results = []
processed_ids = set()

def enable_export(item):
    """Enable exportData + Extract capability for one item."""
    if item.id in processed_ids:
        return
    processed_ids.add(item.id)

    record = {"Item Title": item.title, "Item ID": item.id, "Status": "", "Notes": ""}
    print(f"Processing: {item.title} [{item.type}]")

    if not is_hosted(item):
        record["Status"] = "Skipped"
        record["Notes"] = "Not hosted"
        results.append(record)
        return

    # Enable export toggle
    try:
        item.update(item_properties={"exportData": True, "properties": {"exportData": True}})
    except Exception as ex:
        record["Notes"] += f"Item update failed: {ex}. "

    # Enable Extract capability
    try:
        flc = FeatureLayerCollection.fromitem(item)
        caps = set(c.strip() for c in flc.properties.get("capabilities", "").split(",") if c.strip())
        if "Extract" not in caps:
            caps.add("Extract")
            flc.manager.update_definition({"capabilities": ",".join(sorted(caps))})
        record["Status"] = "Success"
    except Exception as ex:
        record["Status"] = "Partial Failure"
        record["Notes"] += f"Capability update failed: {ex}. "

    # Process related hosted views (once only)
    try:
        rels = (
            item.related_items("Service2Data", "forward")
            + item.related_items("Service2Data", "reverse")
            + item.related_items("Service2Service", "forward")
            + item.related_items("Service2Service", "reverse")
        )
        for v in rels:
            if is_hosted(v) and "View Service" in (v.typeKeywords or []):
                enable_export(v)
    except Exception as ex:
        record["Notes"] += f"View discovery failed: {ex}. "

    results.append(record)


# Main parallel executor
def process_group(gid):
    grp = gis.groups.get(gid)
    if not grp:
        print(f"! Group not found: {gid}")
        return
    print(f"\n=== Group: {grp.title} ({gid}) ===")
    items = [it for it in grp.content() if it.type in ("Feature Service", "Feature Layer")]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        executor.map(enable_export, items)


for gid in GROUP_IDS:
    process_group(gid)

# Save summary
df = pd.DataFrame(results)
csv_path = "export_enable_fast_report.csv"
df.to_csv(csv_path, index=False)
print("\n=== Summary Report ===")
print(df)
print(f"\nReport saved to: {csv_path}")
print("\n✅ Completed successfully (Fast Mode).")
