

class ApplicationConfiguration: 
    def __init__(self):
        self.main_organization_id = 0
        self.main_project_id = ''
        self.llm_api_key = ''
        self.langchain_api_key = ''
        self.region_list = []
        self.llm = None



    def __str__(self) -> str:
        return f"ApplicationConfiguration(main_organization_id={self.main_organization_id}, main_project_id={self.main_project_id}, llm_api_key={self.llm_api_key}, langchain_api_key={self.langchain_api_key})"