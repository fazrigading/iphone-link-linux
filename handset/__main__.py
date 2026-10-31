"""Entry point for `python -m handset`."""

import sys


def _print_help() -> None:
    print("iPhone Link - Native iPhone Mirroring & Control")
    print()
    print("Linux/Windows source run:")
    print("  python -m handset                 # default: start backend + window")
    print("  python -m handset --server-only  # backend only")
    print("  python -m handset --server-child --host HOST --port PORT")
    print("                                     # child server for the launcher")
    print()
    print("Linux launcher:")
    print("  ./run_linux.sh                    # same as python -m handset")
    print()
    print("Environment variables:")
    print("  PANE_HOST / PANE_PORT            # override host/port")


def main() -> None:
    if "--help" in sys.argv:
        _print_help()
        return

    if (
        "--server-child" in sys.argv
        or "--server-only" in sys.argv
        or ("--port" in sys.argv and "--gui" not in sys.argv and "--smoke-test" not in sys.argv)
    ):
        from handset.server import main as server_main
        server_main()
        return

    if sys.platform == "linux":
        from handset.linux_main import main as linux_main
        linux_main()
    elif sys.platform == "win32":
        from handset.gui import main as gui_main
        gui_main()
    else:
        from handset.gui import main as other_main
        other_main()


if __name__ == "__main__":
    main()
