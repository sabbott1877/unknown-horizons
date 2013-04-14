# Create content/cegui/schemes/UH.scheme
#
# Sets up all images in content/gui/ so they can be used in layouts
# without merging them together in big imagesets.

import os
import xml.etree.ElementTree as ET

root = ET.Element("GUIScheme", Name="UH")

for path, dirs, files in os.walk('content/gui/'):
	for f in files:
		if not f.endswith('png'):
			continue

		filepath = os.path.join(path, f)
		ET.SubElement(root, "ImagesetFromImage", Filename="../../../" + filepath, Name=filepath)

tree = ET.ElementTree()
tree._setroot(root)
tree.write("content/cegui/schemes/UH.scheme")
