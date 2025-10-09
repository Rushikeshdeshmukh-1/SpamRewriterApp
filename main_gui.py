"""
Main GUI Application - Simplified Version
Author: GUI Teammate
Description: Tkinter GUI for spam detection and email rewriting
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import time

# Import backend modules
try:
    from spamDetector import SpamDetector
    from llm_rewriter import EmailRewriter
    BACKENDS_AVAILABLE = True
except ImportError as e:
    BACKENDS_AVAILABLE = False
    IMPORT_ERROR = str(e)

class SpamDetectorRewriterGUI:
    """Main GUI application"""

    def __init__(self, root):
        self.root = root
        self.setup_window()

        # Backend modules
        self.spamDetector = None
        self.email_rewriter = None
        self.api_key = "AIzaSyApRtIWlXf8Ya_bImiYSk0g66CCphZFf3I"

        # Create widgets
        self.create_widgets()

        # Initialize backend
        if BACKENDS_AVAILABLE:
            self.initialize_backend()
        else:
            messagebox.showerror("Error", f"Missing dependencies!\n\nInstall: pip install transformers torch google-generativeai\n\nError: {IMPORT_ERROR}")

    def setup_window(self):
        """Configure the main window"""
        self.root.title("AI Email Spam Detector & Professional Rewriter")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)

        # Configure style
        try:
            style = ttk.Style()
            style.theme_use('clam')
        except:
            pass  # Use default theme if clam not available

    def show_dependency_error(self):
        """Show dependency error message"""
        error_msg = f"""
Missing Required Dependencies!

Please install the required packages:

pip install transformers torch google-generativeai

Error details: {IMPORT_ERROR if not BACKENDS_AVAILABLE else 'Unknown'}

The application will run in demo mode with limited functionality.
"""
        messagebox.showwarning("Dependencies Missing", error_msg)
        self.processing_info.config(text="Running in demo mode - install dependencies for full functionality")

    def initialize_backend(self):
        """Initialize backend modules"""
        def init():
            try:
                self.root.after(0, lambda: self.processing_info.config(text="Loading spam detector..."))
                self.spamDetector = SpamDetector()

                self.root.after(0, lambda: self.processing_info.config(text="Loading email rewriter..."))
                self.email_rewriter = EmailRewriter(api_key=self.api_key)

                self.root.after(0, lambda: self.processing_info.config(text="All models loaded successfully!"))

            except Exception as e:
                error_msg = f"Failed to initialize: {str(e)}"
                self.root.after(0, lambda: self.processing_info.config(text="Initialization failed"))
                self.root.after(0, lambda: messagebox.showerror("Initialization Error", error_msg))

        thread = threading.Thread(target=init)
        thread.daemon = True
        thread.start()

    def create_widgets(self):
        """Create GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(
            title_frame,
            text="AI Email Spam Detector & Professional Rewriter",
            font=('Arial', 14, 'bold')
        )
        title_label.pack(pady=(0, 15))

        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Email Input", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.email_text = scrolledtext.ScrolledText(
            input_frame,
            height=10,
            wrap=tk.WORD,
            font=('Arial', 10)
        )
        self.email_text.pack(fill=tk.BOTH, expand=True)

        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))

        self.analyze_button = ttk.Button(
            button_frame,
            text="Analyze & Rewrite Email",
            command=self.analyze_email
        )
        self.analyze_button.pack(side=tk.LEFT, padx=(0, 5))

        self.clear_button = ttk.Button(
            button_frame,
            text="Clear All",
            command=self.clear_all
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 5))

        self.sample_button = ttk.Button(
            button_frame,
            text="Load Sample",
            command=self.load_sample
        )
        self.sample_button.pack(side=tk.LEFT)

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 10))

        # Results section
        results_frame = ttk.Frame(main_frame)
        results_frame.pack(fill=tk.BOTH, expand=True)

        # Left - Status
        left_frame = ttk.LabelFrame(results_frame, text="🛡️ Detection", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # Spam detection result
        spam_frame = ttk.LabelFrame(left_frame, text="Detection Result", padding="10")
        spam_frame.pack(fill=tk.X, pady=(0, 10))

        self.confidence_label = ttk.Label(left_frame, text="")
        self.confidence_label.pack(pady=5)

        self.status_label = ttk.Label(left_frame, text="Initializing...", foreground='gray')
        self.status_label.pack(pady=5)

        self.method_label = ttk.Label(spam_frame, text="", foreground='gray')
        self.method_label.pack()

        # Processing info
        info_frame = ttk.LabelFrame(left_frame, text="Status", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True)

        self.processing_info = ttk.Label(
            info_frame,
            text="Ready to analyze emails",
            wraplength=200
        )
        self.processing_info.pack(anchor=tk.W)

        self.timing_info = ttk.Label(info_frame, text="", foreground='gray')
        self.timing_info.pack(anchor=tk.W, pady=(5, 0))

        # Right column - Output
        right_frame = ttk.LabelFrame(results_frame, text="Rewritten Email", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.output_text = scrolledtext.ScrolledText(
            right_frame,
            wrap=tk.WORD,
            font=('Arial', 10),
            state=tk.DISABLED,
            bg='#f8f9fa'
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Output buttons
        output_btn_frame = ttk.Frame(right_frame)
        output_btn_frame.pack()

        self.copy_button = ttk.Button(
            output_button_frame,
            text="Copy Result",
            command=self.copy_result
        )
        self.copy_button.pack(side=tk.LEFT, padx=(0, 5))

        self.save_button = ttk.Button(
            output_button_frame,
            text="Save to File",
            command=self.save_result
        )
        self.save_button.pack(side=tk.LEFT)

    def update_char_count(self, event=None):
        """Update character count"""
        content = self.email_text.get("1.0", tk.END).strip()
        char_count = len(content)
        self.char_count_label.config(text=f"{char_count} characters")

    def load_sample(self):
        """Load a sample spam email"""
        sample = """URGENT BUSINESS PROPOSAL!!!

Hello Dear Friend,

I hope this email finds you in good health. I am MR. JOHN SMITH from LONDON BANK.

I have a BUSINESS PROPOSAL for you worth $15,000,000 (Fifteen Million USD) that will benefit both of us. This transaction is 100% RISK FREE and CONFIDENTIAL.

Please contact me IMMEDIATELY for more details!!! Time is running out!!!

Best Regards,
Mr. John Smith"""

        self.email_text.delete("1.0", tk.END)
        self.email_text.insert("1.0", sample)
        self.update_char_count()

    def analyze_email(self):
        """Analyze email"""
        email_content = self.email_text.get("1.0", tk.END).strip()

        if not email_content:
            messagebox.showwarning("Warning", "Please enter an email!")
            return

        if not BACKENDS_AVAILABLE or not self.spam_detector or not self.email_rewriter:
            messagebox.showerror("Error", "Backend not initialized!")
            return

        if not self.spamDetector or not self.email_rewriter:
            messagebox.showerror("Error", "Backend models not initialized!")
            return

        # Disable button and start processing
        self.analyze_button.config(state=tk.DISABLED)
        self.progress.start(10)
        self.processing_info.config(text="Analyzing email...")

        # Process in background
        thread = threading.Thread(target=self.process_email, args=(email_content,))
        thread.daemon = True
        thread.start()

    def show_demo_result(self):
        """Show demo result when backends not available"""
        email_content = self.email_text.get("1.0", tk.END).strip()

        # Simple demo analysis
        spam_keywords = ['urgent', 'money', 'click', 'limited', '$$$', '!!!']
        spam_count = sum(1 for keyword in spam_keywords if keyword.lower() in email_content.lower())

        is_spam = spam_count >= 2
        confidence = min(0.5 + (spam_count * 0.1), 0.9)

        # Update UI
        if is_spam:
            self.spam_result_label.config(text="SPAM DETECTED (Demo)", foreground='red')
            demo_rewrite = f"[DEMO MODE - Install dependencies for full functionality]\n\nThis email appears to be spam and would be professionally rewritten using AI.\n\nOriginal email:\n{email_content[:200]}..."
        else:
            self.spam_result_label.config(text="Legitimate Email (Demo)", foreground='green')
            demo_rewrite = "[DEMO MODE] This email appears legitimate and doesn't need rewriting."

        self.confidence_label.config(text=f"Confidence: {confidence:.1%}")
        self.method_label.config(text="Method: demo (keywords)")

        # Show output
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", demo_rewrite)
        self.output_text.config(state=tk.DISABLED)

        self.processing_info.config(text="Demo analysis complete")

    def process_email(self, email_content):
        """Process email in background"""
        try:
            start_time = time.time()

            # Step 1: Spam detection
            self.root.after(0, lambda: self.processing_info.config(text="Running spam detection..."))
            spam_result = selfD.predict_spam(email_content)

            # Rewrite if spam
            if spam_result['is_spam']:
                self.root.after(0, lambda: self.processing_info.config(text="Rewriting email..."))
                rewrite_start = time.time()
                rewrite_result = self.email_rewriter.rewrite_email(email_content, instructions)
                rewrite_time = time.time() - rewrite_start

                if rewrite_result['success']:
                    rewritten_text = rewrite_result['rewritten_text']
                else:
                    rewritten_text = f"Rewriting failed: {rewrite_result.get('error', 'Unknown error')}"
            else:
                rewritten_text = "Email appears legitimate and doesn't require rewriting.\n\nIf you'd still like to enhance it professionally, you can modify the instructions and analyze again."

            total_time = time.time() - start_time

            # Update GUI
            self.root.after(0, self.update_results, spam_result, rewritten_text, total_time)

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Processing failed: {str(e)}"))
            self.root.after(0, lambda: self.analyze_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.status_label.config(text="❌ Error"))

    def update_results(self, spam_result, rewritten_text, total_time):
        """Update GUI with results"""
        # Update detection display
        if spam_result['is_spam']:
            self.spam_result_label.config(text="SPAM DETECTED", foreground='red')
        else:
            self.spam_result_label.config(text="Legitimate Email", foreground='green')

        self.confidence_label.config(text=f"{spam_result['confidence']:.0%} confident")

        # Update output
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", rewritten_text)
        self.output_text.config(state=tk.DISABLED)

        # Reset button and status
        self.analyze_button.config(state=tk.NORMAL)

        status = "Spam detected and rewritten!" if spam_result['is_spam'] else "✅ Analysis complete"
        self.processing_info.config(text=status)

    def show_error(self, error_msg):
        """Show error message"""
        self.progress.stop()
        self.analyze_button.config(state=tk.NORMAL)
        self.processing_info.config(text="❌ Error occurred")
        messagebox.showerror("Processing Error", error_msg)

    def copy_result(self):
        """Copy to clipboard"""
        result = self.output_text.get("1.0", tk.END).strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            messagebox.showinfo("Success", "Copied!")
        else:
            messagebox.showwarning("Warning", "Nothing to copy!")

    def save_result(self):
        """Save to file"""
        result = self.output_text.get("1.0", tk.END).strip()
        if not result:
            messagebox.showwarning("Warning", "Nothing to save!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(result)
                messagebox.showinfo("Success", "Saved!")
            except Exception as e:
                messagebox.showerror("Error", f"Save failed: {str(e)}")

    def clear_all(self):
        """Clear all content"""
        self.email_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.spam_label.config(text="No analysis", foreground='black')
        self.confidence_label.config(text="")
        self.status_label.config(text="Ready")

def main():
    """Run application"""
    root = tk.Tk()
    app = SpamDetectorRewriterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()