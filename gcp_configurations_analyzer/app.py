from utils.app.init_utils import InitUtils
import routes.best_practices_analyzer as bpa
import utils.app.console_utils as cu

import routes.best_practices_analyzer as bpa
from models.gcp_best_practices_state import GCPBestPracticesState


def main():
    InitUtils.start_app_init()

    bpa.start_analysis()

if __name__ == "__main__":
    main()
