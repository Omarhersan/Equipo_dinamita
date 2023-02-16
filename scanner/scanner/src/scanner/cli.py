from .utils import scan_path
import pandas as pd
from typing import Optional

class CLI():
    def run(self, path: Optional[str]= None)-> None:
        scanned_path = scan_path(path)
        scanned_path = pd.DataFrame(scanned_path)

        scanned_path.to_csv(path)
