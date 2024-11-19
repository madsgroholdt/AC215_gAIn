# coding: utf-8

"""
    Strava API v3

    The [Swagger Playground](https://developers.strava.com/playground) is the easiest way to familiarize yourself with the Strava API by submitting HTTP requests and observing the responses before you write any client code. It will show what a response will look like with different endpoints depending on the authorization scope you receive from your athletes. To use the Playground, go to https://www.strava.com/settings/api and change your “Authorization Callback Domain” to developers.strava.com. Please note, we only support Swagger 2.0. There is a known issue where you can only select one scope at a time. For more information, please check the section “client code” at https://developers.strava.com/docs.  # noqa: E501

    OpenAPI spec version: 3.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class IdStarredBody(object):
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
        'starred': 'bool'
    }

    attribute_map = {
        'starred': 'starred'
    }

    def __init__(self, starred=False):  # noqa: E501
        """IdStarredBody - a model defined in Swagger"""  # noqa: E501
        self._starred = None
        self.discriminator = None
        self.starred = starred

    @property
    def starred(self):
        """Gets the starred of this IdStarredBody.  # noqa: E501

        If true, star the segment; if false, unstar the segment.  # noqa: E501

        :return: The starred of this IdStarredBody.  # noqa: E501
        :rtype: bool
        """
        return self._starred

    @starred.setter
    def starred(self, starred):
        """Sets the starred of this IdStarredBody.

        If true, star the segment; if false, unstar the segment.  # noqa: E501

        :param starred: The starred of this IdStarredBody.  # noqa: E501
        :type: bool
        """
        if starred is None:
            raise ValueError("Invalid value for `starred`, must not be `None`")  # noqa: E501

        self._starred = starred

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(IdStarredBody, dict):
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
        if not isinstance(other, IdStarredBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other