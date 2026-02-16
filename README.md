# EVE Industry Management System

A PySide6 and DuckDB GUI application for EVE Online industry management.

## Features

- **BPO Management**: Track Blueprint Originals with ME/TE levels, locations, and categories
- **BPC Inventory**: Manage Blueprint Copies with run counts and locations
- **Recipe Management**: Store and manage manufacturing recipes with materials
- **Facility Management**: Track manufacturing facilities with services, slots, and rigs
- **Price Integration**: Fetch market prices from ESI API
- **YAML Import/Export**: Easy data exchange via YAML files

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/eve-industry.git
   cd eve-industry
   ```

2. Install dependencies:
   ```bash
   pip install -e .
   ```

3. For development:
   ```bash
   pip install -e ".[dev]"
   ```

## Usage

Run the application:
```bash
eve-industry
```

## Project Structure

```
eve-industry/
├── src/eve_industry/          # Main Python package
│   ├── main.py               # Application entry point
│   ├── database/             # Database layer
│   ├── gui/                  # GUI components
│   ├── modules/              # Business logic modules
│   └── styles/               # Styling files
├── data/                     # Application data
│   ├── initial/              # Initial YAML data files
│   ├── database/             # DuckDB database files
│   └── exports/              # Export directory
├── tests/                    # Test suite
└── AI/                       # AI-generated content (git-ignored)
```

## AI Directory Usage

The `AI/` directory is excluded from git version control (see `.gitignore`) and is intended for:

- **AI-generated analyses**: Project analysis, code reviews, and architecture assessments
- **AI prompts**: Conversation histories, prompt templates, and AI interaction logs
- **Temporary AI files**: Generated documentation, code suggestions, and other AI outputs
- **Tool integration**: Files created by AI tools like Cline, Cursor, Copilot, etc.

**Purpose**: This directory keeps the main codebase clean while providing a dedicated space for AI-assisted development artifacts that shouldn't be committed to version control.

## Database Schema

The application uses DuckDB with the following main tables:

- **bpos**: Blueprint Originals (name, me_level, te_level, location, category, materials_json)
- **bpcs**: Blueprint Copies (name, source_bpo, runs_remaining, location, category, materials_json)
- **recipes**: Manufacturing recipes (name, recipe_type, base_item, me_level, te_level, materials_json, upgrade_paths_json)
- **facilities**: Manufacturing facilities (name, system, region, facility_type, owner, services_json, manufacturing_slots, research_slots, cost_index, rigs_json, notes)
- **metadata**: Application metadata

## Development

- Code formatting: `black src tests`
- Linting: `flake8 src tests`
- Testing: `pytest`

## License

MIT License