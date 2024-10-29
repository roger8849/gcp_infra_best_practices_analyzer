from typing import List
from typing_extensions import TypedDict
from utils.app.init_utils import InitUtils


class GCPBestPracticesState(TypedDict):
    projects : List[str] # Projects inside organization.