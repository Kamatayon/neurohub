from typing import TypedDict, List, Optional, Dict
from typing import Any

class Client(TypedDict):
    client_uuid: str
    client_name: str

class ChecklistSummary(TypedDict):
    checklist_uuid: str
    checklist_name: str
    client_uuid: str

class Criteria(TypedDict):
    criteria_uuid: str
    criteria_name: str
    criteria_prompt_id: str
    criteria_parent_uuid: Optional[str]
    criteria_examples: List[str]
    criteria_iterate: bool
    criteria_weight: float
    criteria_actor: str
    criteria_description: str

class CriteriaGroup(TypedDict):
    criteria_group_uuid: str
    criteria_group_name: str
    criteria_group_prompt_id: str
    parent_criteria_group_uuid: Optional[str]
    criteria_group_weight: float
    criteria_group_rules: Dict[str, Any]
    criteria_group_type: str
    # criteria: List[Criteria]

class ChecklistDetailed(ChecklistSummary):
    criteria_group: List[CriteriaGroup]

class ManagerDepartment(TypedDict):
    department_name: str
    client_uuid: str

class Manager(TypedDict):
    manager_uuid: str
    manager_name: str
    department_uuid: str
    department: ManagerDepartment

class Department(TypedDict):
    department_uuid: str
    department_name: str
    client_uuid: str
    latitude: float
    longitude: float

class CriteriaResultQA(TypedDict):
    criteria_result_qa_uuid: str
    file_uuid: str
    criteria_uuid: str
    situation_id: str
    criteria_score: float
    qa_time_1: str
    qa_time_2: str
    qa_time_3: str
    criteria: Dict[str, str]  # {name: ..., prompt_id: ...}

class CriteriaResultEntity(TypedDict):
    criteria_result_entity_uuid: str
    file_uuid: str
    criteria_uuid: str
    criteria_value: str
    entity_time: str
    criteria: Dict[str, str]
    criteria_clasification_list: List[Dict[str, Any]]  # Expand this if needed

class CriteriaClasificationGroup(TypedDict):
    criteria_clasification_list_group_uuid: str
    criteria_clasification_list_group_name: str

class CriteriaClasificationItem(TypedDict):
    criteria_clasification_list_uuid: str
    criteria_clasification_list_value: str
    criteria_clasification_list_group: CriteriaClasificationGroup

class CriteriaResultAnalysis(TypedDict):
    criteria_result_analysis_uuid: str
    file_uuid: str
    criteria_uuid: str
    criteria_result: str
    analysis_evidence: str
    criteria: Dict[str, str]
    classifications: List[CriteriaClasificationItem]

class ChecklistCriteriaGroupLink(TypedDict):
    checklist_uuid: str
    checklist_name: str
    criteria_group_uuid: str
    criteria_group_name: str

class CriteriaGroupCriteriaLink(TypedDict):
    criteria_group_uuid: str
    criteria_group_name: str
    criteria_uuid: str
    criteria_name: str
