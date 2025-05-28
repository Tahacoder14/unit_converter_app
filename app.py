import streamlit as st
from utils.conversion_data import CONVERSION_FACTORS
from utils.converters import convert_standard, convert_temperature
import os

# --- Initialize Session State (must be done early) ---
if "input_value" not in st.session_state:
    st.session_state.input_value = 1.0
if "selected_category_key" not in st.session_state:
    st.session_state.selected_category_key = "Length"
if "from_unit" not in st.session_state:
    # Initialize based on the default selected_category_key
    default_cat_units = list(CONVERSION_FACTORS[st.session_state.selected_category_key]["units"].keys())
    st.session_state.from_unit = default_cat_units[0]
if "to_unit" not in st.session_state:
    default_cat_units = list(CONVERSION_FACTORS[st.session_state.selected_category_key]["units"].keys())
    st.session_state.to_unit = default_cat_units[1] if len(default_cat_units) > 1 else default_cat_units[0]
if "result" not in st.session_state:
    st.session_state.result = None
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light" # Default to light mode

# --- Page Configuration (must be the first Streamlit command) ---
st.set_page_config(
    layout="centered",
    page_title="Pro Unit Converter",
    page_icon="🔄",
    initial_sidebar_state="expanded"
    # We will set theme dynamically using st._config.set_option
)

# --- Apply Theme (if not default) ---
# This needs to be after set_page_config and uses an internal API, but it's the way for dynamic theme changes
# This will apply the theme from session_state on subsequent runs/reruns
if hasattr(st, '_config') and hasattr(st._config, 'set_option'):
    st._config.set_option('theme.base', st.session_state.theme_mode)
elif st.session_state.theme_mode == "dark": # Fallback for very old versions if _config is not there
    st.warning("Dynamic theme switching might not be fully supported. Consider upgrading Streamlit.")


# --- Load Custom CSS (Optional) ---
def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Check if assets/styles.css exists before trying to load
css_file_path = os.path.join("assets", "styles.css")
if os.path.exists(css_file_path):
    load_css(css_file_path)
else:
    # Provide some default minimal styling if custom CSS is missing,
    # especially for the metric if it was heavily styled by styles.css
    st.markdown("""
    <style>
        div[data-testid="stMetric"] {
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            border: 1px solid #dadee3;
        }
        div[data-testid="stMetric"] label { font-size: 1.1em; color: #31333F;}
        div[data-testid="stMetric"] p { font-size: 1.8em !important; font-weight: bold; color: #007bff; }
    </style>
    """, unsafe_allow_html=True)


# --- App Header ---
if os.path.exists(os.path.join("assets", "logo.png")):
    st.image(os.path.join("assets", "logo.png"), width=100)

st.title("🚀 Pro Unit Converter")
st.markdown("Seamlessly convert units across various categories with live updates!")
st.markdown("---")

# --- Sidebar ---
st.sidebar.header("⚙️ Settings")

# Theme Toggle Button
current_theme_label = "🌙 Dark Mode" if st.session_state.theme_mode == "light" else "☀️ Light Mode"
if st.sidebar.button(current_theme_label, use_container_width=True):
    st.session_state.theme_mode = "dark" if st.session_state.theme_mode == "light" else "light"
    # Apply the theme change
    if hasattr(st, '_config') and hasattr(st._config, 'set_option'):
        st._config.set_option('theme.base', st.session_state.theme_mode)
    st.rerun() # Rerun to apply theme and update button label

st.sidebar.markdown("---") # Separator

# Category Selection
category_names_icons = {
    key: f"{data['icon']} {key}" for key, data in CONVERSION_FACTORS.items()
}
selected_category_display = st.sidebar.selectbox(
    "Select Conversion Category:",
    options=list(category_names_icons.values()),
    index=list(category_names_icons.keys()).index(st.session_state.selected_category_key)
)

new_selected_category_key = [k for k, v in category_names_icons.items() if v == selected_category_display][0]

if new_selected_category_key != st.session_state.selected_category_key:
    st.session_state.selected_category_key = new_selected_category_key
    category_data_on_change = CONVERSION_FACTORS[st.session_state.selected_category_key]
    unit_names_list_on_change = list(category_data_on_change["units"].keys())
    st.session_state.from_unit = unit_names_list_on_change[0]
    st.session_state.to_unit = unit_names_list_on_change[1] if len(unit_names_list_on_change) > 1 else unit_names_list_on_change[0]
    st.session_state.input_value = 1.0
    st.session_state.result = None
    st.rerun() # Rerun to update main page content for new category

category_data = CONVERSION_FACTORS[st.session_state.selected_category_key]
unit_names = list(category_data["units"].keys())

# --- Main Interface ---
st.subheader(f"Converting: {st.session_state.selected_category_key} {category_data['icon']}")

col_input, col_clear_button = st.columns([4, 1])
with col_input:
    # Ensure keys are unique and consistently used for widgets if their values are in session_state
    current_input_val = st.session_state.get("input_value_widget", st.session_state.input_value) # Use a widget-specific key if needed or sync carefully
    st.session_state.input_value = st.number_input(
        f"Enter Value:",
        value=float(st.session_state.input_value), # Use the main session state value
        step=0.01,
        format="%.4f",
        key="num_input_main_interface" # More specific key
    )
with col_clear_button:
    st.markdown("<br/>", unsafe_allow_html=True)
    if st.button("Clear", use_container_width=True, key="clear_btn_main"):
        st.session_state.input_value = 0.0
        st.session_state.result = 0.0
        st.rerun()

col_from, col_swap, col_to = st.columns([5, 1, 5])

with col_from:
    # Ensure `from_unit` from session state is valid for current category
    if st.session_state.from_unit not in unit_names:
        st.session_state.from_unit = unit_names[0]
    st.session_state.from_unit = st.selectbox(
        "From Unit:",
        unit_names,
        index=unit_names.index(st.session_state.from_unit),
        key="from_unit_select_main"
    )

with col_swap:
    st.markdown("<br/>", unsafe_allow_html=True)
    if st.button("⇄", use_container_width=True, help="Swap Units", key="swap_btn_main"):
        current_from = st.session_state.from_unit
        current_to = st.session_state.to_unit
        st.session_state.from_unit = current_to
        st.session_state.to_unit = current_from
        # Optional: Swap input with result
        if st.session_state.result is not None:
             # Check if result can be meaningfully used as new input
            try:
                new_input = float(st.session_state.result)
                # Only swap if the current input is not already the result of a previous swap
                # This check might be complex; simpler to just swap input with result
                # if float(st.session_state.input_value) != new_input:
                st.session_state.input_value = new_input
            except ValueError:
                pass # Result might be non-numeric after formatting, or None
        st.rerun() # FIXED: Replaced experimental_rerun

with col_to:

    if st.session_state.to_unit not in unit_names:
        st.session_state.to_unit = unit_names[1] if len(unit_names) > 1 else unit_names[0]
    st.session_state.to_unit = st.selectbox(
        "To Unit:",
        unit_names,
        index=unit_names.index(st.session_state.to_unit),
        key="to_unit_select_main"
    )

# --- Perform Conversion (Live) ---
if st.session_state.input_value is not None:
    if st.session_state.selected_category_key == "Temperature":
        from_unit_symbol = category_data["units"][st.session_state.from_unit]
        to_unit_symbol = category_data["units"][st.session_state.to_unit]
        st.session_state.result = convert_temperature(st.session_state.input_value, from_unit_symbol, to_unit_symbol)
    else:
        st.session_state.result = convert_standard(st.session_state.input_value, st.session_state.from_unit, st.session_state.to_unit, category_data)

# --- Display Result ---
st.markdown("---")
st.subheader("🎯 Result")

if st.session_state.result is not None:
    try:
        # Ensure input_value is float for formatting
        input_val_float = float(st.session_state.input_value)
        result_float = float(st.session_state.result)

        formatted_input = f"{input_val_float:.4g} {st.session_state.from_unit}"
        formatted_result = f"{result_float:.6g} {st.session_state.to_unit}"
        st.metric(label=formatted_input, value=formatted_result)

        if st.session_state.from_unit == st.session_state.to_unit:
            st.info("Input and output units are the same.")
    except (ValueError, TypeError) as e:
        st.error(f"Could not display result. Input: {st.session_state.input_value}, Result: {st.session_state.result}. Error: {e}")
        st.metric(label="Error", value="Invalid calculation")

else:
    st.info("Enter a value and select units to see the conversion.")

# --- How it works / Details Expander ---
with st.expander("ℹ️ How It Works & Conversion Details", expanded=False):
    st.markdown("""
    This app converts values between different units within a selected category **live** as you type or change units.
    - For most categories, conversions are done by:
        1. Converting the input value to a standard **base unit**.
        2. Converting this base unit value to the desired target unit.
    - **Temperature** conversions use specific mathematical formulas.
    - Use the **Clear** button to reset the input value.
    - Use the **⇄** button to swap the 'From' and 'To' units. The input value might also update to the previous result.
    - Toggle between **Light and Dark Mode** using the button in the sidebar.
    """)
    # if st.session_state.selected_category_key != "Temperature":
    #     st.markdown(f"**Base Unit for {st.session_state.selected_category_key}:** `{category_data['base_unit']}`")

st.sidebar.markdown("---")
st.sidebar.markdown("Made by **Taha**")