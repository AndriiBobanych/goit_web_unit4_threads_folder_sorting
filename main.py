import argparse
import logging
from pathlib import Path
from shutil import copyfile
from threading import Thread
import logging
from datetime import datetime

"""
--source [-s] folder
--output [-o]
"""

parser = argparse.ArgumentParser(description="Folder sorter")
parser.add_argument("--source", "-s", help="Source folder for sorting", required=True)
parser.add_argument("--output", "-o", help="Output folder to save files", default="sorted")

args = vars(parser.parse_args())
source = args.get("source")
output = args.get("output")

folders = []


def folders_handler(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            # th = Thread(target=folders.append(el), args=(el,))
            # th.start()
            folders.append(el)
            folders_handler(el)


def copy_file(path: Path) -> None:
    for el in path.iterdir():
        if el.is_file():
            extension = el.suffix
            new_path = folder_to_save / extension[1:]
            try:
                new_path.mkdir(exist_ok=True, parents=True)
                copyfile(el, new_path / el.name)
            except OSError as err:
                logging.error(err)


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR, format="%(threadName)s %(message)s")
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")

    start_time = datetime.now()
    # logging.debug(f"Process is started at {start_time}")
    print(f"Process is started at {start_time}")
    folder_for_sorting = Path(source)
    folder_to_save = Path(output)
    folders.append(folder_for_sorting)
    folders_handler(folder_for_sorting)

    threads = []

    for folder in folders:
        thread = Thread(target=copy_file, args=(folder, ))
        thread.start()

    [thread.join() for thread in threads]

    end_time = datetime.now()
    total_time = end_time - start_time

    print(f"Files was sorted and copied into new folder '{output}'\n"
          f"Old folder '{source}' with garbage-files could be deleted.")
    print(f"Process is finished at {end_time}")
    print(f"Total time for sorting: {total_time.total_seconds()} seconds")
    # logging.debug(f"Process is finished at {end_time}")
    # logging.debug(f"Total time for sorting: {start_time - end_time} seconds")
