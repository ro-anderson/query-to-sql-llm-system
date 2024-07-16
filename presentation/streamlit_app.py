import streamlit as st
from services.langchain_service import langchain_service

def main():
  st.set_page_config(page_title="Text-to-SQL System", page_icon="🔍", layout="wide")

  st.title("Text-to-SQL System")
  st.write("Enter a question to generate the corresponding SQL query and get the result.")

  question = st.text_input("Question", "What is the total value of all sales made per year?")

  if st.button("Submit"):
      with st.spinner("Generating SQL and fetching results..."):
          sql_query, sql_result, answer = langchain_service.get_sql_query(question)

      st.markdown("---")  # Horizontal line for separation

      st.markdown(f"### Question")
      st.code(question, language="")

      st.markdown("### SQL Query")
      st.code(sql_query, language="sql")

      st.markdown("### SQL Result")
      st.code(sql_result, language="")

      st.markdown("### Answer")
      st.markdown(answer)

      st.markdown("---")  # Horizontal line for separation

if __name__ == "__main__":
  main()