import json
import random
from typing import List, Dict

class EvaluationQAGenerator:
    def __init__(self):
        self.qa_pairs = []
    
    def generate_evaluation_qa(self) -> List[Dict]:
        """Generate comprehensive Q&A pairs for LLM evaluation"""
        
        # Basic Coverage Questions
        basic_coverage = [
            {
                "question": "What is the overall deductible for in-network coverage?",
                "answer": "The overall deductible for in-network coverage is $400 per policy year.",
                "category": "basic_coverage",
                "difficulty": "easy",
                "source_files": ["Summary_of_Benefits.pdf", "Master_Policy.pdf"]
            },
            {
                "question": "What is the out-of-pocket limit for in-network individual coverage?",
                "answer": "The out-of-pocket limit for in-network individual coverage is $1,500 per policy year.",
                "category": "basic_coverage", 
                "difficulty": "easy",
                "source_files": ["Summary_of_Benefits.pdf", "Master_Policy.pdf"]
            },
            {
                "question": "What is the out-of-pocket limit for out-of-network individual coverage?",
                "answer": "The out-of-pocket limit for out-of-network individual coverage is $4,000 per policy year.",
                "category": "basic_coverage",
                "difficulty": "easy", 
                "source_files": ["Summary_of_Benefits.pdf", "Master_Policy.pdf"]
            },
            {
                "question": "What is the family out-of-pocket limit for in-network coverage?",
                "answer": "The family out-of-pocket limit for in-network coverage is $3,000 per policy year.",
                "category": "basic_coverage",
                "difficulty": "easy",
                "source_files": ["Summary_of_Benefits.pdf", "Master_Policy.pdf"]
            },
            {
                "question": "What is the family out-of-pocket limit for out-of-network coverage?",
                "answer": "The family out-of-pocket limit for out-of-network coverage is $8,000 per policy year.",
                "category": "basic_coverage",
                "difficulty": "easy",
                "source_files": ["Summary_of_Benefits.pdf", "Master_Policy.pdf"]
            }
        ]
        
        # Referral and Authorization Questions
        referral_auth = [
            {
                "question": "Do I need a referral to see a gastroenterologist (GI doctor)?",
                "answer": "Yes, you must get a referral from school health services for off-campus care including specialist visits like gastroenterologists. Without a referral, benefits will be paid at out-of-network coverage cost sharing.",
                "category": "referral_auth",
                "difficulty": "medium",
                "source_files": ["Master_Policy.pdf", "Aetna_SH_Major_Medical_Outline_of_Coverage.pdf"]
            },
            {
                "question": "What happens if I don't get a required referral?",
                "answer": "If you don't get a referral when required, the plan will pay covered benefits at the out-of-network coverage cost sharing instead of in-network rates, which means you'll pay significantly more.",
                "category": "referral_auth",
                "difficulty": "medium",
                "source_files": ["Master_Policy.pdf", "Aetna_SH_Major_Medical_Outline_of_Coverage.pdf"]
            },
            {
                "question": "Are there any exceptions to the referral requirement?",
                "answer": "Yes, exceptions include: emergency medical conditions, obstetric and gynecological care, pediatric care, when you're more than 25 miles from school health services, when school health services is closed, annual eye exams, mental health and substance abuse services, women's health services, preventive/routine services, and outpatient lab services.",
                "category": "referral_auth",
                "difficulty": "hard",
                "source_files": ["Master_Policy.pdf", "Aetna_SH_Major_Medical_Outline_of_Coverage.pdf"]
            },
            {
                "question": "Do I need a referral for emergency care?",
                "answer": "No, emergency medical conditions are an exception to the referral requirement. You can go directly to the emergency room without a referral.",
                "category": "referral_auth",
                "difficulty": "easy",
                "source_files": ["Master_Policy.pdf", "Aetna_SH_Major_Medical_Outline_of_Coverage.pdf"]
            }
        ]
        
        # Cost Sharing Questions
        cost_sharing = [
            {
                "question": "What is the copayment for a routine physical exam?",
                "answer": "There is no copayment or policy year deductible for routine physical exams. The plan pays 100% of the negotiated charge for in-network providers.",
                "category": "cost_sharing",
                "difficulty": "easy",
                "source_files": ["Master_Policy.pdf"]
            },
            {
                "question": "What is the copayment for an office visit to a physician or specialist?",
                "answer": "For office visits to a physician or specialist (non-surgical and non-preventive), you pay a $35 copayment, then the plan pays 100% of the balance of the negotiated charge for in-network providers.",
                "category": "cost_sharing",
                "difficulty": "medium",
                "source_files": ["Master_Policy.pdf"]
            },
            {
                "question": "What is the copayment for emergency room visits?",
                "answer": "For emergency room visits, you pay a $100 copayment, then the plan pays 100% of the balance of the negotiated charge for in-network providers.",
                "category": "cost_sharing",
                "difficulty": "medium",
                "source_files": ["Master_Policy.pdf", "Aetna_SH_Major_Medical_Outline_of_Coverage.pdf"]
            },
            {
                "question": "What is the copayment for inpatient surgery?",
                "answer": "For inpatient surgery performed by a surgeon during your stay in a hospital or birthing center, you pay a $100 copayment, then the plan pays 100% of the balance of the negotiated charge for in-network providers.",
                "category": "cost_sharing",
                "difficulty": "medium",
                "source_files": ["Master_Policy.pdf"]
            },
            {
                "question": "What is the copayment for walk-in clinic visits?",
                "answer": "For walk-in clinic visits (non-emergency), you pay a $35 copayment, then the plan pays 100% of the balance of the negotiated charge for in-network providers.",
                "category": "cost_sharing",
                "difficulty": "medium",
                "source_files": ["Master_Policy.pdf"]
            }
        ]
        
        # Prescription Drug Questions
        prescription_drugs = [
            {
                "question": "What is the copayment for generic prescription drugs?",
                "answer": "For generic prescription drugs, you pay a $10 copayment per prescription for in-network pharmacies.",
                "category": "prescription_drugs",
                "difficulty": "easy",
                "source_files": ["Master_Policy.pdf"]
            },
            {
                "question": "What is the copayment for brand name prescription drugs?",
                "answer": "For brand name prescription drugs, you pay a $25 copayment per prescription for in-network pharmacies.",
                "category": "prescription_drugs",
                "difficulty": "easy",
                "source_files": ["Master_Policy.pdf"]
            },
            {
                "question": "What is the copayment for specialty prescription drugs?",
                "answer": "For specialty prescription drugs, you pay a $50 copayment per prescription for in-network pharmacies.",
                "category": "prescription_drugs",
                "difficulty": "medium",
                "source_files": ["Master_Policy.pdf"]
            },
            {
                "question": "What is the annual prescription drug limit?",
                "answer": "I am unable to answer this question at this time. The specific annual prescription drug limit is not clearly stated in the available documents.",
                "category": "prescription_drugs",
                "difficulty": "medium",
                "source_files": ["Master_Policy.pdf"],
                "note": "Unable to find specific annual limit information"
            }
        ]
        
        # Mental Health Questions
        mental_health = [
            {
                "question": "What mental health services are covered?",
                "answer": "Covered mental health services include outpatient mental health services, inpatient mental health services, behavioral health services, substance abuse treatment, and telemedicine consultations for mental health disorders.",
                "category": "mental_health",
                "difficulty": "medium",
                "source_files": ["Master_Policy.pdf"]
            },
            {
                "question": "Do I need a referral for mental health services?",
                "answer": "No, mental health and substance abuse services are exceptions to the referral requirement. You can access these services directly without a referral from school health services.",
                "category": "mental_health",
                "difficulty": "medium",
                "source_files": ["Master_Policy.pdf", "Aetna_SH_Major_Medical_Outline_of_Coverage.pdf"]
            },
            {
                "question": "What is the copayment for mental health office visits?",
                "answer": "I am unable to answer this question at this time. The specific copayment for mental health office visits is not clearly detailed in the available documents.",
                "category": "mental_health",
                "difficulty": "medium",
                "source_files": ["Master_Policy.pdf"],
                "note": "Mental health copayment details not found in available documents"
            }
        ]
        
        # Preventive Care Questions
        preventive_care = [
            {
                "question": "What preventive care services are covered at 100%?",
                "answer": "Preventive care and wellness services are covered at 100% with no copayment or deductible, including routine physical exams, routine cancer screenings, immunizations, and other evidence-based preventive services.",
                "category": "preventive_care",
                "difficulty": "easy",
                "source_files": ["Master_Policy.pdf"]
            },
            {
                "question": "Are annual eye exams covered?",
                "answer": "Yes, annual eye exams are covered and are an exception to the referral requirement. You can get annual eye exams without a referral from school health services.",
                "category": "preventive_care",
                "difficulty": "medium",
                "source_files": ["Master_Policy.pdf", "Aetna_SH_Major_Medical_Outline_of_Coverage.pdf"]
            },
            {
                "question": "What is the copayment for annual eye exams?",
                "answer": "I am unable to answer this question at this time. The specific copayment for annual eye exams is not clearly stated in the available documents.",
                "category": "preventive_care",
                "difficulty": "medium",
                "source_files": ["Master_Policy.pdf"],
                "note": "Eye exam copayment details not found"
            }
        ]
        
        # Emergency Care Questions
        emergency_care = [
            {
                "question": "What should I do in a medical emergency?",
                "answer": "In a medical emergency, you should go to the nearest emergency room immediately. Emergency medical conditions are an exception to the referral requirement, and you don't need prior authorization for emergency care.",
                "category": "emergency_care",
                "difficulty": "easy",
                "source_files": ["Master_Policy.pdf", "Aetna_SH_Major_Medical_Outline_of_Coverage.pdf"]
            },
            {
                "question": "What is the copayment for emergency room visits?",
                "answer": "For emergency room visits, you pay a $100 copayment, then the plan pays 100% of the balance of the negotiated charge for in-network providers.",
                "category": "emergency_care",
                "difficulty": "easy",
                "source_files": ["Master_Policy.pdf", "Aetna_SH_Major_Medical_Outline_of_Coverage.pdf"]
            },
            {
                "question": "What is considered an emergency medical condition?",
                "answer": "I am unable to answer this question at this time. The specific definition of emergency medical conditions is not clearly detailed in the available documents.",
                "category": "emergency_care",
                "difficulty": "medium",
                "source_files": ["Master_Policy.pdf"],
                "note": "Emergency condition definition not found in available documents"
            }
        ]
        
        # Telemedicine Questions
        telemedicine = [
            {
                "question": "Are telemedicine visits covered?",
                "answer": "Yes, telemedicine visits are covered. All in-person physician or specialist office visits that are covered benefits are also covered if you use telemedicine instead. Telemedicine may have different cost sharing than other outpatient services.",
                "category": "telemedicine",
                "difficulty": "medium",
                "source_files": ["Master_Policy.pdf"]
            },
            {
                "question": "What types of telemedicine services are available?",
                "answer": "Telemedicine services are available for physician and specialist consultations, mental health services, substance abuse treatment, and behavioral health services.",
                "category": "telemedicine",
                "difficulty": "medium",
                "source_files": ["Master_Policy.pdf"]
            },
            {
                "question": "What is the copayment for telemedicine visits?",
                "answer": "I am unable to answer this question at this time. The specific copayment for telemedicine visits is not clearly detailed in the available documents, though it may differ from in-person visits.",
                "category": "telemedicine",
                "difficulty": "medium",
                "source_files": ["Master_Policy.pdf"],
                "note": "Telemedicine copayment details not specified"
            }
        ]
        
        # Complex Scenario Questions
        complex_scenarios = [
            {
                "question": "I'm a student and my spouse needs to see a specialist. Do they need a referral?",
                "answer": "No, your covered dependents (including your spouse) do not use school health services for care, so they don't need to get referrals. They can go directly to in-network providers.",
                "category": "complex_scenarios",
                "difficulty": "hard",
                "source_files": ["Master_Policy.pdf", "Aetna_SH_Major_Medical_Outline_of_Coverage.pdf"]
            },
            {
                "question": "I'm more than 25 miles away from campus and need to see a doctor. Do I need a referral?",
                "answer": "No, when you are more than 25 miles away from school health services, you don't need a referral. This is one of the exceptions to the referral requirement.",
                "category": "complex_scenarios",
                "difficulty": "hard",
                "source_files": ["Master_Policy.pdf", "Aetna_SH_Major_Medical_Outline_of_Coverage.pdf"]
            },
            {
                "question": "What happens if I go to an out-of-network provider without a referral?",
                "answer": "If you go to an out-of-network provider without a required referral, the plan will pay benefits at out-of-network coverage cost sharing, which means you'll pay 70% of the recognized charge instead of the lower in-network rates.",
                "category": "complex_scenarios",
                "difficulty": "hard",
                "source_files": ["Master_Policy.pdf", "Aetna_SH_Major_Medical_Outline_of_Coverage.pdf"]
            },
            {
                "question": "What if school health services is closed and I need to see a specialist?",
                "answer": "When school health services is closed, you don't need a referral. This is one of the exceptions to the referral requirement, so you can go directly to a specialist.",
                "category": "complex_scenarios",
                "difficulty": "hard",
                "source_files": ["Master_Policy.pdf", "Aetna_SH_Major_Medical_Outline_of_Coverage.pdf"]
            }
        ]
        
        # Coverage Limits and Exclusions Questions
        coverage_limits = [
            {
                "question": "What is the maximum number of physical therapy visits covered?",
                "answer": "I am unable to answer this question at this time. The specific limit for physical therapy visits is not clearly stated in the available documents.",
                "category": "coverage_limits",
                "difficulty": "medium",
                "source_files": ["Master_Policy.pdf"],
                "note": "Physical therapy visit limits not found in available documents"
            },
            {
                "question": "Are cosmetic procedures covered?",
                "answer": "I am unable to answer this question at this time. The specific coverage details for cosmetic procedures are not clearly detailed in the available documents.",
                "category": "coverage_limits",
                "difficulty": "medium",
                "source_files": ["Master_Policy.pdf"],
                "note": "Cosmetic procedure coverage details not found"
            },
            {
                "question": "What is the coverage for dental services?",
                "answer": "I am unable to answer this question at this time. The specific coverage details for dental services are not clearly detailed in the available documents.",
                "category": "coverage_limits",
                "difficulty": "medium",
                "source_files": ["Master_Policy.pdf"],
                "note": "Dental coverage details not found in available documents"
            }
        ]
        
        # Combine all categories
        all_qa_pairs = (basic_coverage + referral_auth + cost_sharing + 
                       prescription_drugs + mental_health + preventive_care + 
                       emergency_care + telemedicine + complex_scenarios + coverage_limits)
        
        return all_qa_pairs
    
    def save_evaluation_dataset(self, filename: str = "evaluation_qa_dataset.json"):
        """Save the evaluation dataset to a JSON file"""
        qa_pairs = self.generate_evaluation_qa()
        
        # Add metadata
        dataset = {
            "metadata": {
                "description": "Evaluation Q&A dataset for LLM performance testing on Aetna student health insurance PDFs",
                "total_questions": len(qa_pairs),
                "categories": list(set([qa["category"] for qa in qa_pairs])),
                "difficulty_levels": list(set([qa["difficulty"] for qa in qa_pairs])),
                "source_files": ["Master_Policy.pdf", "Summary_of_Benefits.pdf", "Aetna_SH_Major_Medical_Outline_of_Coverage.pdf"],
                "generated_date": "2025-01-27",
                "notes": "Questions marked as 'unable to answer' indicate information not found in available documents"
            },
            "questions": qa_pairs
        }
        
        with open(filename, 'w') as f:
            json.dump(dataset, f, indent=2)
        
        return dataset

def main():
    generator = EvaluationQAGenerator()
    dataset = generator.save_evaluation_dataset()
    
    print(f"Generated {dataset['metadata']['total_questions']} evaluation Q&A pairs")
    print(f"Categories: {', '.join(dataset['metadata']['categories'])}")
    print(f"Difficulty levels: {', '.join(dataset['metadata']['difficulty_levels'])}")
    
    # Count questions that cannot be answered
    unable_to_answer = [qa for qa in dataset['questions'] if 'note' in qa]
    print(f"Questions unable to answer confidently: {len(unable_to_answer)}")
    
    # Print sample questions
    print("\nSample Questions:")
    for i, qa in enumerate(dataset['questions'][:5]):
        print(f"\n{i+1}. {qa['question']}")
        print(f"   Answer: {qa['answer']}")
        print(f"   Category: {qa['category']}, Difficulty: {qa['difficulty']}")
        if 'note' in qa:
            print(f"   Note: {qa['note']}")

if __name__ == "__main__":
    main()
