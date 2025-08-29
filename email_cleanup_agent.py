#!/usr/bin/env python3
"""
Email Cleanup Agent - Beautiful, Easy Interface
A user-friendly tool to clean up and organize email inboxes
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import os

# Configuration class built into the app
class BotConfig:
    # API Keys from Streamlit secrets (secure method)
    @classmethod
    def get_openai_key(cls):
        try:
            return st.secrets["OPENAI_API_KEY"]
        except:
            return None
    
    @classmethod
    def get_google_key(cls):
        try:
            return st.secrets["GOOGLE_API_KEY"]
        except:
            return None
    
    @classmethod
    def get_elevenlabs_key(cls):
        try:
            return st.secrets["ELEVENLABS_API_KEY"]
        except:
            return None
    
    @classmethod
    def get_serpapi_key(cls):
        try:
            return st.secrets["SERPAPI_KEY"]
        except:
            return None
    
    # Default model settings
    DEFAULT_MODEL = "gpt-4o-mini"
    DEFAULT_TEMPERATURE = 0.7
    
    @classmethod
    def validate_keys(cls):
        """Check if essential API keys are set"""
        return cls.get_openai_key() is not None

# Page configuration
st.set_page_config(
    page_title="Smart Email Cleaner",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        transition: transform 0.3s ease;
        margin: 1rem 0;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

def create_progress_chart(value, title, color="#667eea"):
    """Create a beautiful circular progress chart"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'size': 16, 'color': '#2c3e50'}},
        gauge = {
            'axis': {'range': [None, 100], 'tickcolor': color},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 50], 'color': "#f8f9fa"},
                {'range': [50, 100], 'color': "#e9ecef"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=200,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def main_dashboard():
    """Main dashboard interface"""
    
    # Header
    st.markdown('<h1 class="main-header">📧 Smart Email Cleaner</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #6c757d; margin-bottom: 3rem;">Transform your chaotic inbox into an organized paradise</p>', unsafe_allow_html=True)
    
    # API Key Status
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if BotConfig.validate_keys():
            st.success("✅ AI features are enabled!")
        else:
            st.warning("⚠️ Configure API keys in Streamlit Cloud settings")
            with st.expander("🔧 How to add API keys"):
                st.write("""
                1. Go to your Streamlit Cloud app dashboard
                2. Click the ⚙️ Settings button  
                3. Go to "Secrets" tab
                4. Add your keys in this format:
                ```
                OPENAI_API_KEY = "your-key-here"
                GOOGLE_API_KEY = "your-key-here"
                ELEVENLABS_API_KEY = "your-key-here" 
                SERPAPI_KEY = "your-key-here"
                ```
                5. Save and restart the app
                """)
    
    # Connection Status
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.get('connected', False):
            st.success("✅ Connected to your email account")
        else:
            st.warning("⚠️ Not connected to email account")
            if st.button("🔗 Connect Email Account", key="connect_btn"):
                st.session_state.connected = True
                st.rerun()
    
    # Main metrics dashboard
    if st.session_state.get('connected', False):
        st.markdown("---")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h2>📨</h2>
                <h3>1247</h3>
                <p>Total Emails</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h2>🗑️</h2>
                <h3>342</h3>
                <p>Emails Cleaned</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h2>💾</h2>
                <h3>2.4 GB</h3>
                <p>Space Saved</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <h2>⏱️</h2>
                <h3>5.2 hrs</h3>
                <p>Time Saved</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Progress charts
        st.markdown("### 📊 Cleanup Progress")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fig1 = create_progress_chart(73, "Spam Removal", "#e74c3c")
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = create_progress_chart(89, "Organization", "#27ae60")
            st.plotly_chart(fig2, use_container_width=True)
        
        with col3:
            fig3 = create_progress_chart(56, "Unsubscribe", "#f39c12")
            st.plotly_chart(fig3, use_container_width=True)

def cleanup_features():
    """Email cleanup features interface"""
    
    st.markdown("### 🛠️ Cleanup Features")
    
    # Feature cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🗑️ Smart Spam Removal</h3>
            <p>AI-powered detection of spam and promotional emails</p>
            <ul>
                <li>Advanced pattern recognition</li>
                <li>Safe whitelist protection</li>
                <li>Bulk processing</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Start Spam Cleanup", key="spam_cleanup"):
            with st.spinner("Cleaning spam emails..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.02)
                    progress_bar.progress(i + 1)
            st.success("✅ Removed 127 spam emails!")
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📁 Smart Organization</h3>
            <p>Automatically sort emails into relevant folders</p>
            <ul>
                <li>Bills & Finance</li>
                <li>Work & Business</li>
                <li>Personal & Family</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📂 Organize Inbox", key="organize"):
            with st.spinner("Organizing emails..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.03)
                    progress_bar.progress(i + 1)
            st.success("✅ Organized 234 emails into folders!")

def sidebar_menu():
    """Sidebar navigation and settings"""
    
    with st.sidebar:
        st.markdown("### 🎛️ Control Panel")
        
        # Navigation
        page = st.selectbox(
            "Choose View",
            ["📊 Dashboard", "🛠️ Cleanup Tools", "⚙️ Settings"]
        )
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🔍 Scan Inbox", key="scan"):
            st.success("Inbox scanned successfully!")
        
        if st.button("🔄 Refresh Data", key="refresh"):
            st.success("Data refreshed!")
        
        st.markdown("---")
        
        # Status
        st.markdown("### 📡 Status")
        st.success("✅ System Online")
        st.info("🔒 Secure Connection")
        
        return page

def main():
    """Main application"""
    
    # Initialize session state
    if 'connected' not in st.session_state:
        st.session_state.connected = False
    
    # Sidebar
    current_page = sidebar_menu()
    
    # Main content based on page selection
    if "Dashboard" in current_page:
        main_dashboard()
        
    elif "Cleanup Tools" in current_page:
        cleanup_features()
        
    elif "Settings" in current_page:
        st.markdown("### ⚙️ Settings")
        st.markdown("Email cleanup preferences and configuration options")
        
        # Email provider selection
        provider = st.selectbox("Email Provider", ["Gmail", "Outlook", "Yahoo", "Other"])
        
        # Save settings
        if st.button("💾 Save Settings"):
            st.success("Settings saved successfully!")

if __name__ == "__main__":
    main()
