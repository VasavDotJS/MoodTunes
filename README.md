# 🎵 MoodTune - Music Mood Recommender

A beautiful dark-themed app that recommends music genres based on your current mood using sentiment analysis.

## Features

- 🎭 **Mood Detection** - Analyzes your text input to detect your current mood
- 🎵 **Genre Recommendations** - Suggests perfect music genres for your mood
- 🎨 **Dark Theme UI** - Modern, eye-friendly dark interface
- 🎧 **Spotify Integration** - Direct links to explore genres on Spotify
- ⚡ **Real-time Analysis** - Instant mood detection and recommendations

## Moods Detected

- **Happy** 😊 - Pop, DnB, Hyperpop, Electrocrush
- **Sad** 😢 - Lo-fi HipHop, Orchestral, Indie, Bedroom Pop
- **Calm** 😌 - Ambient, Noise, IDM, Soul/R&B
- **Angry** 😤 - Black Metal, NuMetal, Trap, Hardstyle
- **Energetic** ⚡ - Dubstep, Color Bass, Alternative

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/moodtune.git
cd moodtune
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run music_recommender_dark.py
```

## Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed deployment instructions.

**Quick Deploy (Streamlit Cloud):**
1. Push to GitHub
2. Go to https://share.streamlit.io/
3. Connect your repo and deploy!

## Technologies Used

- **Streamlit** - Web framework
- **TextBlob** - Sentiment analysis
- **Python 3.8+** - Programming language

## How It Works

1. User enters their current feelings as text
2. TextBlob analyzes the sentiment polarity of the text
3. Mood is detected based on polarity score
4. Relevant music genres are recommended
5. Direct Spotify links provided for easy listening

## Contributing
Feel free to open issues or submit pull requests!

