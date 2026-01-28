import streamlit as st 
from textblob import TextBlob 
import urllib.parse
import nltk

try:
    nltk.data.find('corpora/brown.zip')
except LookupError:
    nltk.download('brown', quiet=True)
    nltk.download('punkt', quiet=True)
def detect_mood(text):
    polarity = TextBlob(text).sentiment.polarity
    
    if polarity > 0.5:
        return "Happy"
    elif polarity > 0.1:
        return "Energetic"
    elif polarity < -0.1:
        return "Angry"
    elif polarity < -0.5:
        return "Sad"
    else:
        return "Calm"

mood_genre = {
    "Happy": ["Pop", "DnB", "Hyperpop", "Electrocrush"],
    "Sad": ["Lo-fi HipHop", "Orchestral", "Indie", "Bedroom Pop"],
    "Calm": ["Ambient", "Noise", "IDM", "Soul/R&B"],
    "Angry": ["Black Metal", "NuMetal", "Trap", "Hardstyle"],
    "Energetic": ["Dubstep", "Color Bass", "Alternative"]
}

mood_colors = {
    "Happy": "#FFD700",
    "Sad": "#4A90E2",
    "Calm": "#7EC8E3",
    "Angry": "#E74C3C",
    "Energetic": "#FF6B6B"
}

mood_emojis = {
    "Happy": "😊",
    "Sad": "😢",
    "Calm": "😌",
    "Angry": "😤",
    "Energetic": "⚡"
}

def spotify_search_link(query):
    encoded_query = urllib.parse.quote(query)
    return f"https://open.spotify.com/search/{encoded_query}"

# Page Configuration
st.set_page_config(
    page_title="MoodTune - Music Recommender",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Dark theme background */
    .stApp {
        background: #0a0e27;
        font-family: 'Inter', sans-serif;
    }
    
    /* Remove default Streamlit padding */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    
    /* Main title */
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    .subtitle {
        text-align: center;
        color: #a0aec0;
        font-size: 1.2rem;
        margin-bottom: 3rem;
        font-weight: 300;
    }
    
    /* Text area styling - HIGH CONTRAST */
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #2d3748 !important;
        padding: 1.2rem !important;
        font-size: 1.1rem !important;
        background: #1a202c !important;
        color: #e2e8f0 !important;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextArea textarea:focus {
        border-color: #1DB954 !important;
        box-shadow: 0 0 0 3px rgba(29, 185, 84, 0.2) !important;
        background: #2d3748 !important;
        color: #ffffff !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #718096 !important;
    }
    
    /* Label styling */
    .stTextArea label, .stMarkdown h3 {
        color: #e2e8f0 !important;
        font-weight: 600;
    }
    
    /* Button styling with hover effects */
    .stButton button {
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1rem 3rem !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(29, 185, 84, 0.3) !important;
        width: 100% !important;
        margin-top: 1.5rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(29, 185, 84, 0.5) !important;
        background: linear-gradient(135deg, #1ed760 0%, #1DB954 100%) !important;
    }
    
    .stButton button:active {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 15px rgba(29, 185, 84, 0.4) !important;
    }
    
    /* Mood card styling */
    .mood-card {
        background: linear-gradient(135deg, var(--mood-color) 0%, var(--mood-color-dark) 100%);
        border-radius: 16px;
        padding: 2.5rem;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
        animation: fadeInUp 0.6s ease-out;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .mood-emoji {
        font-size: 5rem;
        margin-bottom: 1rem;
        display: block;
        filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
    }
    
    .mood-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    /* Genre card styling with hover effects */
    .genre-card {
        background: #1a202c;
        border-radius: 12px;
        padding: 1.8rem;
        text-align: center;
        transition: all 0.3s ease;
        border: 2px solid #2d3748;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
        cursor: pointer;
    }
    
    .genre-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 12px 24px rgba(29, 185, 84, 0.3);
        border-color: #1DB954;
        background: #2d3748;
    }
    
    .genre-name {
        font-size: 1.3rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 0.8rem;
    }
    
    .spotify-link {
        color: #1DB954;
        text-decoration: none;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        transition: all 0.3s ease;
        font-size: 1rem;
    }
    
    .spotify-link:hover {
        color: #1ed760;
        transform: scale(1.05);
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #e2e8f0;
        margin: 2.5rem 0 1.5rem 0;
        text-align: center;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Warning styling */
    .stAlert {
        border-radius: 12px;
        background: #2d3748 !important;
        border-left: 5px solid #f6ad55 !important;
        color: #e2e8f0 !important;
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #2d3748;
        margin: 2rem 0;
    }
    
    /* Tip box */
    .tip-box {
        text-align: center;
        padding: 1.5rem;
        background: #1a202c;
        border-radius: 12px;
        margin-top: 2rem;
        border: 1px solid #2d3748;
    }
    
    .tip-box p {
        margin: 0;
        color: #a0aec0;
        font-size: 1rem;
    }
    
    .tip-box strong {
        color: #1DB954;
    }
    
    /* Footer */
    .footer-text {
        text-align: center;
        color: #718096;
        padding: 1rem;
        font-size: 0.95rem;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0e27;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #2d3748;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #1DB954;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">🎵 MoodTune</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Discover music that matches your vibe ✨</p>', unsafe_allow_html=True)

# Main content container
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    # User input section
    st.markdown("### 💭 How are you feeling today?")
    user_input = st.text_area(
        "",
        placeholder="Type your thoughts here... (e.g., 'I'm feeling great today!' or 'Having a tough day...')",
        height=150,
        label_visibility="collapsed",
        key="mood_input"
    )
    
    # Recommend button
    if st.button("🎧 Get Music Recommendations"):
        if user_input.strip() == "":
            st.warning("⚠️ Please share your feelings first!")
        else: 
            mood = detect_mood(user_input)
            genres = mood_genre.get(mood, [])
            mood_color = mood_colors.get(mood, "#1DB954")
            mood_emoji = mood_emojis.get(mood, "🎵")
            
            # Mood display card
            st.markdown(f"""
                <div class="mood-card" style="--mood-color: {mood_color}; --mood-color-dark: {mood_color}dd;">
                    <span class="mood-emoji">{mood_emoji}</span>
                    <h2 class="mood-title">You're feeling {mood}!</h2>
                </div>
            """, unsafe_allow_html=True)
            
            # Genres section
            st.markdown('<h3 class="section-header">🎼 Perfect Genres for Your Mood</h3>', unsafe_allow_html=True)
            
            # Create genre cards in a grid
            cols = st.columns(2)
            for idx, genre in enumerate(genres):
                with cols[idx % 2]:
                    search_query = f"{mood} {genre} music"
                    link = spotify_search_link(search_query)
                    
                    st.markdown(f"""
                        <div class="genre-card">
                            <div class="genre-name">{genre}</div>
                            <a href="{link}" target="_blank" class="spotify-link">
                                🎧 Listen on Spotify →
                            </a>
                        </div>
                    """, unsafe_allow_html=True)
            
            # Tip section
            st.markdown("---")
            st.markdown("""
                <div class="tip-box">
                    <p>💡 <strong>Tip:</strong> Music can significantly affect your mood and productivity. Choose wisely! 🎶</p>
                </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div class="footer-text">
        <p>Made with ❤️ for music lovers everywhere</p>
    </div>
""", unsafe_allow_html=True)    

def detect_mood(text):
    polarity = TextBlob(text).sentiment.polarity
    
    if polarity > 0.5:
        return "Happy"
    elif polarity > 0.1:
        return "Energetic"
    elif polarity < -0.1:
        return "Angry"
    elif polarity < -0.5:
        return "Sad"
    else:
        return "Calm"

mood_genre = {
    "Happy": ["Pop", "DnB", "Hyperpop", "Electrocrush"],
    "Sad": ["Lo-fi HipHop", "Orchestral", "Indie", "Bedroom Pop"],
    "Calm": ["Ambient", "Noise", "IDM", "Soul/R&B"],
    "Angry": ["Black Metal", "NuMetal", "Trap", "Hardstyle"],
    "Energetic": ["Dubstep", "Color Bass", "Alternative"]
}

mood_colors = {
    "Happy": "#FFD700",
    "Sad": "#4A90E2",
    "Calm": "#7EC8E3",
    "Angry": "#E74C3C",
    "Energetic": "#FF6B6B"
}

mood_emojis = {
    "Happy": "😊",
    "Sad": "😢",
    "Calm": "😌",
    "Angry": "😤",
    "Energetic": "⚡"
}

def spotify_search_link(query):
    encoded_query = urllib.parse.quote(query)
    return f"https://open.spotify.com/search/{encoded_query}"

# Page Configuration
st.set_page_config(
    page_title="MoodTune - Music Recommender",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Dark theme background */
    .stApp {
        background: #0a0e27;
        font-family: 'Inter', sans-serif;
    }
    
    /* Remove default Streamlit padding */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    
    /* Main title */
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    .subtitle {
        text-align: center;
        color: #a0aec0;
        font-size: 1.2rem;
        margin-bottom: 3rem;
        font-weight: 300;
    }
    
    /* Text area styling - HIGH CONTRAST */
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #2d3748 !important;
        padding: 1.2rem !important;
        font-size: 1.1rem !important;
        background: #1a202c !important;
        color: #e2e8f0 !important;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextArea textarea:focus {
        border-color: #1DB954 !important;
        box-shadow: 0 0 0 3px rgba(29, 185, 84, 0.2) !important;
        background: #2d3748 !important;
        color: #ffffff !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #718096 !important;
    }
    
    /* Label styling */
    .stTextArea label, .stMarkdown h3 {
        color: #e2e8f0 !important;
        font-weight: 600;
    }
    
    /* Button styling with hover effects */
    .stButton button {
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1rem 3rem !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(29, 185, 84, 0.3) !important;
        width: 100% !important;
        margin-top: 1.5rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(29, 185, 84, 0.5) !important;
        background: linear-gradient(135deg, #1ed760 0%, #1DB954 100%) !important;
    }
    
    .stButton button:active {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 15px rgba(29, 185, 84, 0.4) !important;
    }
    
    /* Mood card styling */
    .mood-card {
        background: linear-gradient(135deg, var(--mood-color) 0%, var(--mood-color-dark) 100%);
        border-radius: 16px;
        padding: 2.5rem;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
        animation: fadeInUp 0.6s ease-out;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .mood-emoji {
        font-size: 5rem;
        margin-bottom: 1rem;
        display: block;
        filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
    }
    
    .mood-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    /* Genre card styling with hover effects */
    .genre-card {
        background: #1a202c;
        border-radius: 12px;
        padding: 1.8rem;
        text-align: center;
        transition: all 0.3s ease;
        border: 2px solid #2d3748;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
        cursor: pointer;
    }
    
    .genre-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 12px 24px rgba(29, 185, 84, 0.3);
        border-color: #1DB954;
        background: #2d3748;
    }
    
    .genre-name {
        font-size: 1.3rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 0.8rem;
    }
    
    .spotify-link {
        color: #1DB954;
        text-decoration: none;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        transition: all 0.3s ease;
        font-size: 1rem;
    }
    
    .spotify-link:hover {
        color: #1ed760;
        transform: scale(1.05);
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #e2e8f0;
        margin: 2.5rem 0 1.5rem 0;
        text-align: center;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Warning styling */
    .stAlert {
        border-radius: 12px;
        background: #2d3748 !important;
        border-left: 5px solid #f6ad55 !important;
        color: #e2e8f0 !important;
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #2d3748;
        margin: 2rem 0;
    }
    
    /* Tip box */
    .tip-box {
        text-align: center;
        padding: 1.5rem;
        background: #1a202c;
        border-radius: 12px;
        margin-top: 2rem;
        border: 1px solid #2d3748;
    }
    
    .tip-box p {
        margin: 0;
        color: #a0aec0;
        font-size: 1rem;
    }
    
    .tip-box strong {
        color: #1DB954;
    }
    
    /* Footer */
    .footer-text {
        text-align: center;
        color: #718096;
        padding: 1rem;
        font-size: 0.95rem;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0e27;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #2d3748;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #1DB954;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">🎵 MoodTune</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Discover music that matches your vibe ✨</p>', unsafe_allow_html=True)

# Main content container
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    # User input section
    st.markdown("### 💭 How are you feeling today?")
    user_input = st.text_area(
        "",
        placeholder="Type your thoughts here... (e.g., 'I'm feeling great today!' or 'Having a tough day...')",
        height=150,
        label_visibility="collapsed",
        key="mood_input"
    )
    
    # Recommend button
    if st.button("🎧 Get Music Recommendations"):
        if user_input.strip() == "":
            st.warning("⚠️ Please share your feelings first!")
        else: 
            mood = detect_mood(user_input)
            genres = mood_genre.get(mood, [])
            mood_color = mood_colors.get(mood, "#1DB954")
            mood_emoji = mood_emojis.get(mood, "🎵")
            
            # Mood display card
            st.markdown(f"""
                <div class="mood-card" style="--mood-color: {mood_color}; --mood-color-dark: {mood_color}dd;">
                    <span class="mood-emoji">{mood_emoji}</span>
                    <h2 class="mood-title">You're feeling {mood}!</h2>
                </div>
            """, unsafe_allow_html=True)
            
            # Genres section
            st.markdown('<h3 class="section-header">🎼 Perfect Genres for Your Mood</h3>', unsafe_allow_html=True)
            
            # Create genre cards in a grid
            cols = st.columns(2)
            for idx, genre in enumerate(genres):
                with cols[idx % 2]:
                    search_query = f"{mood} {genre} music"
                    link = spotify_search_link(search_query)
                    
                    st.markdown(f"""
                        <div class="genre-card">
                            <div class="genre-name">{genre}</div>
                            <a href="{link}" target="_blank" class="spotify-link">
                                🎧 Listen on Spotify →
                            </a>
                        </div>
                    """, unsafe_allow_html=True)
            
            # Tip section
            st.markdown("---")
            st.markdown("""
                <div class="tip-box">
                    <p>💡 <strong>Tip:</strong> Music can significantly affect your mood and productivity. Choose wisely! 🎶</p>
                </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div class="footer-text">
        <p>Made with ❤️ for music lovers everywhere</p>
    </div>
""", unsafe_allow_html=True)
                                                                          
