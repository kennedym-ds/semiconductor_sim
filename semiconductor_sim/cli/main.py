#!/usr/bin/env python3
"""Main entry point for the semiconductor-sim CLI."""

import argparse
import sys
from typing import List, Optional

from .commands import iv, cv, sweep


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser."""
    parser = argparse.ArgumentParser(
        prog="semiconductor-sim",
        description="A command-line tool for semiconductor device simulation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        metavar="COMMAND",
    )
    
    # IV characteristic command
    iv.setup_parser(subparsers)
    
    # CV characteristic command  
    cv.setup_parser(subparsers)
    
    # Parameter sweep command
    sweep.setup_parser(subparsers)
    
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    if not args.command:
        parser.print_help()
        return 1
        
    try:
        if args.command == "iv":
            return iv.run(args)
        elif args.command == "cv":
            return cv.run(args)
        elif args.command == "sweep":
            return sweep.run(args)
        else:
            parser.print_help()
            return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())