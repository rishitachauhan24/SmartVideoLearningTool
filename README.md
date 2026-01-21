# 🎓 Smart Video Learning Tool

## AI-Powered YouTube Learning Assistant

Transform any YouTube educational video into a complete learning package with AI-generated summaries, key points, and interactive quizzes!

---

## 🌟 Features

### ✨ Core Capabilities

- **📝 Automatic Transcript Extraction**: Extracts complete video transcripts from YouTube videos
- **🤖 AI-Powered Summaries**: Generates comprehensive, well-structured summaries using OpenAI GPT
- **🎯 Key Learning Points**: Automatically identifies 5-8 core learning points from video content
- **❓ Interactive Quiz Generation**: Creates exactly 10 multiple-choice questions for self-assessment
- **💻 Modern Web Interface**: Beautiful, responsive UI built with HTML, CSS, and JavaScript
- **🔄 Real-time Processing**: Live progress tracking and instant results
- **📊 Self-Assessment**: Interactive quiz with instant feedback and scoring

---

## 📋 Problem Statement

In modern digital learning environments, students face several challenges:

- ❌ Educational videos are lengthy, unstructured, and require continuous attention
- ❌ Students often miss or forget critical information
- ❌ No built-in mechanism to extract summaries or exam-oriented notes
- ❌ Manual note-taking is time-consuming and error-prone
- ❌ No automatic way to generate quizzes for self-assessment

### ✅ Our Solution

This tool addresses all these challenges by providing:
- ✅ Instant summaries and structured learning points
- ✅ AI-generated notes from actual video content
- ✅ Easy revision with highlighted key points
- ✅ 10 quiz questions for comprehensive self-assessment
- ✅ Complete learning package in minutes

---

## 🏗️ Project Structure

```
SmartVideoLearningTool/
│
├── backend/                    # Flask backend server
│   ├── app.py                 # Main Flask application
│   ├── youtube_service.py     # YouTube transcript extractor
│   ├── ai_engine.py           # OpenAI connection handler
│   ├── summarizer.py          # Summary generator
│   ├── keypoints.py           # Key points generator
│   ├── quiz_generator.py      # Quiz question generator
│   ├── formatter.py           # Output formatter
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # Web interface
│   ├── index.html             # Main HTML page
│   ├── style.css              # Styling and design
│   └── script.js              # Frontend logic and API calls
│
├── data/
│   └── transcripts/           # Saved video transcripts
│
├── models/
│   └── prompts.py             # AI prompt templates
│
└── README.md                  # This file
```

---

## 🔧 Installation & Setup

### Prerequisites

Before running this application, ensure you have:

1. **Python 3.8 or higher** installed
2. **OpenAI API Key** (get it from [OpenAI Platform](https://platform.openai.com/))
3. A modern web browser (Chrome, Firefox, Edge, etc.)

### Step 1: Clone or Download the Project

```powershell
cd C:\Users\navgurukul\OneDrive\Desktop
# Project folder: SmartVideoLearningTool
```

### Step 2: Install Python Dependencies

Open PowerShell and navigate to the backend folder:

```powershell
cd SmartVideoLearningTool\backend
pip install -r requirements.txt
```

**Dependencies installed:**
- `flask` - Web framework
- `flask-cors` - Cross-Origin Resource Sharing
- `youtube-transcript-api` - YouTube transcript extraction
- `openai` - OpenAI API client
- `python-dotenv` - Environment variable management

### Step 3: Configure OpenAI API Key

Create a `.env` file in the `backend` folder:

```powershell
cd backend
New-Item .env -ItemType File
```

Open `.env` file and add your OpenAI API key:

```
OPENAI_API_KEY=your-openai-api-key-here
```

**How to get OpenAI API Key:**
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Go to API Keys section
4. Create a new API key
5. Copy and paste it in the `.env` file

---

## 🚀 Running the Application

### Step 1: Start Backend Server

Open PowerShell and run:

```powershell
cd SmartVideoLearningTool\backend
python app.py
```

You should see:
```
Smart Video Learning Tool - Backend Server
========================================
Server starting on http://localhost:5000

Available endpoints:
  - GET  /              : Health check
  - POST /api/process   : Process video and generate learning package
  - POST /api/transcript: Get transcript only
```

**Keep this terminal window open!**

### Step 2: Open Frontend

Open `frontend\index.html` in your web browser:

**Option 1: Double-click**
- Navigate to `SmartVideoLearningTool\frontend\`
- Double-click on `index.html`

**Option 2: PowerShell command**
```powershell
cd SmartVideoLearningTool\frontend
Start-Process index.html
```

**Option 3: Direct path**
- Open browser and enter: `file:///C:/Users/navgurukul/OneDrive/Desktop/SmartVideoLearningTool/frontend/index.html`

---

## 📖 How to Use

### Step 1: Enter YouTube URL

1. Copy any educational YouTube video URL
   - Example: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
   - Also supports: `https://youtu.be/dQw4w9WgXcQ`

2. Paste it in the input field

### Step 2: Generate Learning Package

1. Click **"Generate Learning Package"** button
2. Wait while the AI processes your video:
   - ⏳ Extracting transcript...
   - ⏳ Generating AI summary...
   - ⏳ Creating quiz questions...
   - ✅ Complete!

### Step 3: Review Content

You'll receive:

1. **📝 AI-Generated Summary**
   - Comprehensive overview of video content
   - Well-structured and easy to understand
   - 200-300 words

2. **💡 Key Learning Points**
   - 5-8 most important takeaways
   - Numbered for easy reference
   - Clear and actionable points

3. **❓ Interactive Quiz**
   - Exactly 10 multiple-choice questions
   - 4 options per question
   - Based on actual video content

### Step 4: Take the Quiz

1. Read each question carefully
2. Select your answer (A, B, C, or D)
3. Click **"Submit Quiz"** when done
4. View your score and feedback
5. See correct/incorrect answers highlighted

### Step 5: Process Another Video

Click **"Process Another Video"** to start over!

---

## 🛠️ API Endpoints

### 1. Health Check
```
GET http://localhost:5000/
```
Returns API status

### 2. Process Video (Main Endpoint)
```
POST http://localhost:5000/api/process
Content-Type: application/json

{
  "youtube_url": "https://www.youtube.com/watch?v=..."
}
```

**Response:**
```json
{
  "success": true,
  "video_id": "...",
  "transcript": {
    "text": "...",
    "word_count": 1234
  },
  "summary": {
    "text": "..."
  },
  "key_points": {
    "points": ["...", "..."],
    "total": 5
  },
  "quiz": {
    "questions": [
      {
        "question": "...",
        "options": {
          "A": "...",
          "B": "...",
          "C": "...",
          "D": "..."
        },
        "correct_answer": "A"
      }
    ],
    "total_questions": 10
  }
}
```

### 3. Get Transcript Only
```
POST http://localhost:5000/api/transcript
Content-Type: application/json

{
  "youtube_url": "https://www.youtube.com/watch?v=..."
}
```

---

## 🎨 Features Breakdown

### Backend Features

1. **YouTube Service** (`youtube_service.py`)
   - Extracts video ID from various URL formats
   - Downloads transcript using YouTube Transcript API
   - Supports multiple languages (defaults to English)
   - Saves transcripts to `data/transcripts/`

2. **AI Engine** (`ai_engine.py`)
   - Connects to OpenAI GPT-3.5-turbo
   - Handles API authentication
   - Manages token usage
   - Error handling for API issues

3. **Summarizer** (`summarizer.py`)
   - Generates 200-300 word summaries
   - Uses custom AI prompts
   - Structures content logically

4. **Key Points Generator** (`keypoints.py`)
   - Extracts 5-8 key learning points
   - Identifies core concepts
   - Formats as numbered list

5. **Quiz Generator** (`quiz_generator.py`)
   - Creates exactly 10 MCQ questions
   - Generates 4 options per question
   - Identifies correct answers
   - Parses AI responses intelligently

6. **Formatter** (`formatter.py`)
   - Structures complete learning package
   - Handles errors gracefully
   - Saves data in JSON format

### Frontend Features

1. **Modern UI Design**
   - Gradient backgrounds
   - Card-based layout
   - Smooth animations
   - Responsive design

2. **User Experience**
   - Real-time progress tracking
   - Loading animations
   - Error handling with friendly messages
   - Smooth scrolling

3. **Interactive Quiz**
   - Radio button selections
   - Answer validation
   - Color-coded feedback (green for correct, red for incorrect)
   - Score calculation with percentage
   - Motivational messages

---

## 🔍 Troubleshooting

### Backend Issues

**Problem: "OPENAI_API_KEY not found"**
- Solution: Make sure `.env` file exists in `backend` folder
- Verify API key is correctly formatted
- No quotes needed around the key

**Problem: "Failed to extract transcript"**
- Solution: Video might not have captions
- Try another video with subtitles
- Check if URL is correct

**Problem: "Rate limit exceeded"**
- Solution: OpenAI free tier has limits
- Wait a few minutes and try again
- Consider upgrading your OpenAI plan

### Frontend Issues

**Problem: "API not reachable"**
- Solution: Make sure backend server is running
- Check terminal for `Running on http://localhost:5000`
- Verify no firewall is blocking port 5000

**Problem: Quiz not showing**
- Solution: AI might have failed to generate questions
- Check browser console for errors
- Try processing the video again

---

## 💡 Tips for Best Results

1. **Choose Quality Videos**
   - Educational content works best
   - Videos with clear speech
   - Videos with subtitles/captions

2. **Video Length**
   - 5-30 minute videos work best
   - Too long videos might take more time
   - Very short videos might not have enough content

3. **Quiz Accuracy**
   - AI generates questions based on transcript
   - Quality depends on video content clarity
   - Review answers even if you score high

---

## 🔐 Security & Privacy

- Your API key is stored locally in `.env` file
- Transcripts are saved locally in `data/transcripts/`
- No data is shared with third parties
- OpenAI API usage follows their privacy policy

---

## 📝 License

This project is for educational purposes.

---

## 🤝 Support

For issues or questions:
1. Check troubleshooting section
2. Verify all dependencies are installed
3. Ensure OpenAI API key is valid
4. Check terminal/console for error messages

---

## 🎉 Enjoy Learning!

Transform your YouTube learning experience with AI-powered insights!

**Made with ❤️ for better education**

---

## 📊 Technology Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **AI**: OpenAI GPT-3.5-turbo
- **APIs**: YouTube Transcript API, OpenAI API
- **Storage**: Local JSON files

---

## 🚧 Future Enhancements (Coming Soon)

- [ ] Support for multiple languages
- [ ] Video duration estimation
- [ ] Export to PDF/Word
- [ ] Flashcard generation
- [ ] Study timer integration
- [ ] User accounts and history
- [ ] Mobile app version

---

**Version**: 1.0.0  
**Last Updated**: January 2026
