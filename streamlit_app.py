import streamlit as st
import random
import json
import os
import tempfile
import io
import pickle
import time

# Constants for session persistence
SESSION_FILE = "exam_session.pkl"

def save_session_state():
    """Save critical session state to file for persistence"""
    try:
        session_data = {
            'questions': st.session_state.get('questions', []),
            'current_question': st.session_state.get('current_question', 0),
            'score': st.session_state.get('score', 0),
            'answered': st.session_state.get('answered', False),
            'user_answers': st.session_state.get('user_answers', []),
            'exam_completed': st.session_state.get('exam_completed', False),
            'topics': st.session_state.get('topics', {}),
            'questions_loaded': st.session_state.get('questions_loaded', False),
            'last_uploaded_file_name': st.session_state.get('last_uploaded_file_name', None),
            'session_timestamp': time.time()
        }
        
        with open(SESSION_FILE, 'wb') as f:
            pickle.dump(session_data, f)
    except Exception as e:
        print(f"Warning: Could not save session: {e}")

def load_session_state():
    """Load session state from file if it exists and is recent"""
    try:
        if os.path.exists(SESSION_FILE):
            # Check if session file is recent (less than 24 hours old)
            file_age = time.time() - os.path.getmtime(SESSION_FILE)
            if file_age < 24 * 3600:  # 24 hours
                with open(SESSION_FILE, 'rb') as f:
                    session_data = pickle.load(f)
                return session_data
    except Exception as e:
        print(f"Warning: Could not load session: {e}")
    return None

def load_questions_from_json():
    """Load questions from JSON file with the programming_languages_exam_questions structure"""
    try:
        # Try to load from local file first
        if os.path.exists("programming_questions.json"):
            with open("programming_questions.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
                questions = extract_questions_from_data(data)
                if questions:
                    st.success(f"✅ Loaded {len(questions)} exam questions from local file")
                    return questions
        
        # If local file doesn't exist, use fallback questions
        st.info("📝 Using built-in exam questions")
        return get_fallback_exam_questions()
        
    except Exception as e:
        st.error(f"❌ Error loading questions: {e}")
        return get_fallback_exam_questions()

def extract_questions_from_data(data):
    """Extract questions from JSON data structure"""
    # If data is already a list of questions
    if isinstance(data, list) and len(data) > 0:
        if validate_question_structure(data[0]):
            return data
    
    # Look for questions in common keys
    possible_keys = [
        "programming_languages_exam_questions",
        "chemistry_questions",
        "questions",
        "quiz_questions",
        "exam_questions",
        "question_bank",
        "items"
    ]
    
    for key in possible_keys:
        if key in data and isinstance(data[key], list) and len(data[key]) > 0:
            questions = data[key]
            if validate_question_structure(questions[0]):
                return questions
    
    # If no standard key found, look for any list with question structure
    for key, value in data.items():
        if isinstance(value, list) and len(value) > 0:
            if validate_question_structure(value[0]):
                return value
    
    return None

def validate_question_structure(question):
    """Validate that the question has the required structure"""
    if not isinstance(question, dict):
        return False
    
    required_fields = ['question', 'options', 'correct_answer']
    return all(field in question for field in required_fields)

def get_fallback_exam_questions():
    """Provide comprehensive fallback exam questions"""
    return [
   

  [
  {
    "id": 1,
    "topic": "Carbohydrates",
    "question": "Which general formula represents carbohydrates?",
    "options": {
      "A": "(CH2O)n",
      "B": "CnHnO2",
      "C": "C2H5OH",
      "D": "CH4"
    },
    "correct_answer": "A",
    "page": 1,
    "explanation": "Carbohydrates typically have the general empirical formula (CH2O)n, where 'n' is the number of carbon atoms."
  },
  {
    "id": 2,
    "topic": "Carbohydrates",
    "question": "Fischer projection represents carbohydrates in:",
    "options": {
      "A": "Cyclic form",
      "B": "Open chain form",
      "C": "Branched form",
      "D": "Crystalline form"
    },
    "correct_answer": "B",
    "page": 1,
    "explanation": "Fischer projections are standard 2D representations used to depict the open-chain structure of sugar molecules."
  },
  {
    "id": 3,
    "topic": "Carbohydrates",
    "question": "Haworth projection represents carbohydrates in:",
    "options": {
      "A": "Open chain form",
      "B": "Cyclic form",
      "C": "Hydrated form",
      "D": "Branched form"
    },
    "correct_answer": "B",
    "page": 1,
    "explanation": "Haworth projections are used to represent the cyclic (ring) structure of monosaccharides."
  },
  {
    "id": 4,
    "topic": "Carbohydrates",
    "question": "Glucose, galactose, and fructose are:",
    "options": {
      "A": "Polymers",
      "B": "Isomers",
      "C": "Enzymes",
      "D": "Hormones"
    },
    "correct_answer": "B",
    "page": 1,
    "explanation": "These sugars share the same molecular formula (C6H12O6) but differ in atomic arrangement, making them structural isomers."
  },
  {
    "id": 5,
    "topic": "Carbohydrates",
    "question": "A sugar with an aldehyde group is:",
    "options": {
      "A": "Ketose",
      "B": "Aldose",
      "C": "Disaccharide",
      "D": "Polysaccharide"
    },
    "correct_answer": "B",
    "page": 1,
    "explanation": "Monosaccharides containing an aldehyde group (-CHO) at the end of the carbon chain are classified as aldoses."
  },
  {
    "id": 6,
    "topic": "Carbohydrates",
    "question": "The major energy molecule formed from glucose is:",
    "options": {
      "A": "ATP",
      "B": "DNA",
      "C": "RNA",
      "D": "FADH2"
    },
    "correct_answer": "A",
    "page": 2,
    "explanation": "During cellular respiration, glucose is broken down to produce Adenosine Triphosphate (ATP), the primary energy carrier in cells."
  },
  {
    "id": 7,
    "topic": "Carbohydrates",
    "question": "The alpha form of glucose has its OH on carbon-1:",
    "options": {
      "A": "Above the ring",
      "B": "Below the ring",
      "C": "On the side chain",
      "D": "Absent"
    },
    "correct_answer": "B",
    "page": 2,
    "explanation": "In alpha-glucose, the hydroxyl (-OH) group on the anomeric carbon (C1) is positioned below the ring plane (trans to the CH2OH group)."
  },
  {
    "id": 8,
    "topic": "Carbohydrates",
    "question": "Disaccharides are formed through:",
    "options": {
      "A": "Hydrolysis",
      "B": "Dehydration synthesis",
      "C": "Combustion",
      "D": "Oxidation"
    },
    "correct_answer": "B",
    "page": 2,
    "explanation": "Disaccharides form when two monosaccharides join via a glycosidic bond, releasing a water molecule in a process called dehydration synthesis."
  },
  {
    "id": 9,
    "topic": "Carbohydrates",
    "question": "A glycosidic bond connects:",
    "options": {
      "A": "Two proteins",
      "B": "Two lipids",
      "C": "Two monosaccharides",
      "D": "A lipid and a sugar"
    },
    "correct_answer": "C",
    "page": 2,
    "explanation": "A glycosidic bond is the covalent linkage formed between the hemiacetal or hemiketal group of a saccharide and the hydroxyl group of another compound (usually another monosaccharide)."
  },
  {
    "id": 10,
    "topic": "Carbohydrates",
    "question": "Lactose consists of:",
    "options": {
      "A": "Glucose + glucose",
      "B": "Glucose + galactose",
      "C": "Glucose + fructose",
      "D": "Galactose + fructose"
    },
    "correct_answer": "B",
    "page": 2,
    "explanation": "Lactose (milk sugar) is a disaccharide composed of one glucose molecule and one galactose molecule linked by a beta-1,4-glycosidic bond."
  },
  {
    "id": 11,
    "topic": "Carbohydrates",
    "question": "Starch is made up of:",
    "options": {
      "A": "Amylose and cellulose",
      "B": "Amylose and amylopectin",
      "C": "Cellulose and glycogen",
      "D": "Maltose and sucrose"
    },
    "correct_answer": "B",
    "page": 3,
    "explanation": "Starch is a polysaccharide composed of two types of alpha-glucose polymers: linear amylose and branched amylopectin."
  },
  {
    "id": 12,
    "topic": "Carbohydrates",
    "question": "Glycogen is stored mainly in:",
    "options": {
      "A": "Bones",
      "B": "Skin",
      "C": "Liver and muscles",
      "D": "Pancreas"
    },
    "correct_answer": "C",
    "page": 3,
    "explanation": "In animals, glycogen is primarily stored in the liver (for blood glucose regulation) and skeletal muscles (for local energy)."
  },
  {
    "id": 13,
    "topic": "Carbohydrates",
    "question": "Cellulose contains:",
    "options": {
      "A": "α 1-4 linkages",
      "B": "β 1-4 linkages",
      "C": "α 1-6 linkages",
      "D": "β 1-6 linkages"
    },
    "correct_answer": "B",
    "page": 3,
    "explanation": "Cellulose is a linear polymer of glucose units connected by beta (β) 1-4 glycosidic bonds."
  },
  {
    "id": 14,
    "topic": "Carbohydrates",
    "question": "Humans cannot digest cellulose because:",
    "options": {
      "A": "It contains no glucose",
      "B": "It is too large",
      "C": "Humans lack cellulase",
      "D": "It is poisonous"
    },
    "correct_answer": "C",
    "page": 3,
    "explanation": "Humans lack the enzyme cellulase required to hydrolyze the beta 1-4 linkages found in cellulose."
  },
  {
    "id": 15,
    "topic": "Carbohydrates",
    "question": "Chitin is composed of:",
    "options": {
      "A": "N-acetylglucosamine",
      "B": "Maltose units",
      "C": "Sucrose units",
      "D": "Fructose units"
    },
    "correct_answer": "A",
    "page": 3,
    "explanation": "Chitin is a structural polysaccharide composed of repeating units of N-acetylglucosamine (a derivative of glucose)."
  },
  {
    "id": 16,
    "topic": "Carbohydrates",
    "question": "Amino sugars have an OH group replaced by:",
    "options": {
      "A": "COOH",
      "B": "NH2",
      "C": "SH",
      "D": "CH3"
    },
    "correct_answer": "B",
    "page": 4,
    "explanation": "In amino sugars, a hydroxyl group (-OH) is replaced by an amine group (-NH2)."
  },
  {
    "id": 17,
    "topic": "Carbohydrates",
    "question": "The A blood group antigen has which dominant sugar?",
    "options": {
      "A": "Glucose",
      "B": "Mannose",
      "C": "D-galactose",
      "D": "N-acetylgalactosamine"
    },
    "correct_answer": "D",
    "page": 4,
    "explanation": "The specific immunodominant sugar responsible for blood group A specificity is N-acetylgalactosamine."
  },
  {
    "id": 18,
    "topic": "Carbohydrates",
    "question": "Polysaccharides are generally:",
    "options": {
      "A": "Sweet",
      "B": "Insoluble in water",
      "C": "Low molecular weight",
      "D": "Crystals"
    },
    "correct_answer": "B",
    "page": 4,
    "explanation": "Polysaccharides are large, complex molecules that are typically not sweet and are often insoluble in water due to their high molecular weight."
  },
  {
    "id": 19,
    "topic": "Carbohydrates",
    "question": "A homopolysaccharide contains:",
    "options": {
      "A": "Different sugars",
      "B": "One type of monosaccharide",
      "C": "Amino acids",
      "D": "Lipids"
    },
    "correct_answer": "B",
    "page": 4,
    "explanation": "Homopolysaccharides are formed from the polymerization of a single type of monosaccharide monomer."
  },
  {
    "id": 20,
    "topic": "Carbohydrates",
    "question": "Inulin consists mainly of:",
    "options": {
      "A": "Glucose units",
      "B": "Fructose units",
      "C": "Ribose units",
      "D": "Galactose units"
    },
    "correct_answer": "B",
    "page": 4,
    "explanation": "Inulin is a storage polysaccharide found in some plants, consisting primarily of fructose chains."
  },
  {
    "id": 21,
    "topic": "Carbohydrates",
    "question": "The most abundant biopolymer on Earth is:",
    "options": {
      "A": "Starch",
      "B": "Cellulose",
      "C": "Chitin",
      "D": "Glycogen"
    },
    "correct_answer": "B",
    "page": 5,
    "explanation": "Cellulose, which forms the primary structural component of plant cell walls, is considered the most abundant organic polymer on Earth."
  },
  {
    "id": 22,
    "topic": "Carbohydrates",
    "question": "Starch digestion begins in the:",
    "options": {
      "A": "Stomach",
      "B": "Mouth",
      "C": "Liver",
      "D": "Small intestine"
    },
    "correct_answer": "B",
    "page": 5,
    "explanation": "Digestion of starch starts in the mouth with the action of the enzyme salivary amylase."
  },
  {
    "id": 23,
    "topic": "Carbohydrates",
    "question": "The ring form of glucose predominates in solution at:",
    "options": {
      "A": "Less than 10 percent",
      "B": "About 50 percent",
      "C": "Over 99 percent",
      "D": "Never forms"
    },
    "correct_answer": "C",
    "page": 5,
    "explanation": "In an aqueous solution, glucose exists in equilibrium, but over 99% is in the cyclic (pyranose) form rather than the open chain."
  },
  {
    "id": 24,
    "topic": "Carbohydrates",
    "question": "Maltose consists of:",
    "options": {
      "A": "Two glucose molecules",
      "B": "Glucose + fructose",
      "C": "Fructose + galactose",
      "D": "Glucose + mannose"
    },
    "correct_answer": "A",
    "page": 5,
    "explanation": "Maltose is a disaccharide formed by two glucose units joined by an alpha-1,4-glycosidic bond."
  },
  {
    "id": 25,
    "topic": "Carbohydrates",
    "question": "A ketose sugar contains its carbonyl group:",
    "options": {
      "A": "At the terminal carbon",
      "B": "In the middle of the carbon chain",
      "C": "At carbon-1",
      "D": "On a side chain only"
    },
    "correct_answer": "B",
    "page": 5,
    "explanation": "Ketoses have a ketone group (C=O) located within the carbon chain (usually at C2), whereas aldoses have it at the terminal end."
  },
  {
    "id": 26,
    "topic": "Carbohydrates",
    "question": "Hyaluronic acid is a:",
    "options": {
      "A": "Homopolysaccharide",
      "B": "Disaccharide",
      "C": "Heteropolysaccharide",
      "D": "Protein"
    },
    "correct_answer": "C",
    "page": 6,
    "explanation": "Hyaluronic acid is a heteropolysaccharide (specifically a glycosaminoglycan) made of alternating units of N-acetylglucosamine and glucuronic acid."
  },
  {
    "id": 27,
    "topic": "Carbohydrates",
    "question": "Glycogen is structurally similar to:",
    "options": {
      "A": "Cellulose",
      "B": "Amylopectin",
      "C": "Amylose",
      "D": "Ribose"
    },
    "correct_answer": "B",
    "page": 6,
    "explanation": "Glycogen is structurally very similar to amylopectin (both are branched glucose polymers), though glycogen is more extensively branched."
  },
  {
    "id": 28,
    "topic": "Carbohydrates",
    "question": "The linkage in amylose is:",
    "options": {
      "A": "α 1-6",
      "B": "β 1-4",
      "C": "α 1-4",
      "D": "β 1-6"
    },
    "correct_answer": "C",
    "page": 6,
    "explanation": "Amylose is a linear polymer of glucose units linked by alpha (α) 1-4 glycosidic bonds."
  },
  {
    "id": 29,
    "topic": "Carbohydrates",
    "question": "Mucopolysaccharides are also called:",
    "options": {
      "A": "Lipoproteins",
      "B": "Glycosaminoglycans",
      "C": "Phospholipids",
      "D": "Steroids"
    },
    "correct_answer": "B",
    "page": 6,
    "explanation": "'Mucopolysaccharides' is an older term for Glycosaminoglycans (GAGs), which are long unbranched polysaccharides."
  },
  {
    "id": 30,
    "topic": "Carbohydrates",
    "question": "Excess carbohydrate intake may lead to:",
    "options": {
      "A": "Obesity",
      "B": "Increased immunity",
      "C": "Rapid height growth",
      "D": "Stronger bones"
    },
    "correct_answer": "A",
    "page": 6,
    "explanation": "Excess carbohydrates in the diet are converted into lipids and stored in adipose tissue, which can lead to obesity."
  }
]
]


def analyze_exam_topics(questions):
    """Analyze and categorize exam questions by topic"""
    topics = {}
    for q in questions:
        topic = q.get('topic', 'General')
        topics[topic] = topics.get(topic, 0) + 1
    return topics

def initialize_exam_state(questions=None, restore_progress=False):
    """Initialize or reset the exam state"""
    if questions is None:
        questions = load_questions_from_json()
    
    if restore_progress and st.session_state.get('questions_loaded', False):
        # Keep existing progress
        st.info("🔄 Restored your exam progress")
    else:
        # Reset progress
        st.session_state.questions = questions
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.user_answers = [None] * len(questions)
        st.session_state.exam_completed = False
        st.session_state.topics = analyze_exam_topics(questions)
        st.session_state.questions_loaded = True
    
    # Save session after initialization
    save_session_state()

def parse_uploaded_json(uploaded_file):
    """Parse uploaded JSON file and extract questions"""
    try:
        # Read the file content
        content = uploaded_file.read()
        
        # Try to decode as JSON
        try:
            data = json.loads(content.decode('utf-8'))
        except UnicodeDecodeError:
            # If UTF-8 fails, try other encodings
            try:
                data = json.loads(content.decode('latin-1'))
            except:
                st.error("❌ Could not decode the file. Please use UTF-8 encoding.")
                return None
        
        # Extract questions from the data
        questions = extract_questions_from_data(data)
        
        if questions:
            st.success(f"✅ Successfully loaded {len(questions)} questions!")
            return questions
        else:
            st.error("❌ No valid questions found in the uploaded file. Please check the format.")
            return None
        
    except json.JSONDecodeError as e:
        st.error(f"❌ Invalid JSON format: {e}")
        return None
    except Exception as e:
        st.error(f"❌ Error parsing JSON file: {e}")
        return None

def save_uploaded_file(uploaded_file):
    """Save uploaded file locally"""
    try:
        with open("programming_questions.json", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("✅ File saved successfully!")
        return True
    except Exception as e:
        st.error(f"❌ Error saving file: {e}")
        return False

def main():
    # Set page configuration
    st.set_page_config(
        page_title="EXAM QUESTIONS",
        page_icon="💻",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Try to load existing session first
    if 'questions_loaded' not in st.session_state:
        saved_session = load_session_state()
        if saved_session:
            # Restore from saved session
            for key, value in saved_session.items():
                st.session_state[key] = value
            st.success("🔁 Restored your previous exam session!")
        else:
            # Initialize fresh session
            initialize_exam_state()
    
    # Header
    st.title("💻 Exam - Persistent Session")
    st.markdown("### Your progress is automatically saved! Leave and return anytime.")
    
    # Auto-save notice
    st.info("💾 **Auto-save enabled**: Your progress is automatically saved and will be restored when you return.")
    
    # File Upload Section
    with st.expander("📁 Upload Your JSON Question File", expanded=False):
        st.markdown("""
        **Upload your JSON file with questions in this format:**
        ```json
        {
          "programming_languages_exam_questions": [
            {
              "id": 1,
              "topic": "Your Topic",
              "question": "Your question?",
              "options": {
                "A": "Option A",
                "B": "Option B",
                "C": "Option C",
                "D": "Option D"
              },
              "correct_answer": "A",
              "explanation": "Your explanation here"
            }
          ]
        }
        ```
        """)
        
        uploaded_file = st.file_uploader(
            "Choose a JSON file", 
            type="json",
            help="Upload your questions in JSON format",
            key="file_uploader"
        )
        
        # AUTO-LOAD when file is uploaded
        if uploaded_file is not None:
            # Parse the uploaded file
            questions = parse_uploaded_json(uploaded_file)
            
            if questions:
                # Store file info for persistence
                st.session_state.last_uploaded_file_name = uploaded_file.name
                
                # Initialize with new questions but preserve progress if compatible
                current_questions = st.session_state.get('questions', [])
                if len(current_questions) == len(questions):
                    st.info("📚 Questions updated while preserving your progress!")
                    st.session_state.questions = questions
                else:
                    st.warning("🔄 Question set changed - resetting progress")
                    initialize_exam_state(questions)
                
                save_session_state()
                st.rerun()
        
        # Manual controls for uploaded file
        if uploaded_file is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔄 Reload Uploaded Questions", type="primary"):
                    uploaded_file.seek(0)  # Reset file pointer
                    questions = parse_uploaded_json(uploaded_file)
                    if questions:
                        initialize_exam_state(questions)
                        st.success(f"✅ Reloaded {len(questions)} questions!")
                        st.rerun()
            
            with col2:
                if st.button("💾 Save File Locally"):
                    if save_uploaded_file(uploaded_file):
                        st.info("File saved as 'programming_questions.json'. It will be loaded automatically next time.")
    
    # Quick JSON Input Section
    with st.expander("📝 Or Paste JSON Directly", expanded=False):
        json_text = st.text_area(
            "Paste your JSON here:",
            height=200,
            placeholder='Paste your JSON questions here...',
            key="json_text_area"
        )
        
        if st.button("📥 Load from Text", type="secondary"):
            if json_text.strip():
                try:
                    # Create a temporary file-like object
                    fake_file = io.BytesIO(json_text.encode('utf-8'))
                    fake_file.name = "pasted_json.json"
                    
                    questions = parse_uploaded_json(fake_file)
                    if questions:
                        initialize_exam_state(questions)
                        st.success(f"✅ Loaded {len(questions)} questions from pasted JSON!")
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Error parsing JSON text: {e}")
            else:
                st.warning("Please paste some JSON text first.")
    
    # Show warning if no questions
    if not st.session_state.get('questions'):
        st.error("❌ No exam questions available.")
        return
    
    # Exam info header
    st.write("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Questions", len(st.session_state.questions))
    with col2:
        st.metric("Topics Covered", len(st.session_state.topics))
    with col3:
        if not st.session_state.exam_completed:
            current_attempted = sum(1 for ans in st.session_state.user_answers if ans is not None)
            st.metric("Current Score", f"{st.session_state.score}/{current_attempted}")
        else:
            st.metric("Final Score", f"{st.session_state.score}/{len(st.session_state.questions)}")
    with col4:
        if st.button("🔄 Reset Exam", help="Start over with current questions"):
            initialize_exam_state(st.session_state.questions)
            st.rerun()
    
    # Progress persistence info
    answered_count = sum(1 for ans in st.session_state.user_answers if ans is not None)
    st.write(f"**Progress:** {answered_count}/{len(st.session_state.questions)} questions answered • **Auto-saved**")
    
    # Source indicator
    if st.session_state.get('last_uploaded_file_name'):
        current_source = f"📁 {st.session_state.last_uploaded_file_name}"
    else:
        current_source = "📝 Built-in Questions"
    st.write(f"**Question source:** {current_source}")
    
    # Sidebar for exam progress and info
    with st.sidebar:
        st.header("📊 Exam Progress")
        
        current_score = st.session_state.score
        total_questions = len(st.session_state.questions)
        answered_count = sum(1 for ans in st.session_state.user_answers if ans is not None)
        
        if not st.session_state.exam_completed:
            progress = answered_count / total_questions
            score_percentage = (current_score / answered_count) * 100 if answered_count > 0 else 0
        else:
            progress = 1.0
            score_percentage = (current_score / total_questions) * 100
        
        st.write(f"**Score:** {current_score}/{answered_count}")
        st.write(f"**Accuracy:** {score_percentage:.1f}%")
        st.progress(progress)
        st.write(f"**Progress:** {answered_count}/{total_questions}")
        
        # Session management
        st.header("💾 Session")
        if st.button("💾 Save Progress Now", use_container_width=True):
            save_session_state()
            st.success("Progress saved!")
        
        if st.button("🗑️ Clear Saved Session", use_container_width=True):
            if os.path.exists(SESSION_FILE):
                os.remove(SESSION_FILE)
            st.success("Saved session cleared!")
            st.rerun()
        
        # Exam controls
        st.header("🎯 Exam Controls")
        if st.button("🔄 Restart Exam", use_container_width=True):
            initialize_exam_state(st.session_state.questions)
            st.rerun()
        
        if st.button("🔀 Shuffle Questions", use_container_width=True):
            random.shuffle(st.session_state.questions)
            st.session_state.current_question = 0
            st.session_state.answered = False
            save_session_state()
            st.success("Questions shuffled!")
            st.rerun()
        
        # Exam topics
        st.header("📚 Exam Topics")
        for topic, count in st.session_state.topics.items():
            st.write(f"• {topic}: {count} questions")
    
    # Main exam interface
    if not st.session_state.exam_completed:
        current_q = st.session_state.questions[st.session_state.current_question]
        
        # Question header with metadata
        st.subheader(f"📝 Question {st.session_state.current_question + 1}")
        st.markdown(f"**Topic:** {current_q.get('topic', 'General')}")
        if 'page' in current_q:
            st.markdown(f"**Reference:** Page {current_q['page']}")
        
        # Question text
        st.markdown(f"### {current_q['question']}")
        
        if not st.session_state.answered:
            # Display options for answering
            option_labels = list(current_q['options'].keys())
            
            # Pre-select if already answered
            previous_answer = st.session_state.user_answers[st.session_state.current_question]
            user_answer = st.radio(
                "Select your answer:",
                option_labels,
                index=option_labels.index(previous_answer) if previous_answer in option_labels else 0,
                format_func=lambda x: f"{x}. {current_q['options'][x]}",
                key=f"q{st.session_state.current_question}"
            )
            
            # Submit button
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("🚀 Submit Answer", type="primary"):
                    st.session_state.answered = True
                    st.session_state.user_answers[st.session_state.current_question] = user_answer
                    
                    # Check if answer is correct
                    if user_answer == current_q['correct_answer']:
                        st.session_state.score += 1
                    
                    # Auto-save after answering
                    save_session_state()
                    st.rerun()
        
        else:
            # AFTER ANSWERING - SHOW RESULTS AND EXPLANATION
            st.write("---")
            
            # Show answer result
            user_answer = st.session_state.user_answers[st.session_state.current_question]
            if user_answer == current_q['correct_answer']:
                st.success("🎉 **Correct!** Well done!")
            else:
                st.error(f"😞 **Incorrect.** The correct answer is **{current_q['correct_answer']}**")
            
            # Show color-coded options review
            st.subheader("📋 Answer Review")
            option_labels = list(current_q['options'].keys())
            for option in option_labels:
                option_text = f"{option}. {current_q['options'][option]}"
                if option == current_q['correct_answer']:
                    st.success(f"✅ **{option_text}** - **Correct Answer**")
                elif option == user_answer:
                    st.error(f"❌ **{option_text}** - **Your Answer**")
                else:
                    st.write(f"📝 {option_text}")
            
            # SHOW EXPLANATION
            st.write("---")
            if 'explanation' in current_q and current_q['explanation']:
                st.subheader("💡 Explanation")
                st.info(current_q['explanation'])
            else:
                st.warning("No explanation available for this question.")
            
            # Navigation buttons
            st.write("---")
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.session_state.current_question > 0:
                    if st.button("⏮️ Previous Question", use_container_width=True):
                        st.session_state.current_question -= 1
                        st.session_state.answered = False
                        save_session_state()
                        st.rerun()
            
            with col2:
                if st.session_state.current_question < len(st.session_state.questions) - 1:
                    if st.button("⏭️ Next Question", type="primary", use_container_width=True):
                        st.session_state.current_question += 1
                        st.session_state.answered = False
                        save_session_state()
                        st.rerun()
                else:
                    if st.button("🏁 Finish Exam", type="primary", use_container_width=True):
                        st.session_state.exam_completed = True
                        save_session_state()
                        st.rerun()
            
            with col3:
                if st.button("🔄 Try Again", use_container_width=True):
                    st.session_state.answered = False
                    save_session_state()
                    st.rerun()
    
    else:
        # Exam completed
        st.balloons()
        st.success("## 🎉 Exam Completed!")
        
        final_score = st.session_state.score
        total_questions = len(st.session_state.questions)
        score_percentage = (final_score / total_questions) * 100
        
        # Final results
        st.subheader("📈 Final Exam Results")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Questions", total_questions)
        with col2:
            st.metric("Correct Answers", final_score)
        with col3:
            st.metric("Final Score", f"{score_percentage:.1f}%")
        
        # Performance message
        st.write("---")
        if score_percentage >= 90:
            st.success("### 🏆 Outstanding! Exams Genius!")
        elif score_percentage >= 80:
            st.success("### 🌟 Excellent! Strong Understanding of Concepts!")
        elif score_percentage >= 70:
            st.info("### 👍 Very Good! Solid Knowledge Base!")
        elif score_percentage >= 60:
            st.warning("### 📚 Good! Review Challenging Topics!")
        else:
            st.error("### 💪 Keep Studying! Focus on Fundamental Concepts!")
        
        # Restart option
        st.write("---")
        if st.button("🔄 Take Exam Again", type="primary"):
            initialize_exam_state(st.session_state.questions)
            st.rerun()

if __name__ == "__main__":
    main()
