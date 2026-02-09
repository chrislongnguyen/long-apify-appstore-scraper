# App Store Volatility Analyzer

Deterministic extraction and statistical analysis of "Enshittification" signals from App Store reviews.

## Setup

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

**Important:** Always activate the virtual environment first:

```bash
# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Then run the script
python main.py

# Or use smoke test mode (10 reviews, first app only)
python main.py --smoke-test

# With explicit API token
python main.py --smoke-test --apify-token YOUR_TOKEN
```

**Alternative:** Use venv Python directly without activation:
```bash
venv/bin/python main.py --smoke-test
```

## Project Structure

- `config/` - Configuration files (targets.json, pain_keywords.json)
- `src/` - Source code (Fetcher, Analyzer, Reporter classes)
- `reports/` - Generated analysis reports

## Documentation

See `docs/ai/` for requirements, design, and planning documentation.
