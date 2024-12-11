"""
Configuration for running an experiment in the cloud.

This module provides a class that holds the configuration for running an
experiment in the cloud. The configuration includes the subscription ID,
resource group name, and workspace name of the Azure ML workspace.
"""

import os
from typing import Optional


def _try_get_env_var(variable_name: str) -> str:
    """
    Try to read environment variable.

    :param variable_name: Environment variable name.
    :type variable_name: str
    :return: Value of the environment variable.
    :rtype: str
    :raises ValueError: If the variable doesn't exist or is empty.
    """
    value = os.environ.get(variable_name)
    if value is None or value == "":
        raise ValueError(
            f"env var '{variable_name}' is not set or is empty."
        )
    return value


def _get_optional_env_var(variable_name: str) -> str:
    """
    Read environment variable. Return None if it doesn't exist or is empty.

    :param variable_name: Environment variable name.
    :type variable_name: str
    :return: Value of the environment variable or None.
    :rtype: str
    """
    value = os.environ.get(variable_name)
    if value is None or value == "":
        return None
    return value


class ExperimentCloudConfig:
    """
    Configuration for running an experiment in the cloud.

    :param subscription_id: Subscription ID of the Azure ML workspace.
    :type subscription_id: str
    :param resource_group_name: Resource group name of the Azure ML workspace.
    :type resource_group_name: str
    :param workspace_name: Name of the Azure ML workspace.
    :type workspace_name: str
    """

    def __init__(
        self,
        subscription_id: Optional[str] = None,
        resource_group_name: Optional[str] = None,
        workspace_name: Optional[str] = None,
        env_name: Optional[str] = None,
        compute_target: Optional[str] = None,
    ):
        """Initialize the configuration."""
        self.subscription_id = subscription_id or _try_get_env_var(
            "SUBSCRIPTION_ID"
        )
        self.resource_group_name = resource_group_name or _try_get_env_var(
            "RESOURCE_GROUP_NAME"
        )
        self.workspace_name = workspace_name or _try_get_env_var(
            "WORKSPACE_NAME"
        )
        self.environment_name = env_name or _get_optional_env_var(
            "ENV_NAME"
        )
        self.compute_target = compute_target or _get_optional_env_var(
            "COMPUTE_TARGET"
        )
