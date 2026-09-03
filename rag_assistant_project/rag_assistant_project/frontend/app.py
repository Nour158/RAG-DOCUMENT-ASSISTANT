import streamlit as st
from api_client import ask
st.set_page_config(page_title="DocWise RAG",page_icon="📚",layout="centered")
st.title("📚 DocWise — RAG Document Assistant")
st.caption("Ask questions about the indexed documents. Answers are grounded and source-cited.")
if "messages" not in st.session_state: st.session_state.messages=[]
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])
q=st.chat_input("Ask a question about your documents...")
if q:
    st.session_state.messages.append({"role":"user","content":q}); st.chat_message("user").markdown(q)
    with st.chat_message("assistant"):
        try:
            with st.spinner("Searching documents and generating a grounded answer..."): data=ask(q)
            text=data["answer"]
            if data.get("sources"): text += "\n\n**Sources**\n"+"\n".join(f"- {s}" for s in data["sources"])
            st.markdown(text); st.session_state.messages.append({"role":"assistant","content":text})
        except Exception as e: st.error(f"Could not reach the API: {e}")
