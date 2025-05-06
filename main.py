import streamlit as st
import requests
import json
from datetime import datetime

class CareerCoachApp:
    def __init__(self):
        self.setup_page_config()
        self.initialize_session_state()
        self.create_sidebar()
        self.render_selected_tab()
        
    def setup_page_config(self):
        """Configure the Streamlit page settings"""
        st.set_page_config(
            page_title="AI Career Coach",
            page_icon="🧠",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        self.apply_custom_css()
    
    def apply_custom_css(self):
        """Apply custom CSS to improve the app's appearance"""
        st.markdown("""
        <style>
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: #808080;
            border-radius: 4px 4px 0 0;
            padding-left: 20px;
            padding-right: 20px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #808080;
            color: white;
        }
        h1, h2, h3 {
            color: #4c6ef5;
        }
        .results-box {
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            padding: 15px;
            background-color: #808080;
            height: 300px;
            overflow-y: auto;
        }
        .chat-message {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            display: flex;
        }
        .chat-message.user {
            background-color: #e6f3ff;
        }
        .chat-message.assistant {
            background-color: #808080;
        }
        .chat-message .message-content {
            display: flex;
            flex-direction: column;
            margin-left: 10px;
        }
        .chat-message .avatar {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            object-fit: cover;
            background-color: #4c6ef5;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 18px;
            font-weight: bold;
            color: white;
        }
        .chat-message .user-avatar {
            background-color: #2e7d32;
        }
        .suggestion-button {
            background-color: #808080;
            color: #0066cc;
            border: none;
            border-radius: 15px;
            padding: 5px 10px;
            cursor: pointer;
            margin-right: 5px;
            margin-bottom: 5px;
            font-size: 0.8em;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        if 'career_results' not in st.session_state:
            st.session_state.career_results = ""
            
        if 'skills_results' not in st.session_state:
            st.session_state.skills_results = ""
            
        if 'subject_results' not in st.session_state:
            st.session_state.subject_results = ""
    
    def create_sidebar(self):
        """Create the sidebar with app information"""
        with st.sidebar:
            st.title("AI Career Coach")
            st.markdown("---")
            st.markdown("""
            ## About
            This AI-powered tool helps students:
            - Discover suitable career paths
            - Analyze required skills
            - Get advice on subjects to study
            - Chat with an AI career coach
            
            """)
            st.markdown("---")
            
            if st.button("Reset All Data", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state.career_results = ""
                st.session_state.skills_results = ""
                st.session_state.subject_results = ""
                st.experimental_rerun()
    
    def render_selected_tab(self):
        """Render the main content of the app with tabs"""
        st.title("🧠 AI Career Coach for Students")
        
        tabs = st.tabs([
            "🔍 Career Discovery", 
            "🛠️ Skills Analysis", 
            "📚 Subject Advice", 
            "💬 AI Coach Chat"
        ])
        
        with tabs[0]:
            self.render_career_discovery_tab()
        
        with tabs[1]:
            self.render_skills_analysis_tab()
            
        with tabs[2]:
            self.render_subject_advice_tab()
            
        with tabs[3]:
            self.render_chat_tab()
    
    def render_career_discovery_tab(self):
        """Render the Career Discovery tab content"""
        st.header("Discover Careers Based on Your Profile")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.subheader("Tell us about yourself")
            
            interests = st.text_area(
                "What subjects do you enjoy?",
                placeholder="Examples: Math, Science, Art, Writing, History",
                height=100
            )
            
            skills = st.text_area(
                "What are your strengths or skills?",
                placeholder="Examples: Problem solving, creativity, public speaking, coding",
                height=100
            )
            
            personality = st.text_area(
                "What are your personality traits?",
                placeholder="Examples: Outgoing, analytical, detail-oriented, creative",
                height=100
            )
            
            col1_1, col1_2, col1_3 = st.columns([1, 1, 1])
            with col1_2:
                discover_button = st.button("🔍 Discover Career Paths", use_container_width=True)
            
            if discover_button:
                if not interests and not skills and not personality:
                    st.error("Please enter at least some information about your interests, skills, or personality.")
                else:
                    with st.spinner("Analyzing your profile and finding career matches..."):
                        self._discover_careers(interests, skills, personality)
        
        with col2:
            st.subheader("Career Recommendations")
            
            if st.session_state.career_results:
                st.markdown(f"""
                <div class="results-box">
                    {st.session_state.career_results}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Complete your profile and click 'Discover Career Paths' to see recommendations.")
            
            if st.button("🔄 Start Over", key="career_start_over"):
                st.session_state.career_results = ""
                st.experimental_rerun()
    
    def _discover_careers(self, interests, skills, personality):
        """Process career discovery request"""
        prompt = f"Based on the following information, suggest career paths that match this student's profile. Please provide 3-5 career options with a brief description of each, required skills, and suggested subjects to study:\n\nInterests: {interests}\nSkills: {skills}\nPersonality traits: {personality}"
        
        response = self.query_ai(prompt)
        st.session_state.career_results = response
    
    def render_skills_analysis_tab(self):
        """Render the Skills Analysis tab content"""
        st.header("Analyze Skills Needed for Future Careers")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.subheader("Select Career Field")
            
            career_field = st.text_input(
                "Enter a career field you're interested in:",
                placeholder="Examples: Software Engineering, Medicine, Business, Art"
            )
            
            st.write("**Quick select:**")
            
            # Create buttons for quick selection in 2 rows
            quick_cols1 = st.columns(3)
            quick_cols2 = st.columns(3)
            
            common_fields = [
                "Software Engineering", "Healthcare", "Business", 
                "Education", "Design", "Engineering"
            ]
            
            for i, field in enumerate(common_fields[:3]):
                if quick_cols1[i].button(field, key=f"quick_{field}", use_container_width=True):
                    career_field = field
                    
            for i, field in enumerate(common_fields[3:]):
                if quick_cols2[i].button(field, key=f"quick_{field}", use_container_width=True):
                    career_field = field
            
            # Analyze button
            analyze_col1, analyze_col2, analyze_col3 = st.columns([1, 1, 1])
            with analyze_col2:
                analyze_button = st.button("🔍 Analyze Required Skills", use_container_width=True)
            
            if analyze_button:
                if not career_field:
                    st.error("Please enter a career field to analyze.")
                else:
                    with st.spinner(f"Analyzing skills needed for {career_field}..."):
                        self._analyze_skills(career_field)
        
        with col2:
            st.subheader("Skills Analysis")
            
            if st.session_state.skills_results:
                st.markdown(f"""
                <div class="results-box">
                    {st.session_state.skills_results}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Select a career field and click 'Analyze Required Skills' to see results.")
            
            if st.button("🔄 Start Over", key="skills_start_over"):
                st.session_state.skills_results = ""
                st.experimental_rerun()
    
    def _analyze_skills(self, career_field):
        """Process skills analysis request"""
        prompt = f"For someone interested in a career in {career_field}, provide a detailed analysis of:\n1. Essential skills needed to succeed\n2. Technical skills and knowledge requirements\n3. Soft skills that are valuable\n4. How to develop these skills during high school and college\n5. Future trends in skill requirements for this field"
        
        response = self.query_ai(prompt)
        st.session_state.skills_results = response
    
    def render_subject_advice_tab(self):
        """Render the Subject Advice tab content"""
        st.header("Get Advice on Subjects to Study")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.subheader("Your Educational Profile")
            
            goals = st.text_area(
                "What are your career goals or interests?",
                placeholder="Examples: Becoming a doctor, working in tech, starting a business",
                height=100
            )
            
            current_subjects = st.text_area(
                "What subjects are you currently studying?",
                placeholder="Examples: Math, Biology, History, Computer Science",
                height=100
            )
            
            education_level = st.selectbox(
                "Your current education level:",
                ["Middle School", "High School", "College", "Graduate School", "Other"],
                index=1  # Default to High School
            )
            
            advice_col1, advice_col2, advice_col3 = st.columns([1, 1, 1])
            with advice_col2:
                advice_button = st.button("📚 Get Subject Advice", use_container_width=True)
            
            if advice_button:
                if not goals:
                    st.error("Please enter your career goals or interests.")
                else:
                    with st.spinner("Getting personalized subject recommendations..."):
                        self._get_subject_advice(goals, current_subjects, education_level)
        
        with col2:
            st.subheader("Subject Recommendations")
            
            if st.session_state.subject_results:
                st.markdown(f"""
                <div class="results-box">
                    {st.session_state.subject_results}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Complete your educational profile and click 'Get Subject Advice' to see recommendations.")
            
            if st.button("🔄 Start Over", key="subject_start_over"):
                st.session_state.subject_results = ""
                st.experimental_rerun()
    
    def _get_subject_advice(self, goals, current_subjects, education_level):
        """Process subject advice request"""
        prompt = f"Based on a student's career goals in {goals}, current education level ({education_level})"
        
        if current_subjects:
            prompt += f", and current subjects ({current_subjects}), recommend:"
        else:
            prompt += ", recommend:"
            
        prompt += f"""
1. Which subjects they should focus on in {education_level.lower()}
2. Additional subjects they should consider taking
3. Extracurricular activities that would benefit their career path
4. Any specialized courses or certifications to consider
5. How these subjects connect to their career goals
"""
        
        response = self.query_ai(prompt)
        st.session_state.subject_results = response
    
    def render_chat_tab(self):
        """Render the AI Coach Chat tab content"""
        st.header("Chat with AI Career Coach")
        
        if len(st.session_state.chat_history) == 0:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "Hello! I'm your AI Career Coach. How can I help you today? You can ask me about career paths, required skills, subject choices, or future job trends."
            })
        
        chat_container = st.container()
        
        st.write("**Try asking:**")
        
        suggestions = [
            "What careers match my interests?",
            "How do I prepare for tech jobs?",
            "Which subjects should I take?",
            "Tell me about future job trends",
            "Skills for data science"
        ]
        
        suggestion_html = '<div style="display: flex; flex-wrap: wrap; margin-bottom: 10px;">'
        for suggestion in suggestions:
            suggestion_html += f'<button class="suggestion-button" onclick="this.innerText=\'Clicking...\'; setTimeout(() => {{document.querySelector(\'input[aria-label=\'Message AI Career Coach\']\').value = \'{suggestion}\';document.querySelector(\'button[aria-label=\'Send message\']\').click();}}, 100)">{suggestion}</button>'
        suggestion_html += '</div>'
        
        st.markdown(suggestion_html, unsafe_allow_html=True)
        
        user_input = st.chat_input("Message AI Career Coach")
        
        with chat_container:
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    self.user_message(message["content"])
                else:
                    self.assistant_message(message["content"])
        
        if user_input:
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input
            })
            
            with chat_container:
                self.user_message(user_input)
            
            with st.spinner("AI Coach is thinking..."):
                assistant_response = self.query_ai(user_input, use_history=True)
            
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": assistant_response
            })
            
            with chat_container:
                self.assistant_message(assistant_response)
            
            if len(st.session_state.chat_history) > 12:
                st.session_state.chat_history = st.session_state.chat_history[-12:]
            
            st.experimental_rerun()
    
    def user_message(self, message):
        """Display a user message in the chat"""
        st.markdown(f'''
        <div class="chat-message user">
            <div class="avatar user-avatar">U</div>
            <div class="message-content">
                <span><strong>You</strong></span>
                <span>{message}</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    def assistant_message(self, message):
        """Display an assistant message in the chat"""
        st.markdown(f'''
        <div class="chat-message assistant">
            <div class="avatar">AI</div>
            <div class="message-content">
                <span><strong>AI Coach</strong></span>
                <span>{message}</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    def query_ai(self, command, use_history=False):
        
        url = "https://ai.hackclub.com/chat/completions"
        headers = {"Content-Type": "application/json"}
        
        system_message = {
            "role": "system", 
            "content": "You are a Career Coach that helps students discover careers based on their interests, skills, and personality traits. You also offer advice on subjects to study, skills to build, and future job trends. Provide concise, practical and specific guidance. Format your answers with clear headings and bullet points when appropriate. Don't include any asterics"
        }
        
        if use_history and len(st.session_state.chat_history) > 0:
            messages = [system_message]
            for message in st.session_state.chat_history[-6:]:
                messages.append(message)
            if messages[-1]["role"] != "user" or messages[-1]["content"] != command:
                messages.append({"role": "user", "content": command})
        else:
            messages = [
                system_message,
                {"role": "user", "content": command}
            ]
        
        data = {"messages": messages}

        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except requests.exceptions.Timeout:
            return "Sorry, the AI server took too long to respond. Please try again."
        except requests.exceptions.ConnectionError:
            return "Could not connect to the AI server. Please check your internet connection."
        except Exception as e:
            return f"An error occurred: {str(e)}"


if __name__ == "__main__":
    CareerCoachApp()