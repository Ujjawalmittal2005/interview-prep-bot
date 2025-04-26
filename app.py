import streamlit as st

# Title
st.title("🎯 Interview Preparation Bot")

# Welcome message
st.write("Welcome! Let's practice some interview questions together.")

# Updated Questions
questions = [
    "1. Tell me about yourself.",
    "2. What are your strengths and weaknesses?",
    "3. Describe a challenging situation you faced and how you handled it.",
    "4. What experience do you bring to this role, and how does it align with your professional background?",
    "5. How do you envision contributing to the growth and success of our company?"
]

# Resources
resources = [
    "• Read 'Cracking the Coding Interview' by Gayle Laakmann McDowell.",
    "• Practice STAR method answers (Situation, Task, Action, Result).",
    "• Improve communication skills with mock interviews.",
]

# Initialize session state
if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "score" not in st.session_state:
    st.session_state.score = 0

# Function to reset everything
def reset():
    st.session_state.question_index = 0
    st.session_state.answers = {}
    st.session_state.score = 0
    st.rerun()  # Refresh the app

# Function to create summary text for download
def create_summary():
    summary = ""
    summary += "🎯 Interview Summary\n\n"
    
    # Strengths
    summary += "✔️ Strengths:\n"
    for question in strengths:
        summary += f"- {question}\n"

    # Areas to Improve
    summary += "\n⚡ Areas to Improve:\n"
    for question in improvements:
        summary += f"- {question}\n"

    # Final Score
    summary += f"\n🌟 Final Score: {final_score}/10\n"

    return summary

# Main flow
if st.session_state.question_index < len(questions):
    question = questions[st.session_state.question_index]

    # Display the question text clearly
    st.header(question)

    # Get answer from session state, if available
    answer = st.text_area("Your Answer:", value=st.session_state.answers.get(question, ""), key=question)

    col1, col2, col3 = st.columns(3)

    # Submit answer
    with col1:
        if st.button("✅ Submit Answer"):
            st.session_state.answers[question] = answer
            if len(answer.strip()) >= 30:
                st.session_state.score += 1
            st.session_state.question_index += 1
            st.rerun()  # Refresh the page

    # Retry current question
    with col2:
        if st.button("🔄 Retry"):
            # Clear current answer from session state
            st.session_state.answers[question] = ""
            st.session_state.question_index -= 1  # Keep the current question to retry
            st.rerun()  # Refresh the page with an empty text box

    # Skip current question
    with col3:
        if st.button("⏭️ Skip"):
            st.session_state.answers[question] = "Skipped"
            st.session_state.question_index += 1
            st.rerun()  # Refresh the page

else:
    # End of questions
    st.success("🎉 You have completed the interview practice!")

    st.write("## 📝 Your Answers and Feedback:")
    strengths = []
    improvements = []

    for question, answer in st.session_state.answers.items():
        st.subheader(question)
        if answer == "Skipped":
            st.info("You skipped this question.")
            improvements.append(question)
        elif len(answer.strip()) < 30:
            st.warning("Answer is too short. Try to add more details next time!")
            improvements.append(question)
        else:
            st.success("Good detailed answer! 👍")
            strengths.append(question)

    # Final Score
    total_questions = len(questions)
    final_score = int((st.session_state.score / total_questions) * 10)

    st.write("---")
    st.header("🏆 Final Summary Report")

    st.subheader("✔️ Strengths:")
    if strengths:
        for s in strengths:
            st.markdown(f"- {s}")
    else:
        st.write("No strong answers found yet. Keep practicing!")

    st.subheader("⚡ Areas to Improve:")
    if improvements:
        for i in improvements:
            st.markdown(f"- {i}")
    else:
        st.write("Amazing! No major improvements needed.")

    st.subheader("📚 Suggested Resources:")
    for res in resources:
        st.markdown(res)

    st.subheader(f"🌟 Final Score: {final_score}/10")

    # Create summary text for download
    summary_text = create_summary()

    # Add a download button for the summary
    st.download_button(
        label="Download Interview Summary",
        data=summary_text,
        file_name="interview_summary.txt",
        mime="text/plain"
    )

    # Restart Button
    if st.button("🔄 Practice Again"):
        reset()
