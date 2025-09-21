import streamlit as st
import cv2
import numpy as np
from PIL import Image
import tempfile
import os
from omr_processor import OMRProcessor
from answer_keys import ANSWER_KEY

# Set page config
st.set_page_config(
    page_title="Professional OMR Evaluation System",
    page_icon="📝",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .score-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .correct {
        color: green;
        font-weight: bold;
    }
    .incorrect {
        color: red;
        font-weight: bold;
    }
    .not-attempted {
        color: gray;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">📝 Professional OMR Evaluation System</h1>', unsafe_allow_html=True)
    
    # File upload section
    st.header("📤 Upload OMR Sheet")
    uploaded_file = st.file_uploader(
        "Choose an OMR sheet image (JPG, JPEG, PNG)",
        type=["jpg", "jpeg", "png"],
        help="Upload a clear image of the filled OMR sheet"
    )
    
    if uploaded_file is not None:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_image_path = tmp_file.name
        
        try:
            # Initialize OMR processor
            processor = OMRProcessor(ANSWER_KEY)
            
            # Process the OMR sheet
            with st.spinner("🔍 Processing OMR sheet..."):
                results = processor.process_omr_sheet(temp_image_path)
            
            # Display results
            st.success("✅ OMR sheet processed successfully!")
            
            # Score card
            st.header("📊 Results")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Score", f"{results['total_score']}/100")
            
            with col2:
                percentage = (results['total_score'] / 100) * 100
                st.metric("Percentage", f"{percentage:.2f}%")
            
            with col3:
                attempted = sum(1 for q, res in results['detailed_results'].items() 
                              if res['status'] != 'Not Attempted')
                st.metric("Attempted", f"{attempted}/100")
            
            # Progress bar
            st.progress(results['total_score'] / 100)
            
            # Detailed results
            st.header("📋 Detailed Analysis")
            
            # Incorrect questions
            incorrect_questions = [
                q for q, res in results['detailed_results'].items() 
                if res['status'] == 'Incorrect'
            ]
            
            if incorrect_questions:
                st.warning(f"❌ Incorrect Answers: {len(incorrect_questions)}")
                st.write(", ".join(map(str, incorrect_questions)))
            else:
                st.success("🎉 All attempted answers are correct!")
            
            # Not attempted questions
            not_attempted = [
                q for q, res in results['detailed_results'].items() 
                if res['status'] == 'Not Attempted'
            ]
            
            if not_attempted:
                st.info(f"📝 Not Attempted: {len(not_attempted)} questions")
            
            # Processed image
            st.header("🖼️ Processed Image")
            st.image(results['processed_image'], caption="Thresholded OMR Sheet", use_column_width=True)
            
            # Detailed question view
            st.header("🔍 Question-wise Results")
            
            # Create tabs for different question ranges
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["1-20", "21-40", "41-60", "61-80", "81-100"])
            
            tabs = [tab1, tab2, tab3, tab4, tab5]
            
            for i, tab in enumerate(tabs):
                start_q = i * 20 + 1
                end_q = start_q + 19
                
                with tab:
                    st.subheader(f"Questions {start_q}-{end_q}")
                    
                    for q_num in range(start_q, end_q + 1):
                        res = results['detailed_results'][q_num]
                        
                        if res['status'] == 'Correct':
                            st.write(f"Q{q_num}: ✅ Correct (Marked: {res['marked'].upper()})")
                        elif res['status'] == 'Incorrect':
                            st.write(f"Q{q_num}: ❌ Incorrect (Marked: {res['marked'].upper()}, Correct: {res['correct'].upper()})")
                        else:
                            st.write(f"Q{q_num}: ⏭️ Not Attempted")
            
            # Download report
            st.header("📥 Download Results")
            report = processor.generate_report(results)
            
            st.download_button(
                label="📄 Download Evaluation Report",
                data=report,
                file_name="omr_evaluation_report.txt",
                mime="text/plain"
            )
            
        except Exception as e:
            st.error(f"❌ Error processing OMR sheet: {str(e)}")
            st.info("Please ensure the image is clear and properly aligned.")
        
        finally:
            # Clean up temporary file
            os.unlink(temp_image_path)
    
    else:
        # Instructions
        st.info("""
        ### 📋 Instructions:
        1. Upload a clear image of the filled OMR sheet
        2. Ensure the image is well-lit and properly aligned
        3. The system will automatically detect and evaluate the answers
        4. View detailed results and download the evaluation report
        """)

if __name__ == "__main__":
    main()