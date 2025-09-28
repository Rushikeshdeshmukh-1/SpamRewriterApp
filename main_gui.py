"""
Main GUI Application
Author: [GUI Teammate Name]
Description: Tkinter-based GUI that integrates spam detection and email rewriting

TODO for GUI teammate:
1. Design the layout with proper widgets
2. Integrate with spam_detector.py and llm_rewriter.py
3. Add error handling and user feedback
4. Make the interface user-friendly
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import os


# Import the other modules (your teammates need to make sure these work)
# from spam_detector import SpamDetector
# from llm_rewriter import EmailRewriter

class SpamDetectorRewriterGUI:
    """
    Main GUI application for spam detection and email rewriting
    """

    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()

        # TODO: Initialize the backend modules
        # Uncomment when your teammates complete their modules
        # self.spam_detector = SpamDetector()
        # self.email_rewriter = EmailRewriter()

        # For demo purposes
        self.spam_detector = None
        self.email_rewriter = None

    def setup_window(self):
        """
        Configure the main window
        """
        self.root.title("Email Spam Detector & Rewriter")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)

        # Configure style
        style = ttk.Style()
        style.theme_use('clam')  # Modern looking theme

    def create_widgets(self):
        """
        Create and layout all GUI widgets
        """
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="Email Spam Detector & Rewriter",
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Input Email", padding="10")
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(1, weight=1)

        # Email input
        ttk.Label(input_frame, text="Paste your email here:").grid(row=0, column=0, sticky=tk.W)
        self.email_text = scrolledtext.ScrolledText(input_frame, width=80, height=8,
                                                    wrap=tk.WORD, font=('Arial', 10))
        self.email_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0))

        # Instructions input
        instruction_frame = ttk.Frame(main_frame)
        instruction_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        instruction_frame.columnconfigure(1, weight=1)

        ttk.Label(instruction_frame, text="Rewrite Instructions:").grid(row=0, column=0, sticky=tk.W)
        self.instruction_entry = ttk.Entry(instruction_frame, font=('Arial', 10))
        self.instruction_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        self.instruction_entry.insert(0, "Make it more professional and formal")

        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(0, 20))

        self.analyze_button = ttk.Button(button_frame, text="Analyze & Rewrite",
                                         command=self.analyze_email)
        self.analyze_button.pack(side=tk.LEFT, padx=(0, 10))

        self.clear_button = ttk.Button(button_frame, text="Clear All",
                                       command=self.clear_all)
        self.clear_button.pack(side=tk.LEFT)

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        # Results section
        results_frame = ttk.Frame(main_frame)
        results_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.columnconfigure(0, weight=1)
        results_frame.columnconfigure(1, weight=1)
        results_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)

        # Spam detection result
        spam_frame = ttk.LabelFrame(results_frame, text="Spam Detection Result", padding="10")
        spam_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))

        self.spam_result_label = ttk.Label(spam_frame, text="No analysis yet",
                                           font=('Arial', 12, 'bold'))
        self.spam_result_label.pack()

        self.confidence_label = ttk.Label(spam_frame, text="")
        self.confidence_label.pack()

        # Processing info
        info_frame = ttk.LabelFrame(results_frame, text="Processing Info", padding="10")
        info_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))

        self.processing_info = ttk.Label(info_frame, text="Ready to process")
        self.processing_info.pack()

        # Rewritten email output
        output_frame = ttk.LabelFrame(results_frame, text="Rewritten Email", padding="10")
        output_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)

        self.output_text = scrolledtext.ScrolledText(output_frame, width=80, height=10,
                                                     wrap=tk.WORD, font=('Arial', 10),
                                                     state=tk.DISABLED)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Copy button
        copy_button = ttk.Button(output_frame, text="Copy Result", command=self.copy_result)
        copy_button.grid(row=1, column=0, pady=(5, 0))

    def analyze_email(self):
        """
        Main function to analyze email and rewrite it
        TODO: Integrate with actual backend modules
        """
        email_content = self.email_text.get("1.0", tk.END).strip()

        if not email_content:
            messagebox.showwarning("Warning", "Please enter an email to analyze!")
            return

        # Disable button and show progress
        self.analyze_button.config(state=tk.DISABLED)
        self.progress.start(10)
        self.processing_info.config(text="Processing...")

        # Run analysis in separate thread to prevent GUI freezing
        thread = threading.Thread(target=self._process_email, args=(email_content,))
        thread.daemon = True
        thread.start()

    def _process_email(self, email_content):
        """
        Process email in background thread
        TODO: Replace dummy implementation with actual backend calls
        """
        try:
            instructions = self.instruction_entry.get().strip()

            # TODO: Replace with actual spam detection
            if self.spam_detector:
                spam_result = self.spam_detector.predict_spam(email_content)
            else:
                # Dummy implementation for demo
                spam_keywords = ['urgent', 'money', 'click', 'limited', '$$$', '!!!']
                email_lower = email_content.lower()
                spam_count = sum(1 for keyword in spam_keywords if keyword in email_lower)

                spam_result = {
                    'is_spam': spam_count >= 2,
                    'confidence': min(0.5 + (spam_count * 0.1), 0.95),
                    'label': 'spam' if spam_count >= 2 else 'ham',
                    'error': None
                }

            # TODO: Replace with actual email rewriting
            if self.email_rewriter and spam_result['is_spam']:
                rewrite_result = self.email_rewriter.rewrite_email(email_content, instructions)
                rewritten_text = rewrite_result.get('rewritten_text', 'Error in rewriting')
            else:
                # Dummy implementation for demo
                if spam_result['is_spam']:
                    rewritten_text = f"[DEMO] This email was detected as spam and would be rewritten here.\n\nOriginal: {email_content}\n\nInstructions: {instructions}"
                else:
                    rewritten_text = "Email appears to be legitimate and doesn't need rewriting."

            # Update GUI in main thread
            self.root.after(0, self._update_results, spam_result, rewritten_text)

        except Exception as e:
            error_msg = f"Error processing email: {str(e)}"
            self.root.after(0, self._show_error, error_msg)

    def _update_results(self, spam_result, rewritten_text):
        """
        Update GUI with results (called from main thread)
        """
        # Update spam detection result
        if spam_result['is_spam']:
            self.spam_result_label.config(text="⚠️ SPAM DETECTED", foreground='red')
        else:
            self.spam_result_label.config(text="✅ Legitimate Email", foreground='green')

        confidence_text = f"Confidence: {spam_result['confidence']:.1%}"
        self.confidence_label.config(text=confidence_text)

        # Update rewritten text
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", rewritten_text)
        self.output_text.config(state=tk.DISABLED)

        # Reset UI
        self.progress.stop()
        self.analyze_button.config(state=tk.NORMAL)
        self.processing_info.config(text="Analysis complete!")

    def _show_error(self, error_msg):
        """
        Show error message and reset UI
        """
        self.progress.stop()
        self.analyze_button.config(state=tk.NORMAL)
        self.processing_info.config(text="Error occurred")
        messagebox.showerror("Error", error_msg)

    def copy_result(self):
        """
        Copy the rewritten email to clipboard
        """
        result_text = self.output_text.get("1.0", tk.END).strip()
        if result_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(result_text)
            messagebox.showinfo("Copied", "Result copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No result to copy!")

    def clear_all(self):
        """
        Clear all inputs and outputs
        """
        self.email_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)

        self.spam_result_label.config(text="No analysis yet", foreground='black')
        self.confidence_label.config(text="")
        self.processing_info.config(text="Ready to process")


def main():
    """
    Main function to run the application
    """
    root = tk.Tk()
    app = SpamDetectorRewriterGUI(root)

    # Add sample email for demo
    sample_email = """URGENT BUSINESS PROPOSAL!!!

Hello Dear,

I hope this email finds you in good health. I am MR. JOHN SMITH from LONDON. 

I have a BUSINESS PROPOSAL for you worth $15,000,000 (Fifteen Million USD) that will benefit both of us. This transaction is 100% RISK FREE.

Please contact me IMMEDIATELY for more details!!! Time is running out!!!

Best Regards,
Mr. John Smith"""

    app.email_text.insert("1.0", sample_email)

    root.mainloop()


if __name__ == "__main__":
    main()

"""
IMPLEMENTATION GUIDE FOR GUI TEAMMATE:

1. Current structure is ready to use - run this file to see the demo

2. Key integration points:
   - Uncomment the imports at the top
   - Uncomment the initialization in __init__
   - Replace dummy implementations in _process_email

3. UI improvements to consider:
   - Add menu bar with File/Edit/Help
   - Add status bar at bottom
   - Implement drag-and-drop for email files
   - Add settings dialog for API keys
   - Add email templates/examples

4. Error handling:
   - Add try-catch around backend calls
   - Show user-friendly error messages
   - Handle network timeouts gracefully

5. Performance improvements:
   - Add loading animations
   - Cache results for repeated emails
   - Implement batch processing

6. Testing:
   - Test with various email formats
   - Test with very long emails
   - Test error scenarios (no internet, invalid API key)

7. Packaging:
   - Consider using PyInstaller for executable
   - Include icon and proper metadata
"""