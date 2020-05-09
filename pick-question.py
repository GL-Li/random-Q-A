from sys import argv, exit
import glob
import random
from PIL import Image

alldirs = ["R/",
           "python/",
           "clinical_data_science/",
           "sql/",
           "natural_language_processing/",
           "machine_learning/",
           "aws/",
           "web_development/",
           "others"]
if len(argv) == 1:
    subdirs = alldirs
else:
    subdirs = argv[1:]
    for i, sd in enumerate(subdirs):
        if not sd.endswith("/"):
            subdirs[i] = sd + "/"
    if not all(ele in alldirs for ele in subdirs):
        print(f"Please choose from {alldirs}.")
        exit()

random.seed()  # use current system time as seed

# no repeating quesions
answered_questions = []
finished_subdir = []

while True:
    subdirs = [sd for sd in subdirs if sd not in finished_subdir]
    if len(subdirs) == 0:
        print(f"You have answered all questions in {finished_subdir}")
        break
    # number of questions in each subdir and the chance of picking a subdir
    # should be proportional to the number of questions
    n_question_in_subdir = [len(glob.glob(sd + 'Q*')) for sd in subdirs]
    subdir = random.choices(subdirs, n_question_in_subdir)[0]

    questions = glob.glob(subdir + "Q*")
    questions = [q for q in questions if q not in answered_questions]

    if len(questions) == 0:
        print(f"No more questions in {subdir}")
        finished_subdir.append(subdir)
        continue

    question = random.choice(questions)
    print(f"\n--- {question} ---")
    answered_questions.append(question)
    Image.open(question).show()

    c = input("Press a for answer, q for quit, or Enter for next question > ")

    if c == "a":
        answer = question.replace("Q", "A")
        print(f"\n--- {answer} ---")
        Image.open(answer).show()
        c = input("Press q for quit or Enter for next question > ")
        if c == "q":
            break
    elif c == "q":
        break
