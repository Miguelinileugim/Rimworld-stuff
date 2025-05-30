from pathlib import Path
import findParent


def patchDefs(defsExportFolder):
    for XMLFilePath in Path(defsExportFolder).rglob("*"):
        parentChain = [XMLFilePath]
        findParent(defsExportFolder, XMLFilePath, parentChain)

        if len(parentChain) == 1:
            continue

        baseFile = parentChain.pop()
        appliedFile = parentChain[-1]
        print(baseFile, appliedFile)
