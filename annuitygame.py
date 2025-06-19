import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Annuity Game", layout="centered")

st.title("📈 Annuity Quiz Game")
st.markdown("Test your understanding of **Future Value (FV)** and **Present Value (PV)** of annuities using standard annuity tables.")

# Sample annuity table for FV and PV
annuity_table = {
    "n": list(range(1, 11)),
    "i=5%": [1.050, 2.103, 3.159, 4.216, 5.276, 6.338, 7.402, 8.469, 9.538, 10.610],
    "i=7%": [1.070, 2.145, 3.215, 4.280, 5.339, 6.393, 7.442, 8.486, 9.525, 10.558],
    "i=10%": [1.100, 2.210, 3.310, 4.410, 5.510, 6.610, 7.710, 8.810, 9.910, 11.000]
}
annuity_df = pd.DataFrame(annuity_table)

st.subheader("📊 Annuity Table (Future Value of $1 per period)")
st.dataframe(annuity_df, use_container_width=True)

if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.q_count = 0

# Generate new question
def generate_question():
    rate = random.choice(["i=5%", "i=7%", "i=10%"])
    n = random.randint(3, 9)
    payment = random.choice([100, 200, 500])
    fv_factor = annuity_df.loc[annuity_df["n"] == n, rate].values[0]
    fv = round(payment * fv_factor, 2)
    correct_answer = fv
    options = [round(fv * (1 + random.uniform(-0.15, 0.15)), 2) for _ in range(3)]
    options.append(correct_answer)
    random.shuffle(options)
    return {
        "rate": rate,
        "n": n,
        "payment": payment,
        "correct": correct_answer,
        "options": options
    }

if 'question' not in st.session_state:
    st.session_state.question = generate_question()

q = st.session_state.question
st.markdown(f"""
### Question {st.session_state.q_count + 1}
If you invest **${q['payment']} per year** for **{q['n']} years** at **{q['rate']}**, what is the **Future Value**?
""")

selected = st.radio("Choose your answer:", q['options'], key=f"question_{st.session_state.q_count}")

if st.button("Submit Answer"):
    if selected == q['correct']:
        st.success("✅ Correct!")
        st.session_state.score += 1
    else:
        st.error(f"❌ Incorrect. The correct answer was ${q['correct']}")
    
    st.session_state.q_count += 1

    if st.session_state.q_count >= 5:
        st.markdown("## 🏁 Game Over")
        st.markdown(f"**Your final score:** {st.session_state.score} / 5")
        st.button("Restart Game", on_click=lambda: st.session_state.clear())
    else:
        st.session_state.question = generate_question()
        st.rerun()
