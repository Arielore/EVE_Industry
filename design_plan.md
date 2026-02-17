# EVE_INDUSTRY Application Design
sk-ed9d66990f264f2cb3143842e3f4bb57
## Project Overview

A PySide6 and DuckDB GUI application for EVE Online industry management.

## Project Structure

EVE_INDUSTRY/
├── pyproject.toml
├── README.md
├── .gitignore
├── check_recipes.py
├── test_export.py
├── test_enhanced_export.py
├── design_plan.md
├── src/
│   └── eve_industry/
│       ├── __init__.py
│       ├── main.py
│       ├── database/
│       │   ├── __init__.py
│       │   ├── connection.py
│       │   ├── schema.py
│       │   ├── loader.py
│       │   └── migrations/
│       ├── gui/
│       │   ├── __init__.py
│       │   ├── main_window.py
│       │   ├── views/
│       │   │   ├── __init__.py
│       │   │   ├── bpo_list_view.py
│       │   │   ├── bpc_inventory_view.py
│       │   │   ├── recipes_view.py
│       │   │   ├── recipes_view_fixed.py
│       │   │   ├── facilities_view.py
│       │   │   ├── intake_view.py
│       │   │   └── sde_view.py
│       │   ├── dialogs/
│       │   │   ├── __init__.py
│       │   ├── widgets/
│       │       ├── __init__.py
│       ├── modules/
│       │   ├── __init__.py
│       │   ├── yaml_handler.py
│       │   └── sde_importer.py
│       └── styles/
│           └── dark_theme.qss
├── data/
│   ├── initial/
│   │   ├── bpos.yaml
│   │   ├── bpcs.yaml
│   │   ├── facilities.yaml
│   │   └── eve-online-static-data-3201939-yaml.zip
│   ├── database/
│   │   └── industry.duckdb
│   ├── exports/
│   └── sde/
│       └── parquet/
│           ├── categories.parquet
│           ├── groups.parquet
│           ├── industryActivity.parquet
│           ├── industryActivityMaterials.parquet
│           ├── industryActivityProducts.parquet
│           ├── industryActivitySkills.parquet
│           ├── marketGroups.parquet
│           ├── typeMaterials.parquet
│           └── types.parquet
└── tests/
    ├── __init__.py
    ├── test_app_start.py
    ├── test_db_simple.py
    ├── test_db.py
    ├── test_duckdb_syntax.py
    └── test_final.py

## pyproject.toml

[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "eve-industry"
version = "0.1.0"
description = "EVE Online Industry Management System"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "PySide6>=6.8.0",
    "duckdb>=1.0.0",
    "pyyaml>=6.0",
    "requests>=2.31.0",
    "python-dateutil>=2.8.2",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "black>=23.0",
    "flake8>=6.0",
]

[project.scripts]
eve-industry = "eve_industry.main:main"

[tool.setuptools.packages.find]
where = ["src"]

## Database Schema

Table: bpos

- id INTEGER PRIMARY KEY
- name TEXT UNIQUE
- me_level INTEGER
- te_level INTEGER
- location TEXT
- category TEXT
- materials_json TEXT

Table: bpcs

- id INTEGER PRIMARY KEY
- name TEXT UNIQUE
- source_bpo TEXT
- runs_remaining INTEGER
- location TEXT
- category TEXT
- materials_json TEXT

Table: recipes

- id INTEGER PRIMARY KEY
- name TEXT UNIQUE
- recipe_type TEXT
- base_item TEXT
- me_level INTEGER
- te_level INTEGER
- materials_json TEXT
- upgrade_paths_json TEXT

Table: facilities

- id INTEGER PRIMARY KEY
- name TEXT UNIQUE
- system TEXT
- region TEXT
- facility_type TEXT
- owner TEXT
- services_json TEXT
- manufacturing_slots INTEGER
- research_slots INTEGER
- cost_index DECIMAL
- rigs_json TEXT
- notes TEXT

Table: metadata

- key TEXT PRIMARY KEY
- value TEXT
- updated_at TIMESTAMP

## Initial YAML Files

data/initial/bpos.yaml:
- Contains initial Blueprint Original (BPO) data
- Sample BPOs: Capital Capacitor Battery, Oxygen Fuel Block, XL Cruise Missile Launcher
- Used for initial database population

data/initial/facilities.yaml:
- Contains initial facility data
- Sample facilities: Empire Reforged, Starforge of Bravery, The Science Lounge
- Used for initial database population

data/initial/bpcs.yaml:
- Contains initial Blueprint Copy (BPC) data
- Sample BPCs: T2 Light Missile Launcher
- Used for initial database population

Note: recipes.yaml file has been removed as recipes currently contain only sample data.
Recipe export functionality has been disabled in yaml_handler.py to prevent creating
recipes.yaml files with fake sample data during exports.

## Main Window Design

The main window features a split layout:

- Left side: Vertical button bar with navigation buttons: "BPO List", "BPC Inventory", "Recipes", "Facilities", "Settings"
- Right side: Stacked widget showing the selected view

## Views

BPO List View:

- QTableWidget with columns: Name, ME, TE, Location, Category
- Refresh button and Add BPO button above table
- Double-click row to open edit dialog
- Loads data from database, falls back to sample data if empty

BPC Inventory View:

- QTableWidget with columns: Name, Source BPO, Runs, Location, Category
- Refresh button and Add BPC button above table
- Rows with runs < 10 are color-coded yellow
- Loads data from database, falls back to sample data if empty

Recipes View:

- Split view: Left side shows recipe categories tree, right side shows selected recipe details
- Tree categories: "BPO Recipes" (by category), "BPC Recipes" (by source), "PI Components" (by tier)
- Recipe details include name, type, material requirements table, upgrade paths
- Add Recipe and Edit Recipe buttons
- Uses sample data for demonstration

Facilities View:

- QTableWidget with columns: Name, System, Type, Owner, Manufacturing Slots, Research Slots, Cost Index
- Refresh, Add Facility, Import YAML, Export YAML buttons above table
- Double-click row to open facility edit dialog with tabs for basic info, services, rigs, notes
- Uses sample data for demonstration

Intake View:

- Handles import and export of YAML data files
- Import from YAML: Loads BPOs, BPCs, facilities, recipes from YAML files
- Export to YAML: Exports BPOs, BPCs, facilities, SDE blueprints (recipes not exported)
- Progress dialogs with threading for background operations
- Shows database statistics

SDE View:

- Handles Static Data Export (SDE) import functionality
- Loads EVE Online SDE data from Parquet files
- Creates database views for types, groups, categories, industry activities
- Provides SDE blueprint data for export

## Dialogs

Import Recipe Dialog:

- Modal dialog with large text area for pasting EVE industry copy-paste data
- Parse button to analyze pasted text
- Preview area showing detected item name, materials, quantities, runs
- Dropdown to select recipe type (BPO/BPC/PI)
- Save to Database and Cancel buttons
- Handles industry window material lists, blueprint research window, market window item details

Facility Edit Dialog:

- Tabs: Basic Info (name, system, region, type, owner), Services (checkboxes), Rigs (list with add/edit), Notes
- Save and Cancel buttons

BPO Edit Dialog:

- Form fields: name, ME level, TE level, location, category
- Material requirements table with add/edit/delete
- Save and Cancel buttons

## Modules

price_fetcher.py:

- Class PriceFetcher with methods fetch_current_prices, fetch_historical_prices, get_cached_price, refresh_cache
- Threading support via QThread
- Caching with configurable duration

esi_client.py:

- Handles ESI API communication
- Base URL: <https://esi.evetech.net/latest/>
- Market prices endpoint: /markets/prices/
- Region orders endpoint: /markets/{region_id}/orders/
- Rate limiting with exponential backoff
- Error handling and retry logic

yaml_handler.py:

- Import/export facilities, BPOs, BPCs from/to YAML
- Import recipes from YAML (recipes are not exported as they contain only sample data)
- Export SDE blueprint data when SDE is loaded
- Validate YAML structure against schemas
- Convert between YAML and database formats

bom_tree.py:

- Bill of Materials (BOM) tree analysis for manufacturing planning
- Recursively builds trees from final products back to raw materials
- Supports both custom recipes and SDE manufacturing data
- Generates flat BOMs with raw material totals
- Creates operations sequences with timing for machine scheduling
- Includes caching and intelligent raw material detection
- Provides MaterialNode and BOMAnalysis data structures

## Database Module

connection.py:

- Thread-local DuckDB connections
- Context manager for safe queries
- Methods execute() and execute_df()

schema.py:

- Table creation statements
- Index creation
- Schema version tracking

loader.py:

- On first run, check if database exists
- If not, create schema and load all YAML files from data/initial/
- Methods to reload from YAML with confirmation
- Validate YAML structure before loading

## Styling

dark_theme.qss:

- Dark background: #2b2b2b
- Light text: #ffffff
- Accent color for buttons: #0a6b9c
- Table styling with alternate row colors
- Card styling for dashboard elements

## Status Bar

Bottom of main window showing:

- Last updated timestamp
- Record counts for each table
- Price fetch status
- Database connection status

## Threading

- All database queries run in QThread to prevent UI freezing
- Price fetching runs in separate QThread with progress updates
- YAML import/export runs in background thread with progress dialog
- Signals used to communicate results back to main thread

## Entry Point

src/eve_industry/main.py:

- def main(): function that creates QApplication, loads styles, creates main window, and starts event loop
- if __name__ == "__main__": main()
