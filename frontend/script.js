// Smart Video Learning Tool - Frontend JavaScript
// Handles all UI interactions and API calls

// Configuration
const API_BASE_URL = 'http://localhost:5000';

// State management
let currentQuizData = null;
let userAnswers = {};

// DOM Elements
const elements = {
    youtubeUrl: document.getElementById('youtubeUrl'),
    processBtn: document.getElementById('processBtn'),
    inputSection: document.getElementById('inputSection'),
    loadingSection: document.getElementById('loadingSection'),
    errorSection: document.getElementById('errorSection'),
    resultsSection: document.getElementById('resultsSection'),
    loadingStatus: document.getElementById('loadingStatus'),
    progressBar: document.getElementById('progressBar'),
    errorMessage: document.getElementById('errorMessage'),
    summaryContent: document.getElementById('summaryContent'),
    keypointsContent: document.getElementById('keypointsContent'),
    quizContent: document.getElementById('quizContent'),
    submitQuizBtn: document.getElementById('submitQuizBtn'),
    quizResults: document.getElementById('quizResults'),
    scoreValue: document.getElementById('scoreValue'),
    scoreMessage: document.getElementById('scoreMessage')
};

// Event Listeners
elements.processBtn.addEventListener('click', handleProcessVideo);
elements.youtubeUrl.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleProcessVideo();
    }
});
elements.submitQuizBtn.addEventListener('click', handleSubmitQuiz);

// Main function to process video
async function handleProcessVideo() {
    const youtubeUrl = elements.youtubeUrl.value.trim();
    
    // Validate URL
    if (!youtubeUrl) {
        showError('Please enter a YouTube URL');
        return;
    }
    
    if (!isValidYouTubeUrl(youtubeUrl)) {
        showError('Please enter a valid YouTube URL');
        return;
    }
    
    // Show loading state
    showLoading();
    
    try {
        // Simulate progress
        updateProgress(10, 'Extracting video transcript...');
        
        // Call API
        const response = await fetch(`${API_BASE_URL}/api/process`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ youtube_url: youtubeUrl })
        });
        
        updateProgress(50, 'Generating AI summary and key points...');
        
        const data = await response.json();
        
        if (!response.ok || !data.success) {
            throw new Error(data.error || 'Failed to process video');
        }
        
        updateProgress(90, 'Creating quiz questions...');
        
        // Wait a moment for better UX
        await new Promise(resolve => setTimeout(resolve, 500));
        
        updateProgress(100, 'Complete!');
        
        // Display results
        displayResults(data);
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'An unexpected error occurred. Please try again.');
    }
}

// Validate YouTube URL
function isValidYouTubeUrl(url) {
    const patterns = [
        /^(https?:\/\/)?(www\.)?youtube\.com\/watch\?v=[\w-]{11}/,
        /^(https?:\/\/)?(www\.)?youtu\.be\/[\w-]{11}/,
        /^(https?:\/\/)?(www\.)?youtube\.com\/embed\/[\w-]{11}/
    ];
    
    return patterns.some(pattern => pattern.test(url));
}

// Show loading state
function showLoading() {
    elements.inputSection.classList.add('hidden');
    elements.errorSection.classList.add('hidden');
    elements.resultsSection.classList.add('hidden');
    elements.loadingSection.classList.remove('hidden');
    elements.progressBar.style.width = '0%';
}

// Update progress
function updateProgress(percent, message) {
    elements.progressBar.style.width = `${percent}%`;
    elements.loadingStatus.textContent = message;
}

// Show error
function showError(message) {
    elements.loadingSection.classList.add('hidden');
    elements.resultsSection.classList.add('hidden');
    elements.errorSection.classList.remove('hidden');
    elements.errorMessage.textContent = message;
}

// Display results
function displayResults(data) {
    // Hide loading
    elements.loadingSection.classList.add('hidden');
    
    // Display summary
    displaySummary(data.summary);
    
    // Display key points
    displayKeyPoints(data.key_points);
    
    // Display quiz
    displayQuiz(data.quiz);
    
    // Show results section
    elements.resultsSection.classList.remove('hidden');
    
    // Scroll to results
    elements.resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Display summary
function displaySummary(summaryData) {
    const summaryText = summaryData.text || 'Summary not available';
    elements.summaryContent.innerHTML = `
        <p>${formatText(summaryText)}</p>
    `;
}

// Display key points
function displayKeyPoints(keypointsData) {
    const keypoints = keypointsData.points || [];
    
    if (keypoints.length === 0) {
        elements.keypointsContent.innerHTML = '<p>No key points available</p>';
        return;
    }
    
    const keypointsHtml = keypoints.map((point, index) => `
        <div class="keypoint-item">
            <div class="keypoint-number">${index + 1}</div>
            <div class="keypoint-text">${point}</div>
        </div>
    `).join('');
    
    elements.keypointsContent.innerHTML = keypointsHtml;
}

// Display quiz
function displayQuiz(quizData) {
    const questions = quizData.questions || [];
    currentQuizData = questions;
    userAnswers = {};
    
    if (questions.length === 0) {
        elements.quizContent.innerHTML = '<p>No quiz questions available</p>';
        elements.submitQuizBtn.style.display = 'none';
        return;
    }
    
    const quizHtml = questions.map((q, index) => `
        <div class="quiz-question" data-question-index="${index}">
            <div class="question-header">
                <span class="question-number">Question ${index + 1}:</span>
                <span>${q.question}</span>
            </div>
            <div class="quiz-options">
                ${Object.entries(q.options).map(([key, value]) => `
                    <label class="quiz-option" data-option="${key}">
                        <input 
                            type="radio" 
                            name="question_${index}" 
                            value="${key}"
                            onchange="recordAnswer(${index}, '${key}')"
                        >
                        <span class="option-label"><strong>${key})</strong> ${value}</span>
                    </label>
                `).join('')}
            </div>
        </div>
    `).join('');
    
    elements.quizContent.innerHTML = quizHtml;
    elements.submitQuizBtn.style.display = 'inline-flex';
    elements.quizResults.classList.add('hidden');
}

// Record user answer
function recordAnswer(questionIndex, answer) {
    userAnswers[questionIndex] = answer;
}

// Handle quiz submission
function handleSubmitQuiz() {
    // Check if all questions are answered
    const totalQuestions = currentQuizData.length;
    const answeredQuestions = Object.keys(userAnswers).length;
    
    if (answeredQuestions < totalQuestions) {
        alert(`Please answer all questions. You have answered ${answeredQuestions} out of ${totalQuestions} questions.`);
        return;
    }
    
    // Calculate score
    let score = 0;
    
    currentQuizData.forEach((question, index) => {
        const userAnswer = userAnswers[index];
        const correctAnswer = question.correct_answer;
        
        // Highlight correct/incorrect answers
        const questionElement = document.querySelector(`[data-question-index="${index}"]`);
        const options = questionElement.querySelectorAll('.quiz-option');
        
        options.forEach(option => {
            const optionKey = option.dataset.option;
            
            if (optionKey === correctAnswer) {
                option.classList.add('correct');
            }
            
            if (optionKey === userAnswer && optionKey !== correctAnswer) {
                option.classList.add('incorrect');
            }
            
            // Disable further changes
            const radio = option.querySelector('input[type="radio"]');
            radio.disabled = true;
        });
        
        // Count correct answers
        if (userAnswer === correctAnswer) {
            score++;
        }
    });
    
    // Display score
    displayScore(score, totalQuestions);
    
    // Disable submit button
    elements.submitQuizBtn.disabled = true;
    elements.submitQuizBtn.textContent = 'Quiz Submitted';
    
    // Scroll to results
    elements.quizResults.scrollIntoView({ behavior: 'smooth' });
}

// Display quiz score
function displayScore(score, total) {
    const percentage = (score / total) * 100;
    
    let message = '';
    if (percentage >= 90) {
        message = '🎉 Excellent! You have mastered this content!';
    } else if (percentage >= 70) {
        message = '👍 Great job! You understand most of the concepts!';
    } else if (percentage >= 50) {
        message = '👌 Good effort! Review the key points to improve!';
    } else {
        message = '📚 Keep learning! Review the summary and try again!';
    }
    
    elements.scoreValue.textContent = score;
    elements.scoreMessage.textContent = message;
    elements.quizResults.classList.remove('hidden');
}

// Format text (convert newlines to paragraphs)
function formatText(text) {
    return text
        .split('\n\n')
        .map(para => para.trim())
        .filter(para => para.length > 0)
        .map(para => `<p>${para.replace(/\n/g, '<br>')}</p>`)
        .join('');
}

// Reset app
function resetApp() {
    elements.youtubeUrl.value = '';
    elements.inputSection.classList.remove('hidden');
    elements.loadingSection.classList.add('hidden');
    elements.errorSection.classList.add('hidden');
    elements.resultsSection.classList.add('hidden');
    currentQuizData = null;
    userAnswers = {};
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Check API health on load
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/`);
        const data = await response.json();
        console.log('API Status:', data);
    } catch (error) {
        console.warn('API not reachable. Make sure backend server is running on http://localhost:5000');
    }
}

// Initialize
checkAPIHealth();

console.log('Smart Video Learning Tool - Frontend Loaded ✓');
