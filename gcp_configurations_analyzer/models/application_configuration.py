

class ApplicationConfiguration: 
    def __init__(self, main_organization_id, main_project_id, open_ai_key):
        self.main_organization_id = main_organization_id
        self.main_project_id =  main_project_id
        self.open_ai_key = open_ai_key


    def __str__(self):
        return ''.join([self.main_organization_id, self.main_project_id, self.open_ai_key], " ")