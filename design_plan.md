# EVE_INDUSTRY Application Design
sk-ed9d66990f264f2cb3143842e3f4bb57
## Project Overview

A PySide6 and DuckDB GUI application for EVE Online industry management.

## Project Structure

EVE_INDUSTRY/
├── pyproject.toml
├── README.md
├── .gitignore
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
│       │   │   ├── facilities_view.py
│       │   │   └── settings_view.py
│       │   ├── dialogs/
│       │   │   ├── __init__.py
│       │   │   ├── import_recipe_dialog.py
│       │   │   ├── facility_edit_dialog.py
│       │   │   └── bpo_edit_dialog.py
│       │   └── widgets/
│       │       ├── __init__.py
│       │       └── refresh_button.py
│       ├── modules/
│       │   ├── __init__.py
│       │   ├── price_fetcher.py
│       │   ├── esi_client.py
│       │   └── yaml_handler.py
│       └── styles/
│           └── dark_theme.qss
├── data/
│   ├── initial/
│   │   ├── bpos.yaml
│   │   ├── bpcs.yaml
│   │   ├── recipes.yaml
│   │   └── facilities.yaml
│   ├── database/
│   │   └── industry.duckdb
│   └── exports/
└── tests/
    ├── __init__.py
    ├── test_database.py
    └── test_import.py

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
bpos:

- name: "Capital Capacitor Battery"
    me_level: 9
    te_level: 18
    location: "Keberz"
    category: "capital_components"
    materials:
      Tritanium: 500000
      Pyerite: 250000
      Mexallon: 100000
      Isogen: 50000
      Nocxium: 10000
      Zydrine: 5000
      Megacyte: 2000
- name: "Oxygen Fuel Block"
    me_level: 10
    te_level: 10
    location: "UALX-3"
    category: "fuel"
    materials:
      Tritanium: 500
      Pyerite: 250
      Mexallon: 100
      Isogen: 50
      LiquidOzone: 100
      HeavyWater: 50
- name: "XL Cruise Missile Launcher"
    me_level: 8
    te_level: 0
    location: "Keberz"
    category: "capital_components"
    materials:
      Tritanium: 300000
      Pyerite: 150000
      Mexallon: 75000
      Isogen: 30000
      Nocxium: 5000
      Zydrine: 2500
      Megacyte: 1000

data/initial/facilities.yaml:
facilities:

- name: "Empire Reforged"
    system: "Keberz"
    region: "Khanid"
    facility_type: "Azbel"
    owner: "Brave Empire"
    services: ["manufacturing", "research", "invention"]
    manufacturing_slots: 10
    research_slots: 8
    cost_index: 0.035
    rigs:
  - name: "Standup L-Set Basic Ship Manufacturing Efficiency I"
        bonus: "-2% time"
    notes: "Main Empire manufacturing hub"
- name: "Starforge of Bravery"
    system: "UALX-3"
    region: "The Citadel"
    facility_type: "Sotiyo"
    owner: "Brave Collective"
    services: ["manufacturing", "research", "invention"]
    manufacturing_slots: 15
    research_slots: 10
    cost_index: 0.0659
    rigs:
  - name: "Standup XL-Set Ship Manufacturing Efficiency I"
        bonus: "-3% material"
    notes: "Capital manufacturing disabled"
- name: "The Science Lounge"
    system: "UALX-3"
    region: "The Citadel"
    facility_type: "Sotiyo"
    owner: "Brave Collective"
    services: ["research", "invention"]
    manufacturing_slots: 0
    research_slots: 20
    cost_index: 0.0659
    rigs:
  - name: "Standup XL-Set Laboratory Optimization I"
        bonus: "-2% time"
    notes: "Research and invention only"

data/initial/bpcs.yaml:
bpcs:

- name: "T2 Light Missile Launcher"
    source_bpo: "Light Missile Launcher"
    runs_remaining: 10
    location: "Keberz"
    category: "module_t2"
    materials:
      Tritanium: 2000
      Pyerite: 1000
      Mexallon: 500
      Isogen: 200
      Morphite: 50

data/initial/recipes.yaml:
recipes:

- name: "T2 Light Missile Launcher"
    recipe_type: "BPC"
    base_item: "Light Missile Launcher"
    me_level: 2
    te_level: 2
    materials:
      Tritanium: 2000
      Pyerite: 1000
      Mexallon: 500
      Isogen: 200
      Morphite: 50
    upgrade_paths:
  - type: "invention"
        datacores: 8
        decryptor: "Test Reports"
        chance: 0.4

## Main Window Design

The main window features a split layout:

- Left side: Vertical button bar with navigation buttons: "BPO List", "BPC Inventory", "Recipes", "Facilities", "Settings"
- Right side: Stacked widget showing the selected view

## Views

BPO List View:

- QTableWidget with columns: Name, ME, TE, Location, Category
- Refresh button and Add BPO button above table
- Double-click row to open edit dialog

BPC Inventory View:

- QTableWidget with columns: Name, Source BPO, Runs, Location, Category
- Refresh button and Add BPC button above table
- Rows with runs < 10 are color-coded yellow

Recipes View:

- Split view: Left side shows recipe categories tree, right side shows selected recipe details
- Tree categories: "BPO Recipes" (by category), "BPC Recipes" (by source), "PI Components" (by tier)
- Recipe details include name, type, material requirements table, upgrade paths
- Add Recipe and Edit Recipe buttons

Facilities View:

- QTableWidget with columns: Name, System, Type, Owner, Manufacturing Slots, Research Slots, Cost Index
- Refresh, Add Facility, Import YAML, Export YAML buttons above table
- Double-click row to open facility edit dialog with tabs for basic info, services, rigs, notes

Settings View:

- Database path configuration
- Import/Export buttons for YAML (all tables)
- Default trade hub selection (Jita, Amarr, etc.)
- Cache duration settings for price fetcher

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

- Import/export facilities, recipes, BPOs from/to YAML
- Validate YAML structure against schemas
- Convert between YAML and database formats

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
