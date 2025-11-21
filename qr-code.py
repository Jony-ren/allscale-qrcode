import streamlit as st
import qrcode
from PIL import Image, ImageColor
import io

# --- Page Configuration (OpenAI-like Minimalist Design) ---
st.set_page_config(
    page_title="QR Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Light Mode & OpenAI Design Language ---
st.markdown("""
    <style>
        /* General Font and Background */
        .stApp {
            font-family: 'Söhne', 'Helvetica Neue', Helvetica, Arial, sans-serif;
            background-color: #FFFFFF;
            color: #000000;
        }
        
        /* Headers */
        h1, h2, h3 {
            font-weight: 600;
            color: #202123;
        }
        
        /* Buttons - OpenAI Green/Black Style */
        .stButton > button {
            background-color: #10a37f;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        .stButton > button:hover {
            background-color: #0d8a6a;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        /* Inputs */
        .stTextInput > div > div > input {
            background-color: #FFFFFF;
            border: 1px solid #e5e5e5;
            color: #000000;
            border-radius: 4px;
        }
        
        /* Remove Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Canvas Container */
        .css-1544g2n {
            padding: 2rem;
            background-color: #f7f7f8;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

def create_qr_code(url, fill_color, back_color="transparent"):
    """Generates a QR code image with transparent background."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1, # Minimal border
    )
    qr.add_data(url)
    qr.make(fit=True)

    if back_color == "transparent":
        # Generate with white background first, then convert to transparent
        img = qr.make_image(fill_color=fill_color, back_color="white").convert("RGBA")
        datas = img.getdata()
        newData = []
        for item in datas:
            # If the pixel is white (background), make it transparent
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        img.putdata(newData)
        return img
    else:
        return qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGBA")

def main():
    # --- Sidebar Controls ---
    with st.sidebar:
        st.title("Settings")
        st.markdown("---")
        
        # 1. Content Input
        st.subheader("1. Content")
        target_url = st.text_input("QR Link URL", value="https://openai.com", help="Enter the website link for the QR code.")
        
        # 2. Design Input
        st.subheader("2. Design")
        # Default color matches the light green in the provided poster (~#E3FCEF)
        qr_color = st.color_picker("QR Color", "#E3FCEF") 
        
        st.markdown("---")
        st.subheader("3. Export")
        st.caption("Adjust the position on the right, then download.")

    # --- Main Area ---
    st.title("Poster Editor")
    st.markdown("Upload your poster, customize the QR code, and download the result.")

    # File Uploader
    uploaded_file = st.file_uploader("Upload Poster Image", type=['jpg', 'jpeg', 'png'])

    if uploaded_file:
        # Load Base Image
        base_image = Image.open(uploaded_file).convert("RGBA")
        base_w, base_h = base_image.size

        # Layout: Canvas (Left) + Controls (Right)
        col1, col2 = st.columns([3, 1])

        with col2:
            st.info("🎨 **Canvas Controls**")
            st.markdown("Use these sliders to position the QR code.")
            
            # Smart defaults: position roughly in the center
            default_size = int(base_w * 0.3)
            default_x = int((base_w - default_size) / 2)
            default_y = int((base_h - default_size) / 2)

            # Sliders for "Drag and Drop" simulation
            qr_size = st.slider("Size (Scale)", min_value=50, max_value=int(base_w), value=default_size)
            pos_x = st.slider("Horizontal Position (X)", min_value=0, max_value=base_w, value=default_x)
            pos_y = st.slider("Vertical Position (Y)", min_value=0, max_value=base_h, value=default_y)

        # Processing
        if target_url:
            # 1. Generate QR
            qr_img = create_qr_code(target_url, qr_color)
            
            # 2. Resize QR
            qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
            
            # 3. Composite (Create a copy to not mutate original)
            final_image = base_image.copy()
            
            # Paste QR code onto base image using the QR code itself as a mask (for transparency)
            final_image.paste(qr_img, (pos_x, pos_y), qr_img)

            # 4. Display
            with col1:
                st.image(final_image, caption="Real-time Preview", use_column_width=True)

            # 5. Download Button
            # Convert to bytes
            buf = io.BytesIO()
            final_image.convert("RGB").save(buf, format="JPEG", quality=95)
            byte_im = buf.getvalue()

            with st.sidebar:
                st.download_button(
                    label="Download Final Poster",
                    data=byte_im,
                    file_name="poster_with_new_qr.jpg",
                    mime="image/jpeg"
                )
    else:
        # Empty State
        st.info("👆 Please upload a poster image to begin.")
        # Optional: Show a placeholder or skeleton
        st.markdown(
            """
            <div style="background-color: #f7f7f8; height: 400px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #8e8ea0;">
                Preview Area
            </div>
            """, 
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
