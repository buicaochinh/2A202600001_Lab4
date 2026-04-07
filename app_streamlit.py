import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from agent import graph


st.set_page_config(
    page_title="TravelBuddy",
    page_icon="✈️",
    layout="wide",
)


def init_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []


def reset_chat() -> None:
    st.session_state.messages = []


def render_message_history() -> None:
    for message in st.session_state.messages:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
        elif isinstance(message, AIMessage) and message.content:
            with st.chat_message("assistant"):
                st.markdown(message.content)


def main() -> None:
    init_state()

    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, #fff2d9 0%, transparent 28%),
                radial-gradient(circle at top right, #dff3ff 0%, transparent 24%),
                linear-gradient(180deg, #fffdf8 0%, #fff7ec 100%);
        }
        .hero-card {
            padding: 1.25rem 1.5rem;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid rgba(205, 176, 130, 0.35);
            box-shadow: 0 18px 40px rgba(167, 124, 55, 0.08);
            margin-bottom: 1rem;
        }
        .hero-title {
            font-size: 2rem;
            font-weight: 700;
            color: #8a4b08;
            margin-bottom: 0.25rem;
        }
        .hero-subtitle {
            color: #6b5b45;
            font-size: 1rem;
            margin-bottom: 0;
        }
        </style>
        <div class="hero-card">
            <div class="hero-title">TravelBuddy</div>
            <p class="hero-subtitle">
                Trợ lý du lịch thông minh để tìm chuyến bay, khách sạn và ước tính ngân sách cho chuyến đi của bạn.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.header("Tùy chọn")
        st.button("Xóa hội thoại", use_container_width=True, on_click=reset_chat)
        st.markdown("**Gợi ý nhanh**")
        st.caption("Bạn có thể thử một trong các câu sau:")
        st.code("Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng")
        st.code("Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu")
        st.code("Tìm khách sạn ở Đà Nẵng dưới 800000 một đêm")

    render_message_history()

    prompt = st.chat_input("Bạn muốn đi đâu?")
    if not prompt:
        return

    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("TravelBuddy đang tư vấn..."):
            result = graph.invoke({"messages": st.session_state.messages})
            st.session_state.messages = result["messages"]
            final_message = st.session_state.messages[-1]
            st.markdown(final_message.content)


if __name__ == "__main__":
    main()
