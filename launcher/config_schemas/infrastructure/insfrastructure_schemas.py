from dataclasses import dataclass

from omegaconf import MISSING

from launcher.config_schemas.infrastructure.instance_group_creator_schemas import InstanceGroupCreatorConfig


@dataclass
class InfrastructureConfig:
    project_id: str = MISSING
    region: str = MISSING
    zone: str = MISSING
    instance_group_creator: InstanceGroupCreatorConfig = InstanceGroupCreatorConfig()
