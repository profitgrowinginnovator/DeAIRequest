# coding: utf-8

"""
    Bacalhau API

    This page is the reference of the Bacalhau REST API. Project docs are available at https://docs.bacalhau.org/. Find more information about Bacalhau at https://github.com/bacalhau-project/bacalhau.  # noqa: E501

    OpenAPI spec version: ${PYPI_VERSION}
    Contact: team@bacalhau.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six


class ComputeNodeInfo(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        "available_capacity": "ResourceUsageData",
        "enqueued_executions": "int",
        "execution_engines": "list[Engine]",
        "max_capacity": "ResourceUsageData",
        "max_job_requirements": "ResourceUsageData",
        "running_executions": "int",
    }

    attribute_map = {
        "available_capacity": "AvailableCapacity",
        "enqueued_executions": "EnqueuedExecutions",
        "execution_engines": "ExecutionEngines",
        "max_capacity": "MaxCapacity",
        "max_job_requirements": "MaxJobRequirements",
        "running_executions": "RunningExecutions",
    }

    def __init__(
        self,
        available_capacity=None,
        enqueued_executions=None,
        execution_engines=None,
        max_capacity=None,
        max_job_requirements=None,
        running_executions=None,
    ):  # noqa: E501
        """ComputeNodeInfo - a model defined in Swagger"""  # noqa: E501
        self._available_capacity = None
        self._enqueued_executions = None
        self._execution_engines = None
        self._max_capacity = None
        self._max_job_requirements = None
        self._running_executions = None
        self.discriminator = None
        if available_capacity is not None:
            self.available_capacity = available_capacity
        if enqueued_executions is not None:
            self.enqueued_executions = enqueued_executions
        if execution_engines is not None:
            self.execution_engines = execution_engines
        if max_capacity is not None:
            self.max_capacity = max_capacity
        if max_job_requirements is not None:
            self.max_job_requirements = max_job_requirements
        if running_executions is not None:
            self.running_executions = running_executions

    @property
    def available_capacity(self):
        """Gets the available_capacity of this ComputeNodeInfo.  # noqa: E501


        :return: The available_capacity of this ComputeNodeInfo.  # noqa: E501
        :rtype: ResourceUsageData
        """
        return self._available_capacity

    @available_capacity.setter
    def available_capacity(self, available_capacity):
        """Sets the available_capacity of this ComputeNodeInfo.


        :param available_capacity: The available_capacity of this ComputeNodeInfo.  # noqa: E501
        :type: ResourceUsageData
        """

        self._available_capacity = available_capacity

    @property
    def enqueued_executions(self):
        """Gets the enqueued_executions of this ComputeNodeInfo.  # noqa: E501


        :return: The enqueued_executions of this ComputeNodeInfo.  # noqa: E501
        :rtype: int
        """
        return self._enqueued_executions

    @enqueued_executions.setter
    def enqueued_executions(self, enqueued_executions):
        """Sets the enqueued_executions of this ComputeNodeInfo.


        :param enqueued_executions: The enqueued_executions of this ComputeNodeInfo.  # noqa: E501
        :type: int
        """

        self._enqueued_executions = enqueued_executions

    @property
    def execution_engines(self):
        """Gets the execution_engines of this ComputeNodeInfo.  # noqa: E501


        :return: The execution_engines of this ComputeNodeInfo.  # noqa: E501
        :rtype: list[Engine]
        """
        return self._execution_engines

    @execution_engines.setter
    def execution_engines(self, execution_engines):
        """Sets the execution_engines of this ComputeNodeInfo.


        :param execution_engines: The execution_engines of this ComputeNodeInfo.  # noqa: E501
        :type: list[Engine]
        """

        self._execution_engines = execution_engines

    @property
    def max_capacity(self):
        """Gets the max_capacity of this ComputeNodeInfo.  # noqa: E501


        :return: The max_capacity of this ComputeNodeInfo.  # noqa: E501
        :rtype: ResourceUsageData
        """
        return self._max_capacity

    @max_capacity.setter
    def max_capacity(self, max_capacity):
        """Sets the max_capacity of this ComputeNodeInfo.


        :param max_capacity: The max_capacity of this ComputeNodeInfo.  # noqa: E501
        :type: ResourceUsageData
        """

        self._max_capacity = max_capacity

    @property
    def max_job_requirements(self):
        """Gets the max_job_requirements of this ComputeNodeInfo.  # noqa: E501


        :return: The max_job_requirements of this ComputeNodeInfo.  # noqa: E501
        :rtype: ResourceUsageData
        """
        return self._max_job_requirements

    @max_job_requirements.setter
    def max_job_requirements(self, max_job_requirements):
        """Sets the max_job_requirements of this ComputeNodeInfo.


        :param max_job_requirements: The max_job_requirements of this ComputeNodeInfo.  # noqa: E501
        :type: ResourceUsageData
        """

        self._max_job_requirements = max_job_requirements

    @property
    def running_executions(self):
        """Gets the running_executions of this ComputeNodeInfo.  # noqa: E501


        :return: The running_executions of this ComputeNodeInfo.  # noqa: E501
        :rtype: int
        """
        return self._running_executions

    @running_executions.setter
    def running_executions(self, running_executions):
        """Sets the running_executions of this ComputeNodeInfo.


        :param running_executions: The running_executions of this ComputeNodeInfo.  # noqa: E501
        :type: int
        """

        self._running_executions = running_executions

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value
        if issubclass(ComputeNodeInfo, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ComputeNodeInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other