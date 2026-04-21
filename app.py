import re
import io
import qrcode
from datetime import datetime
import streamlit as st
import pandas as pd

# ── Constants ──────────────────────────────────────────────────────────────────
TOTAL_TWO_WHEELERS = 100
TOTAL_FOUR_WHEELERS = 200
TWO_WHEELER_RATE = 30
FOUR_WHEELER_RATE = 60
TAX_RATE = 0.18
VNO_PATTERN = r"^[A-Z]{2}-\d{2}-[A-Z]{1,2}-\d{4}$"

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Parking Management System",
    page_icon="🅿️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .receipt-box {
    background: #f8f9fa;
    padding: 24px;
    border-radius: 12px;
    border: 1px solid #dee2e6;
    font-family: 'Segoe UI', sans-serif;
  }
  .receipt-title {
    text-align: center;
    color: #0d6efd;
    margin-bottom: 12px;
  }
  .receipt-total {
    color: #198754;
    font-size: 1.3rem;
  }
  .receipt-footer {
    text-align: center;
    color: #6c757d;
    font-size: 0.9rem;
    margin-top: 12px;
  }
  div[data-testid="stMetricValue"] { font-size: 1.4rem; }
</style>
""", unsafe_allow_html=True)

# ── Session State Init ─────────────────────────────────────────────────────────
if "vehicles" not in st.session_state:
    st.session_state.vehicles = []
if "tw_used" not in st.session_state:
    st.session_state.tw_used = 0
if "fw_used" not in st.session_state:
    st.session_state.fw_used = 0


# ── Helpers ────────────────────────────────────────────────────────────────────
def get_vehicle(vno: str) -> dict | None:
    for v in st.session_state.vehicles:
        if v["vno"] == vno:
            return v
    return None


def tw_left() -> int:
    return TOTAL_TWO_WHEELERS - st.session_state.tw_used


def fw_left() -> int:
    return TOTAL_FOUR_WHEELERS - st.session_state.fw_used


def space_color(remaining: int, total: int) -> str:
    ratio = remaining / total
    if ratio > 0.2:
        return "green"
    if ratio > 0.05:
        return "orange"
    return "red"


def generate_qr_buffer(text: str) -> io.BytesIO:
    qr = qrcode.QRCode(version=1, box_size=6, border=4)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🅿️ Parking System")
    st.markdown("---")

    st.subheader("Available Spaces")
    col_a, col_b = st.columns(2)
    with col_a:
        tw = tw_left()
        st.metric("🛵 Two-Wheeler", f"{tw}", delta=f"/{TOTAL_TWO_WHEELERS}")
    with col_b:
        fw = fw_left()
        st.metric("🚗 Four-Wheeler", f"{fw}", delta=f"/{TOTAL_FOUR_WHEELERS}")

    tw_c = space_color(tw, TOTAL_TWO_WHEELERS)
    fw_c = space_color(fw, TOTAL_FOUR_WHEELERS)
    st.markdown(
        f"🛵 Status: :{tw_c}[{'Available' if tw > 0 else 'FULL'}]  "
        f"&nbsp;&nbsp; 🚗 Status: :{fw_c}[{'Available' if fw > 0 else 'FULL'}]"
    )

    st.markdown("---")
    st.subheader("Pricing (per hour)")
    st.markdown(f"- 🛵 Two-Wheeler &nbsp; **₹{TWO_WHEELER_RATE}**")
    st.markdown(f"- 🚗 Four-Wheeler &nbsp; **₹{FOUR_WHEELER_RATE}**")
    st.markdown(f"- 🧾 GST &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **18%**")

    st.markdown("---")
    total_parked = len(st.session_state.vehicles)
    st.metric("Vehicles Parked", total_parked)

    if st.button("🔄 Reset Session", use_container_width=True, type="secondary"):
        st.session_state.vehicles = []
        st.session_state.tw_used = 0
        st.session_state.fw_used = 0
        st.rerun()


# ── Header ─────────────────────────────────────────────────────────────────────
st.title("🅿️ Parking Management System")
st.caption("Streamlined vehicle entry, space tracking, and automated billing.")
st.markdown("---")

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🚘 Vehicle Entry",
    "🗑️  Remove Vehicle",
    "📋  View Records",
    "🧾  Generate Bill",
])


# ── Tab 1 — Vehicle Entry ──────────────────────────────────────────────────────
with tab1:
    st.subheader("Register a New Vehicle")

    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            vno_input = st.text_input(
                "Vehicle Number *",
                placeholder="KA-08-AS-2345",
                help="Indian vehicle number format: XX-00-XX-0000",
            )
            vtype_input = st.selectbox("Vehicle Type *", ["Two-Wheeler", "Four-Wheeler"])
        with col2:
            vname_input = st.text_input("Vehicle Name", placeholder="Honda Activa")
            owner_input = st.text_input("Owner Name", placeholder="Rahul Sharma")

        submitted = st.form_submit_button("✅ Register Vehicle", use_container_width=True)

    if submitted:
        vno = vno_input.upper().strip()
        if not vno:
            st.error("Vehicle number cannot be empty.")
        elif not re.match(VNO_PATTERN, vno):
            st.error("❌ Invalid format. Expected: KA-08-AS-2345 (State-RTO-Series-Number)")
        elif get_vehicle(vno):
            st.error(f"❌ Vehicle **{vno}** is already registered.")
        elif vtype_input == "Two-Wheeler" and tw_left() == 0:
            st.error("❌ No two-wheeler spaces available.")
        elif vtype_input == "Four-Wheeler" and fw_left() == 0:
            st.error("❌ No four-wheeler spaces available.")
        else:
            now = datetime.now()
            st.session_state.vehicles.append({
                "vno": vno,
                "vtype": vtype_input,
                "vname": vname_input.strip() or "Unknown",
                "owner": owner_input.strip() or "Unknown",
                "date": now.strftime("%d-%m-%Y"),
                "time": now.strftime("%H:%M:%S"),
            })
            if vtype_input == "Two-Wheeler":
                st.session_state.tw_used += 1
            else:
                st.session_state.fw_used += 1
            st.success(f"✅ Vehicle **{vno}** registered successfully!")
            st.rerun()


# ── Tab 2 — Remove Vehicle ─────────────────────────────────────────────────────
with tab2:
    st.subheader("Remove a Vehicle Entry")

    if not st.session_state.vehicles:
        st.info("No vehicles currently parked.")
    else:
        vnos = [v["vno"] for v in st.session_state.vehicles]
        selected_remove = st.selectbox("Select Vehicle to Remove", vnos, key="remove_select")

        v_preview = get_vehicle(selected_remove)
        if v_preview:
            st.markdown(
                f"**Owner:** {v_preview['owner']} &nbsp;|&nbsp; "
                f"**Type:** {v_preview['vtype']} &nbsp;|&nbsp; "
                f"**Entry:** {v_preview['date']} {v_preview['time']}"
            )

        if st.button("🗑️ Confirm Remove", type="primary", use_container_width=False):
            v = get_vehicle(selected_remove)
            if v:
                st.session_state.vehicles.remove(v)
                if v["vtype"] == "Two-Wheeler":
                    st.session_state.tw_used -= 1
                else:
                    st.session_state.fw_used -= 1
                st.success(f"✅ **{selected_remove}** removed. Space freed.")
                st.rerun()


# ── Tab 3 — View Records ───────────────────────────────────────────────────────
with tab3:
    st.subheader("All Parked Vehicles")

    if not st.session_state.vehicles:
        st.info("No vehicles currently parked.")
    else:
        df = pd.DataFrame(st.session_state.vehicles, columns=["vno", "vtype", "vname", "owner", "date", "time"])
        df.columns = ["Vehicle No.", "Type", "Vehicle Name", "Owner", "Date", "Entry Time"]

        col_f1, col_f2 = st.columns([2, 1])
        with col_f1:
            search = st.text_input("Search by vehicle no. or owner", placeholder="KA-08...")
        with col_f2:
            type_filter = st.selectbox("Filter by type", ["All", "Two-Wheeler", "Four-Wheeler"])

        filtered = df.copy()
        if search:
            mask = (
                filtered["Vehicle No."].str.contains(search.upper(), na=False) |
                filtered["Owner"].str.contains(search, case=False, na=False)
            )
            filtered = filtered[mask]
        if type_filter != "All":
            filtered = filtered[filtered["Type"] == type_filter]

        st.dataframe(filtered, use_container_width=True, hide_index=True)
        st.caption(f"Showing {len(filtered)} of {len(df)} vehicle(s).")


# ── Tab 4 — Generate Bill ──────────────────────────────────────────────────────
with tab4:
    st.subheader("Generate Parking Bill & QR Receipt")

    if not st.session_state.vehicles:
        st.info("No vehicles currently parked.")
    else:
        vnos = [v["vno"] for v in st.session_state.vehicles]
        selected_bill = st.selectbox("Select Vehicle", vnos, key="bill_select")
        hours = st.number_input("Parking Duration (hours)", min_value=1, max_value=720, value=1, step=1)

        if st.button("🧾 Generate Bill", type="primary"):
            v = get_vehicle(selected_bill)
            rate = TWO_WHEELER_RATE if v["vtype"] == "Two-Wheeler" else FOUR_WHEELER_RATE
            amt = hours * rate
            tax = TAX_RATE * amt
            total = amt + tax
            now = datetime.now()

            st.markdown("---")
            col_receipt, col_qr = st.columns([3, 1])

            with col_receipt:
                st.markdown(f"""
<div class="receipt-box">
  <h3 class="receipt-title">🚗 Parking Receipt</h3>
  <hr/>
  <p><b>Vehicle No:</b> {v['vno']}</p>
  <p><b>Vehicle Name:</b> {v['vname']}</p>
  <p><b>Type:</b> {v['vtype']}</p>
  <p><b>Owner:</b> {v['owner']}</p>
  <hr/>
  <p><b>Entry Date &amp; Time:</b> {v['date']} &nbsp; {v['time']}</p>
  <p><b>Billing Date &amp; Time:</b> {now.strftime('%d-%m-%Y')} &nbsp; {now.strftime('%H:%M:%S')}</p>
  <p><b>Duration:</b> {hours} hour(s)</p>
  <hr/>
  <p><b>Rate:</b> ₹{rate}/hr</p>
  <p><b>Parking Charge:</b> ₹{amt:.2f}</p>
  <p><b>GST (18%):</b> ₹{tax:.2f}</p>
  <p class="receipt-total"><b>Total Amount: ₹{total:.2f}</b></p>
  <p class="receipt-footer">✅ Thank you for using our parking service!</p>
</div>
""", unsafe_allow_html=True)

            with col_qr:
                receipt_text = (
                    f"PARKING RECEIPT\n"
                    f"----------------\n"
                    f"Vehicle : {v['vno']}\n"
                    f"Type    : {v['vtype']}\n"
                    f"Owner   : {v['owner']}\n"
                    f"Entry   : {v['date']} {v['time']}\n"
                    f"Duration: {hours}hr(s)\n"
                    f"Charge  : Rs.{amt:.2f}\n"
                    f"GST 18% : Rs.{tax:.2f}\n"
                    f"TOTAL   : Rs.{total:.2f}\n"
                    f"----------------\n"
                    f"Thank You!"
                )
                qr_buf = generate_qr_buffer(receipt_text)
                st.image(qr_buf, caption="Scan for receipt", width=180)
                st.download_button(
                    label="⬇️ Download QR",
                    data=qr_buf,
                    file_name=f"receipt_{v['vno']}.png",
                    mime="image/png",
                    use_container_width=True,
                )
