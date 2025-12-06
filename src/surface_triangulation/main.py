from .app import create_app
from surface_triangulation.config.app_config import configure_app

def main() -> None:
    # Load the application configuration
    configure_app()

    # Launch the application
    create_app()

if __name__ == "__main__":
    main()
