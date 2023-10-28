import hydra

from hydra.utils import instantiate
from omegaconf import DictConfig

from launcher.config_schemas.config import setup_config
from launcher.utils.utils import JobInfo

setup_config()


@hydra.main(config_path=".", config_name="config", version_base="1.3")
def run(config: DictConfig) -> None:
    instance_group_creator = instantiate(config.infrastructure.instance_group_creator)
    instance_ids = instance_group_creator.launch_instance_group()
    job_info = JobInfo(
        project_id=config.infrastructure.project_id,
        zone=config.infrastructure.zone,
        instance_group_name=config.infrastructure.instance_group_creator.name,
        instance_ids=instance_ids,
    )
    job_info.print_job_info()


if __name__ == "__main__":
    run()
