# ArcGIS Online – Bulk Export Enabler for Hosted Layers Automation

This Python tool automates toggling the **“Allow others to export to different formats”** setting across multiple hosted feature layers and hosted views in ArcGIS Online.  
It is especially useful in **distributed collaboration environments** and **ArcGIS Hub / Open Data portals** where layers must be exportable in formats like CSV, Shapefile, GeoJSON, FileGDB, Excel, and more.

---

## 🧭 Overview

When data is shared through **ArcGIS Hub** or **distributed collaboration workspaces**, each hosted feature layer must have the  
“Allow others to export to different formats” toggle turned **ON** to allow public export options.

Manually enabling this for hundreds of layers and hosted views is slow  and time consuming— this script automates it safely and efficiently.

### ✅ The script performs

1. Enables item-level toggle → `exportData = True`  
2. Adds service-level capability → `"Extract"`  
3. Recursively applies the same settings to all **hosted views**  
4. Generates a detailed **CSV summary report**

---

## 💡 Key Features

| Feature | Description |
|----------|--------------|
| ⚙️ **Bulk Automation** | Enables export for all hosted feature layers and views in selected groups |
| ⚡ **Parallel Processing** | Uses ThreadPoolExecutor for 4–6× faster performance |
| 🧠 **Smart Recursion** | Automatically detects and updates hosted views |
| 📊 **Summary Report** | Exports audit results to CSV (`export_enable_report.csv`) |
| 🧱 **Multi-Group Support** | Works across distributed collaboration workspaces |

---

## 🧰 Requirements

- ArcGIS API for Python (≥ 2.1)  
- pandas  
- ArcGIS Online or Portal credentials with update access

### Install dependencies
```bash
pip install arcgis pandas

## 🚀 Usage

1. Edit the script to include your target **Group IDs**:

   ```python
   GROUP_IDS = [
       "8a422fc62b134b7182e57ff3c78f5971",
       "4d168b55c84d4f1abc8797ffbfec5323",
       "aa33558d2e3247ef9e341ac45ee091d8",
       "84e69fd1f7a94d39adb94b070e4e910a"
   ]
   ```

2. Run the script:

   ```bash
   python enable_export_fast.py
   ```

3. Review the output and the summary CSV.

---

## 🖥️ Example Console Output

```text
=== Group: Public Works Layers (8a422fc62b134b7182e57ff3c78f5971) ===
Processing: Streetlight Outages [Feature Service] (abc123)
  ✓ Item toggle set: exportData = True
  ✓ Service capability 'Extract' enabled
  ↳ View detected: Streetlight_Outages_View

Report saved to: export_enable_report.csv
✅ Completed successfully. All hosted layers/views reviewed.
```

---

## 📂 Example – ArcGIS Online Export Options

Below is an example of how layers appear after the script successfully enables the export toggle.
!([Toggle for Export AGOL.png](https://github.com/prakashmadai10/ArcGIS-Online-Enable-Bulk-Export-Extract-on-Hosted-Feature-Layers-Views/blob/main/Toggle%20for%20Export%20AGOL.png))
*Figure: “Allow others to export to different formats” enables these options for public users.*

When shared via **ArcGIS Hub**, users can now export in any of these formats:
![ArcGIS Export Options](https://github.com/prakashmadai10/ArcGIS-Online-Enable-Bulk-Export-Extract-on-Hosted-Feature-Layers-Views/blob/main/Different%20File%20Formats.png)

---

## 📊 Example Summary CSV Output

| Item Title               | Item ID | Status  | Notes |
| ------------------------ | ------- | ------- | ----- |
| Streetlight Outages      | abc123  | Success |       |
| Streetlight_Outages_View | xyz789  | Success |       |

📄 **Saved as:** `export_enable_report.csv`

---

## 🏛️ Real-World Use Case – City of Midland

This tool is actively used in the **City of Midland’s distributed collaboration setup** to automate enabling export permissions for
hundreds of hosted layers shared between **ArcGIS Enterprise ↔ ArcGIS Online**, ensuring all public-facing layers on **ArcGIS Hub** remain downloadable in open formats.

