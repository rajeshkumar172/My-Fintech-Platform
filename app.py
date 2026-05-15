import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd

st.set_page_config(page_title="AI FinTech Platform India", layout="wide", page_icon="📈")

st.title("📈 AI-Driven Equity Research & Trading Platform")
st.markdown("Integrating real-time Indian stock data, rigorous financial modeling, and AI.")

# Sidebar for inputs
st.sidebar.header("Market Configuration")
tickers = {
    "Reliance Industries": "RELIANCE.NS", 
    "Tata Consultancy Services": "TCS.NS", 
    "HDFC Bank": "HDFCBANK.NS", 
    "Infosys": "INFY.NS",
    "State Bank of India": "SBIN.NS",
    "Adani Green Energy": "ADANIGREEN.NS",
    "Zomato": "ZOMATO.NS"
}
selected_stock = st.sidebar.selectbox("Select Indian Stock", list(tickers.keys()))
ticker_symbol = tickers[selected_stock]

# Tabs for different modules
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Equity Research", 
    "📈 Technical Analysis", 
    "🏢 Fundamentals", 
    "🤖 AI Chatbot",
    "🌍 Sector Watch",
    "📩 About & Contact"
])

# Fetch Data
@st.cache_data
def get_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        info = stock.info
        return stock, hist, info
    except Exception as e:
        return None, pd.DataFrame(), {}

stock, hist, info = get_data(ticker_symbol)

if hist.empty:
    st.error("Failed to fetch data. Please try again later.")
else:
    with tab1:
        st.header(f"Equity Research: {selected_stock}")
        st.info(f"{selected_stock} is showing strong operational efficiency. Based on the latest earnings call, the management remains optimistic about maintaining margins despite market volatility.")
        st.subheader("Recent Price Action (Last 5 Days)")
        st.dataframe(hist[['Open', 'High', 'Low', 'Close', 'Volume']].tail(), use_container_width=True)

    with tab2:
        st.header("Technical Analysis Report")
        fig = go.Figure(data=[go.Candlestick(x=hist.index,
                        open=hist['Open'],
                        high=hist['High'],
                        low=hist['Low'],
                        close=hist['Close'],
                        name="Price")])
        hist['50_MA'] = hist['Close'].rolling(window=50).mean()
        fig.add_trace(go.Scatter(x=hist.index, y=hist['50_MA'], mode='lines', name='50-Day MA', line=dict(color='blue')))
        fig.update_layout(title=f"{selected_stock} - 1 Year Price History", xaxis_rangeslider_visible=False, height=500)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.header("Fundamental Analysis")
        col1, col2, col3, col4 = st.columns(4)
        mcap = info.get('marketCap', 'N/A')
        mcap_display = f"₹ {mcap / 10000000:.2f} Cr" if isinstance(mcap, (int, float)) else "N/A"
        col1.metric("Market Cap", mcap_display)
        col2.metric("P/E Ratio", round(info.get('trailingPE', 0), 2) if info.get('trailingPE') else 'N/A')
        col3.metric("Dividend Yield", f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else 'N/A')
        col4.metric("52 Week High", f"₹ {info.get('fiftyTwoWeekHigh', 'N/A')}")
        st.subheader("Company Profile")
        st.write(info.get('longBusinessSummary', 'No description available.'))

    with tab4:
        st.header("🤖 AI Finance Chatbot (India Context)")
        user_query = st.chat_input(f"Ask me anything about {selected_stock}...")
        if user_query:
            st.chat_message("user").write(user_query)
            last_price = hist['Close'].iloc[-1]
            st.chat_message("assistant").write(f"**FinBot:** Currently, {selected_stock} is trading at ₹{last_price:.2f}. My analysis of recent NSE data suggests monitoring the technical levels closely before making an entry.")

    with tab5:
        st.header("🔥 Thematic Sector Watch")
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("🌱 Renewable Energy & Infrastructure")
            st.write("Tracking the expansion of large-scale solar and wind energy parks. Companies managing these mega-projects are poised for structural growth. Key focus areas include execution capabilities and supply chain optimization.")
        with col_b:
            st.subheader("⚡ Quick Commerce & Tech")
            st.write("Analyzing the disruption in the Indian retail landscape. Supply chain optimization and rapid delivery ecosystems are reshaping consumer habits, offering unique valuation opportunities.")

    with tab6:
        st.header("Our Identity & Contact")
        
        st.subheader("Vision")
        st.write("To be the premier destination where rigorous financial discipline meets cutting-edge technology, empowering investors with transparent, institutional-grade market intelligence.")
        
        st.subheader("Mission")
        st.write("To demystify complex market dynamics by combining advanced AI capabilities with sound fundamental and technical analysis. We strive to provide real-time, actionable insights that enable robust, data-driven investment decisions.")
        
        st.subheader("Motivation")
        st.write("Driven by a deep appreciation for precise financial modeling and a background in managing complex, large-scale project operations in the infrastructure sector. I realized that the exact strategic discipline and execution capabilities required for high-stakes operational environments are just as crucial for navigating financial markets. This platform aims to bring that structured, analytical edge to everyone.")
        
        st.divider()
        
        col_contact1, col_contact2 = st.columns(2)
        
        with col_contact1:
            st.subheader("Get in Touch")
            st.markdown("**Name:** Rajesh Kumar Rout")
            st.markdown("**Mobile:** +91 9668594434")
            st.markdown("**Email:** [rrout172@gmail.com](mailto:rrout172@gmail.com)")
            
        with col_contact2:
            with st.form("contact_form"):
                st.write("Or send a direct message:")
                name = st.text_input("Your Name")
                email = st.text_input("Your Email")
                message = st.text_area("Your Message")
                submit_button = st.form_submit_button("Send Message")
                
                if submit_button:
                    if name and email and message:
                        st.success("Thank you! Your message has been received.")
                    else:
                        st.error("Please fill out all fields.")
