import unittest
from omr_processor import OMRProcessor
from answer_keys import ANSWER_KEY

class TestOMRSystem(unittest.TestCase):
    
    def setUp(self):
        self.processor = OMRProcessor(ANSWER_KEY)
    
    def test_answer_key_completeness(self):
        """Test that answer key has all 100 questions"""
        self.assertEqual(len(ANSWER_KEY), 100)
        for i in range(1, 101):
            self.assertIn(i, ANSWER_KEY)
    
    def test_answer_key_values(self):
        """Test that answer key values are valid options"""
        valid_options = {'a', 'b', 'c', 'd'}
        for q_num, answer in ANSWER_KEY.items():
            self.assertIn(answer, valid_options, f"Invalid answer for Q{q_num}: {answer}")
    
    def test_processor_initialization(self):
        """Test that processor initializes correctly with answer key"""
        self.assertEqual(self.processor.answer_key, ANSWER_KEY)
    
    def test_evaluate_answers_correct(self):
        """Test evaluation with all correct answers"""
        perfect_answers = {q: answer for q, answer in ANSWER_KEY.items()}
        score, results = self.processor.evaluate_answers(perfect_answers)
        self.assertEqual(score, 100)
        for q_num, result in results.items():
            self.assertEqual(result['status'], 'Correct')
    
    def test_evaluate_answers_incorrect(self):
        """Test evaluation with all incorrect answers"""
        wrong_answers = {q: 'x' if answer == 'a' else 'a' for q, answer in ANSWER_KEY.items()}
        score, results = self.processor.evaluate_answers(wrong_answers)
        self.assertEqual(score, 0)
        for q_num, result in results.items():
            self.assertEqual(result['status'], 'Incorrect')
    
    def test_evaluate_answers_mixed(self):
        """Test evaluation with mixed correct/incorrect answers"""
        mixed_answers = {}
        expected_score = 0
        
        for q_num, correct_answer in ANSWER_KEY.items():
            if q_num % 2 == 0:  # Even questions: correct
                mixed_answers[q_num] = correct_answer
                expected_score += 1
            else:  # Odd questions: incorrect
                mixed_answers[q_num] = 'x' if correct_answer == 'a' else 'a'
        
        score, results = self.processor.evaluate_answers(mixed_answers)
        self.assertEqual(score, expected_score)
    
    def test_evaluate_answers_not_attempted(self):
        """Test evaluation with not attempted questions"""
        partial_answers = {q: ANSWER_KEY[q] for q in range(1, 51)}  # First 50 attempted
        for q in range(51, 101):  # Last 50 not attempted
            partial_answers[q] = None
        
        score, results = self.processor.evaluate_answers(partial_answers)
        self.assertEqual(score, 50)
        
        for q in range(1, 51):
            self.assertEqual(results[q]['status'], 'Correct')
        
        for q in range(51, 101):
            self.assertEqual(results[q]['status'], 'Not Attempted')

if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)