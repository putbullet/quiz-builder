"""
Quiz Builder GUI - Main Tkinter interface for creating and editing quizzes
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from gui.quiz_manager import QuizManager


class QuestionEditor:
    """Dialog for editing a single question"""
    
    def __init__(self, parent, question_data: Optional[Dict] = None):
        self.result = None
        self.question_data = question_data or {}
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Question")
        self.dialog.geometry("600x700")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Question type
        ttk.Label(self.dialog, text="Question Type:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.type_var = tk.StringVar(value=self.question_data.get('type', 'multiple_choice_single'))
        type_combo = ttk.Combobox(self.dialog, textvariable=self.type_var, 
                                 values=['multiple_choice_single', 'multiple_choice_multiple', 
                                        'true_false', 'short_answer', 'paragraph'],
                                 state='readonly', width=30)
        type_combo.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        type_combo.bind('<<ComboboxSelected>>', self.on_type_change)
        
        # Question text
        ttk.Label(self.dialog, text="Question Text:").grid(row=1, column=0, sticky='nw', padx=5, pady=5)
        self.question_text = tk.Text(self.dialog, height=3, width=50)
        self.question_text.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        self.question_text.insert('1.0', self.question_data.get('text', ''))
        
        # Weight/Points
        ttk.Label(self.dialog, text="Points:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.weight_var = tk.StringVar(value=str(self.question_data.get('weight', 1)))
        ttk.Entry(self.dialog, textvariable=self.weight_var, width=10).grid(row=2, column=1, sticky='w', padx=5, pady=5)
        
        # Options frame
        self.options_frame = ttk.Frame(self.dialog)
        self.options_frame.grid(row=3, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        
        # Answers frame
        self.answers_frame = ttk.Frame(self.dialog)
        self.answers_frame.grid(row=4, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        
        self.option_entries = []
        self.correct_vars = []
        
        self.type_var.trace('w', lambda *args: self.on_type_change())
        self.on_type_change()
        
        # Buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Save", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.cancel).pack(side=tk.LEFT, padx=5)
        
        self.dialog.columnconfigure(1, weight=1)
        self.dialog.rowconfigure(1, weight=1)
        
    def on_type_change(self, event=None):
        """Update UI based on question type"""
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        for widget in self.answers_frame.winfo_children():
            widget.destroy()
        self.option_entries.clear()
        self.correct_vars.clear()
        
        q_type = self.type_var.get()
        
        if q_type in ['multiple_choice_single', 'multiple_choice_multiple']:
            ttk.Label(self.options_frame, text="Options (one per line):").pack(anchor='w')
            options_text = tk.Text(self.options_frame, height=5, width=50)
            options_text.pack(fill='both', expand=True, padx=5, pady=5)
            existing_options = self.question_data.get('options', [''])
            options_text.insert('1.0', '\n'.join(existing_options))
            self.option_entries.append(options_text)
            
            ttk.Label(self.options_frame, text="Correct Answer(s):").pack(anchor='w', pady=(5,0))
            correct_text = tk.Text(self.options_frame, height=2, width=50)
            correct_text.pack(fill='x', padx=5, pady=5)
            correct_answers = self.question_data.get('correct_answer', [])
            if isinstance(correct_answers, list):
                correct_text.insert('1.0', '\n'.join(correct_answers))
            else:
                correct_text.insert('1.0', str(correct_answers))
            self.correct_vars.append(correct_text)
            
        elif q_type == 'true_false':
            ttk.Label(self.options_frame, text="Correct Answer:").pack(anchor='w')
            tf_var = tk.StringVar(value=self.question_data.get('correct_answer', 'True'))
            ttk.Radiobutton(self.options_frame, text="True", variable=tf_var, value='True').pack(anchor='w')
            ttk.Radiobutton(self.options_frame, text="False", variable=tf_var, value='False').pack(anchor='w')
            self.correct_vars.append(tf_var)
            
        elif q_type in ['short_answer', 'paragraph']:
            ttk.Label(self.answers_frame, text="Correct Answer (optional - leave empty for manual grading):").pack(anchor='w')
            answer_text = tk.Text(self.answers_frame, height=3 if q_type == 'paragraph' else 1, width=50)
            answer_text.pack(fill='x', padx=5, pady=5)
            answer_text.insert('1.0', self.question_data.get('correct_answer', ''))
            self.correct_vars.append(answer_text)
    
    def save(self):
        """Save question data"""
        q_type = self.type_var.get()
        question_text = self.question_text.get('1.0', 'end-1c').strip()
        
        if not question_text:
            messagebox.showerror("Error", "Question text cannot be empty")
            return
        
        try:
            weight = float(self.weight_var.get())
        except ValueError:
            messagebox.showerror("Error", "Points must be a number")
            return
        
        result = {
            'type': q_type,
            'text': question_text,
            'weight': weight,
            'correct_answer': None
        }
        
        if q_type in ['multiple_choice_single', 'multiple_choice_multiple']:
            options_text = self.option_entries[0].get('1.0', 'end-1c').strip()
            options = [opt.strip() for opt in options_text.split('\n') if opt.strip()]
            if len(options) < 2:
                messagebox.showerror("Error", "Multiple choice questions need at least 2 options")
                return
            result['options'] = options
            
            correct_text = self.correct_vars[0].get('1.0', 'end-1c').strip()
            if q_type == 'multiple_choice_single':
                result['correct_answer'] = correct_text
            else:
                result['correct_answer'] = [opt.strip() for opt in correct_text.split('\n') if opt.strip()]
                
        elif q_type == 'true_false':
            result['correct_answer'] = self.correct_vars[0].get()
            
        elif q_type in ['short_answer', 'paragraph']:
            result['correct_answer'] = self.correct_vars[0].get('1.0', 'end-1c').strip()
        
        self.result = result
        self.dialog.destroy()
    
    def cancel(self):
        """Cancel editing"""
        self.result = None
        self.dialog.destroy()


class QuizBuilderGUI:
    """Main quiz builder application"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Offline Quiz Builder")
        self.root.geometry("900x700")
        
        self.manager = QuizManager()
        self.current_quiz = None
        self.launched = False
        
        self.setup_ui()
        self.load_quiz_list()
    
    def setup_ui(self):
        """Create the main UI"""
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Quiz", command=self.new_quiz)
        file_menu.add_command(label="Load Quiz", command=self.load_quiz_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        # Top section: Quiz selection and actions
        top_frame = ttk.LabelFrame(main_frame, text="Quiz Management", padding="10")
        top_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(top_frame, text="Quiz:").grid(row=0, column=0, sticky='w', padx=5)
        self.quiz_combo = ttk.Combobox(top_frame, state='readonly', width=30)
        self.quiz_combo.grid(row=0, column=1, padx=5)
        self.quiz_combo.bind('<<ComboboxSelected>>', self.on_quiz_selected)
        
        ttk.Button(top_frame, text="New", command=self.new_quiz).grid(row=0, column=2, padx=5)
        ttk.Button(top_frame, text="Delete", command=self.delete_quiz).grid(row=0, column=3, padx=5)
        ttk.Button(top_frame, text="Preview", command=self.preview_quiz).grid(row=0, column=4, padx=5)
        ttk.Button(top_frame, text="Results", command=self.view_results, style='Accent.TButton').grid(row=0, column=5, padx=5)
        
        # Quiz properties frame
        props_frame = ttk.LabelFrame(main_frame, text="Quiz Properties", padding="10")
        props_frame.pack(fill='x', pady=(0, 10))
        
        # Quiz name/title
        ttk.Label(props_frame, text="Quiz Name (file):").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.name_var = tk.StringVar()
        ttk.Entry(props_frame, textvariable=self.name_var, width=40).grid(row=0, column=1, sticky='ew', padx=5, pady=2)
        
        ttk.Label(props_frame, text="Quiz Title (displayed):").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.title_var = tk.StringVar()
        ttk.Entry(props_frame, textvariable=self.title_var, width=40).grid(row=1, column=1, sticky='ew', padx=5, pady=2)
        
        # Other properties
        self.require_name_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(props_frame, text="Require Full Name", variable=self.require_name_var).grid(row=2, column=0, columnspan=2, sticky='w', padx=5, pady=2)
        
        ttk.Label(props_frame, text="Timer (minutes):").grid(row=3, column=0, sticky='w', padx=5, pady=2)
        self.timer_var = tk.StringVar(value="30")
        ttk.Entry(props_frame, textvariable=self.timer_var, width=10).grid(row=3, column=1, sticky='w', padx=5, pady=2)
        
        self.shuffle_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(props_frame, text="Shuffle Questions", variable=self.shuffle_var).grid(row=4, column=0, columnspan=2, sticky='w', padx=5, pady=2)
        
        ttk.Label(props_frame, text="Start Message:").grid(row=5, column=0, sticky='nw', padx=5, pady=2)
        self.start_msg = tk.Text(props_frame, height=3, width=40)
        self.start_msg.grid(row=5, column=1, sticky='ew', padx=5, pady=2)
        
        ttk.Label(props_frame, text="End Message:").grid(row=6, column=0, sticky='nw', padx=5, pady=2)
        self.end_msg = tk.Text(props_frame, height=3, width=40)
        self.end_msg.grid(row=6, column=1, sticky='ew', padx=5, pady=2)
        
        props_frame.columnconfigure(1, weight=1)
        
        # Questions frame
        q_frame = ttk.LabelFrame(main_frame, text="Questions", padding="10")
        q_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Questions list
        list_frame = ttk.Frame(q_frame)
        list_frame.pack(fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.questions_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=10)
        self.questions_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.questions_listbox.yview)
        
        # Question buttons
        q_btn_frame = ttk.Frame(q_frame)
        q_btn_frame.pack(fill='x', pady=5)
        ttk.Button(q_btn_frame, text="Add Question", command=self.add_question).pack(side=tk.LEFT, padx=2)
        ttk.Button(q_btn_frame, text="Edit Question", command=self.edit_question).pack(side=tk.LEFT, padx=2)
        ttk.Button(q_btn_frame, text="Delete Question", command=self.remove_question).pack(side=tk.LEFT, padx=2)
        ttk.Button(q_btn_frame, text="Move Up", command=self.move_question_up).pack(side=tk.LEFT, padx=2)
        ttk.Button(q_btn_frame, text="Move Down", command=self.move_question_down).pack(side=tk.LEFT, padx=2)
        
        # Action buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill='x')
        
        self.save_btn = ttk.Button(action_frame, text="Save Quiz", command=self.save_quiz)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        self.launch_btn = ttk.Button(action_frame, text="Launch Quiz", command=self.launch_quiz, 
                                     style='Accent.TButton')
        self.launch_btn.pack(side=tk.LEFT, padx=5)
        
        self.status_label = ttk.Label(action_frame, text="Ready", foreground='green')
        self.status_label.pack(side=tk.LEFT, padx=10)
    
    def load_quiz_dialog(self):
        """Load quiz from dialog"""
        self.load_quiz_list()
        if self.quiz_combo['values']:
            messagebox.showinfo("Load Quiz", 
                              "Select a quiz from the dropdown above and it will load automatically.")
        else:
            messagebox.showinfo("No Quizzes", 
                              "No quizzes found. Create a new quiz first.")
    
    def show_about(self):
        """Show about dialog"""
        about_text = (
            "Offline Quiz Builder + Live Timed Exam Server\n\n"
            "Version 1.0\n\n"
            "A complete quiz builder and live exam delivery system\n"
            "designed for educators teaching young children.\n\n"
            "Built with Python, Tkinter, Flask, and ngrok."
        )
        messagebox.showinfo("About Quiz Builder", about_text)
    
    def load_quiz_list(self):
        """Load and display list of quizzes"""
        quizzes = self.manager.list_quizzes()
        self.quiz_combo['values'] = quizzes
        if quizzes:
            self.quiz_combo.current(0)
            self.on_quiz_selected()
    
    def on_quiz_selected(self, event=None):
        """Load selected quiz"""
        quiz_name = self.quiz_combo.get()
        if quiz_name:
            quiz_data = self.manager.load_quiz(quiz_name)
            if quiz_data:
                self.load_quiz_data(quiz_data)
    
    def load_quiz_data(self, quiz_data: Dict):
        """Load quiz data into UI"""
        if self.launched:
            messagebox.showwarning("Warning", "Cannot edit quiz while it's launched!")
            return
        
        self.current_quiz = quiz_data
        self.name_var.set(quiz_data.get('name', ''))
        self.title_var.set(quiz_data.get('title', ''))
        self.require_name_var.set(quiz_data.get('require_full_name', True))
        self.timer_var.set(str(quiz_data.get('timer_minutes', 30)))
        self.shuffle_var.set(quiz_data.get('shuffle_questions', False))
        self.start_msg.delete('1.0', 'end')
        self.start_msg.insert('1.0', quiz_data.get('start_message', ''))
        self.end_msg.delete('1.0', 'end')
        self.end_msg.insert('1.0', quiz_data.get('end_message', ''))
        
        self.refresh_questions_list()
        self.update_status("Quiz loaded")
    
    def refresh_questions_list(self):
        """Update the questions listbox"""
        self.questions_listbox.delete(0, 'end')
        if self.current_quiz and 'questions' in self.current_quiz:
            for i, q in enumerate(self.current_quiz['questions'], 1):
                q_type = q.get('type', 'unknown').replace('_', ' ').title()
                preview = q.get('text', '')[:50]
                self.questions_listbox.insert('end', f"{i}. [{q_type}] {preview}...")
    
    def new_quiz(self):
        """Create a new quiz"""
        if self.launched:
            messagebox.showwarning("Warning", "Cannot create new quiz while one is launched!")
            return
        
        name = simpledialog.askstring("New Quiz", "Enter quiz name:")
        if name:
            quiz_data = self.manager.get_default_quiz()
            quiz_data['name'] = name
            quiz_data['title'] = name
            self.load_quiz_data(quiz_data)
            self.quiz_combo['values'] = list(self.quiz_combo['values']) + [name]
            self.quiz_combo.set(name)
            self.update_status("New quiz created")
    
    def delete_quiz(self):
        """Delete current quiz"""
        if self.launched:
            messagebox.showwarning("Warning", "Cannot delete quiz while it's launched!")
            return
        
        quiz_name = self.quiz_combo.get()
        if quiz_name and messagebox.askyesno("Delete Quiz", f"Delete '{quiz_name}'?"):
            if self.manager.delete_quiz(quiz_name):
                self.load_quiz_list()
                self.current_quiz = None
                self.name_var.set('')
                self.title_var.set('')
                self.questions_listbox.delete(0, 'end')
                self.update_status("Quiz deleted")
    
    def add_question(self):
        """Add a new question"""
        if not self.current_quiz:
            messagebox.showwarning("Warning", "Please create or load a quiz first")
            return
        
        editor = QuestionEditor(self.root)
        self.root.wait_window(editor.dialog)
        
        if editor.result:
            if 'questions' not in self.current_quiz:
                self.current_quiz['questions'] = []
            self.current_quiz['questions'].append(editor.result)
            self.refresh_questions_list()
            self.update_status("Question added")
    
    def edit_question(self):
        """Edit selected question"""
        if not self.current_quiz:
            return
        
        selection = self.questions_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a question to edit")
            return
        
        idx = selection[0]
        question_data = self.current_quiz['questions'][idx]
        
        editor = QuestionEditor(self.root, question_data)
        self.root.wait_window(editor.dialog)
        
        if editor.result:
            self.current_quiz['questions'][idx] = editor.result
            self.refresh_questions_list()
            self.update_status("Question updated")
    
    def remove_question(self):
        """Remove selected question"""
        if not self.current_quiz:
            return
        
        selection = self.questions_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a question to delete")
            return
        
        idx = selection[0]
        if messagebox.askyesno("Delete Question", "Delete this question?"):
            del self.current_quiz['questions'][idx]
            self.refresh_questions_list()
            self.update_status("Question deleted")
    
    def move_question_up(self):
        """Move question up in list"""
        selection = self.questions_listbox.curselection()
        if selection and selection[0] > 0:
            idx = selection[0]
            questions = self.current_quiz['questions']
            questions[idx], questions[idx-1] = questions[idx-1], questions[idx]
            self.refresh_questions_list()
            self.questions_listbox.select_set(idx-1)
    
    def move_question_down(self):
        """Move question down in list"""
        selection = self.questions_listbox.curselection()
        if selection and self.current_quiz:
            idx = selection[0]
            questions = self.current_quiz['questions']
            if idx < len(questions) - 1:
                questions[idx], questions[idx+1] = questions[idx+1], questions[idx]
                self.refresh_questions_list()
                self.questions_listbox.select_set(idx+1)
    
    def save_quiz(self):
        """Save current quiz"""
        if self.launched:
            messagebox.showwarning("Warning", "Cannot save quiz while it's launched!")
            return
        
        if not self.current_quiz:
            messagebox.showwarning("Warning", "No quiz to save")
            return
        
        # Update quiz data from UI
        self.current_quiz['name'] = self.name_var.get() or 'unnamed_quiz'
        self.current_quiz['title'] = self.title_var.get() or 'Untitled Quiz'
        self.current_quiz['require_full_name'] = self.require_name_var.get()
        try:
            self.current_quiz['timer_minutes'] = int(self.timer_var.get())
        except ValueError:
            messagebox.showerror("Error", "Timer must be a number")
            return
        self.current_quiz['shuffle_questions'] = self.shuffle_var.get()
        self.current_quiz['start_message'] = self.start_msg.get('1.0', 'end-1c')
        self.current_quiz['end_message'] = self.end_msg.get('1.0', 'end-1c')
        
        if self.manager.save_quiz(self.current_quiz):
            self.load_quiz_list()
            self.quiz_combo.set(self.current_quiz['name'])
            self.update_status("Quiz saved successfully")
        else:
            messagebox.showerror("Error", "Failed to save quiz")
    
    def preview_quiz(self):
        """Preview quiz in a new window"""
        if not self.current_quiz or not self.current_quiz.get('questions'):
            messagebox.showwarning("Warning", "No questions to preview")
            return
        
        preview_window = tk.Toplevel(self.root)
        preview_window.title(f"Preview: {self.current_quiz.get('title', 'Quiz')}")
        preview_window.geometry("700x600")
        
        text_widget = tk.Text(preview_window, wrap='word', padx=10, pady=10)
        text_widget.pack(fill='both', expand=True)
        
        preview_text = f"QUIZ PREVIEW\n{'='*60}\n\n"
        preview_text += f"Title: {self.current_quiz.get('title', 'N/A')}\n"
        preview_text += f"Timer: {self.current_quiz.get('timer_minutes', 0)} minutes\n"
        preview_text += f"Questions: {len(self.current_quiz.get('questions', []))}\n\n"
        preview_text += f"Start Message:\n{self.current_quiz.get('start_message', 'N/A')}\n\n"
        preview_text += f"{'='*60}\n\n"
        
        for i, q in enumerate(self.current_quiz.get('questions', []), 1):
            preview_text += f"Question {i} [{q.get('type', 'unknown').replace('_', ' ').title()}] - {q.get('weight', 1)} points\n"
            preview_text += f"{q.get('text', 'N/A')}\n"
            if 'options' in q:
                preview_text += f"Options: {', '.join(q['options'])}\n"
            preview_text += f"Correct Answer: {q.get('correct_answer', 'N/A')}\n\n"
        
        text_widget.insert('1.0', preview_text)
        text_widget.config(state='disabled')
    
    def view_results(self):
        """View quiz results for selected quiz"""
        quiz_name = self.quiz_combo.get()
        if not quiz_name:
            messagebox.showwarning("Warning", "Please select a quiz to view results")
            return
        
        results_dir = os.path.join('results', quiz_name)
        if not os.path.exists(results_dir):
            messagebox.showinfo("No Results", f"No results found for quiz: {quiz_name}")
            return
        
        # Get all JSON result files
        result_files = [f for f in os.listdir(results_dir) if f.endswith('.json')]
        if not result_files:
            messagebox.showinfo("No Results", f"No submissions found for quiz: {quiz_name}")
            return
        
        # Create results window
        results_window = tk.Toplevel(self.root)
        results_window.title(f"Results: {quiz_name}")
        results_window.geometry("900x700")
        
        # Add scrollbar and text widget
        frame = ttk.Frame(results_window)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side='right', fill='y')
        
        text_widget = tk.Text(frame, wrap='word', padx=10, pady=10, yscrollcommand=scrollbar.set, font=('Courier', 10))
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=text_widget.yview)
        
        # Build results text
        results_text = f"QUIZ RESULTS SUMMARY\n"
        results_text += f"{'='*80}\n"
        results_text += f"Quiz: {quiz_name}\n"
        results_text += f"Total Submissions: {len(result_files)}\n"
        results_text += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        results_text += f"{'='*80}\n\n"
        
        # Load and display each result
        for i, filename in enumerate(sorted(result_files), 1):
            filepath = os.path.join(results_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    result_data = json.load(f)
                
                results_text += f"\n{'─'*80}\n"
                results_text += f"SUBMISSION #{i}\n"
                results_text += f"{'─'*80}\n"
                results_text += f"Student Name: {result_data.get('student_name', 'N/A')}\n"
                results_text += f"Submitted: {result_data.get('timestamp', 'N/A')}\n"
                results_text += f"Session ID: {result_data.get('session_id', 'N/A')}\n\n"
                
                score = result_data.get('score', {})
                results_text += f"TOTAL POINTS POSSIBLE: {score.get('total_points', 0)}\n"
                results_text += f"(Teacher: Review answers below and calculate final score)\n\n"
                
                results_text += f"STUDENT RESPONSES:\n"
                results_text += f"{'─'*80}\n"
                
                # Get questions from result data
                questions = result_data.get('questions', [])
                answers = result_data.get('answers', {})
                
                for i, question in enumerate(questions):
                    q_num = i + 1
                    q_text = question.get('text', 'N/A')
                    q_type = question.get('type', 'unknown').replace('_', ' ').title()
                    q_weight = question.get('weight', 1)
                    correct_answer = question.get('correct_answer', 'N/A')
                    
                    # Get student's answer
                    student_answer = answers.get(str(i), '[No Answer]')
                    if isinstance(student_answer, list):
                        student_answer = ', '.join(str(a) for a in student_answer)
                    if isinstance(correct_answer, list):
                        correct_answer = ', '.join(str(a) for a in correct_answer)
                    
                    results_text += f"\nQuestion {q_num} [{q_type}] - {q_weight} point(s)\n"
                    results_text += f"  Question: {q_text}\n"
                    
                    # Show options for multiple choice
                    if 'options' in question:
                        results_text += f"  Options: {', '.join(question['options'])}\n"
                    
                    results_text += f"  STUDENT ANSWERED: {student_answer}\n"
                    results_text += f"  CORRECT ANSWER:  {correct_answer}\n"
                
                results_text += f"\n"
                
            except Exception as e:
                results_text += f"\n[Error loading {filename}: {e}]\n\n"
        
        results_text += f"\n{'='*80}\n"
        results_text += f"END OF RESULTS\n"
        results_text += f"{'='*80}\n"
        
        text_widget.insert('1.0', results_text)
        text_widget.config(state='disabled')
        
        # Auto-save results to text file in the results directory
        results_txt_path = os.path.join(results_dir, f"{quiz_name}_ALL_RESULTS.txt")
        try:
            with open(results_txt_path, 'w', encoding='utf-8') as f:
                f.write(results_text)
        except Exception as e:
            logger.warning(f"Could not auto-save results file: {e}")
        
        # Add buttons
        btn_frame = ttk.Frame(results_window)
        btn_frame.pack(pady=5)
        
        ttk.Label(btn_frame, text=f"Results auto-saved to: {results_txt_path}", 
                 foreground='green').pack(side=tk.LEFT, padx=10)
        
        ttk.Button(btn_frame, text="Open Results Folder", 
                  command=lambda: os.startfile(results_dir)).pack(side=tk.LEFT, padx=5)
    
    def export_results(self, results_text: str, quiz_name: str):
        """Export results to a text file"""
        filename = f"{quiz_name}_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(results_text)
            messagebox.showinfo("Export Successful", f"Results exported to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export results:\n{e}")
    
    def launch_quiz(self):
        """Launch the quiz server"""
        # Make sure we have the currently selected quiz loaded
        quiz_name = self.quiz_combo.get()
        if not quiz_name:
            messagebox.showwarning("Warning", "Please select a quiz to launch")
            return
        
        # Reload the selected quiz to ensure we have the right one
        quiz_data = self.manager.load_quiz(quiz_name)
        if quiz_data:
            self.load_quiz_data(quiz_data)
        
        if not self.current_quiz:
            messagebox.showwarning("Warning", "Failed to load quiz")
            return
        
        if not self.current_quiz.get('questions'):
            messagebox.showerror("Error", "Quiz must have at least one question")
            return
        
        # Warn if another quiz is running
        if self.launched:
            if not messagebox.askyesno("Quiz Running", 
                                      "Another quiz is already running.\n\n"
                                      "Launching a new quiz will replace it.\n\n"
                                      "Continue?"):
                return
        
        # Save quiz first
        self.save_quiz()
        
        # Import and start server launcher
        try:
            import threading
            import webbrowser
            from run_server import launch_quiz_server
            
            quiz_file = f"{self.current_quiz['name']}.json"
            
            def launch_in_thread():
                try:
                    url, _ = launch_quiz_server(quiz_file, self.root)
                    # Update UI in main thread - capture url in default parameter
                    self.root.after(0, lambda url=url: self.on_launch_success(url))
                except Exception as e:
                    # Capture error message in default parameter to avoid closure issue
                    error_msg = str(e)
                    self.root.after(0, lambda msg=error_msg: self.on_launch_error(msg))
            
            # Launch in separate thread to avoid blocking GUI
            thread = threading.Thread(target=launch_in_thread, daemon=True)
            thread.start()
            
        except ImportError as e:
            messagebox.showerror("Error", f"Failed to import server modules:\n{e}\n\nMake sure all dependencies are installed.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch quiz server:\n{e}")
            import traceback
            traceback.print_exc()
    
    def on_launch_success(self, url: str):
        """Callback when quiz launches successfully"""
        self.launched = True
        self.save_btn.config(state='disabled')
        self.launch_btn.config(text="Launch Another Quiz", state='normal')
        quiz_title = self.current_quiz.get('title', 'Quiz') if self.current_quiz else 'Quiz'
        self.update_status(f"'{quiz_title}' launched - URL: {url}", 'blue')
    
    def on_launch_error(self, error_msg: str):
        """Callback when quiz launch fails"""
        messagebox.showerror("Error", f"Failed to launch quiz server:\n{error_msg}")
        self.update_status("Launch failed", 'red')
    
    def update_status(self, message: str, color: str = 'green'):
        """Update status label"""
        self.status_label.config(text=message, foreground=color)
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


if __name__ == '__main__':
    app = QuizBuilderGUI()
    app.run()

