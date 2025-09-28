"""
Main GUI Application - FIXED VERSION
Author: GUI Teammate (Completed)
Description: Tkinter-based GUI that integrates spam detection and email rewriting
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import time
import sys
import os

# Import backend modules with error handling
try:
    from spam_detector import SpamDetector
    from llm_rewriter import EmailRewriter
    BACKENDS_AVAILABLE = True
except ImportError as e:
    BACKENDS_AVAILABLE = False
    IMPORT_ERROR = str(e)

class SpamDetectorRewriterGUI:
    """
    Main GUI application for spam detection and email rewriting
    """

    def __init__(self, root):
        self.root = root
        self.setup_window()

        # Backend modules
        self.spam_detector = None
        self.email_rewriter = None
        self.api_key = "AIzaSyApRtIWlXf8Ya_bImiYSk0g66CCphZFf3I"

        # Create widgets
        self.create_widgets()

        # Initialize backend if available
        if BACKENDS_AVAILABLE:
            self.initialize_backend()
        else:
            self.show_dependency_error()

    def setup_window(self):
        """Configure the main window"""
        self.root.title("🛡️ AI Email Spam Detector & Professional Rewriter")
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
        self.processing_info.config(text="⚠️ Running in demo mode - install dependencies for full functionality")

    def initialize_backend(self):
        """Initialize backend modules"""
        def init_in_thread():
            try:
                self.root.after(0, lambda: self.processing_info.config(text="🔄 Loading spam detector..."))
                self.spam_detector = SpamDetector()

                self.root.after(0, lambda: self.processing_info.config(text="🔄 Loading email rewriter..."))
                self.email_rewriter = EmailRewriter(api_key=self.api_key)

                self.root.after(0, lambda: self.processing_info.config(text="✅ All models loaded successfully!"))

            except Exception as e:
                error_msg = f"Failed to initialize: {str(e)}"
                self.root.after(0, lambda: self.processing_info.config(text="❌ Initialization failed"))
                self.root.after(0, lambda: messagebox.showerror("Initialization Error", error_msg))

        # Initialize in background thread
        thread = threading.Thread(target=init_in_thread)
        thread.daemon = True
        thread.start()

    def create_widgets(self):
        """Create and layout all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))

        title_label = ttk.Label(
            title_frame,
            text="🛡️ AI Email Spam Detector & Professional Rewriter",
            font=('Arial', 14, 'bold')
        )
        title_label.pack()

        subtitle_label = ttk.Label(
            title_frame,
            text="Powered by Gemini 2.5 Flash & Advanced ML",
            font=('Arial', 9),
            foreground='gray'
        )
        subtitle_label.pack()

        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="📧 Email Input", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Character counter
        counter_frame = ttk.Frame(input_frame)
        counter_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(counter_frame, text="Paste your email here:").pack(side=tk.LEFT)
        self.char_count_label = ttk.Label(counter_frame, text="0 characters", foreground='gray')
        self.char_count_label.pack(side=tk.RIGHT)

        # Email text area
        self.email_text = scrolledtext.ScrolledText(
            input_frame,
            height=8,
            wrap=tk.WORD,
            font=('Arial', 10)
        )
        self.email_text.pack(fill=tk.BOTH, expand=True)
        self.email_text.bind('<KeyRelease>', self.update_char_count)

        # Instructions section
        instr_frame = ttk.LabelFrame(main_frame, text="✏️ Rewriting Instructions", padding="10")
        instr_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(instr_frame, text="Custom instructions (optional):").pack(anchor=tk.W)

        self.instruction_entry = ttk.Entry(instr_frame, font=('Arial', 10))
        self.instruction_entry.pack(fill=tk.X, pady=(5, 0))
        self.instruction_entry.insert(0, "Make it professional and appropriate for business communication")

        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))

        self.analyze_button = ttk.Button(
            button_frame,
            text="🔍 Analyze & Rewrite Email",
            command=self.analyze_email
        )
        self.analyze_button.pack(side=tk.LEFT, padx=(0, 5))

        self.clear_button = ttk.Button(
            button_frame,
            text="🗑️ Clear All",
            command=self.clear_all
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 5))

        self.sample_button = ttk.Button(
            button_frame,
            text="📄 Load Sample",
            command=self.load_sample
        )
        self.sample_button.pack(side=tk.LEFT)

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 10))

        # Results section
        results_frame = ttk.Frame(main_frame)
        results_frame.pack(fill=tk.BOTH, expand=True)

        # Left column - Status
        left_frame = ttk.Frame(results_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # Spam detection result
        spam_frame = ttk.LabelFrame(left_frame, text="🛡️ Detection Result", padding="10")
        spam_frame.pack(fill=tk.X, pady=(0, 10))

        self.spam_result_label = ttk.Label(
            spam_frame,
            text="No analysis yet",
            font=('Arial', 11, 'bold')
        )
        self.spam_result_label.pack()

        self.confidence_label = ttk.Label(spam_frame, text="")
        self.confidence_label.pack()

        self.method_label = ttk.Label(spam_frame, text="", foreground='gray')
        self.method_label.pack()

        # Processing info
        info_frame = ttk.LabelFrame(left_frame, text="ℹ️ Status", padding="10")
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
        right_frame = ttk.LabelFrame(results_frame, text="✨ Rewritten Email", padding="10")
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
        output_button_frame = ttk.Frame(right_frame)
        output_button_frame.pack(fill=tk.X)

        self.copy_button = ttk.Button(
            output_button_frame,
            text="📋 Copy Result",
            command=self.copy_result
        )
        self.copy_button.pack(side=tk.LEFT, padx=(0, 5))

        self.save_button = ttk.Button(
            output_button_frame,
            text="💾 Save to File",
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
        """Main analysis function"""
        email_content = self.email_text.get("1.0", tk.END).strip()

        if not email_content:
            messagebox.showwarning("Warning", "Please enter an email to analyze!")
            return

        if not BACKENDS_AVAILABLE:
            self.show_demo_result()
            return

        if not self.spam_detector or not self.email_rewriter:
            messagebox.showerror("Error", "Backend models not initialized!")
            return

        # Disable button and start processing
        self.analyze_button.config(state=tk.DISABLED)
        self.progress.start(10)
        self.processing_info.config(text="🔍 Analyzing email...")

        # Run in background thread
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
            self.spam_result_label.config(text="🚨 SPAM DETECTED (Demo)", foreground='red')
            demo_rewrite = f"[DEMO MODE - Install dependencies for full functionality]\n\nThis email appears to be spam and would be professionally rewritten using AI.\n\nOriginal email:\n{email_content[:200]}..."
        else:
            self.spam_result_label.config(text="✅ Legitimate Email (Demo)", foreground='green')
            demo_rewrite = "[DEMO MODE] This email appears legitimate and doesn't need rewriting."

        self.confidence_label.config(text=f"Confidence: {confidence:.1%}")
        self.method_label.config(text="Method: demo (keywords)")

        # Show output
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", demo_rewrite)
        self.output_text.config(state=tk.DISABLED)

        self.processing_info.config(text="⚠️ Demo analysis complete")

    def process_email(self, email_content):
        """Process email in background thread"""
        try:
            start_time = time.time()
            instructions = self.instruction_entry.get().strip()

            # Step 1: Spam detection
            self.root.after(0, lambda: self.processing_info.config(text="🔍 Running spam detection..."))
            spam_result = self.spam_detector.predict_spam(email_content)

            # Step 2: Email rewriting (if spam detected)
            rewrite_time = 0
            if spam_result['is_spam']:
                self.root.after(0, lambda: self.processing_info.config(text="✍️ Rewriting email..."))
                rewrite_start = time.time()
                rewrite_result = self.email_rewriter.rewrite_email(email_content, instructions)
                rewrite_time = time.time() - rewrite_start

                if rewrite_result['success']:
                    rewritten_text = rewrite_result['rewritten_text']
                else:
                    rewritten_text = f"❌ Rewriting failed: {rewrite_result.get('error', 'Unknown error')}"
            else:
                rewritten_text = "✅ Email appears legitimate and doesn't require rewriting.\n\nIf you'd still like to enhance it professionally, you can modify the instructions and analyze again."

            total_time = time.time() - start_time

            # Update GUI
            self.root.after(0, self.update_results, spam_result, rewritten_text, total_time, rewrite_time)

        except Exception as e:
            error_msg = f"Processing error: {str(e)}"
            self.root.after(0, self.show_error, error_msg)

    def update_results(self, spam_result, rewritten_text, total_time, rewrite_time):
        """Update GUI with results"""
        # Update spam detection display
        if spam_result['is_spam']:
            self.spam_result_label.config(text="🚨 SPAM DETECTED", foreground='red')
        else:
            self.spam_result_label.config(text="✅ Legitimate Email", foreground='green')

        self.confidence_label.config(text=f"Confidence: {spam_result['confidence']:.1%}")
        self.method_label.config(text=f"Method: {spam_result.get('method', 'unknown')}")

        # Update output
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", rewritten_text)
        self.output_text.config(state=tk.DISABLED)

        # Update timing
        timing_text = f"Processing time: {total_time:.2f}s"
        if rewrite_time > 0:
            timing_text += f" (Rewrite: {rewrite_time:.2f}s)"
        self.timing_info.config(text=timing_text)

        # Reset UI
        self.progress.stop()
        self.analyze_button.config(state=tk.NORMAL)

        status = "🚨 Spam detected and rewritten!" if spam_result['is_spam'] else "✅ Analysis complete"
        self.processing_info.config(text=status)

    def show_error(self, error_msg):
        """Show error message"""
        self.progress.stop()
        self.analyze_button.config(state=tk.NORMAL)
        self.processing_info.config(text="❌ Error occurred")
        messagebox.showerror("Processing Error", error_msg)

    def copy_result(self):
        """Copy result to clipboard"""
        result_text = self.output_text.get("1.0", tk.END).strip()
        if result_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(result_text)
            messagebox.showinfo("Success", "Result copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No result to copy!")

    def save_result(self):
        """Save result to file"""
        result_text = self.output_text.get("1.0", tk.END).strip()
        if not result_text:
            messagebox.showwarning("Warning", "No result to save!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Rewritten Email"
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(result_text)
                messagebox.showinfo("Success", f"Saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")

    def clear_all(self):
        """Clear all content"""
        self.email_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)

        self.spam_result_label.config(text="No analysis yet", foreground='black')
        self.confidence_label.config(text="")
        self.method_label.config(text="")
        self.processing_info.config(text="Ready to analyze emails")
        self.timing_info.config(text="")
        self.char_count_label.config(text="0 characters")

def main():
    """Main application entry point"""
    print("🚀 Starting Email Spam Detector & Rewriter")
    print("=" * 50)

    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher required")
        sys.exit(1)

    root = tk.Tk()

    try:
        app = SpamDetectorRewriterGUI(root)
        print("✅ GUI initialized successfully")

        if BACKENDS_AVAILABLE:
            print("✅ Backend modules loaded")
        else:
            print("⚠️  Running in demo mode - install dependencies for full features")

        print("\n🎯 Ready to use!")
        root.mainloop()

    except Exception as e:
        error_msg = f"Application failed to start: {str(e)}"
        print(f"❌ {error_msg}")
        try:
            messagebox.showerror("Startup Error", error_msg)
        except:
            pass
        sys.exit(1)

if __name__ == "__main__":
    main()