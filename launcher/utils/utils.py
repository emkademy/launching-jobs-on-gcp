import inspect
import logging
import socket

from dataclasses import dataclass
from typing import Any

from google.api_core.exceptions import GoogleAPICallError
from google.api_core.extended_operation import ExtendedOperation
from google.cloud import compute_v1


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"[{socket.gethostname()}] {name}")


GCP_UTILS_LOGGER = get_logger(__name__)


def wait_for_extended_operation(
    operation: ExtendedOperation, verbose_name: str = "operation", timeout: int = 300
) -> Any:
    try:
        result = operation.result(timeout=timeout)
    except GoogleAPICallError as ex:
        GCP_UTILS_LOGGER.exception("Exception occurred")
        for attr in ["details", "domain", "errors", "metadata", "reason", "response"]:
            value = getattr(ex, attr, None)
            if value:
                GCP_UTILS_LOGGER.error(f"ex.{attr}:\n{value}")
        if isinstance(ex.response, compute_v1.Operation):
            for error in ex.response.error.errors:
                GCP_UTILS_LOGGER.error(f"Error message: {error.message}")

        raise RuntimeError("Exception during extended operation") from ex

    if operation.error_code:
        GCP_UTILS_LOGGER.error(
            f"Error during {verbose_name}: [Code: {operation.error_code}]: {operation.error_message}"
        )
        GCP_UTILS_LOGGER.error(f"Operation ID: {operation.name}")
        raise operation.exception() or RuntimeError(operation.error_message)

    if operation.warnings:
        GCP_UTILS_LOGGER.warning(f"Warnings during {verbose_name}:\n")
        for warning in operation.warnings:
            GCP_UTILS_LOGGER.warning(f" - {warning.code}: {warning.message}")

    return result


@dataclass
class JobInfo:
    project_id: str
    zone: str
    instance_group_name: str
    instance_ids: list[str]

    def print_job_info(self) -> None:
        print(f"============= Task {self.instance_group_name.lower()} details ================")
        print(self.get_job_info_message())

    def get_job_info_message(self) -> str:
        instance_ids_regex, log_viewer_url, cluster_url = self._get_job_tracking_links()

        run_description = f"""
            Deployed cluster: {cluster_url}
            Experiment logs: {log_viewer_url}

            if something goes wring type in log viewer query field:
            ```
            resource.type="gce_instance"
            logName="projects/{self.project_id}/logs/GCEMetadataScripts"
            resource.labels.instance_id={instance_ids_regex}
            ```
        """
        return inspect.cleandoc(run_description)

    def _get_job_tracking_links(self) -> tuple[str, str, str]:
        instance_ids = [str(id_) for id_ in self.instance_ids]
        instance_ids_regex = " OR ".join(instance_ids)
        instance_ids_url = "%20OR%20".join(instance_ids)
        cluster_url = f"https://console.cloud.google.com/compute/instanceGroups/details/{self.zone}/{self.instance_group_name.lower()}?project={self.project_id}"
        log_viewer_url = f"https://console.cloud.google.com/logs/query;query=resource.type%3D%22gce_instance%22%0Aresource.labels.instance_id%3D%2528{instance_ids_url}%2529?project={self.project_id}"
        return instance_ids_regex, log_viewer_url, cluster_url
