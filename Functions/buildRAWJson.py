import xml.etree.ElementTree as ET
from pathlib import Path


def buildRawJSON(XMLFilePaths):
    for XMLFilePath in XMLFilePaths:
        try:
            tree = ET.parse(XMLFilePath)
            root = tree.getroot()

            for ThingDef in root.iter(tag="ThingDef"):
                defNameElement = ThingDef.find("defName")
                if defNameElement is not None and defNameElement.text:
                    # Create a new element with only ThingDef
                    new_tree = ET.ElementTree(ThingDef)

                    # Output path with defname as filename
                    output_path = Path(defsExportFolder) / f"{defNameElement.text}.xml"
                    new_tree.write(output_path, encoding="utf-8", xml_declaration=True)
        except Exception:
            pass
