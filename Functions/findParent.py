import xml.etree.ElementTree as ET


def findParent(defsExportFolder, XMLFilePath, parentChain):
    newParentChain = []
    try:
        tree = ET.parse(XMLFilePath)
        root = tree.getroot()
        attributes = root.attrib
        parentChain.append(attributes["ParentName"])
    except KeyError:
        return parentChain
    except ET.ParseError:
        # print(XMLFilePath, "ParseError")
        pass

    if len(newParentChain) == len(parentChain):
        return parentChain
    else:
        try:
            findParent(
                defsExportFolder,
                defsExportFolder + "\\" + parentChain[-1] + ".xml",
                parentChain,
            )
        except FileNotFoundError:
            return parentChain
        except TypeError:  # That damn blindfold file
            return parentChain
