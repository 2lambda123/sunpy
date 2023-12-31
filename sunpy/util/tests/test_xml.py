from xml.dom.minidom import Document, parseString
from xml.parsers.expat import ExpatError

import pytest

from sunpy.util import xml


def test_xml_to_dict1():
    """
    should return dict of xml string.
    """
    source_xml = "<outer>\
          <inner1>one</inner1>\
          <inner2>two</inner2>\
        </outer>"

    xml_dict = xml.xml_to_dict(source_xml)
    expected_dict = {'outer': {'inner2': 'two', 'inner1': 'one'}}

    assert xml_dict == expected_dict


def test_xml_to_dict2():
    """
    should return dict of xml string and if a tag is duplicated it takes the
    last one.
    """
    source_xml = "<outer>\
                    <inner1>one-one</inner1>\
                    <inner1>one-two</inner1>\
                    <inner2>two-one</inner2>\
                    <inner2>two-two</inner2>\
                 </outer>"

    xml_dict = xml.xml_to_dict(source_xml)
    expected_dict = {'outer': {'inner2': 'two-two', 'inner1': 'one-two'}}

    assert xml_dict == expected_dict


def test_xml_to_dict3():
    """
    should return dict of xml string with empty value if there are no inner
    elements.
    """
    source_xml = "<outer/>"

    xml_dict = xml.xml_to_dict(source_xml)
    expected_dict = {'outer': ''}

    assert xml_dict == expected_dict


def test_xml_to_dict4():
    """
    should return dict of xml string with empty value if there are no inner
    elements.
    """
    source_xml = "<outer></outer>"

    xml_dict = xml.xml_to_dict(source_xml)
    expected_dict = {'outer': ''}

    assert xml_dict == expected_dict


def test_xml_to_dict5():
    """
    should return dict of xml string with 2 layer nesting.
    """
    source_xml = "<outer>\
                    <mid1>\
                        <inner1>one-one</inner1>\
                    </mid1>\
                    <mid2>\
                        <inner2>two-one</inner2>\
                    </mid2>\
                 </outer>"

    xml_dict = xml.xml_to_dict(source_xml)
    expected_dict = {'outer': {'mid2': {'inner2': 'two-one'}, 'mid1': {'inner1': 'one-one'}}}

    assert xml_dict == expected_dict


def test_xml_to_dict6():
    """
    should return dict of xml string with 2 layer nesting and if a tag is
    duplicated it takes the last one.
    """
    source_xml = "<outer>\
                    <mid>\
                        <inner1>one-one</inner1>\
                    </mid>\
                    <mid>\
                        <inner2>two-one</inner2>\
                    </mid>\
                 </outer>"

    xml_dict = xml.xml_to_dict(source_xml)
    expected_dict = {'outer': {'mid': {'inner2': 'two-one'}}}

    assert xml_dict == expected_dict


def test_xml_to_dict7():
    """
    should raise TypeError when passed None.
    """
    assert pytest.raises(TypeError, xml.xml_to_dict, None)


def test_xml_to_dict8():
    """
    should raise TypeError when passed non string.
    """
    assert pytest.raises(TypeError, xml.xml_to_dict, 9)


def test_xml_to_dict9():
    """
    should raise ExpatError when passed empty string.
    """
    assert pytest.raises(ExpatError, xml.xml_to_dict, "")


def test_xml_to_dict10():
    """
    should raise ExpatError when passed space.
    """
    assert pytest.raises(ExpatError, xml.xml_to_dict, " ")


def test_get_node_text1():
    """
    should raise NotTextNodeError if there is a non text node.
    """
    doc = Document()
    outer = doc.createElement("outer")
    doc.appendChild(outer)
    pytest.raises(xml.NotTextNodeError, xml.get_node_text, doc)


def test_get_node_text2():
    """
    should return empty string for a node with no child nodes.
    """
    assert xml.get_node_text(Document()) == ""


def test_get_node_text3():
    """
    should return node text.
    """
    node = parseString("<outer>one</outer>")
    text_node = node.childNodes[0]

    assert xml.get_node_text(text_node) == "one"


def test_get_node_text4():
    """
    should raise AttributeError when sent None.
    """
    assert pytest.raises(AttributeError, xml.get_node_text, None)


def test_get_node_text5():
    """
    should raise AttributeError when sent wrong type.
    """
    assert pytest.raises(AttributeError, xml.get_node_text, "wrong type")


def test_node_to_dict1():
    """
    should return dict of node.
    """

    doc = Document()

    outer = doc.createElement("outer")
    doc.appendChild(outer)

    inner1 = doc.createElement("inner1")
    inner2 = doc.createElement("inner2")
    outer.appendChild(inner1)
    outer.appendChild(inner2)

    inner1_text = doc.createTextNode("one")
    inner2_text = doc.createTextNode("two")
    inner1.appendChild(inner1_text)
    inner2.appendChild(inner2_text)

    expected_dict = {'outer': {'inner2': 'two', 'inner1': 'one'}}
    xml_dict = xml.node_to_dict(doc)

    assert xml_dict == expected_dict


def test_node_to_dict2():
    """
    should return dict of node double nested.
    """

    doc = Document()

    outer = doc.createElement("outer")
    doc.appendChild(outer)

    mid1 = doc.createElement("mid1")
    outer.appendChild(mid1)
    mid2 = doc.createElement("mid2")
    outer.appendChild(mid2)

    inner1 = doc.createElement("inner1")
    inner2 = doc.createElement("inner2")
    mid1.appendChild(inner1)
    mid2.appendChild(inner2)

    inner1_text = doc.createTextNode("one")
    inner2_text = doc.createTextNode("two")
    inner1.appendChild(inner1_text)
    inner2.appendChild(inner2_text)

    expected_dict = {'outer': {'mid2': {'inner2': 'two'}, 'mid1': {'inner1': 'one'}}}
    xml_dict = xml.node_to_dict(doc)

    assert xml_dict == expected_dict


def test_node_to_dict3():
    """
    should return empty dict when sent empty doc.
    """
    expected_dict = {}
    xml_dict = xml.node_to_dict(Document())

    assert xml_dict == expected_dict


def test_node_to_dict4():
    """
    should raise AttributeError when sent wrong type.
    """
    assert pytest.raises(AttributeError, xml.node_to_dict, 9)


def test_node_to_dict5():
    """
    should raise AttributeError when sent None.
    """
    assert pytest.raises(AttributeError, xml.node_to_dict, None)


def test_with_multiple_children_in_list():
    """
    Setting the 'multiple' attribute of parent node should put child nodes in a
    list.
    """
    def getChild(lst_of_children, key, value):
        for child in lst_of_children:
            if child[key] == value:
                return child

        raise ValueError(f"No children with key {key} set to {value} found.")

    source = '''<?xml version="1.0" encoding="UTF-8"?>
                <Config>
                    <Name>With multiple children</Name>
                    <Children multiple="true">
                      <Child>
                        <Name>First Child</Name>
                        <Value>Value 1</Value>
                      </Child>
                      <Child>
                        <Name>Second Child</Name>
                        <Value>Value 2</Value>
                      </Child>
                    </Children>
                </Config>'''

    expected = {'Config': {'Children': [{'Name': 'First Child', 'Value': 'Value 1'},
                                        {'Name': 'Second Child', 'Value': 'Value 2'}],
                           'Name': 'With multiple children'}}

    actual = xml.xml_to_dict(source)

    assert len(expected['Config']) == len(actual['Config'])
    assert expected['Config']['Name'] == actual['Config']['Name']

    assert len(actual['Config']['Children']) == 2

    # As the child dictionaries are in lists we cannot be certain what order
    # they are in. Test individually.

    expected_children = expected['Config']['Children']
    actual_children = actual['Config']['Children']

    expected_first_child = getChild(expected_children, key='Name', value='First Child')
    actual_first_child = getChild(actual_children, key='Name', value='First Child')

    assert expected_first_child == actual_first_child

    expected_second_child = getChild(expected_children, key='Name', value='Second Child')
    actual_second_child = getChild(actual_children, key='Name', value='Second Child')

    assert expected_second_child == actual_second_child
