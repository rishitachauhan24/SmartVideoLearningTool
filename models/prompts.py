"""
AI Prompt Templates for Smart Video Learning Tool
"""

SUMMARY_PROMPT = """
You are an expert educational content summarizer. Based on the following video transcript, create a comprehensive, well-structured summary.

**Requirements:**
- Write a clear and concise summary (200-300 words)
- Organize the content logically
- Include all important concepts and ideas
- Use proper headings and bullet points where appropriate
- Make it easy to understand for students

**Transcript:**
{transcript}

**Summary:**
"""

KEYPOINTS_PROMPT = """
You are an expert educator analyzing educational content. Based on the following video transcript, identify and extract the most important learning points.

**Requirements:**
- Extract exactly 5-8 key learning points
- Each point should be clear, specific, and actionable
- Focus on core concepts and takeaways
- Format each point as a complete sentence
- Number each point (1, 2, 3, etc.)

**Transcript:**
{transcript}

**Key Learning Points:**
"""

QUIZ_PROMPT = """
You are an expert quiz creator for educational content. Based on the following video transcript, create exactly 10 multiple-choice questions (MCQs).

**Requirements:**
- Create exactly 10 questions
- Each question must have 4 options (A, B, C, D)
- Only one option should be correct
- Questions should test understanding, not just memorization
- Cover different parts of the content
- Indicate the correct answer for each question

**Format for each question:**
Question X: [Question text]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
Correct Answer: [A/B/C/D]

**Transcript:**
{transcript}

**Quiz (10 Questions):**
"""
