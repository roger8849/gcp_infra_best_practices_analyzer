from routes.best_practices_analyzer import BestPracticesAnalyzer
from utils.app.init_utils import InitUtils

class App:
    def __init__(self, init_utils = InitUtils(), best_practices__analyzer = BestPracticesAnalyzer()):
        self.init_utils = init_utils
        self.best_practices_analyzer = best_practices__analyzer


    def main(self):
        self.init_utils.start_app_init()
        BestPracticesAnalyzer.start_analysis()

if __name__ == "__main__":
    app = App()
    app.main()
