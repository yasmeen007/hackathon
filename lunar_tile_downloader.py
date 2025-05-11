import requests
from PIL import Image
from io import BytesIO
import xml.etree.ElementTree as ET

# 🛰️ Define Landing Site & Zoom
LAT, LON = 31.204, -85.248  # Example landing site
ZOOM_LEVEL = 14  # Adjust for resolution

# 🔍 Bounding Box (Modify if needed)
BBOX = "-75.302,50.320,224.697,196.320"  # Adjusted BBOX values may be needed
WIDTH, HEIGHT = 1024, 1024  # Image resolution

# 🌍 WMS Server URL
WMS_SERVER = "https://wms.lroc.asu.edu/wms"

# 🔄 Alternative Layers
LAYER_CANDIDATES = ["LOLA_Shade", "WAC_GLOBAL", "LOLA_Color_Shade", "LOLA_HiRes_Shade"]

# 📝 Function to Check Available WMS Layers
def get_available_layers():
    print("🔍 Fetching available layers from WMS server...")
    capabilities_url = f"{WMS_SERVER}?SERVICE=WMS&REQUEST=GetCapabilities"
    response = requests.get(capabilities_url)

    if response.status_code != 200:
        print(f"❌ Failed to fetch capabilities. HTTP Code: {response.status_code}")
        return []

    try:
        # Handle XML namespaces
        namespaces = {"wms": "http://www.opengis.net/wms"}
        root = ET.fromstring(response.content)
        
        # Extract all layer names
        layers = [elem.text for elem in root.findall(".//wms:Name", namespaces)]
        
        if not layers:
            print("⚠️ No layers found in the WMS response. Check server response format.")
        
        print(f"✅ Available Layers: {layers}")
        return layers
    except ET.ParseError:
        print("⚠️ Error parsing WMS capabilities response.")
        return []

# ✅ Get Available Layers
available_layers = get_available_layers()

# 🔄 Find a Valid Layer
valid_layer = None
for layer in LAYER_CANDIDATES:
    if layer in available_layers:
        valid_layer = layer
        print(f"✅ Using layer: {valid_layer}")
        break

if not valid_layer:
    print("⚠️ No valid WMS layers found. Please check layer names or server settings.")
    exit()

# 🌍 WMS Image Request URL
WMS_URL = f"{WMS_SERVER}?SERVICE=WMS&REQUEST=GetMap&LAYERS={valid_layer}&FORMAT=image/png&BBOX={BBOX}&WIDTH={WIDTH}&HEIGHT={HEIGHT}"

print(f"🔗 Requesting image from:\n{WMS_URL}")

# 📥 Download Image
response = requests.get(WMS_URL)

if response.status_code == 200:
    image = Image.open(BytesIO(response.content))
    image.show()  # Display the image
    image.save("lunar_map.png")  # Save the image locally
    print("✅ Lunar map downloaded successfully as 'lunar_map.png'")
else:
    print(f"❌ Failed to download image. HTTP Status Code: {response.status_code}")
