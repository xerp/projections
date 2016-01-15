"""Unit test."""

import unittest


class ClassA:

    def __init__(self):
        self.attr_class_a = 1
        self.value = None

    def set_value(self, value):
        self.value = value


class ClassB:

    __setters = {}

    def __init__(self):
        __class_a = ClassA()
        self.__dict__['attr_class_a'] = __class_a.attr_class_a
        self.__dict__['value'] = __class_a.value

        self.__setters['value'] = __class_a.set_value

    def __setattr__(self, name, value):
        prop = self.__setters[name]
        prop(value)


class TestClassesAttributes(unittest.TestCase):

    def test_not_attributes(self):
        class_b = ClassB()

        self.assertIsNotNone(class_b.attr_class_a)

    def test_attribute_equality(self):
        class_a = ClassA()
        class_b = ClassB()

        self.assertEqual(class_a.attr_class_a, class_b.attr_class_a)

    def test_attribute_setting(self):
        class_a = ClassA()
        class_b = ClassB()

        class_b.value = True

        self.assertEqual(class_a.value, class_b.value)

if __name__ == '__main__':
    unittest.main()
