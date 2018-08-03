# coding=utf-8

from poco.sdk.exceptions import UnableToSetAttributeException
from poco.sdk.AbstractNode import AbstractNode
from poco.utils.six import string_types

__author__ = 'linzecong'


class OSXUINode(AbstractNode):

    NameTime = {}

    def __init__(self, control, dumper):
        self.Control = control
        self.dumper = dumper

    def getParent(self):
        return OSXUINode(self.Control.AXParent, self.dumper)

    def getChildren(self):
        childs = self.Control.AXChildren
        if childs is not None:
            for node in childs:
                yield OSXUINode(node, self.dumper)

    def getAttr(self, attrName):
        # default value
        attr = {
            'name': 'Uname',
            'originType': 'Unknow',
            'type': 'Root',
            'visible': True,
            'pos': [0.0, 0.0],
            'size': [0.0, 0.0],
            'scale': [1.0, 1.0],
            'anchorPoint': [0.5, 0.5],
            'zOrders': {'local': 0, 'global': 0},
            'text': 'Empty',
        }

        attrs = self.Control.getAttributes()

        if attrName == 'name':
            if 'AXTitle' in attrs:
                if self.Control.AXTitle != "" and self.Control.AXTitle is not None:
                    return self.Control.AXTitle
            if 'AXRole' in attrs:
                return self.Control.AXRole[2:]

        if attrName == 'originType':
            if 'AXRole' in attrs:
                return self.Control.AXRole
            return "Unknow"

        if attrName == 'type':
            if 'AXRole' in attrs:
                return self.Control.AXRole[2:]
            return "Unknow"

        if attrName == 'pos':
            pos = self.Control.AXPosition
            size = self.Control.AXSize
            return [float(pos[0] + size[0] / 2.0 - self.dumper.RootLeft) / float(self.dumper.RootWidth), float(pos[1] + size[1] / 2.0 - self.dumper.RootTop) / float(self.dumper.RootHeight)]

        if attrName == 'size':
            pos = self.Control.AXPosition
            size = self.Control.AXSize
            return [size[0] / float(self.dumper.RootWidth), size[1] / float(self.dumper.RootHeight)]

        if attrName == 'text':
            if 'AXValue' in attrs:
                if isinstance(self.Control.AXValue, string_types):
                    return self.Control.AXValue
                if isinstance(self.Control.AXValue, int):
                    return self.Control.AXValue
                return self.Control.AXValue.AXValue
            return 'Empty'

        return attr.get(attrName)

    def setAttr(self, attrName, val):
        attrs = self.Control.getAttributes()
        if attrName != 'text':
            raise UnableToSetAttributeException(attrName, self)
        else:
            if 'AXValue' in attrs:
                self.Control.AXValue = val
            else:
                raise UnableToSetAttributeException(attrName, self)

    def getAvailableAttributeNames(self):
        return super(OSXUINode, self).getAvailableAttributeNames() + ('text', 'originType')
