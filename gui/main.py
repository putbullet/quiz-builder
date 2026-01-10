"""
Main entry point for the Quiz Builder GUI application
"""
from gui.quiz_builder import QuizBuilderGUI


def main():
    """Launch the quiz builder application"""
    app = QuizBuilderGUI()
    app.run()


if __name__ == '__main__':
    main()

