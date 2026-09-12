from typing import TypedDict, Optional, Dict


class AgentState(TypedDict):

    dataset_path: str
    evaluation_result: Optional[Dict]
    final_result: Optional[Dict]

    workflow_complete: Optional[bool]