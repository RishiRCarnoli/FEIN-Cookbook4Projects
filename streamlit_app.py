import streamlit as st
import time
import json
import random
import pandas as pd
import plotly.express as px
import os

# --- 1. SET PAGE CONFIG (MUST BE FIRST STREAMLIT COMMAND) ---
st.set_page_config(layout="wide", page_title="NovaForge Projects", page_icon="✨")

# --- 2. GLOBAL STYLES & GRADIENT BACKGROUND ---
st.markdown("""
    <style>
    @import url('https://fonts.com/css2?family=Space+Grotesk:wght@400;700&family=Roboto:wght@300;400;700&display=swap');

    body {
        font-family: 'Roboto', sans-serif;
        color: #FFFFFF;
        background: linear-gradient(135deg, #0F121C 0%, #1A202C 100%);
        background-attachment: fixed;
    }

    .stApp {
        background: none;
    }

    /* Header & Branding */
    .st-emotion-cache-vk33gh {
        background: none !important;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif;
        color: #8CFFB5;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: rgba(26, 32, 44, 0.9);
        backdrop-filter: blur(8px);
        border-right: 1px solid rgba(140, 255, 181, 0.2);
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.3);
    }
    [data-testid="stSidebar"] .st-emotion-cache-1jm6gsa {
        color: #E0E0E0;
    }

    /* Main Content Area */
    .st-emotion-cache-z5fcl4 {
        padding-top: 3rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 3rem;
    }

    /* Project Cards */
    .project-card {
        background-color: rgba(36, 41, 51, 0.8);
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(140, 255, 181, 0.3);
        transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .project-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.5);
    }
    .project-title {
        font-size: 1.5em;
        color: #8CFFB5;
        margin-bottom: 12px;
        text-shadow: 0px 0px 5px rgba(140, 255, 181, 0.3);
    }
    .project-description {
        font-size: 1.0em;
        color: #D3D3D3;
        margin-bottom: 18px;
        flex-grow: 1;
        line-height: 1.6;
    }
    .project-details {
        font-size: 0.85em;
        color: #A9A9A9;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    .project-details span {
        background-color: #333A4A;
        border-radius: 6px;
        padding: 4px 10px;
        margin-right: 6px;
        margin-bottom: 6px;
        display: inline-block;
        font-weight: 500;
        color: #BBBBBB;
    }
    .card-buttons {
        display: flex;
        gap: 10px;
        margin-top: 20px;
        flex-wrap: wrap;
        justify-content: flex-end;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: background-color 0.3s ease, transform 0.2s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
    }

    .stButton[data-testid="base-button-secondary"] > button {
        background-color: #4CAF50;
        color: white;
        border: none;
    }
    .stButton[data-testid="base-button-secondary"] > button:hover {
        background-color: #45a049;
    }
    .stLinkButton > button {
        background-color: #556B8D;
        color: white;
        border: none;
    }
    .stLinkButton > button:hover {
        background-color: #4A5C7A;
    }
    .stButton[data-testid="base-button-primary"] > button {
        background-color: #8CFFB5;
        color: #0F121C;
        border: none;
        box-shadow: 0 4px 8px rgba(140, 255, 181, 0.4);
    }
    .stButton[data-testid="base-button-primary"] > button:hover {
        background-color: #72E09B;
        box_shadow: 0 6px 12px rgba(140, 255, 181, 0.6);
    }

    /* Text Inputs & Selectboxes */
    .stTextInput>div>div>input, .stMultiSelect>div>div>div>div, .stSelectbox>div>div>div {
        background-color: #1A202C;
        border: 1px solid #333A4A;
        border-radius: 8px;
        color: #E0E0E0;
        padding: 10px;
    }
    .stTextInput>div>div>input:focus, .stMultiSelect>div>div>div>div:focus, .stSelectbox>div>div>div:focus {
        border-color: #8CFFB5;
        box-shadow: 0 0 0 0.1rem rgba(140, 255, 181, 0.25);
    }

    /* Expander */
    .stExpander {
        border: 1px solid #333A4A;
        border-radius: 8px;
        background-color: rgba(26, 32, 44, 0.6);
    }
    .stExpander span p {
        color: #8CFFB5;
        font-weight: bold;
    }

    /* Testimonials */
    .testimonial-card {
        background-color: rgba(36, 41, 51, 0.8);
        border-left: 5px solid #8CFFB5;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        font-style: italic;
        color: #E0E0E0;
    }
    .testimonial-author {
        font-weight: bold;
        color: #8CFFB5;
        margin-top: 10px;
        font-style: normal;
    }
    </style>
""", unsafe_allow_html=True)


# --- Lottie animations and associated functions removed ---

# --- 4. PROJECT DATABASE (Loaded from JSON) ---
PROJECT_DB = {}
try:
    with open("projects_data.json", "r") as f:
        json_data = json.load(f)
    
    for entry in json_data:
        domain = entry.get("domain")
        projects = entry.get("projects", [])
        if domain:
            PROJECT_DB[domain] = projects

except FileNotFoundError:
    st.error("projects_data.json not found. Please create the file with your project data.")
except json.JSONDecodeError:
    st.error("Error decoding projects_data.json. Please check if the JSON is correctly formatted.")
except Exception as e:
    st.error(f"An unexpected error occurred while loading project data: {e}")

if not PROJECT_DB:
    st.warning("PROJECT_DB is empty. Please add projects to your projects_data.json file.")

# --- 5. Utility Functions ---
def search_text_match(project, search_text):
    if not search_text:
        return True
    search_text_lower = search_text.lower()
    return (
        search_text_lower in project['title'].lower() or
        search_text_lower in project['description'].lower() or
        any(search_text_lower in tech.lower() for tech in project['tech']) or
        any(search_text_lower in kw.lower() for kw in project.get('keywords', []))
    )

# --- GLOBAL VISIT COUNTER FUNCTIONS (File-based) ---
GLOBAL_VISIT_COUNT_FILE = "global_visits.txt"

def get_global_visit_count():
    if not os.path.exists(GLOBAL_VISIT_COUNT_FILE):
        return 0
    try:
        with open(GLOBAL_VISIT_COUNT_FILE, "r") as f:
            count = int(f.read().strip())
            return count
    except (ValueError, FileNotFoundError):
        return 0

def increment_global_visit_count():
    current_count = get_global_visit_count()
    new_count = current_count + 1
    try:
        with open(GLOBAL_VISIT_COUNT_FILE, "w") as f:
            f.write(str(new_count))
        return new_count
    except Exception as e:
        st.error(f"Could not update global visit count: {e}")
        return current_count

# --- 6. Session State Initialization ---
if 'selected_project_for_ai' not in st.session_state:
    st.session_state['selected_project_for_ai'] = None
if 'search_triggered' not in st.session_state:
    st.session_state['search_triggered'] = False
# Initialize search filters in session state to maintain state across page changes
if 'last_topic' not in st.session_state:
    st.session_state['last_topic'] = ''
if 'last_difficulty_range' not in st.session_state:
    st.session_state['last_difficulty_range'] = (1, 4)
if 'last_tech_filter' not in st.session_state:
    st.session_state['last_tech_filter'] = []
if 'last_dataset_filter' not in st.session_state:
    st.session_state['last_dataset_filter'] = ''
if 'last_keywords_filter' not in st.session_state:
    st.session_state['last_keywords_filter'] = ''

# --- PER-SESSION VISIT COUNTER INITIALIZATION & INCREMENT ---
if 'page_visits_this_session' not in st.session_state:
    st.session_state.page_visits_this_session = 0
st.session_state.page_visits_this_session += 1

# --- PROJECT DISPLAY LIMIT INITIALIZATION ---
if 'project_display_limit' not in st.session_state:
    st.session_state.project_display_limit = 10 # Start by showing 10 projects


# --- Testimonials Data ---
TESTIMONIALS = [
    {"quote": "Idk he just told to drop a review here, The AI prompt generator is a game-changer, helped me through typing arbitrage", "author": "Tanusha Aggarwal, CSE Core Student"},
    {"quote": "As a student, finding relevant projects was tough. This platform provides exactly what I need, tailored to my interests. The UI is minimal, ty Ojas.", "author": "Rohan Bharadwaj, CSE Student"},
    {"quote": "Thanks a lot cause clutched the project reviews last minute, hope profs don't find about this or am cooked 🤍", "author": "Anya Sharma, CSE with Bioinformatics"},
    {"quote": "I love the clean design and minimal functionality, would be better if you add github repo links too 🙏🏼", "author": "Devika Singh, CSE Core Student"},
    {"quote": "Bro isn't this your 13th app or something, 🤓 Rishi ftw fr", "author": "Shreya, CSE Core Student"}
]




def animated_search(): 
    with st.sidebar:
        # App Name & Branding
        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
                <h2 style="color: #8CFFB5; font-family: 'Space Grotesk', sans-serif; font-size: 2.2em;">NovaForge Projects</h2>
            </div>
            <p style="font-size: 0.8em; color: #BBBBBB; margin-top: -15px;">
                <span style="font-weight: bold; color: #8CFFB5;">Empowering Innovation.</span>
            </p>
            <p style="font-size: 0.7em; color: #888888; text-align: right; margin-top: 20px;">
                Made by <span style="color:#8CFFB5; font-weight:bold;">Ojas Singh</span><br>
                21BDS0187, VIT Vellore
            </p>
            <hr style="border-top: 1px dashed rgba(140, 255, 181, 0.3); margin: 20px 0;">
        """, unsafe_allow_html=True)

        # --- Display Visit Counters in Sidebar ---
        st.sidebar.info(f"🌐 Page visits (this session): **{st.session_state.page_visits_this_session}**")
        st.sidebar.success(f"📈 Total global visits: **{st.session_state.global_total_visits}**")
        st.divider()
        # --- End Visit Counters ---

        # This button is specific to being on the AI prompt generator view
        if st.session_state.get('selected_project_for_ai') is not None:
            if st.button("⬅️ Back to Projects", key="back_to_projects_btn", use_container_width=True):
                st.session_state['selected_project_for_ai'] = None
                st.session_state['search_triggered'] = False # Reset search trigger when going back
                st.session_state['project_display_limit'] = 10 # Reset limit to initial for fresh view
                st.rerun()
            st.divider()

        # Search & Filter UI
        topic_value = st.session_state['last_topic']
        difficulty_range_value = st.session_state['last_difficulty_range']
        tech_filter_value = st.session_state['last_tech_filter']
        dataset_filter_value = st.session_state['last_dataset_filter']
        keywords_filter_value = st.session_state['last_keywords_filter']

        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
                <h3 style="color: #E0E0E0; font-family: 'Space Grotesk', sans-serif;">Search & Filter</h3>
            </div>
        """, unsafe_allow_html=True)

        topic_value = st.text_input("🔍 Search Project Topics/Keywords:", topic_value, placeholder="e.g., Deep Learning, NLP, Robotics, chatbot, security")

        st.subheader("⚙️ Difficulty Level")
        difficulty_mapping = {1: "Beginner", 2: "Intermediate", 3: "Advanced", 4: "Expert"}
        min_diff_numeric, max_diff_numeric = st.slider(
            "Select numerical range:",
            1, 4, difficulty_range_value,
            format="%d",
            key="difficulty_slider"
        )
        difficulty_range_value = (min_diff_numeric, max_diff_numeric)

        st.markdown(f"""
            <p style="font-size:0.9rem; color:#BBBBBB; margin-top:-15px;">
                Current selection: <strong>{difficulty_mapping[min_diff_numeric]}</strong> to <strong>{difficulty_mapping[max_diff_numeric]}</strong>
            </p>
        """, unsafe_allow_html=True)

        with st.expander("🔬 Advanced Filters"):
            all_tech_options = sorted(list(set(tech for domain_projects in PROJECT_DB.values() for project in domain_projects for tech in project['tech'])))
            tech_filter_value = st.multiselect("Tech Stack Contains:", options=all_tech_options, default=tech_filter_value, key="tech_filter")
            dataset_filter_value = st.text_input("Dataset Keywords:", dataset_filter_value, placeholder="e.g., medical, finance, image", key="dataset_keyword")
            keywords_filter_value = st.text_input("Project Keywords:", keywords_filter_value, placeholder="e.g., real-time, generative, blockchain", key="project_keywords")

        if st.button("🚀 Launch Search", type="primary", use_container_width=True):
            st.session_state['search_triggered'] = True
            st.session_state['project_display_limit'] = 10 # Reset limit for new search results
            st.balloons()
            st.rerun() # Rerun to apply filters and reset limit immediately
        st.divider()

        # Update session state with current filter values
        st.session_state['last_topic'] = topic_value
        st.session_state['last_difficulty_range'] = difficulty_range_value
        st.session_state['last_tech_filter'] = tech_filter_value
        st.session_state['last_dataset_filter'] = dataset_filter_value
        st.session_state['last_keywords_filter'] = keywords_filter_value
        
        return topic_value, difficulty_range_value, tech_filter_value, dataset_filter_value, keywords_filter_value


def display_project_cards(projects_to_render):
    # Always display the main heading and introductory text
    st.markdown("<h2 style='color:#8CFFB5;'>✨ Explore Projects</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#BBBBBB; font-size:1.1em;'>Discover innovative Computer Science projects across diverse domains.</p>", unsafe_allow_html=True)

    if st.session_state.get('search_triggered', False):
        st.markdown("<h3 style='color:#8CFFB5;'>Matching Projects</h3>", unsafe_allow_html=True)
        if not projects_to_render:
            st.info("No projects match your current criteria. Please adjust your filters or broaden your search!")
    elif not projects_to_render:
        st.info("No projects available. Please add projects to your projects_data.json file.") # Fallback for empty DB

    if projects_to_render: # Only proceed to display cards if there are projects
        cols_per_row = 2
        for i in range(0, len(projects_to_render), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < len(projects_to_render):
                    project, domain = projects_to_render[i + j]
                    with cols[j]:
                        with st.container(border=False):
                            st.markdown(f'<div class="project-card">', unsafe_allow_html=True)
                            
                            st.markdown(f'<p class="project-title">{project["title"]}</p>', unsafe_allow_html=True)
                            st.markdown(f'<p class="project-description">{project["description"]}</p>', unsafe_allow_html=True)

                            st.markdown('<div class="project-details">', unsafe_allow_html=True)
                            st.markdown(f'<span>🌐 {domain}</span> <span>🧠 {project["difficulty"]}</span>', unsafe_allow_html=True)
                            if project['tech']:
                                st.markdown(f'<span>🛠️ {", ".join(project["tech"])}</span>', unsafe_allow_html=True)
                            if project['datasets']:
                                st.markdown(f'<span>📊 {", ".join(project["datasets"])}</span>', unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)

                            st.markdown('<div class="card-buttons">', unsafe_allow_html=True)
                            if project.get('github_url'):
                                st.link_button("View on GitHub", project['github_url'], help="Open GitHub repository in a new tab", type="secondary", use_container_width=False)
                            
                            if st.button("✨ Generate AI Prompt", key=f"ai_prompt_{project['title']}_{i+j}", use_container_width=False, type="primary"):
                                st.session_state['selected_project_for_ai'] = project
                                st.rerun()
                            st.markdown('</div>', unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    display_testimonials()


def display_testimonials():
    st.markdown("<h2 style='color:#8CFFB5; text-align:center;'>What Our Users Say</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#BBBBBB; text-align:center; margin-bottom: 30px;'>Hear from students, researchers, and professionals who love NovaForge Projects.</p>", unsafe_allow_html=True)

    cols = st.columns(len(TESTIMONIALS))
    for idx, testimonial in enumerate(TESTIMONIALS):
        with cols[idx]:
            st.markdown(f"""
                <div class="testimonial-card">
                    <p>"{testimonial['quote']}"</p>
                    <p class="testimonial-author">- {testimonial['author']}</p>
                </div>
            """, unsafe_allow_html=True)


def generate_ai_prompt_page(project):
    st.title(f"Generate AI Prompt for: {project['title']}")
    st.markdown(f"""
        <p style="font-size: 1.1em; color: #E0E0E0;">
            Use the power of AI to kickstart your project! Select an AI model below to generate a tailored prompt.
        </p>
    """, unsafe_allow_html=True)

    st.markdown(f"**Project Description:** {project['description']}")
    st.markdown(f"**Key Technologies:** {', '.join(project['tech'])}")
    st.markdown(f"**Difficulty:** {project['difficulty']}")

    st.subheader("Choose an AI Model:")
    ai_model = st.selectbox(
        "Select an AI model to generate the prompt:",
        options=["Gemini (Google)", "ChatGPT (OpenAI)", "Llama 3 (Meta)"],
        key="ai_model_select"
    )

    generated_prompt = ""
    model_link = ""

    if ai_model == "Gemini (Google)":
        generated_prompt = f"""
        **Role:** You are an expert Computer Science Project Mentor and a leading AI Engineer specializing in practical project implementation and effective planning.

        **Task:** Generate a highly detailed and actionable project plan for the following project. Your response should serve as a step-by-step guide for a developer to initiate and complete this project successfully.

        **Project Details:**
        * **Project Title:** "{project['title']}"
        * **Project Description:** "{project['description']}"
        * **Key Technologies:** {', '.join(project['tech'])}
        * **Difficulty Level:** {project['difficulty']}

        **Expected Output Structure and Content:**

        **1. Comprehensive Project Breakdown (Phases & Modules):**
        * **Phase 1: Planning & Setup:**
            * Detailed steps for environment setup, dependency installation, and initial project structure.
            * Specific considerations for the chosen technologies (e.g., cloud account setup for paid services, virtual environments for Python).
        * **Phase 2: Core Development - Module 1 (e.g., Data Ingestion/Frontend):**
            * Break down into granular tasks (e.g., "Design API endpoints," "Implement data parsing logic," "Build user authentication").
            * Mention specific libraries or components relevant to each task.
        * **Phase 3: Core Development - Module 2 (e.g., Model Training/Backend Logic):**
            * Similarly, list granular tasks and technology-specific implementation details.
        * **Phase 4: Integration & Testing:**
            * Steps for integrating different modules.
            * Strategies for unit, integration, and system testing.
            * Recommended testing frameworks/tools if applicable.
        * **Phase 5: Deployment & Monitoring:**
            * Detailed steps for deploying the project (e.g., "Containerize application with Docker," "Deploy to AWS Lambda/Azure App Service," "Set up monitoring dashboards").
            * Post-deployment considerations.

        **2. Key Technical Challenges & Solutions:**
        * For each major challenge identified, suggest 2-3 concrete approaches or solutions.
        * Example: "Challenge: Handling real-time data streams. Solution: Use Apache Kafka for message queuing."

        **3. Required Skill Set Enhancement:**
        * Beyond the listed technologies, specify complementary skills that would be highly beneficial (e.g., "Strong understanding of distributed systems," "Proficiency in SQL query optimization").

        **4. Curated Learning Resources (3-5 specific suggestions):**
        * **Online Courses:** Name 1-2 reputable courses (e.g., Coursera, Udemy, edX) relevant to core technologies or concepts.
        * **Documentation/Official Guides:** Mention crucial official documentation (e.g., TensorFlow docs, AWS Boto3 docs).
        * **Research Papers/Blogs:** Suggest types of academic papers or industry blogs for deeper insights.
        * **Open-Source Projects:** Point to similar open-source projects for inspiration or learning patterns.

        **5. Measurable Mini-Milestones (5-7 initial, achievable steps):**
        * "Week 1: Set up project repository, install dependencies, and create a 'Hello World' endpoint."
        * "Week 2: Implement basic data ingestion and storage for a small dataset."
        * Ensure these are concrete and provide a sense of early progress.

        **6. Project Success Metrics & Evaluation:**
        * Define 2-3 quantitative and qualitative metrics for evaluating the project's success (e.g., "Model accuracy > 90%", "Latency < 200ms," "User satisfaction via surveys").

        **Call to Action:** Generate the detailed project plan based on the above instructions.
        """
        model_link = "https://gemini.google.com/"
    elif ai_model == "ChatGPT (OpenAI)":
        generated_prompt = f"""
        **Role:** You are an experienced Software Architect and Project Manager. Your task is to provide a comprehensive architectural outline and strategic plan for the given project, suitable for a team of developers.

        **Task:** Based on the project details below, deliver a structured response covering scope, architecture, features, testing, and future work.

        **Project Details:**
        * **Project Title:** "{project['title']}"
        * **Project Overview:** "{project['description']}"
        * **Technical Stack:** {', '.join(project['tech'])}
        * **Target Difficulty:** {project['difficulty']}

        **Expected Output Structure and Content:**

        **1. Detailed Project Scope & Objectives:**
        * **Primary Objectives:** Clearly state 2-3 main goals of the project.
        * **Key Deliverables:** List specific outputs or artifacts expected from the project (e.g., "Functional web application," "Deployed machine learning API," "Comprehensive test suite").
        * **Non-Goals:** Briefly mention what the project will *not* cover to manage expectations.

        **2. High-Level Architectural Design:**
        * **Components:** Identify the major logical components of the system (e.g., "Frontend UI," "Backend API Service," "Database Layer," "Message Queue," "ML Model Service").
        * **Data Flow Diagram (Conceptual):** Describe the flow of data between these components (e.g., "User interaction -> Frontend -> API Gateway -> Backend Service -> Database").
        * **Architectural Style (if applicable):** Suggest suitable architectural patterns (e.g., Microservices, Monolithic, Serverless, Event-Driven).
        * **Technology Mapping:** Briefly explain which core technologies from the stack map to which architectural components.

        **3. Prioritized Feature List:**
        * **Must-Have (MVP):** 3-5 essential features for a minimum viable product.
        * **Should-Have:** 2-3 important features for a subsequent release.
        * **Nice-to-Have:** 1-2 potential future enhancements.
        * For each feature, briefly describe its purpose.

        **4. Testing Strategies & Quality Assurance:**
        * **Unit Testing:** Describe how unit tests would be structured (e.g., "Per-module/function testing").
        * **Integration Testing:** Outline integration points to test (e.g., "API endpoint testing," "database connectivity").
        * **End-to-End Testing:** Suggest E2E scenarios.
        * **Performance/Load Testing (if applicable):** Briefly mention considerations for high-traffic systems.
        * **Security Testing:** Highlight critical security considerations (e.g., "Input validation," "Authentication/Authorization testing").

        **5. Potential Extensions & Future Work:**
        * Brainstorm 3-5 ideas for evolving the project beyond its initial scope (e.g., "Adding a mobile application," "Integrating advanced analytics," "Multi-language support").

        **Call to Action:** Provide a detailed architectural and strategic project plan using the requested structure.
        """
        model_link = "https://chat.openai.com/"
    elif ai_model == "Llama 3 (Meta)":
        generated_prompt = f"""
        **Role:** You are an Open-Source Advocate and a practical Lead Developer focused on building robust, community-friendly projects.

        **Task:** Provide guidance for a project with the aim of fostering open-source best practices, accelerating development with existing tools, and outlining a clear learning path.

        **Project Details:**
        * **Project Title:** "{project['title']}"
        * **Project Core:** "{project['description']}"
        * **Technologies Involved:** {', '.join(project['tech'])}
        * **Complexity Level:** {project['difficulty']}

        **Expected Output Structure and Content:**

        **1. Core Functionalities (Detailed):**
        * List 5-7 fundamental features that define the project's primary purpose.
        * For each functionality, provide a brief technical explanation of how it would be achieved using the specified technologies.

        **2. Strategic Open-Source Tool & Library Recommendations:**
        * For each major component or task (e.g., "Data processing," "UI Framework," "Deployment," "Database management"), recommend 2-3 specific open-source tools or libraries from the project's tech stack or complementary ones.
        * Briefly explain *why* each tool is a good fit for this project and how it accelerates development.

        **3. Open-Source Community Best Practices:**
        * **Documentation:** What essential documentation should be created (e.g., "README.md," "CONTRIBUTING.md," "API docs," "User Guide")?
        * **Contribution Guidelines:** What process should be established for external contributions (e.g., "Issue tracking," "Pull Request review process," "Code of Conduct")?
        * **Version Control:** Emphasize Git best practices (e.g., branching strategy, commit message conventions).
        * **Licensing:** Suggest a suitable open-source license and explain why.

        **4. Straightforward Deployment Options:**
        * Propose 2-3 accessible deployment strategies, particularly for an open-source context (e.g., "Docker containers on a VPS," "Heroku/Netlify for web apps," "GitHub Pages for static sites").
        * Briefly outline the steps for each option.

        **5. Practical Learning Path for Technologies:**
        * For each core technology listed in the project, suggest a "learn-by-doing" approach.
        * Recommend specific mini-projects or tutorials that would help a developer quickly gain proficiency relevant to this project (e.g., "Build a simple REST API with Flask," "Implement a basic CNN for image classification").
        * Suggest how to leverage official documentation and community forums effectively.

        **Call to Action:** Generate the detailed guidance for this open-source-focused project.
        """
        model_link = "https://llama.meta.com/"
    
    st.subheader("Generated AI Prompt:")
    st.code(generated_prompt, language="markdown")

    st.subheader("Next Steps:")
    st.write("1. **Copy the generated prompt above.**")
    st.write(f"2. **Click the button below to go to the __{ai_model}__ website.**")
    st.write(f"3. **Paste the prompt into the AI model and start generating your detailed project ideas and plans!**")
    
    if st.link_button(f"Go to {ai_model}", model_link, type="primary"):
        pass

# --- 8. Final Main App Execution Block ---

# --- GLOBAL VISIT COUNTER INCREMENT ---
st.session_state.global_total_visits = increment_global_visit_count()

# Call animated_search at the top of the main execution block to ensure sidebar is always rendered
topic, difficulty_range, tech_filter, dataset_filter, keywords_filter = animated_search()

# Determine which page to display based on selected_project_for_ai
if st.session_state.get('selected_project_for_ai'):
    # If a project is selected for AI prompt, show the AI page
    generate_ai_prompt_page(st.session_state['selected_project_for_ai'])
else:
    # Otherwise, show the project explorer
    
    all_projects_flat = []
    for domain, projects_list in PROJECT_DB.items():
        for project in projects_list:
            all_projects_flat.append((project, domain))

    projects_to_consider = []

    if st.session_state.get('search_triggered', False):
        # Filter projects based on current session state filters
        min_diff_val, max_diff_val = st.session_state.last_difficulty_range
        difficulty_levels_map = {"Beginner": 1, "Intermediate": 2, "Advanced": 3, "Expert": 4}
        
        for domain, projects in PROJECT_DB.items():
            for project in projects:
                project_difficulty_numeric = difficulty_levels_map.get(project['difficulty'], 0)
                
                if not (min_diff_val <= project_difficulty_numeric <= max_diff_val): continue
                if st.session_state.last_topic and not search_text_match(project, st.session_state.last_topic): continue
                if st.session_state.last_tech_filter and not any(t in project['tech'] for t in st.session_state.last_tech_filter): continue
                if st.session_state.last_dataset_filter and not any(st.session_state.last_dataset_filter.lower() in ds.lower() for ds in project['datasets']): continue
                if st.session_state.last_keywords_filter and not any(st.session_state.last_keywords_filter.lower() in kw.lower() for kw in project.get('keywords', [])): continue
                
                projects_to_consider.append((project, domain))
        
    else:
        # Initial load or no search triggered, display random projects
        if 'initial_shuffled_projects' not in st.session_state:
            random.shuffle(all_projects_flat)
            st.session_state.initial_shuffled_projects = all_projects_flat
        
        projects_to_consider = st.session_state.initial_shuffled_projects


    # Display the projects up to the current limit
    display_project_cards(projects_to_consider[:st.session_state.project_display_limit])

    # --- "Load More" Button Logic ---
    if st.session_state.project_display_limit < len(projects_to_consider):
        # Calculate how many more can be loaded in the next click
        load_increment = 10 # Number of projects to load with each click
        remaining_projects = len(projects_to_consider) - st.session_state.project_display_limit
        
        # Adjust button text to show how many will be loaded next
        button_text = f"Load {min(load_increment, remaining_projects)} More Projects"
        
        if st.button(button_text, key="load_more_projects", use_container_width=True, type="secondary"):
            st.session_state.project_display_limit += load_increment
            st.rerun() # Rerun the app to display more projects
    elif len(projects_to_consider) > 0: # Only show this if there are projects to display
        st.success("All projects loaded!")
