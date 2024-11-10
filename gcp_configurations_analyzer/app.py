import routes.best_practices_analyzer as bpa
from utils.app.init_utils import InitUtils

class App:
    def main():
        InitUtils.start_app_init()
        bpa.start_analysis()

if __name__ == "__main__":
    app = App()
    app.main()
