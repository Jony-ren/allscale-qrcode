import streamlit as st
from PIL import Image
import qrcode
import io

# --- Page Configuration ---
st.set_page_config(page_title="PosterQR Pro", layout="wide", page_icon="🎨")

# --- Custom CSS to make it look nicer ---
st.markdown("""
<style>
    .stApp {
        background-color: #ffffff;
    }
    .main .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Logic Functions ---

def hex_to_rgb(hex_color):
    """Convert hex string to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def generate_qr_image(content, fg_color, bg_color, size_px):
    """Generate a high-res QR code image"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1,
    )
    qr.add_data(content)
    qr.make(fit=True)

    # Convert colors
    fg_rgb = hex_to_rgb(fg_color)
    bg_rgb = hex_to_rgb(bg_color)

    img_qr = qr.make_image(fill_color=fg_rgb, back_color=bg_rgb).convert("RGBA")
    
    # Resize to target size
    img_qr = img_qr.resize((size_px, size_px), Image.Resampling.LANCZOS)
    
    # Add padding container (matching the style of previous versions)
    padding = int(size_px * 0.05) # 5% padding
    final_size = size_px + (padding * 2)
    
    bg_square = Image.new("RGBA", (final_size, final_size), bg_rgb)
    bg_square.paste(img_qr, (padding, padding), img_qr)
    
    return bg_square

def compose_image(base_img, url, size_pct, x_pct, y_pct, fg, bg):
    """Compose the final poster"""
    working_img = base_img.copy().convert("RGBA")
    width, height = working_img.size
    
    # Calculate Size
    qr_display_size = int((size_pct / 100) * width)
    if qr_display_size < 10: qr_display_size = 10
    
    qr_img = generate_qr_image(url, fg, bg, qr_display_size)
    
    # Calculate Position (Center based)
    pos_x = int((x_pct / 100) * width) - (qr_img.width // 2)
    pos_y = int((y_pct / 100) * height) - (qr_img.height // 2)
    
    # Compose
    working_img.paste(qr_img, (pos_x, pos_y), qr_img)
    
    return working_img

# --- UI Layout ---

st.title("PosterQR Pro")
st.caption("Upload a poster, replace the QR code, and download in HD.")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("1. Settings")
    
    # Upload
    uploaded_file = st.file_uploader("Upload Base Image", type=['png', 'jpg', 'jpeg'])
    
    # Content
    url_input = st.text_input("QR Content (URL)", value="https://openai.com")
    
    st.write("---")
    st.subheader("2. Style & Position")
    
    # Sliders
    size_val = st.slider("Size (%)", 5.0, 80.0, 25.0, 0.5)
    x_val = st.slider("Position X (%)", 0.0, 100.0, 50.0, 0.5)
    y_val = st.slider("Position Y (%)", 0.0, 100.0, 45.0, 0.5)
    
    # Colors
    c1, c2 = st.columns(2)
    with c1:
        fg_color = st.color_picker("QR Color", "#E9F6F1")
    with c2:
        bg_color = st.color_picker("Background", "#15382C")

with col2:
    st.subheader("Preview")
    
    if uploaded_file:
        # Load Image
        base_image = Image.open(uploaded_file)
        
        # Generate Composition
        final_img = compose_image(base_image, url_input, size_val, x_val, y_val, fg_color, bg_color)
        
        # Display
        st.image(final_img, use_container_width=True)
        
        # Download Button
        buf = io.BytesIO()
        final_img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="Download HD Poster",
            data=byte_im,
            file_name="poster_qr_pro.png",
            mime="image/png",
            use_container_width=True,
            type="primary"
        )
        
    else:
        # Empty State
        st.info("👈 Please upload an image from the sidebar to start.")
        st.markdown("""
        <div style="border: 2px dashed #ccc; border-radius: 10px; padding: 40px; text-align: center; color: #ccc;">
            Preview Area
        </div>
        """, unsafe_allow_html=True)
