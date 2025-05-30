from pathlib import Path
import os


def XMLFinder(rimworldFolderPath, force=False):
    # If already written, ends the function
    if os.path.exists("XMLFilePaths.txt") and not force:
        return

    # Excludes older versions
    excludedKeywords = ["1.0", "1.1", "1.2", "1.3", "1.4"]

    # Builds a list with every single XML file path
    XMLFilePaths = []
    for XMLFilePath in Path(rimworldFolderPath).rglob("*.xml"):
        if any(keyword in str(XMLFilePath) for keyword in excludedKeywords):
            continue

        XMLFilePaths.append(XMLFilePath)

    # Writes the list inside a text file
    print(XMLFilePaths)
    with open("XMLFilePaths.txt", "w", encoding="utf-8") as f:
        for XMLFilePath in XMLFilePaths:
            print(XMLFilePath)
            f.write(str(XMLFilePath) + "\n")
