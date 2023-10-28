from dataclasses import dataclass

from hydra.core.config_store import ConfigStore

from launcher.config_schemas.infrastructure.insfrastructure_schemas import InfrastructureConfig


@dataclass
class Config:
    infrastructure: InfrastructureConfig = InfrastructureConfig()


def setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(name="config", node=Config)
