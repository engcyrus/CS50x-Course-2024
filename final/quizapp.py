import tkinter as tk
from tkinter import messagebox, PhotoImage, Toplevel
import random
import json
from PIL import Image, ImageTk

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz App")
        self.master.geometry("800x600")

        # Adiciona o texto, os botões e a caixa de resposta
        self.add_widgets()

        # Adiciona a imagem do logo
        self.add_logo()

        # Inicializa a lista de perguntas
        self.questions = self.load_questions_from_file()

    def add_widgets(self):
        # Caixa de texto para a pergunta
        self.question_label = tk.Label(self.master, text="", font=('Arial Unicode MS', 12), wraplength= 500)
        self.question_label.pack()

        # Imagem associada à pergunta
        self.image_label = tk.Label(self.master)
        self.image_label.pack()

        # Frame para os botões de resposta
        self.answers_frame = tk.Frame(self.master)
        self.answers_frame.pack()

        # Labels para exibir o score
        self.score_label = tk.Label(self.master, text="Score: Certo - 0 | Errado - 0", font=('Arial', 14))
        self.score_label.pack(side=tk.TOP, padx=10, pady=10)

        # Botão para iniciar o quiz
        self.start_button = tk.Button(self.master, text="Iniciar", command=self.start_quiz, bg="green", fg="white", font=("Arial", 14))
        self.start_button.pack()

        # Botões para adicionar e resetar perguntas
        self.add_question_button = tk.Button(self.master, text="Add Perguntas", command=self.add_question, bg="orange", fg="white", font=("Arial", 14))
        self.add_question_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_quiz, bg="red", fg="white", font=("Arial", 14))
        self.reset_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Botão para sair do programa
        self.exit_button = tk.Button(self.master, text="Exit", command=self.master.destroy, bg="purple", fg="white", font=("Arial", 14))
        self.exit_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Botão para exibir a imagem associada à pergunta
        self.view_image_button = tk.Button(self.master, text="Imagem da questão", command=self.view_image, bg="blue", fg="white", font=("Arial", 14))
        self.view_image_button.pack()
        self.view_image_button.config(state=tk.DISABLED)

    def add_logo(self):
        try:
            # Carrega a imagem do logo e redimensiona
            logo_image = Image.open("logo.png")
            logo_image_resized = logo_image.resize((400, 400))
            self.logo_photo = ImageTk.PhotoImage(logo_image_resized)
            logo_label = tk.Label(self.master, image=self.logo_photo)
            logo_label.pack(pady=20)  # Espaçamento inferior para separar a imagem do restante dos widgets
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load logo image: {e}")
    
    



    def start_quiz(self):
        self.reset_score()
        self.next_question()

    def next_question(self):
        if self.questions:
            random_question = random.choice(self.questions)
            self.display_question(random_question)
        else:
            messagebox.showinfo("Quiz App", "No questions available. Please add questions.")
            self.reset_quiz()

    def display_question(self, question):
        self.question_label.config(text=question["question"])

        self.image_path = question.get("image_path", "")

        if self.image_path:
            self.image_label.config(image=None)
            self.view_image_button.config(state=tk.NORMAL)  # Habilita o botão "View Image"
        else:
            self.image_label.config(image=None)
            self.view_image_button.config(state=tk.DISABLED)  # Desabilita o botão "View Image"

        for widget in self.answers_frame.winfo_children():
            widget.destroy()

        for answer in question["answers"]:
            answer_button = tk.Button(self.answers_frame, text=answer, command=lambda ans=answer: self.check_answer(ans, question["correct_answer"]))
            answer_button.pack()

    def check_answer(self, user_answer, correct_answer):
        if user_answer == correct_answer:
            self.score['correct'] += 1
        else:
            self.score['wrong'] += 1
        self.update_score()
        self.next_question()

    def add_question(self):
        add_question_window = tk.Toplevel(self.master)
        add_question_window.title("Add Question")

        question_label = tk.Label(add_question_window, text="Question:", font=('Arial', 12))
        question_label.pack()
        question_entry = tk.Entry(add_question_window, width=50)
        question_entry.pack()

        answers_label = tk.Label(add_question_window, text="Answers (use ';' to separate answers):", font=('Arial', 12))
        answers_label.pack()

        answers_entry = tk.Entry(add_question_window, width=50)
        answers_entry.pack()

        correct_answer_label = tk.Label(add_question_window, text="Correct Answer:", font=('Arial', 12))
        correct_answer_label.pack()
        correct_answer_entry = tk.Entry(add_question_window, width=50)
        correct_answer_entry.pack()

        image_path_label = tk.Label(add_question_window, text="Image Path:", font=('Arial', 12))
        image_path_label.pack()
        image_path_entry = tk.Entry(add_question_window, width=50)
        image_path_entry.pack()

        def save_question():
            question = question_entry.get()
            answers = [ans.strip() for ans in answers_entry.get().split(";")]  # Usar ';' como separador
            correct_answer = correct_answer_entry.get()
            image_path = image_path_entry.get()

            if question and answers and correct_answer:
                new_question = {
                    "question": question,
                    "answers": answers,
                    "correct_answer": correct_answer
                }
                if image_path:
                    new_question["image_path"] = image_path
                self.questions.append(new_question)
                self.save_questions_to_file()
                add_question_window.destroy()  # Destruir a janela após salvar a pergunta
            else:
                messagebox.showerror("Error", "Please provide question, answers, and correct answer.")

        save_button = tk.Button(add_question_window, text="Save", command=save_question)
        save_button.pack()

    def save_questions_to_file(self):
        with open("questions.json", "w") as file:
            json.dump(self.questions, file)

    def load_questions_from_file(self):
        try:
            with open("questions.json", "r") as file:
                questions = json.load(file)
        except FileNotFoundError:
            messagebox.showinfo("Quiz App", "No questions found. Please add questions.")
            questions = []
        return questions

    def reset_quiz(self):
        self.reset_score()
        self.question_label.config(text="")
        self.image_label.config(image=None)
        for widget in self.answers_frame.winfo_children():
            widget.destroy()

    def reset_score(self):
        self.score = {'correct': 0, 'wrong': 0}
        self.update_score()

    def update_score(self):
        self.score_label.config(text=f"Score: Correct - {self.score['correct']} | Wrong - {self.score['wrong']}")

    def view_image(self):
        if hasattr(self, 'image_path') and self.image_path:
            image_window = Toplevel(self.master)
            image_window.title("Image Viewer")

            image_label = tk.Label(image_window)
            image_label.pack()

            try:
                image = PhotoImage(file=self.image_path)
                image_label.config(image=image)
                image_label.image = image
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")

root = tk.Tk()
app = QuizApp(root)
root.mainloop()
