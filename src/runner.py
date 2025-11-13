import argparse
import json
import logging
import sys
from pathlib import Path
import importlib.util
from typing import Any, Dict, List, Optional

DEFAULT_CONFIG: Dict[str, Any] = {
    "input_file": "data/inputs.sample.txt",
    "output_file": "data/output.json",
    "output_format": "json",
    "max_items": 250,
    "log_level": "INFO",
}

def setup_logger(level: str) -> logging.Logger:
    logger = logging.getLogger("facebook_following_scraper")
    if logger.handlers:
        # Already configured
        return logger

    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric_level)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

def load_module(name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module {name} from {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def load_settings(settings_path: Optional[Path], root_dir: Path, logger: logging.Logger) -> Dict[str, Any]:
    config: Dict[str, Any] = dict(DEFAULT_CONFIG)

    if settings_path is None:
        settings_path = root_dir / "src" / "config" / "settings.example.json"

    if not settings_path.is_absolute():
        settings_path = root_dir / settings_path

    if settings_path.is_file():
        try:
            with settings_path.open("r", encoding="utf-8") as f:
                file_config = json.load(f)
            if isinstance(file_config, dict):
                config.update(file_config)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to load settings from %s: %s", settings_path, exc)
    else:
        logger.info(
            "Settings file %s not found, using default configuration.",
            settings_path,
        )

    return config

def apply_cli_overrides(config: Dict[str, Any], args: argparse.Namespace) -> Dict[str, Any]:
    if args.input_file:
        config["input_file"] = args.input_file
    if args.output_file:
        config["output_file"] = args.output_file
    if args.format:
        config["output_format"] = args.format
    if args.max_items is not None:
        config["max_items"] = args.max_items
    return config

def resolve_path(path_str: str, root_dir: Path) -> Path:
    path = Path(path_str)
    if not path.is_absolute():
        path = root_dir / path
    return path

def read_input_urls(input_file: Path, logger: logging.Logger) -> List[str]:
    if not input_file.is_file():
        logger.error("Input file %s does not exist.", input_file)
        raise FileNotFoundError(f"Input file not found: {input_file}")

    urls: List[str] = []
    with input_file.open("r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            urls.append(stripped)

    if not urls:
        logger.warning("No URLs found in input file %s.", input_file)

    return urls

def main() -> None:
    root_dir = Path(__file__).resolve().parents[1]

    parser = argparse.ArgumentParser(
        description="Run the Facebook Following Scraper over a list of profile URLs."
    )
    parser.add_argument(
        "--settings",
        "-c",
        help="Path to JSON settings file (relative to project root or absolute).",
        default=None,
    )
    parser.add_argument(
        "--input-file",
        "-i",
        help="Path to input file containing Facebook profile URLs (one per line).",
    )
    parser.add_argument(
        "--output-file",
        "-o",
        help="Path to output file where scraped data will be written.",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["json", "jsonl", "csv"],
        help="Output format. If omitted, inferred from output file extension.",
    )
    parser.add_argument(
        "--max-items",
        "-m",
        type=int,
        help="Maximum number of following entries to scrape across all profiles.",
    )

    args = parser.parse_args()

    # Temporary logger for early messages
    temp_logger = setup_logger(DEFAULT_CONFIG["log_level"])
    config = load_settings(
        Path(args.settings) if args.settings else None,
        root_dir=root_dir,
        logger=temp_logger,
    )
    config = apply_cli_overrides(config, args)

    logger = setup_logger(config.get("log_level", "INFO"))
    logger.debug("Effective configuration: %s", config)

    input_file = resolve_path(config["input_file"], root_dir)
    output_file = resolve_path(config["output_file"], root_dir)
    output_format = config.get("output_format") or output_file.suffix.lstrip(".") or "json"
    max_items = config.get("max_items")

    try:
        urls = read_input_urls(input_file, logger)
    except FileNotFoundError:
        sys.exit(1)

    if not urls:
        logger.error("No URLs to process. Exiting.")
        sys.exit(1)

    # Dynamically load scraper and exporters
    try:
        facebook_parser_module = load_module(
            "facebook_parser",
            root_dir / "src" / "extractors" / "facebook_parser.py",
        )
        exporters_module = load_module(
            "exporters",
            root_dir / "src" / "outputs" / "exporters.py",
        )
    except ImportError as exc:
        logger.error("Failed to load internal modules: %s", exc)
        sys.exit(1)

    FacebookFollowingScraper = getattr(
        facebook_parser_module,
        "FacebookFollowingScraper",
        None,
    )
    if FacebookFollowingScraper is None:
        logger.error("FacebookFollowingScraper class not found in facebook_parser module.")
        sys.exit(1)

    export_data = getattr(exporters_module, "export_data", None)
    if export_data is None:
        logger.error("export_data function not found in exporters module.")
        sys.exit(1)

    scraper = FacebookFollowingScraper(logger=logger)
    logger.info(
        "Starting scraping for %d profile(s), max_items=%s",
        len(urls),
        max_items if max_items is not None else "unlimited",
    )

    try:
        records = scraper.scrape(urls=urls, max_items=max_items)
    except Exception as exc:  # noqa: BLE001
        logger.error("Scraping failed with an unexpected error: %s", exc, exc_info=True)
        sys.exit(1)

    logger.info("Scraping completed. Collected %d records.", len(records))

    try:
        export_data(
            records=records,
            output_path=str(output_file),
            output_format=output_format,
            logger=logger,
        )
    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to export data: %s", exc, exc_info=True)
        sys.exit(1)

    logger.info("Done. Output saved to %s", output_file)

if __name__ == "__main__":
    main()