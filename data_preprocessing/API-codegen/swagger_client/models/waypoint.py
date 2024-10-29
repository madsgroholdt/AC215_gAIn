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

class Waypoint(object):
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
        'latlng': 'LatLng',
        'target_latlng': 'LatLng',
        'categories': 'list[str]',
        'title': 'str',
        'description': 'str',
        'distance_into_route': 'int'
    }

    attribute_map = {
        'latlng': 'latlng',
        'target_latlng': 'target_latlng',
        'categories': 'categories',
        'title': 'title',
        'description': 'description',
        'distance_into_route': 'distance_into_route'
    }

    def __init__(self, latlng=None, target_latlng=None, categories=None, title=None, description=None, distance_into_route=None):  # noqa: E501
        """Waypoint - a model defined in Swagger"""  # noqa: E501
        self._latlng = None
        self._target_latlng = None
        self._categories = None
        self._title = None
        self._description = None
        self._distance_into_route = None
        self.discriminator = None
        if latlng is not None:
            self.latlng = latlng
        if target_latlng is not None:
            self.target_latlng = target_latlng
        if categories is not None:
            self.categories = categories
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if distance_into_route is not None:
            self.distance_into_route = distance_into_route

    @property
    def latlng(self):
        """Gets the latlng of this Waypoint.  # noqa: E501


        :return: The latlng of this Waypoint.  # noqa: E501
        :rtype: LatLng
        """
        return self._latlng

    @latlng.setter
    def latlng(self, latlng):
        """Sets the latlng of this Waypoint.


        :param latlng: The latlng of this Waypoint.  # noqa: E501
        :type: LatLng
        """

        self._latlng = latlng

    @property
    def target_latlng(self):
        """Gets the target_latlng of this Waypoint.  # noqa: E501


        :return: The target_latlng of this Waypoint.  # noqa: E501
        :rtype: LatLng
        """
        return self._target_latlng

    @target_latlng.setter
    def target_latlng(self, target_latlng):
        """Sets the target_latlng of this Waypoint.


        :param target_latlng: The target_latlng of this Waypoint.  # noqa: E501
        :type: LatLng
        """

        self._target_latlng = target_latlng

    @property
    def categories(self):
        """Gets the categories of this Waypoint.  # noqa: E501

        Categories that the waypoint belongs to  # noqa: E501

        :return: The categories of this Waypoint.  # noqa: E501
        :rtype: list[str]
        """
        return self._categories

    @categories.setter
    def categories(self, categories):
        """Sets the categories of this Waypoint.

        Categories that the waypoint belongs to  # noqa: E501

        :param categories: The categories of this Waypoint.  # noqa: E501
        :type: list[str]
        """

        self._categories = categories

    @property
    def title(self):
        """Gets the title of this Waypoint.  # noqa: E501

        A title for the waypoint  # noqa: E501

        :return: The title of this Waypoint.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this Waypoint.

        A title for the waypoint  # noqa: E501

        :param title: The title of this Waypoint.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def description(self):
        """Gets the description of this Waypoint.  # noqa: E501

        A description of the waypoint (optional)  # noqa: E501

        :return: The description of this Waypoint.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Waypoint.

        A description of the waypoint (optional)  # noqa: E501

        :param description: The description of this Waypoint.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def distance_into_route(self):
        """Gets the distance_into_route of this Waypoint.  # noqa: E501

        The number meters along the route that the waypoint is located  # noqa: E501

        :return: The distance_into_route of this Waypoint.  # noqa: E501
        :rtype: int
        """
        return self._distance_into_route

    @distance_into_route.setter
    def distance_into_route(self, distance_into_route):
        """Sets the distance_into_route of this Waypoint.

        The number meters along the route that the waypoint is located  # noqa: E501

        :param distance_into_route: The distance_into_route of this Waypoint.  # noqa: E501
        :type: int
        """

        self._distance_into_route = distance_into_route

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
        if issubclass(Waypoint, dict):
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
        if not isinstance(other, Waypoint):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
