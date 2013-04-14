# Convert pychan layouts to CEGUI layouts
# TODO handle nested tags

from PIL import Image
import xml.etree.ElementTree as ET

def format_position(position):
	x, y = position.split(',')
	return "{{0,%d},{0,%d}}" % (int(x), int(y))

def process_Container(node):
	root = ET.Element("Window", Type="DefaultWindow", Name=node.get('name'))
	ET.SubElement(root, "Property", Name="UnifiedMaxSize", Value="{{1,0},{1,0}}")
	ET.SubElement(root, "Property", Name="UnifiedAreaRect", Value="{{0,0},{0,0},{1,0},{1,0}}")
	return root

def process_Label(node):
	root = ET.Element("Window", Type="TaharezLook/StaticText", Name=node.get('name'))
	ET.SubElement(root, "Property", Name="FrameEnabled", Value="False")
	ET.SubElement(root, "Property", Name="BackgroundEnabled", Value="False")
	ET.SubElement(root, "Property", Name="VertFormatting", Value="TopAligned")

	tp = ET.SubElement(root, "Property", Name="Text")
	tp.text = node.get('text')

	pos = format_position(node.get('position'))
	ET.SubElement(root, "Property", Name="UnifiedPosition", Value=pos)
	ET.SubElement(root, "Property", Name="UnifiedSize", Value="{{0,100},{0,30}}")

	return root

def process_Icon(node):
	root = ET.Element("Window", Type="TaharezLook/StaticImage")
	ET.SubElement(root, "Property", Name="FrameEnabled", Value="False")
	ET.SubElement(root, "Property", Name="BackgroundEnabled", Value="False")
	ET.SubElement(root, "Property", Name="Disabled", Value="True")
	ET.SubElement(root, "Property", Name="Image", Value="set:" + node.get('image') + " image:full_image")

	with open(node.get('image'), 'rb') as png_file:
		width, height = Image.open(png_file).size
	
	pos = format_position(node.get('position'))
	ET.SubElement(root, "Property", Name="UnifiedPosition", Value=pos)

	size = "{{0,%d},{0,%d}}" % (width, height)
	ET.SubElement(root, "Property", Name="UnifiedSize", Value=size)

	return root

def process_MainmenuButton(node):
	root = ET.Element("Window", Type="TaharezLook/ImageButton", Name=node.get('name'))

	image = "content/gui/icons/mainmenu/%s.png" % node.get("icon")
	ET.SubElement(root, "Property", Name="NormalImage", Value="set:%s image:full_image" % image)
	ET.SubElement(root, "Property", Name="HoverImage", Value="set:%s image:full_image" % image)
	ET.SubElement(root, "Property", Name="PushedImage", Value="set:%s image:full_image" % image)
	ET.SubElement(root, "Property", Name="DisabledImage", Value="set:%s image:full_image" % image)

	with open(image, 'rb') as png_file:
		width, height = Image.open(png_file).size

	size = "{{0,%d},{0,%d}}" % (width, height)
	ET.SubElement(root, "Property", Name="UnifiedSize", Value=size)

	pos = format_position(node.get('position'))
	ET.SubElement(root, "Property", Name="UnifiedPosition", Value=pos)
	return root


output = ET.Element("GUILayout")
current = output

tree = ET.parse('content/gui/xml/mainmenu/mainmenu.xml')
root = tree.getroot()

current.append(process_Container(root))
current = current[0]
for node in root:
	process = globals().get("process_" + node.tag, None)
	if process:
		current.append(process(node))

ET.dump(output)
