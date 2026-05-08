OMR Evaluation System

A professional web-based Optical Mark Recognition (OMR) system that automatically scans, evaluates, and scores OMR sheets using computer vision and machine learning.

 🌐 Live Demo
**Video Demo** (https://youtu.be/lFu0LwnTESo)
**Try it now:** [OMR Evaluation System Web App](https://alokgodhankar-omr-evaluation-system.streamlit.app)
📋 Features

- ✅ **Automatic OMR Sheet Detection** - Uses OpenCV for image processing
- ✅ **Answer Recognition** - Detects marked bubbles accurately
- ✅ **Score Calculation** - Compares with answer key automatically
- ✅ **Web Interface** - User-friendly Streamlit web application
- ✅ **Real-time Processing** - Instant results after upload
- ✅ **Detailed Analytics** - Question-wise performance analysis
- ✅ **Report Generation** - Downloadable evaluation reports

🎯 Use Cases
Educational Institutions - Exam paper evaluation
Competitive Exams - Quick result processing
Surveys & Feedback - Data collection forms
Research Studies - Data analysis and collection

🏗️ How It Works

1. **Upload** an image of filled OMR sheet
2. **System processes** the image using computer vision
3. **Detects marked answers** for each question
4. **Compares** with provided answer key
5. **Calculates score** and generates detailed report
6. **Displays results** with correct/incorrect answers

 🛠️ Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **Computer Vision**: OpenCV
- **Image Processing**: Pillow (PIL)
- **Numerical Computing**: NumPy
- **Deployment**: Streamlit Cloud

📁 Project Structure
omr-evaluation-system/
├── web_app.py # Main Streamlit web application
├── omr_processor.py # Core OMR processing logic
├── answer_keys.py # Answer key configuration
├── requirements.txt # Python dependencies
├── runtime.txt # Python version specification
└── README.md # Project documentation

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Git

  ### Local Installation

#Clone the repository
git clone https://github.com/alokgodhankar/omr-evaluation-system.git
cd omr-evaluation-system

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run web_app.py


📈 Performance
Processes 100 questions in under 10 seconds
Handles multiple simultaneous users
Works with various image qualities
Accurate bubble detection algorithm

🤝 Contributing
We welcome contributions! Please feel free to:
Fork the repository
Create a feature branch
Make your changes
Submit a pull request

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🆘 Support
If you encounter any issues:
Check the live demo
Review the documentation above
Create an issue on GitHub

📞 Contact
Developer: Alok Godhankar
GitHub: alokgodhankar
Project Link: https://github.com/alokgodhankar/omr-evaluation-system
