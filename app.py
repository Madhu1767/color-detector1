import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

# Load color dataset
@st.cache_data
def load_colors():
    df = pd.read_csv("colors.csv")
    return df

# Find closest color name
def get_color_name(R, G, B, color_data):
    min_dist = float('inf')
    closest_color = None
    for _, row in color_data.iterrows():
        d = abs(R - row['R']) + abs(G - row['G']) + abs(B - row['B'])
        if d < min_dist:
            min_dist = d
            closest_color = row
    return closest_color

# UI
st.title("🎨 Color Detection from Image (No OpenCV)")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.write("**Click on the image below to detect a color**")
    
    coords = streamlit_image_coordinates(image, key="click_image")

    if coords is not None:
        x, y = int(coords['x']), int(coords['y'])
        image_np = np.array(image)
        r, g, b = image_np[y, x]
        color_data = load_colors()
        color_info = get_color_name(r, g, b, color_data)
        hex_color = color_info['hex']

        st.markdown(f"""
        ### 🎯 Detected Color: {color_info['color_name']}
        - RGB: ({r}, {g}, {b})
        - HEX: {hex_color}
        """)
        st.markdown(f"""
        <div style="width:100px; height:50px; background-color:{hex_color}; border:1px solid #000;"></div>
        """, unsafe_allow_html=True)
