from typing import Generator, List, Dict
import os
def list_files(target_path : str, include_nested:bool = False) -> Generator:
    if include_nested:
        for root, dirs, files in os.walk(target_path):
            for file in files:
                yield os.path.join(root, file)
    else:
        for file in os.listdir(target_path):
            if os.path.isfile(os.path.join(target_path, file)):
                yield os.path.join(target_path, file)



def scan_path(target_path: str, include_nested: bool =False,
              include_created_at: bool=False, include_file_size: bool=False) -> List[Dict]:
    result = []
    for file in list_files(target_path, include_nested):
        metadata = {}
        metadata["filename"] = file
        if include_created_at:
            metadata["created_at"] = time.ctime(os.path.getctime(file))
        if include_file_size:
            metadata["file_size"] = os.path.getsize(file)
        result.append(metadata)
    return result

