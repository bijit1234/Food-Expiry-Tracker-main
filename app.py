import streamlit as st
import json
from pathlib import Path
from datetime import datetime

DATA_FILE = 'data.json'

# --------------------
# Utility Functions
# --------------------

def load_data():
    if not Path(DATA_FILE).exists() or Path(DATA_FILE).stat().st_size == 0:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
        return []

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def add_item(name, quantity, expiry_date):
    data = load_data()
    data.append({
        "name": name,
        "quantity": quantity,
        "expiry_date": expiry_date
    })
    save_data(data)

def delete_item(index):
    data = load_data()
    if 0 <= index < len(data):
        del data[index]
        save_data(data)

def edit_item(index, name, quantity, expiry_date):
    data = load_data()
    if 0 <= index < len(data):
        data[index]['name'] = name
        data[index]['quantity'] = quantity
        data[index]['expiry_date'] = expiry_date
        save_data(data)

# --------------------
# App
# --------------------

def main():
    st.set_page_config(page_title="EXPIRY - WISE", page_icon="♻️")
    st.title("🥫 Food Expiry Tracker ♻️")
    st.markdown("> Reduce waste by tracking your food expiry dates!")

    st.divider()

    # Barcode scan placeholder
    st.subheader("📷 Barcode Scanning")
    if st.button("🔍 Scan Barcode"):
        st.info("🚧 Feature coming soon!")

    st.divider()

    # Add new items
    st.subheader("➕ Add Food Item")
    with st.form("add_form"):
        name = st.text_input("Food Name")
        quantity = st.text_input("Quantity (e.g. 500g, 1L)")
        expiry = st.date_input("Expiry Date", value=datetime.today())
        submit = st.form_submit_button("Add Item")
        if submit:
            if name.strip() and quantity.strip():
                add_item(name, quantity, str(expiry))
                st.success(f"✅ Added {name} with expiry {expiry}")
                st.rerun()
            else:
                st.warning("Please fill in all fields.")

    st.divider()

    # View items
    st.subheader("📋 Your Food Items")
    data = load_data()

    if not data:
        st.info("No food items added yet.")
    else:
        for idx, item in enumerate(data):
            exp_date = datetime.strptime(item["expiry_date"], "%Y-%m-%d").date()
            days_left = (exp_date - datetime.today().date()).days

            if days_left < 0:
                status = "⚠️ Expired"
                color = "red"
            elif days_left <= 3:
                status = f"⏰ {days_left} day(s) left"
                color = "orange"
            else:
                status = f"✅ {days_left} day(s) left"
                color = "green"

            with st.expander(f"{idx+1}. {item['name']}"):
                st.markdown(f"""
                - Quantity: `{item['quantity']}`
                - Expiry Date: `{item['expiry_date']}`
                - Status: <span style='color:{color}'>{status}</span>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("🗑️ Delete", key=f"del{idx}"):
                        delete_item(idx)
                        st.rerun()

                with col2:
                    if f"edit_mode_{idx}" not in st.session_state:
                        st.session_state[f"edit_mode_{idx}"] = False

                    if st.session_state[f"edit_mode_{idx}"]:
                        new_name = st.text_input(f"Name_{idx}", value=item["name"])
                        new_quantity = st.text_input(f"Quantity_{idx}", value=item["quantity"])
                        new_expiry = st.date_input(f"Expiry_{idx}", value=exp_date)

                        save_col, cancel_col = st.columns(2)
                        with save_col:
                            if st.button("💾 Save", key=f"save_{idx}"):
                                edit_item(idx, new_name, new_quantity, str(new_expiry))
                                st.session_state[f"edit_mode_{idx}"] = False
                                st.success("✅ Item updated!")
                                st.rerun()

                        with cancel_col:
                            if st.button("❌ Cancel", key=f"cancel_{idx}"):
                                st.session_state[f"edit_mode_{idx}"] = False
                                st.rerun()

                    else:
                        if st.button("✏️ Edit", key=f"edit_{idx}"):
                            st.session_state[f"edit_mode_{idx}"] = True

    st.divider()

    # About section
    st.subheader("👨‍💻 About This App")
    st.markdown("""
    Made with ❤️ by **  ->  PARADOX**  
    Track your food expiry and help reduce kitchen waste.
    """)

    st.markdown("### 🔗 Connect with Me:")
    st.markdown("""

)

    """)

    st.caption("© 2026 team PARADOX | Food Expiry Tracker v1.1")

if __name__ == "__main__":
    main()


