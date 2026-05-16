import requests
from requests.exceptions import RequestException
import streamlit as st


st.set_page_config(page_title="Patient Store UI", page_icon="🏥", layout="wide")


def build_url(base_url: str, path: str) -> str:
    return f"{base_url.rstrip('/')}/{path.lstrip('/')}"


def request_json(method: str, path: str, base_url: str, payload: dict | None = None):
    try:
        response = requests.request(method, build_url(base_url, path), json=payload, timeout=5)
        try:
            body = response.json()
        except Exception:
            body = {"detail": response.text}
        return response.status_code, body
    except RequestException as exc:
        return None, {"detail": str(exc)}


def normalize_dimension(patient: dict, primary: str, fallback: str):
    value = patient.get(primary)
    if value is None:
        value = patient.get(fallback)
    return value


def bmi_from_patient(patient: dict):
    height = normalize_dimension(patient, "h", "height")
    weight = normalize_dimension(patient, "w", "weight")
    try:
        height = float(height)
        weight = float(weight)
        if height > 0:
            return round(weight / (height**2), 2)
    except Exception:
        return None
    return None


def render_patient(pid: str, patient: dict):
    left, right = st.columns([1, 2])
    with left:
        st.markdown(f"### {pid}")
        st.metric("Age", patient.get("age", "-"))
        bmi = bmi_from_patient(patient)
        if bmi is not None:
            st.metric("BMI", bmi)
    with right:
        st.write(f"**Name:** {patient.get('name', '-')}")
        st.write(f"**City:** {patient.get('city', '-')}")
        st.write(f"**Gender:** {patient.get('gender', '-')}")
        st.write(f"**Height:** {normalize_dimension(patient, 'h', 'height')}")
        st.write(f"**Weight:** {normalize_dimension(patient, 'w', 'weight')}")
    st.divider()


st.title("Patient Store")
st.caption("Streamlit front end for the FastAPI patient API in api.py.")

with st.sidebar:
    st.header("Connection")
    base_url = st.text_input("API base URL", value="http://localhost:8000")
    st.caption("Make sure the FastAPI server is running before using the app.")
    st.markdown("---")
    st.write("Available routes:")
    st.write("/  /about  /view  /view/{pid}  /create  /edit/{pid}  /delete/{pid}")


top_left, top_right = st.columns([2, 1])
with top_left:
    st.subheader("API Overview")
    if st.button("Load /about"):
        status, about = request_json("GET", "/about", base_url)
        if status == 200:
            st.json(about)
        else:
            st.error(about.get("detail", "Request failed"))
with top_right:
    if st.button("Check /"):
        status, root = request_json("GET", "/", base_url)
        if status == 200:
            st.success(root.get("message", "API is reachable"))
        else:
            st.error(root.get("detail", "Request failed"))


tab_view, tab_create, tab_update, tab_delete = st.tabs(["View", "Create", "Update", "Delete"])

with tab_view:
    st.subheader("View patients")
    view_id = st.text_input("Patient ID", key="view_pid")
    col_a, col_b = st.columns([1, 1])
    with col_a:
        show_one = st.button("View patient")
    with col_b:
        show_all = st.button("Refresh all patients")

    if show_one and view_id:
        status, patient = request_json("GET", f"/view/{view_id}", base_url)
        if status == 200:
            render_patient(view_id, patient)
        else:
            st.error(patient.get("detail", f"Request failed ({status})"))

    if show_all:
        status, patients = request_json("GET", "/view", base_url)
        if status == 200:
            if not patients:
                st.info("No patients found.")
            else:
                for pid, patient in patients.items():
                    render_patient(pid, patient)
        else:
            st.error(patients.get("detail", f"Request failed ({status})"))


with tab_create:
    st.subheader("Create patient")
    with st.form("create_patient_form", clear_on_submit=True):
        create_id = st.text_input("Patient ID", placeholder="P001")
        create_name = st.text_input("Name")
        create_city = st.text_input("City")
        create_age = st.number_input("Age", min_value=1, max_value=119, value=30)
        create_gender = st.selectbox("Gender", options=["male", "female", "others"])
        create_h = st.number_input("Height (h)", min_value=0.1, value=5.5, format="%.2f")
        create_w = st.number_input("Weight (w)", min_value=0.1, value=150.0, format="%.2f")
        create_submit = st.form_submit_button("Create patient")

    if create_submit:
        if not create_id or not create_name or not create_city:
            st.error("Patient ID, Name, and City are required.")
        else:
            payload = {
                "id": create_id,
                "name": create_name,
                "city": create_city,
                "age": int(create_age),
                "gender": create_gender,
                "h": float(create_h),
                "w": float(create_w),
            }
            status, response = request_json("POST", "/create", base_url, payload)
            if status == 201:
                st.success(response.get("message", "Patient created"))
            else:
                st.error(response.get("detail", f"Request failed ({status})"))


with tab_update:
    st.subheader("Update patient")
    with st.form("update_patient_form"):
        update_id = st.text_input("Patient ID to update", placeholder="P001")
        update_name = st.text_input("Name", help="Leave blank to keep the current value")
        update_city = st.text_input("City", help="Leave blank to keep the current value")
        update_age = st.number_input("Age", min_value=0, max_value=119, value=0)
        update_gender = st.selectbox("Gender", options=["keep current", "male", "female", "others"])
        update_h = st.number_input("Height (h)", min_value=0.0, value=0.0, format="%.2f")
        update_w = st.number_input("Weight (w)", min_value=0.0, value=0.0, format="%.2f")
        update_submit = st.form_submit_button("Update patient")

    if update_submit:
        if not update_id:
            st.error("Patient ID is required.")
        else:
            payload = {}
            if update_name.strip():
                payload["name"] = update_name.strip()
            if update_city.strip():
                payload["city"] = update_city.strip()
            if int(update_age) > 0:
                payload["age"] = int(update_age)
            if update_gender != "keep current":
                payload["gender"] = update_gender
            if float(update_h) > 0:
                payload["h"] = float(update_h)
            if float(update_w) > 0:
                payload["w"] = float(update_w)

            if not payload:
                st.warning("Provide at least one field to update.")
            else:
                status, response = request_json("PUT", f"/edit/{update_id}", base_url, payload)
                if status == 201:
                    st.success(response.get("message", "Patient updated"))
                else:
                    st.error(response.get("detail", f"Request failed ({status})"))


with tab_delete:
    st.subheader("Delete patient")
    delete_id = st.text_input("Patient ID to delete", key="delete_pid")
    delete_confirm = st.checkbox("I understand this will permanently remove the patient")
    if st.button("Delete patient"):
        if not delete_id:
            st.error("Patient ID is required.")
        elif not delete_confirm:
            st.warning("Confirm deletion before continuing.")
        else:
            status, response = request_json("DELETE", f"/delete/{delete_id}", base_url)
            if status == 200:
                st.success(response.get("message", "Patient deleted"))
            else:
                st.error(response.get("detail", f"Request failed ({status})"))


st.markdown("---")
st.caption("If your API stores old records with height / weight, the UI will still display them.")



