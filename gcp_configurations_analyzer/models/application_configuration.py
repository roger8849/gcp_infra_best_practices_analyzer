

class ApplicationConfiguration: 
    def __init__(self, main_organization_id, main_project_id, llm_api_key):
        self.main_organization_id = main_organization_id
        self.main_project_id =  main_project_id
        self.llm_api_key = llm_api_key


    def __str__(self):
        return '\n'.join([str(self.main_organization_id), self.main_project_id, self.llm_api_key])