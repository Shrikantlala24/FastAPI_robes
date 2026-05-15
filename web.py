import streamlit as st
import requests
from requests.exceptions import RequestException


st.set_page_config(page_title="Patient Store UI")

st.title("Patient Store — Streamlit UI for FastAPI")

# allow changing base URL in the sidebar
base_url = st.sidebar.text_input("API base URL", value="http://localhost:8000")

st.sidebar.markdown("---")
st.sidebar.write("Endpoints: `/`, `/about`, `/view`, `/create`")

def api_get(path: str):
    try:
        r = requests.get(f"{base_url}{path}", timeout=5)
        r.raise_for_status()
        return r.json()
    except RequestException as e:
        st.error(f"Request failed: {e}")
        return None

def api_post(path: str, payload: dict):
    try:
        r = requests.post(f"{base_url}{path}", json=payload, timeout=5)
        # try to parse json response if any
        try:
            return r.status_code, r.json()
        except Exception:
            return r.status_code, {"detail": r.text}
    except RequestException as e:
        st.error(f"Request failed: {e}")
        return None, None


st.header("About API")
if st.button("Get /about"):
    about = api_get("/about")
    if about:
        st.json(about)

st.header("View Patients")
if st.button("Refresh /view"):
    data = api_get("/view")
    if data is None:
        st.stop()
    if not data:
        st.info("No patients in the database.")
    else:
        for pid, item in data.items():
            st.subheader(f"ID: {pid}")
            # show fields
            st.write(f"Name: {item.get('name')}")
            st.write(f"City: {item.get('city')}")
            st.write(f"Age: {item.get('age')}")
            st.write(f"Gender: {item.get('gender')}")
            st.write(f"Height (h): {item.get('h')}")
            st.write(f"Weight (w): {item.get('w')}")
            # try compute bmi locally if possible
            try:
                h = float(item.get('h'))
                w = float(item.get('w'))
                if h > 0:
                    bmi = round(w / (h ** 2), 2)
                    st.write(f"BMI: {bmi}")
            except Exception:
                pass
            st.markdown("---")

st.header("Create Patient")
with st.form("create_patient"):
    pid = st.text_input("Patient ID", help="e.g. P001")
    name = st.text_input("Name")
    city = st.text_input("City")
    age = st.number_input("Age", min_value=1, max_value=119, value=30)
    gender = st.selectbox("Gender", options=["male", "female", "others"])
    h = st.number_input("Height (h) in feet", min_value=0.1, format="%.2f", value=5.5)
    w = st.number_input("Weight (w) in pounds", min_value=0.1, format="%.2f", value=150.0)
    submitted = st.form_submit_button("Create")

    if submitted:
        if not pid or not name:
            st.error("Please provide at least `Patient ID` and `Name`.")
        else:
            payload = {"id": pid, "name": name, "city": city, "age": int(age), "gender": gender, "h": float(h), "w": float(w)}
            status, resp = api_post("/create", payload)
            if status is None:
                st.stop()
            if status == 201:
                st.success(resp.get("message") if isinstance(resp, dict) else str(resp))
            else:
                # show API error detail when available
                detail = resp.get("detail") if isinstance(resp, dict) else resp
                st.error(f"Error ({status}): {detail}")

st.markdown("---")
st.caption("Set the API base URL in the sidebar if your FastAPI app runs on a different host/port.")



