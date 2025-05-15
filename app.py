import streamlit as st
import cv2
import pandas as pd
import numpy as np
from PIL import Image

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

# UI Layout
st.title("🎨 Color Detection from Images")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    image_np = np.array(image)

    color_data = load_colors()

    st.write("**Click anywhere on the image to detect color**")

    # OpenCV logic
    if st.button("Enable Color Picker"):
        st.info("Close the image window after selecting to return result.")
        
        def click_event(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                b, g, r = image_np[y, x]
                color_info = get_color_name(r, g, b, color_data)
                hex_color = color_info['hex']
                st.session_state['color'] = {
                    'name': color_info['color_name'],
                    'R': r, 'G': g, 'B': b,
                    'hex': hex_color
                }

        cv2.namedWindow('Click Image')
        cv2.setMouseCallback('Click Image', click_event)
        cv2.imshow('Click Image', cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Show detected color
    if 'color' in st.session_state:
        color = st.session_state['color']
        st.markdown(f"""
        ### 🎯 Detected Color: {color['name']}
        - RGB: ({color['R']}, {color['G']}, {color['B']})
        - HEX: {color['hex']}
        """)
        st.markdown(f"""
        <div style="width:100px; height:50px; background-color:{color['hex']}; border:1px solid #000;"></div>
        """, unsafe_allow_html=True)
