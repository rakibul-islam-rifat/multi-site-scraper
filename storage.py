import csv
import logging
from pathlib import Path

logger: logging.Logger = logging.getLogger(__name__)
root_folder: Path = Path(__file__).parent / "output"
root_folder.mkdir(parents=True, exist_ok=True)


def save_to_csv(data: list[dict], filename: str) -> None:
    if not data:
        logger.warning("No data to save for %s", filename)
        return
    csv_file: Path = root_folder / f"{filename}.csv"

    with open(csv_file, "w", encoding="utf-8", newline="") as wf:
        fieldname: list = list(data[0].keys())
        writer = csv.DictWriter(
            wf, fieldnames=fieldname, extrasaction="ignore", restval="N/A"
        )

        writer.writeheader()
        logger.info("Saving data to %s", csv_file.name)

        for item in data:
            row: dict = {k: (v if v is not None else "N/A") for k, v in item.items()}
            writer.writerow(row)
