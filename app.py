import streamlit as st
import random
import time
import pandas as pd
import os

st.title("Cognitive Load and Financial Decision-Making")

st.write("This experiment studies how mental load affects financial decisions.")

DATA_FILE = "responses.csv"

scenarios = [
    {"safe": 100, "prob": 50, "risky": 250},
    {"safe": 150, "prob": 30, "risky": 500},
    {"safe": 80, "prob": 20, "risky": 600},
    {"safe": 120, "prob": 70, "risky": 200},
    {"safe": 200, "prob": 40, "risky": 700},
    {"safe": 90, "prob": 60, "risky": 180},
    {"safe": 250, "prob": 25, "risky": 1000},
    {"safe": 110, "prob": 50, "risky": 300},
    {"safe": 300, "prob": 35, "risky": 900},
    {"safe": 75, "prob": 80, "risky": 120},
]

if "participant_id" not in st.session_state:
    st.session_state.participant_id = ""

if "trial_number" not in st.session_state:
    st.session_state.trial_number = 0

if "experiment_started" not in st.session_state:
    st.session_state.experiment_started = False

if "current_trial" not in st.session_state:
    st.session_state.current_trial = None

if "start_time" not in st.session_state:
    st.session_state.start_time = None


def create_trial():
    load = random.choice(["Low Load", "High Load"])

    if load == "Low Load":
        memory_number = random.randint(100, 999)
    else:
        memory_number = random.randint(1000000, 9999999)

    scenario = scenarios[st.session_state.trial_number]

    st.session_state.current_trial = {
        "load": load,
        "memory_number": memory_number,
        "safe": scenario["safe"],
        "prob": scenario["prob"],
        "risky": scenario["risky"],
    }

    st.session_state.start_time = time.time()


def save_response(choice):
    reaction_time = time.time() - st.session_state.start_time
    trial = st.session_state.current_trial

    new_data = pd.DataFrame([{
        "participant_id": st.session_state.participant_id,
        "trial_number": st.session_state.trial_number + 1,
        "load": trial["load"],
        "memory_number": trial["memory_number"],
        "safe_amount": trial["safe"],
        "risky_probability": trial["prob"],
        "risky_amount": trial["risky"],
        "choice": choice,
        "reaction_time": round(reaction_time, 2)
    }])

    if os.path.exists(DATA_FILE):
        old_data = pd.read_csv(DATA_FILE)
        updated_data = pd.concat([old_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    updated_data.to_csv(DATA_FILE, index=False)

    st.session_state.trial_number += 1

    if st.session_state.trial_number < len(scenarios):
        create_trial()
    else:
        st.session_state.experiment_started = False
        st.session_state.current_trial = None


if not st.session_state.experiment_started:
    participant = st.text_input("Enter Participant ID")

    if st.button("Start Experiment"):
        if participant:
            st.session_state.participant_id = participant
            st.session_state.trial_number = 0
            st.session_state.experiment_started = True
            create_trial()
            st.rerun()
        else:
            st.warning("Please enter a Participant ID.")


if st.session_state.experiment_started and st.session_state.current_trial:
    trial = st.session_state.current_trial

    st.subheader(f"Trial {st.session_state.trial_number + 1} of {len(scenarios)}")

    st.write(f"Condition: **{trial['load']}**")
    st.write(f"Remember this number: **{trial['memory_number']}**")

    st.write("---")

    st.subheader("Financial Decision")
    st.write("Choose one of the following options:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"Safe Option: ₹{trial['safe']} guaranteed"):
            save_response("Safe")
            st.rerun()

    with col2:
        if st.button(f"Risky Option: {trial['prob']}% chance of ₹{trial['risky']}"):
            save_response("Risky")
            st.rerun()


if not st.session_state.experiment_started and st.session_state.trial_number == len(scenarios):
    st.success("Experiment completed. Thank you!")

    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        st.write("Latest saved data:")
        st.dataframe(df.tail(10))