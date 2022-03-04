"""Command line GUI access point."""
import sys
from .Crow import main


def start_Crow():
    """Opens the GUI.
    """
    sys.exit(main())


if __name__ == "__main__":
    start_Crow()
