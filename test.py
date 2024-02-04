import streamlit as st
import extra_streamlit_components as stx

st.code("import extra_streamlit_components as stx")
chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id="tab1", title="✍️ To Do", description="Tasks to take care of"),
    stx.TabBarItemData(id="tab2", title="📣 Done", description="Tasks taken care of"),
    stx.TabBarItemData(id="tab3", title="💔 Overdue", description="Tasks missed out")])

placeholder = st.container()

if chosen_id == "tab1":
    placeholder.markdown(f"## Welcome to `{chosen_id}`")
    placeholder.image("https://placekitten.com/g/1400/600",caption=f"Meowhy from {chosen_id}")

elif chosen_id == "tab2":
    placeholder.markdown(f"## Hello, this is `{chosen_id}`")
    placeholder.image("https://placekitten.com/g/1200/300",caption=f"Hi from {chosen_id}")

elif chosen_id == "tab3":
    placeholder.markdown(f"## And this is ... 🥁 ... `{chosen_id}`")
    placeholder.image("https://placekitten.com/g/900/400",caption=f"Fancy seeing you here at {chosen_id}")

else:
    placeholder = st.empty()