from typing import Iterable
from pathlib import Path
import json
import sys
from tqdm import tqdm


def select_records(
    records: Iterable[str],
    mode: str,
    things_to_find: str | Iterable,
) -> Iterable[str]:
    # Validate inputs using assertions (debugging only)
    assert isinstance(records, Iterable), "records must be an iterable"
    assert mode in {"with", "without"}, f"Invalid mode: {mode}. Use 'with' or 'without'"
    assert isinstance(things_to_find, (str, Iterable)), "things_to_find must be str or Iterable"

    def look_for(thing, record):
        assert thing, "thing cannot be empty"  # Debug check
        if isinstance(thing, str):
            return thing in record
        elif isinstance(thing, Iterable):
            return all(elem in record for elem in thing)
        return False

    def weneed(record: str) -> bool:
        return any(look_for(thing, record) for thing in things_to_find)

    # Load from file if things_to_find is str and not Iterable
    FILE_FORMATS = {
        '.txt': lambda f: [line.strip() for line in f.readlines()],
        '.json': lambda f: list(json.load(f))
    }
    if isinstance(things_to_find, str):
        assert isinstance(things_to_find, Path)
        filename = things_to_find
        try:
            with open(filename) as f:
                things_to_find = FILE_FORMATS[filename.suffix]
        except KeyError(FILE_FORMATS):
            raise ValueError(f"Unsupported file format: {filename}")
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filename} not found")

    new_records = []
    
    if mode == 'without':
        print(f'Filtering records. Initial count: {len(records)}')
        new_records = [record for record in tqdm(records) if not weneed(record)]
        assert len(new_records) <= len(records), "Filtering should not increase records!"
        print(f'Removed {len(records) - len(new_records)} records. Remaining: {len(new_records)}')
        return new_records

    elif mode == 'with':
        for record in tqdm(records):
            if weneed(record):
                new_records.append(record)
        assert all(weneed(record) for record in new_records), "All new_records must match the condition!"
        print(f'Found {len(new_records)} matching records')
        return new_records

if __name__ == "__main__" and len(sys.argv) > 1:
    select_records(*sys.argv[1:4])

    # # --- Test with Assertions ---
    # # Test data
    # records = ["apple banana", "orange lemon", "apple orange"]
    # things_to_find = ["apple", "banana"]

    # # Test 1: Check if function returns non-None
    # selected = select_records(records, "with", things_to_find)
    # assert selected is not None, "Function returned None!"

    # # Test 2: Verify correctness of filtered results
    # expected_with = ["apple banana", "apple orange"]
    # assert selected == expected_with, f"Expected {expected_with}, got {selected}"

    # # Test 3: Check 'without' mode
    # filtered = select_records(records, "without", things_to_find)
    # expected_without = ["orange lemon"]
    # assert filtered == expected_without, f"Expected {expected_without}, got {filtered}"

    # print("All assertions passed! ✅")