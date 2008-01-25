"""Basic XML utilities based on minidom - the built in Document Object Model
"""

import sys
from xml.dom import minidom, Node
#from xml.sax import make_parser, parse as validate, handler

def print_tree(n, indent=0):
    while n:
        #print 'nodeType', n.nodeType, Node.ELEMENT_NODE
        #if n.nodeType != Node.ELEMENT_NODE:
        #    break

        print ' '*indent,\
              'Node name: "%s",' %n.nodeName,\
              'Node type: "%s",' %n.nodeType,\
              'Node value: "%s"' %str(n.nodeValue).strip()
              
        
        print_tree(n.firstChild, indent+4)
        n = n.nextSibling


def pretty_print_tree(n, indent=0):
    print n

def parse(fid):
    """Parse XML file descriptor and return DOM object.
    """

    # FIXME (OLE): XML code should be validated against the DTD
    #validate(fid, handler)
    #doc = minidom.parse(fid, make_parser())

    fid.seek(0)
    doc = minidom.parse(fid)    
    return doc


def get_elements(nodelist):
    """Return list of nodes that are ELEMENT_NODE
    """

    element_list = []
    for node in nodelist:
        if node.nodeType == Node.ELEMENT_NODE:
            element_list.append(node)

    return element_list


def get_text(nodelist):
    """Return a concatenation of text fields from list of nodes
    """

    s = ''
    for node in nodelist:
        if node.nodeType == Node.TEXT_NODE:
            s += node.nodeValue + ', '

    if len(s)>0: s = s[:-2]
    return s





#----------------------------
# XML object model
#----------------------------

class XML_element:
    def __init__(self, tag=None, contents=None):
        """
        contents can be either
          * An XML_element
          * a list of XML_elements
          * a text string
        
        """
        
        if isinstance(contents, XML_element):
            contents = [contents]
            
        self.elements = contents

        self.tag = tag

    def __add__(self, other):
        return str(self) + str(other)

    def __radd__(self, other):
        return str(other) + str(self)    #Python swaps self and other    

    def __repr__(self):
        return str(self)

    def __str__(self):
        pass

    def __str__(self, indent=0):

        s = tab = ' '*indent
        
        s += '<%s>' %self.tag
        if isinstance(self.elements, basestring):
            s += self.elements
        else:
            s += '\n'
            for e in self.elements:
                s += e.__str__(indent+4)
            s += tab

        s += '</%s>\n' %self.tag
        return s

    

    def pretty_print(self, indent=0):
        """Print the document without tags using indentation
        """

        s = tab = ' '*indent
        s += '%s: ' %self.tag        
        if isinstance(self.elements, basestring):
            s += self.elements
        else:
            s += '\n'
            for e in self.elements:
                s += e.pretty_print(indent+4)
        s += '\n'
        
        return s
    
    
    
class XML_document(XML_element):

    def __init__(self, contents=None, version='1.0', encoding='iso-8859-1'):
        tag = '?xml version="%s" encoding="%s"' %(version, encoding)

        XML_element.__init__(self,
                             tag=tag,
                             contents=contents)


    def __str__(self):
        """Generate XML representation for use with xml2object function
        """
        s = '<%s>\n' %self.tag
        for e in self.elements:
            s += str(e)
        return s

    def pretty_print(self):
        s = ''
        for e in self.elements:
            s += e.pretty_print()

        return s


def xml2object(xml, verbose=False):
    """Generate XML object model from XML file or XML text

    This is the inverse operation to the __str__ representation.

    Input xml can be either an
    * xml string ??
    * xml file
    * open xml file object 

    Return XML_document instance.
    """

    #FIXME(Ole): Do the input tests
    #Assume open file object for now

    #fid = open(xml)
    dom = parse(xml)

    print 'Res',    dom2object(dom)



def dom2object(node):

    if node.nodeType == 3 and len(node.nodeValue.strip()) == 0:
        return None
        
    print 'Node name: "%s",' %node.nodeName,\
          'Node type: "%s",' %node.nodeType,\
          'Node value: "%s",' %str(node.nodeValue).strip(),\
          'Node children: %d' %len(node.childNodes)

    

    if node.nodeType == 3:
        contents = node.nodeValue.strip()
    else:    
        contents = []
        for n in node.childNodes:
            x = dom2object(n)
            if x is not None:
                contents.append(x)


    if node.nodeType == 9:
        # Document
        X = XML_document()
        
    X = XML_element(tag=node.nodeName,
                    contents=contents)
    return X
