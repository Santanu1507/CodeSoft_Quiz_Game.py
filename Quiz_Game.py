import tkinter as tk
import random

# Quiz Questions
questions = [
    # List of dictionaries containing questions, options, and correct answers
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Paris", "London", "Rome"],
        "correct_answer": "Paris"
    },
    {
        "question": "Which planet is known as the 'Red Planet'?",
        "options": ["Mars", "Venus", "Jupiter", "Saturn"],
        "correct_answer": "Mars"
    },
    {
        "question": "What is 10 + 5?",
        "options": ["10", "15", "20", "25"],
        "correct_answer": "15"
    },
    {
        "question": "What is the capital of Japan?",
        "options": ["Beijing", "Tokyo", "Seoul", "Bangkok"],
        "correct_answer": "Tokyo"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["Leonardo da Vinci", "Pablo Picasso", "Vincent van Gogh", "Michelangelo"],
        "correct_answer": "Leonardo da Vinci"
    },
    {
        "question": "What is the largest mammal in the world?",
        "options": ["Elephant", "Blue Whale", "Giraffe", "Hippopotamus"],
        "correct_answer": "Blue Whale"
    },
    {
        "question": "Which famous scientist formulated the theory of relativity?",
        "options": ["Isaac Newton", "Albert Einstein", "Galileo Galilei", "Marie Curie"],
        "correct_answer": "Albert Einstein"
    },
    {
        "question": "What is the chemical symbol for water?",
        "options": ["O", "He", "H2O", "CO2"],
        "correct_answer": "H2O"
    },
    {
        "question": "What is the largest organ in the human body?",
        "options": ["Brain", "Heart", "Liver", "Skin"],
        "correct_answer": "Skin"
    },
    {
        "question": "Who wrote the famous play 'Romeo and Juliet'?",
        "options": ["William Shakespeare", "Jane Austen", "Charles Dickens", "Leo Tolstoy"],
        "correct_answer": "William Shakespeare"
    }
]

class QuizGame(tk.Tk):
    def __init__(self):
        super().__init__()

        # Basic window setup
        self.title("Quiz Game")
        self.geometry("700x600")
        self.score = 0
        self.current_question = 0

        # Create the main frame to hold all the widgets
        self.main_frame = tk.Frame(self)
        self.main_frame.pack()

        # Show the welcome screen
        self.create_welcome_widgets()

    def create_welcome_widgets(self):
        # Create and pack the welcome label with styling
        self.label_welcome = tk.Label(self.main_frame, text="Welcome to the Quiz Game!", font=("Comic Sans MS", 16, "bold"))
        self.label_welcome.pack(pady=20)

        # Create and pack the points to know label with styling
        self.label_points = tk.Label(self.main_frame, text="Points to know:\n\n"
                                                           "1. This is a quiz game with multiple-choice questions.\n"
                                                           "2. Each question has four options, and only one is correct.\n"
                                                           "3. Click on the option you think is the correct answer.\n"
                                                           "4. You will see whether your answer is correct or not immediately.\n"
                                                           "5. The correct answer will be highlighted in green, and incorrect answers in red.\n"
                                                           "6. After answering all questions, your final score will be shown.\n",
                                     font=("Comic Sans MS", 12))
        self.label_points.pack(pady=10)

        # Create and pack the start quiz button with styling and command
        self.button_start = tk.Button(self.main_frame, text="Start Quiz", command=self.start_quiz, font=("Comic Sans MS", 12), bg="blue", fg="white")
        self.button_start.pack(pady=20)

    def start_quiz(self):
        # Hide welcome and points labels, and start the quiz
        self.label_welcome.pack_forget()
        self.label_points.pack_forget()
        self.button_start.pack_forget()

        self.create_widgets()
        self.load_question()

    def create_widgets(self):
        # Create and pack the question label with styling
        self.label_question = tk.Label(self.main_frame, text="", wraplength=300, font=("Comic Sans MS", 14))
        self.label_question.pack(pady=20)

        # Create and set a StringVar to store the selected answer
        self.var_answer = tk.StringVar()
        self.var_answer.set(None)

        # Create and pack option buttons for each question option with styling and command
        self.option_buttons = []
        for i in range(4):
            option = tk.Button(self.main_frame, text="", width=25, font=("Comic Sans MS", 12), command=lambda idx=i: self.evaluate_answer(idx), bg="lightblue")
            option.pack(pady=5)
            self.option_buttons.append(option)

        # Create and pack the result label with styling
        self.result_label = tk.Label(self.main_frame, text="", font=("Comic Sans MS", 14))
        self.result_label.pack(pady=20)

        # Create and pack the next button with styling and disable it initially
        self.button_next = tk.Button(self.main_frame, text="Next", command=self.show_question_result, font=("Comic Sans MS", 12), bg="orange")
        self.button_next.pack(pady=10)
        self.button_next.config(state=tk.DISABLED)

        # Create and pack the show result button with styling
        self.button_show_result = tk.Button(self.main_frame, text="Show Result", command=self.show_final_results, font=("Comic Sans MS", 12), bg="purple", fg="white")
        self.button_show_result.pack(pady=10)

        # Hide the show result button initially
        self.button_show_result.pack_forget()

        # Create the "Do you want to play quiz?" message widget but keep it hidden initially
        self.feedback_label = tk.Label(self.main_frame, text="Do you want to play quiz?", font=("Comic Sans MS", 12))
        self.feedback_label.pack(pady=10)
        self.feedback_label.pack_forget()

        # Create a frame for "Yes" and "No" buttons but keep it hidden initially
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)
        self.button_frame.pack_forget()

        # Create and pack the "Yes" button with styling and command
        self.button_yes = tk.Button(self.button_frame, text="Yes", command=self.play_again, font=("Comic Sans MS", 12), bg="green", fg="white")
        self.button_yes.pack(side=tk.LEFT, padx=5)

        # Create and pack the "No" button with styling and command
        self.button_no = tk.Button(self.button_frame, text="No", command=self.confirm_quit_game, font=("Comic Sans MS", 12), bg="red", fg="white")
        self.button_no.pack(side=tk.LEFT, padx=5)

    def load_question(self):
        # Disable the next button for the current question
        self.button_next.config(state=tk.DISABLED)

        # Check if there are more questions to display
        if self.current_question < len(questions):
            question_data = questions[self.current_question]
            self.label_question.config(text=question_data["question"])

            self.var_answer.set(None)  # Clear the previously selected answer

            for i in range(4):
                self.option_buttons[i].config(text=question_data["options"][i], bg="lightblue", state=tk.NORMAL, fg="black")

            if self.current_question == len(questions) - 1:
                # Last question, hide the "Next" button and show the "Show Result" button
                self.button_next.pack_forget()
                self.button_show_result.pack(pady=10)
        else:
            # No more questions, show final results
            self.show_final_results()

    def evaluate_answer(self, selected_index):
        question_data = questions[self.current_question]

        # Disable all option buttons to prevent further selection
        for i in range(4):
            self.option_buttons[i].config(state=tk.DISABLED)

        # Check if the selected option is correct or not
        if question_data["options"][selected_index] == question_data["correct_answer"]:
            self.score += 1
            self.option_buttons[selected_index].config(bg="green", fg="white")  # Mark the selected option as correct
        else:
            self.option_buttons[selected_index].config(bg="red", fg="white")  # Mark the selected option as incorrect

        correct_index = question_data["options"].index(question_data["correct_answer"])
        self.option_buttons[correct_index].config(bg="green", fg="white")  # Mark the correct option in green

        self.button_next.config(state=tk.NORMAL)  # Enable the next button

    def show_question_result(self):
        # Show the next question (if available) or proceed to final results
        if self.current_question < len(questions) - 1:
            self.current_question += 1
            self.load_question()

    def show_final_results(self):
        # Calculate the final score and performance message
        total_questions = len(questions)
        score_percent = (self.score / total_questions) * 100
        performance_msg = "Excellent! You did a great job!" if score_percent >= 70 else "Keep practicing!"

        # Prepare and display the final results
        result_msg = f"Your final score is {self.score} out of {total_questions}.\n\n{performance_msg}"
        self.result_label.config(text=result_msg)

        # Hide question-related widgets
        self.label_question.pack_forget()
        for button in self.option_buttons:
            button.pack_forget()
        self.button_next.pack_forget()

        # Hide the Show Result button
        self.button_show_result.pack_forget()

        # Show the "Do you want to play quiz?" message and "Yes" and "No" buttons
        self.feedback_label.pack(pady=10)
        self.button_frame.pack(pady=10)

    def reset_quiz(self):
        # Reset the score and question index for a new quiz session
        self.score = 0
        self.current_question = 0
        self.result_label.config(text="")
        self.button_show_result.pack_forget()
        self.feedback_label.pack_forget()
        self.label_question.pack_forget()
        for button in self.option_buttons:
            button.pack_forget()
        self.button_next.pack_forget()
        self.button_frame.pack_forget()

    def play_again(self):
        # Reset the quiz and start a new quiz session
        self.reset_quiz()
        self.create_widgets()
        self.load_question()

    def confirm_quit_game(self):
        # Display a thank you message upon quitting the game
        self.feedback_label.config(text="Thank You for Playing!!", font=("Comic Sans MS", 20, "bold"))
        self.button_frame.pack_forget()

if __name__ == "__main__":
    game = QuizGame()
    game.mainloop()