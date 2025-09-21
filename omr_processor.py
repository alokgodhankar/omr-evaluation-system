import cv2
import numpy as np
import json

class OMRProcessor:
    def __init__(self, answer_key):
        self.answer_key = answer_key
        
    def preprocess_image(self, image):
        """Preprocess the image for OMR detection"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        return thresh

    def detect_bubbles(self, thresh):
        """Detect bubbles and extract answers"""
        height, width = thresh.shape
        bubbles = {}
        
        # Define grid parameters (5 columns, 20 rows)
        cols, rows = 5, 20
        col_width = width // cols
        row_height = height // rows
        
        for col in range(cols):
            for row in range(rows):
                q_num = col * rows + row + 1
                
                # Define bubble area for this question
                x_start = col * col_width
                y_start = row * row_height
                x_end = x_start + col_width
                y_end = y_start + row_height
                
                # Extract the bubble region
                bubble_region = thresh[y_start:y_end, x_start:x_end]
                
                # Split into 4 options (A, B, C, D)
                option_height = row_height // 4
                options_intensity = {}
                
                for opt_idx, option in enumerate(['a', 'b', 'c', 'd']):
                    y_opt_start = opt_idx * option_height
                    y_opt_end = y_opt_start + option_height
                    
                    option_region = bubble_region[y_opt_start:y_opt_end, :]
                    intensity = np.sum(option_region) / 255  # Count white pixels
                    options_intensity[option] = intensity
                
                bubbles[q_num] = options_intensity
        
        return bubbles

    def extract_answers(self, bubbles):
        """Extract answers from bubble intensities"""
        answers = {}
        for q_num, options in bubbles.items():
            # Find option with maximum intensity (marked bubble)
            if options:
                marked_option = max(options.items(), key=lambda x: x[1])[0]
                # Check if bubble is actually marked (above threshold)
                if options[marked_option] > 50:  # Threshold for marked bubble
                    answers[q_num] = marked_option
                else:
                    answers[q_num] = None  # No bubble marked
            else:
                answers[q_num] = None
        
        return answers

    def evaluate_answers(self, extracted_answers):
        """Evaluate extracted answers against answer key"""
        results = {}
        score = 0
        
        for q_num, student_answer in extracted_answers.items():
            correct_answer = self.answer_key.get(q_num)
            
            if student_answer is None:
                results[q_num] = {
                    "status": "Not Attempted",
                    "marked": "None",
                    "correct": correct_answer,
                    "is_correct": False
                }
            elif student_answer == correct_answer:
                results[q_num] = {
                    "status": "Correct",
                    "marked": student_answer,
                    "correct": correct_answer,
                    "is_correct": True
                }
                score += 1
            else:
                results[q_num] = {
                    "status": "Incorrect",
                    "marked": student_answer,
                    "correct": correct_answer,
                    "is_correct": False
                }
        
        return score, results

    def process_omr_sheet(self, image_path):
        """Main method to process OMR sheet"""
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image from path: {image_path}")
        
        # Preprocess image
        processed_image = self.preprocess_image(image)
        
        # Detect bubbles and extract answers
        bubbles = self.detect_bubbles(processed_image)
        extracted_answers = self.extract_answers(bubbles)
        
        # Evaluate answers
        score, detailed_results = self.evaluate_answers(extracted_answers)
        
        return {
            "total_score": score,
            "detailed_results": detailed_results,
            "processed_image": processed_image,
            "extracted_answers": extracted_answers
        }

    def save_results(self, results, output_path):
        """Save results to JSON file"""
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)

    def generate_report(self, results):
        """Generate a text report of the results"""
        report = f"OMR Evaluation Report\n"
        report += f"{'='*50}\n"
        report += f"Total Score: {results['total_score']}/100\n"
        report += f"Percentage: {(results['total_score']/100)*100:.2f}%\n\n"
        
        # Count attempts
        attempted = sum(1 for q, res in results['detailed_results'].items() 
                       if res['status'] != 'Not Attempted')
        report += f"Questions Attempted: {attempted}/100\n\n"
        
        # Incorrect questions
        incorrect = [q for q, res in results['detailed_results'].items() 
                    if res['status'] == 'Incorrect']
        if incorrect:
            report += f"Incorrect Questions ({len(incorrect)}): {', '.join(map(str, incorrect))}\n"
        
        return report