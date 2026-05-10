"""Allow running the module with python -m wallpaper_engine"""

import sys
import argparse
from .app import main


def cli():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Wallpaper Engine - Animated particle background"
    )
    parser.add_argument(
        "-f", "--fullscreen",
        action="store_true",
        help="Run in fullscreen mode"
    )
    
    args = parser.parse_args()
    main(fullscreen=args.fullscreen)


if __name__ == "__main__":
    cli()
