import utils
import pandas as pd
class CLI():
    def run(self, path: str)-> None:
        scanned_path = utils.scan_path(path)
        scanned_path = pd.DataFrame(scanned_path)

        scanned_path.to_csv(path)
