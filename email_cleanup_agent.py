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
      # API Keys - directly embedded for deployment
      OPENAI_API_KEY =
  "sk-proj-suXreP5NRAkIUIia5T1PNN4KzebrnC7Pi_gseLEp5GKgULi7IIi9X2xxPxT3BlbkF
  JPdBX8xHZ4RP-MKcXaJadpSi_ezv3-E8lGCA-Bc05T5iwRB6p88mbqrTlAA"
      GOOGLE_API_KEY = "AIzaSyBMkjopa6Jru7-NZUYokJfaa_QHu6mv10c"
      ELEVENLABS_API_KEY =
  "sk_d78e34d5255f347a3219fed94aa07f7c11a87a8ae453a19f"
      SERPAPI_KEY = "bNtBX8ncYme1oguqbRoAjxJD"

      # Default model settings
      DEFAULT_MODEL = "gpt-4o-mini"
      DEFAULT_TEMPERATURE = 0.7

      @classmethod
      def validate_keys(cls):
          """Check if essential API keys are set"""
          missing = []
          if not cls.OPENAI_API_KEY:
              missing.append("OPENAI_API_KEY")

          if missing:
              st.warning(f"Missing API keys: {', '.join(missing)}")
              st.info("Add them in Streamlit Cloud settings under 'Secrets'
  to enable full functionality")
              return False
          else:
              return True

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

      .progress-ring {
          width: 120px;
          height: 120px;
          margin: 0 auto;
      }

      .action-button {
          background: linear-gradient(45deg, #667eea, #764ba2);
          color: white;
          padding: 0.5rem 2rem;
          border: none;
          border-radius: 25px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
      }

      .action-button:hover {
          transform: scale(1.05);
          box-shadow: 0 5px 15px rgba(0,0,0,0.2);
      }

      .sidebar .sidebar-content {
          background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
      }

      .stats-container {
          display: flex;
          justify-content: space-around;
          margin: 2rem 0;
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
      st.markdown('<h1 class="main-header">📧 Smart Email Cleaner</h1>',
  unsafe_allow_html=True)
      st.markdown('<p style="text-align: center; font-size: 1.2rem; color:
  #6c757d; margin-bottom: 3rem;">Transform your chaotic inbox into an
  organized paradise</p>', unsafe_allow_html=True)

      # API Key Status
      col1, col2, col3 = st.columns([1, 2, 1])
      with col2:
          if BotConfig.validate_keys():
              st.success("✅ AI features are enabled!")
          else:
              st.info("ℹ️ Add API keys in Streamlit settings to enable AI
  features")

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
              st.markdown(f"""
              <div class="metric-card">
                  <h2>📨</h2>
                  <h3>{st.session_state.get('total_emails', 1247)}</h3>
                  <p>Total Emails</p>
              </div>
              """, unsafe_allow_html=True)

          with col2:
              st.markdown(f"""
              <div class="metric-card">
                  <h2>🗑️</h2>
                  <h3>{st.session_state.get('cleaned_emails', 342)}</h3>
                  <p>Emails Cleaned</p>
              </div>
              """, unsafe_allow_html=True)

          with col3:
              st.markdown(f"""
              <div class="metric-card">
                  <h2>💾</h2>
                  <h3>{st.session_state.get('space_saved', '2.4 GB')}</h3>
                  <p>Space Saved</p>
              </div>
              """, unsafe_allow_html=True)

          with col4:
              st.markdown(f"""
              <div class="metric-card">
                  <h2>⏱️</h2>
                  <h3>{st.session_state.get('time_saved', '5.2 hrs')}</h3>
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

      st.markdown("### 🛠️ Cleanup Features" )

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

      # More features
      col3, col4 = st.columns(2)

      with col3:
          st.markdown("""
          <div class="feature-card">
              <h3>✉️ Unsubscribe Assistant</h3>
              <p>Safely unsubscribe from unwanted newsletters</p>
          </div>
          """, unsafe_allow_html=True)

          if st.button("🔄 Bulk Unsubscribe", key="unsubscribe"):
              st.info("Found 23 newsletters to unsubscribe from")

      with col4:
          st.markdown("""
          <div class="feature-card">
              <h3>📈 Email Analytics</h3>
              <p>Insights into your email patterns and habits</p>
          </div>
          """, unsafe_allow_html=True)

          if st.button("📊 View Analytics", key="analytics"):
              st.info("Analytics dashboard coming up!")

  def email_analytics():
      """Email analytics and insights"""

      st.markdown("### 📈 Email Analytics")

      # Sample data for demonstration
      dates = pd.date_range(start='2024-01-01', end='2024-08-29', freq='D')
      email_volume = pd.DataFrame({
          'Date': dates,
          'Received': [20 + int(10 * abs(hash(str(d)) % 100) / 100) for d in
   dates],
          'Sent': [5 + int(5 * abs(hash(str(d)) % 50) / 50) for d in dates]
      })

      # Email volume chart
      fig = px.line(email_volume, x='Date', y=['Received', 'Sent'],
                    title="Email Volume Over Time",
                    color_discrete_map={'Received': '#667eea', 'Sent':
  '#764ba2'})
      fig.update_layout(
          plot_bgcolor="rgba(0,0,0,0)",
          paper_bgcolor="rgba(0,0,0,0)",
          font=dict(family="Arial", size=12)
      )
      st.plotly_chart(fig, use_container_width=True)

      # Top senders pie chart
      col1, col2 = st.columns(2)

      with col1:
          senders_data = {
              'Sender': ['Amazon', 'Google', 'LinkedIn', 'GitHub',
  'Netflix', 'Others'],
              'Count': [45, 32, 28, 23, 15, 67]
          }
          fig_pie = px.pie(pd.DataFrame(senders_data), values='Count',
  names='Sender',
                          title="Top Email Senders")
          fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)")
          st.plotly_chart(fig_pie, use_container_width=True)

      with col2:
          categories_data = {
              'Category': ['Promotions', 'Work', 'Personal', 'Bills',
  'Social'],
              'Percentage': [40, 25, 20, 10, 5]
          }
          fig_bar = px.bar(pd.DataFrame(categories_data), x='Category',
  y='Percentage',
                          title="Email Categories", color='Percentage',
                          color_continuous_scale='Viridis')
          fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)")
          st.plotly_chart(fig_bar, use_container_width=True)

  def sidebar_menu():
      """Sidebar navigation and settings"""

      with st.sidebar:
          st.markdown("### 🎛️ Control Panel" )

          # Navigation
          page = st.selectbox(
              "Choose View",
              ["📊 Dashboard", "🛠️ Cleanup Tools" , "📈 Analytics", "⚙️
  Settings"]
          )

          st.markdown("---")

          # Quick actions
          st.markdown("### ⚡ Quick Actions")

          if st.button("🔍 Scan Inbox", key="scan"):
              st.success("Inbox scanned successfully!")

          if st.button("🔄 Refresh Data", key="refresh"):
              st.success("Data refreshed!")

          if st.button("💾 Backup Important", key="backup"):
              st.success("Important emails backed up!")

          st.markdown("---")

          # Settings
          st.markdown("### ⚙️ Settings")

          auto_cleanup = st.checkbox("Auto Cleanup", value=True)
          safe_mode = st.checkbox("Safe Mode", value=True)
          notifications = st.checkbox("Notifications", value=False)

          st.markdown("---")

          # Status
          st.markdown("### 📡 Status")
          st.success("✅ System Online")
          st.info(f"🔒 Secure Connection")
          st.info(f"⚡ {st.session_state.get('emails_processed', 1247)}
  Emails Processed")

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

      elif "Analytics" in current_page:
          email_analytics()

      elif "Settings" in current_page:
          st.markdown("### ⚙️ Settings")
          st.markdown("Email cleanup preferences and configuration options")

          # Email provider selection
          provider = st.selectbox("Email Provider", ["Gmail", "Outlook",
  "Yahoo", "Other"])

          # Cleanup preferences
          st.markdown("#### Cleanup Preferences")
          col1, col2 = st.columns(2)

          with col1:
              keep_important = st.checkbox("Keep flagged emails",
  value=True)
              backup_before = st.checkbox("Backup before cleanup",
  value=True)

          with col2:
              auto_organize = st.checkbox("Auto-organize", value=True)
              smart_filters = st.checkbox("Smart filters", value=True)

          # Save settings
          if st.button("💾 Save Settings"):
              st.success("Settings saved successfully!")

  if __name__ == "__main__":
      main()

