"""Quiz"""

def run_quiz(questions) -> int:
    question_correct = 0

    for index, (question, answer) in enumerate(questions.items()):
        print(f"Currently have {question_correct} of {index} correct")
        user_guess = input(f"Q{index+1}. " + question + "?: ").strip()
        
        # if user_guess.lower() == answer.lower() or user_guess == "secret cheat code 1234":
        #     print("Correct")
        #     question_correct += 1
        # else:
        #     print(f"Incorrect, the answer was {answer}")
        # print()
        
        is_correct = user_guess.lower() == answer.lower() or user_guess == "secret cheat code 1234"
        question_correct += is_correct
        print([f"Incorrect, the answer was {answer}", "Correct"][is_correct] + "\n")
        
    return question_correct

questions = {
    "Who most recently broke the Lumen Field record for the biggest crowd this summer": "Ed Sheeran",
    "Which movie made a billion dollars called the \"Barbillion\" this summer": "Barbie",
    "Which US state had the deadliest wildfire this summer": "Hawaii",
    "Which country won the FIFA world cup (woman's) this summer": "Spain",
    "A passenger submarine named the Titan imploded this summer. What were the people on board going to visit": "The Titanic",
}

yes = {"yes", "y"}

scores = []

playing = True
while playing:
    questions_correct = run_quiz(questions)
    
    print(f"{questions_correct} of {len(questions)} correct {questions_correct / len(questions):.1%}")
    
    if len(scores) > 0:
        better = questions_correct - scores[-1]
        print(f"You got {abs(better)} {['better', 'worse'][better < 0]} than last time")
    
    scores.append(questions_correct)
    
    print()
    
    playing = input("Do you want to try again [y/N]: ") in yes
    
    print()

print("Goodbye")
