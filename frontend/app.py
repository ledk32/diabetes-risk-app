import streamlit as st
import requests

st.set_page_config(page_title="Diabetes Risk Prediction", layout="centered")

st.title("Diabetes Risk Prediction")

st.error(
    "Disclaimer: This application provides an algorithmic estimate of diabetes risk "
    "based on the entered values. It is intended for informational purposes only and "
    "does not constitute medical advice, diagnosis, or treatment. "
    "Always consult a qualified healthcare professional."
)

st.write(
    "Enter the clinical values below to estimate diabetes risk."
)

# -------- Helper functions --------

def parse_number(value):
    if value is None or value.strip() == "":
        return None
    value = value.replace(",", ".")
    try:
        return float(value)
    except:
        return None


def validate(name, value, min_val, max_val):

    if value is None:
        st.error(f"{name}: invalid numeric format.")
        return False

    if value < 0:
        st.error(f"{name}: negative values are not allowed.")
        return False

    if value < min_val or value > max_val:
        st.error(f"{name}: value must be between {min_val} and {max_val}.")
        return False

    return True


# -------- Input fields --------

glucose = st.text_input(
    "Glucose (mg/dL)",
    placeholder="85"
)

blood_pressure = st.text_input(
    "Blood Pressure – Diastolic (mmHg)",
    placeholder="72"
)

skinfold = st.text_input(
    "Skinfold Thickness (mm)",
    placeholder="23"
)

insulin = st.text_input(
    "Insulin (µU/mL)",
    placeholder="85"
)

bmi = st.text_input(
    "Body Mass Index",
    placeholder="28.5"
)

diabetes_pedigree = st.text_input(
    "Diabetes Pedigree Function",
    placeholder="0.45"
)

age = st.text_input(
    "Age",
    placeholder="42"
)


# -------- Predict button --------

if st.button("Predict"):

    glucose = parse_number(glucose)
    blood_pressure = parse_number(blood_pressure)
    skinfold = parse_number(skinfold)
    insulin = parse_number(insulin)
    bmi = parse_number(bmi)
    diabetes_pedigree = parse_number(diabetes_pedigree)
    age = parse_number(age)

    valid = True

    valid &= validate("Glucose", glucose, 40, 400)
    valid &= validate("Blood pressure", blood_pressure, 30, 200)
    valid &= validate("Skinfold thickness", skinfold, 5, 100)
    valid &= validate("Insulin", insulin, 0, 900)
    valid &= validate("BMI", bmi, 10, 80)
    valid &= validate("Diabetes pedigree", diabetes_pedigree, 0, 3)
    valid &= validate("Age", age, 18, 120)

    if not valid:
        st.stop()

    payload = {
        "glucose": glucose,
        "blood_pressure": blood_pressure,
        "skinfold": skinfold,
        "insulin": insulin,
        "bmi": bmi,
        "diabetes_pedigree": diabetes_pedigree,
        "age": age
    }

    with st.spinner("Running prediction..."):

        response = requests.post(
            "https://diabetes-api-s42j.onrender.com/predict",
            json=payload
        )

        result = response.json()["prediction"]

    st.subheader("Prediction Result")

    if result == "true":
        st.warning(
            "The model predicts an elevated diabetes risk.\n\n"
            "This result is an algorithmic estimate and does not represent a medical diagnosis. "
            "Please consult a qualified healthcare professional for proper medical evaluation."
        )
    else:
        st.success(
            "The model predicts a lower estimated diabetes risk.\n\n"
            "This result is not a medical diagnosis. "
            "Consult a healthcare professional for medical advice or screening."
        )