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
    from spam_detector import SpamDetector
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
        self.spam_detector = None
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
        """Configure main window"""
        self.root.title("AI Email Spam Detector & Rewriter")
        self.root.geometry("900x600")
        self.root.minsize(700, 500)

    def initialize_backend(self):
        """Initialize backend modules"""
        def init():
            try:
                self.spam_detector = SpamDetector()
                self.email_rewriter = EmailRewriter(api_key=self.api_key)
                self.root.after(0, lambda: self.status_label.config(text="✅ Ready"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Initialization failed: {str(e)}"))

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
            main_frame,
            text="🛡️ AI Email Spam Detector & Rewriter",
            font=('Arial', 14, 'bold')
        )
        title_label.pack(pady=(0, 15))

        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="📧 Email Input", padding="10")
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
            text="🔍 Analyze & Rewrite",
            command=self.analyze_email
        )
        self.analyze_button.pack(side=tk.LEFT, padx=(0, 5))

        self.clear_button = ttk.Button(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_all
        )
        self.clear_button.pack(side=tk.LEFT)

        # Results section
        results_frame = ttk.Frame(main_frame)
        results_frame.pack(fill=tk.BOTH, expand=True)

        # Left - Status
        left_frame = ttk.LabelFrame(results_frame, text="🛡️ Detection", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        self.spam_label = ttk.Label(left_frame, text="No analysis", font=('Arial', 11, 'bold'))
        self.spam_label.pack(pady=5)

        self.confidence_label = ttk.Label(left_frame, text="")
        self.confidence_label.pack(pady=5)

        self.status_label = ttk.Label(left_frame, text="Initializing...", foreground='gray')
        self.status_label.pack(pady=5)

        # Right - Output
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
        output_btn_frame = ttk.Frame(right_frame)
        output_btn_frame.pack()

        ttk.Button(output_btn_frame, text="📋 Copy", command=self.copy_result).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(output_btn_frame, text="💾 Save", command=self.save_result).pack(side=tk.LEFT)

    def analyze_email(self):
        """Analyze email"""
        email_content = self.email_text.get("1.0", tk.END).strip()

        if not email_content:
            messagebox.showwarning("Warning", "Please enter an email!")
            return

        if not BACKENDS_AVAILABLE or not self.spam_detector or not self.email_rewriter:
            messagebox.showerror("Error", "Backend not initialized!")
            return

        # Disable button
        self.analyze_button.config(state=tk.DISABLED)
        self.status_label.config(text="🔍 Processing...")

        # Process in background
        thread = threading.Thread(target=self.process_email, args=(email_content,))
        thread.daemon = True
        thread.start()

    def process_email(self, email_content):
        """Process email in background"""
        try:
            start_time = time.time()

            # Spam detection
            spam_result = self.spam_detector.predict_spam(email_content)

            # Rewrite if spam
            if spam_result['is_spam']:
                rewrite_result = self.email_rewriter.rewrite_email(email_content)
                rewritten_text = rewrite_result['rewritten_text'] if rewrite_result['success'] else f"❌ Error: {rewrite_result['error']}"
            else:
                rewritten_text = "✅ Email is legitimate and doesn't need rewriting."

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
            self.spam_label.config(text="🚨 SPAM", foreground='red')
        else:
            self.spam_label.config(text="✅ Legitimate", foreground='green')

        self.confidence_label.config(text=f"{spam_result['confidence']:.0%} confident")

        # Update output
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", rewritten_text)
        self.output_text.config(state=tk.DISABLED)

        # Reset button and status
        self.analyze_button.config(state=tk.NORMAL)
        self.status_label.config(text=f"✅ Done ({total_time:.1f}s)")

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