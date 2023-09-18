questions = ["What is the mascot of Seattle Academy?","Who is the teacher who worked at Seattle Academy for 39 years? (first name only)","How many floors does the Middle School have?","What does the 'E' in the STREAM building stand for?","We have End of Tri performances in fall and winter. What is the name for the performances at the end of spring trimester?"]

answers = ["cardinal", "Melinda", "5", "engineering", "curtain call"]


questionsCorrect = 0
questionsAsked = 0

# go through the questions list
for i in range(len(questions)):
    # ask a question
    # get a user response
    userAnswer = input(questions[i] + ": ")

    # check the answer and update the variables
    if userAnswer.lower() == answers[i].lower():
        print("Correct!")
        questionsCorrect += 1
    else:
        print(f"Incorrect! The answer is {answers[i]}.")
    questionsAsked += 1
    print(f"You have correctly answered {questionsCorrect} of {questionsAsked} questions.")

# in addition to fixing the syntax errors, 
# help me out with logical errors!
# Question 2 doesn't work, even when I
# put in the correct answer!
# The questionsAsked get stuck at 0!