#!/usr/bin/env python3
"""
Analyst Dashboard - Entry Point

Usage:
    python main.py              # Run CLI mode
    python main.py --streamlit  # Run Streamlit dashboard
    python main.py --panel      # Run Panel dashboard
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src import AnalystDashboard, main

if __name__ == "__main__":
    main()
