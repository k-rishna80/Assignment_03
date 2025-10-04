import tkinter as tk
from tkinter import ttk
import threading
from gui.widgets import LabeledText, FilePicker, OutputBox
from models.text_classifier import TextClassifier
from models.image_classifier import ImageClassifier

MODEL_CHOICES = {
    "Text-to-Sentiment": ("text", TextClassifier),
    "Image Classification": ("image", ImageClassifier),
}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter AI GUI")
        self.geometry("400x600")
        self.configure(bg="#f0f0f0")

        # Create menu bar
        self.create_menu()

        # Main container with padding
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Model Selection Section
        model_frame = tk.LabelFrame(main_frame, text="Model Selection:", bg="#f0f0f0")
        model_frame.pack(fill="x", pady=5)

        model_inner = tk.Frame(model_frame, bg="#f0f0f0")
        model_inner.pack(fill="x", padx=5, pady=5)

        self.model_var = tk.StringVar(value=list(MODEL_CHOICES.keys())[0])
        model_combo = ttk.Combobox(
            model_inner,
            textvariable=self.model_var,
            values=list(MODEL_CHOICES.keys()),
            state="readonly",
        )
        model_combo.pack(side="left", fill="x", expand=True)
        model_combo.bind("<<ComboboxSelected>>", self._on_model_change)

        # Create horizontal container for User Input and Model Output sections (50/50 split)
        horizontal_frame = tk.Frame(main_frame, bg="#f0f0f0")
        horizontal_frame.pack(fill="both", expand=True, pady=5)

        # User Input Section (Left side - 50%)
        input_frame = tk.LabelFrame(
            horizontal_frame, text="User Input Section", bg="#f0f0f0"
        )
        input_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Radio buttons for input type (conditionally shown)
        self.radio_frame = tk.Frame(input_frame, bg="#f0f0f0")
        self.radio_frame.pack(fill="x", padx=5, pady=5)

        self.input_type = tk.StringVar(value="text")
        self.text_radio = tk.Radiobutton(
            self.radio_frame,
            text="Text",
            variable=self.input_type,
            value="text",
            bg="#f0f0f0",
            command=self._update_input_visibility,
        )
        self.text_radio.pack(side="left")

        self.image_radio = tk.Radiobutton(
            self.radio_frame,
            text="Image",
            variable=self.input_type,
            value="image",
            bg="#f0f0f0",
            command=self._update_input_visibility,
        )
        self.image_radio.pack(side="left", padx=(20, 0))

        # Input areas
        self.text_input_frame = tk.Frame(input_frame, bg="#f0f0f0")
        self.text_input = tk.Text(self.text_input_frame, height=6, width=20)
        self.text_input.pack(fill="both", expand=True, padx=5, pady=5)

        self.image_input_frame = tk.Frame(input_frame, bg="#f0f0f0")
        image_inner = tk.Frame(self.image_input_frame, bg="#f0f0f0")
        image_inner.pack(expand=True, padx=5, pady=5)

        self.image_path = tk.StringVar()

        # Selected file label
        self.selected_file_label = tk.Label(
            image_inner,
            text="No file selected",
            bg="#f0f0f0",
            wraplength=180,
            justify="center",
        )
        self.selected_file_label.pack(pady=(5, 10))

        browse_btn = tk.Button(
            image_inner, text="Browse for Image", command=self.browse_image
        )
        browse_btn.pack(pady=5)

        # Model Output Section (Right side - 50%)
        output_frame = tk.LabelFrame(
            horizontal_frame, text="Model Output Section", bg="#f0f0f0"
        )
        output_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        output_label = tk.Label(output_frame, text="Output Display:", bg="#f0f0f0")
        output_label.pack(anchor="w", padx=5, pady=(5, 0))

        self.output_text = tk.Text(output_frame, height=6, width=20, state="disabled")
        self.output_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Buttons (below the horizontal sections)
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(fill="x", pady=12)

        # Store button reference for loading states
        self.run_btn = tk.Button(
            button_frame, text="Run Model", command=lambda: self.run_model(),
            font=("Arial", 9), padx=20, pady=5
        )
        self.run_btn.pack(side="left", padx=(0, 10))

        clear_btn = tk.Button(
            button_frame, text="Clear", command=self.clear_output,
            font=("Arial", 9), padx=20, pady=5
        )
        clear_btn.pack(side="left")

        # Loading indicator (initially hidden)
        self.loading_frame = tk.Frame(button_frame, bg="#f0f0f0")
        self.loading_frame.pack(side="left", padx=(10, 0))
        
        self.loading_label = tk.Label(
            self.loading_frame, text="🔄 Processing...", 
            bg="#f0f0f0", font=("Arial", 9), fg="blue"
        )
        # Don't pack yet - will show during loading

        # Model Information & Explanation
        info_frame = tk.LabelFrame(
            main_frame, text="Model Information & Explanation", bg="#f0f0f0"
        )
        info_frame.pack(fill="x", pady=10)

        # Left side - Selected Model Info
        left_info = tk.Frame(info_frame, bg="#f0f0f0")
        left_info.pack(side="left", fill="both", expand=True, padx=10, pady=8)

        tk.Label(
            left_info,
            text="Selected Model Info:",
            bg="#f0f0f0",
            font=("Arial", 10, "bold"),
        ).pack(anchor="w", pady=(0, 5))

        # Dynamic model info labels with better spacing
        self.model_name_label = tk.Label(left_info, text="", bg="#f0f0f0", justify="left", font=("Arial", 9))
        self.model_name_label.pack(anchor="w", pady=2)

        self.model_category_label = tk.Label(left_info, text="", bg="#f0f0f0", justify="left", font=("Arial", 9))
        self.model_category_label.pack(anchor="w", pady=2)

        self.model_description_label = tk.Label(left_info, text="", bg="#f0f0f0", justify="left", font=("Arial", 9))
        self.model_description_label.pack(anchor="w", pady=2)

        # Right side - OOP Concepts
        right_info = tk.Frame(info_frame, bg="#f0f0f0")
        right_info.pack(side="right", fill="both", expand=True, padx=10, pady=8)

        tk.Label(
            right_info,
            text="OOP Concepts Explanation:",
            bg="#f0f0f0",
            font=("Arial", 10, "bold"),
        ).pack(anchor="w", pady=(0, 5))
        
        # Dynamic OOP concept labels
        self.oop_concept1_label = tk.Label(right_info, text="", bg="#f0f0f0", justify="left", font=("Arial", 9))
        self.oop_concept1_label.pack(anchor="w", pady=2)
        
        self.oop_concept2_label = tk.Label(right_info, text="", bg="#f0f0f0", justify="left", font=("Arial", 9))
        self.oop_concept2_label.pack(anchor="w", pady=2)
        
        self.oop_concept3_label = tk.Label(right_info, text="", bg="#f0f0f0", justify="left", font=("Arial", 9))
        self.oop_concept3_label.pack(anchor="w", pady=2)
       

        # Notes section
        notes_frame = tk.Frame(main_frame, bg="#f0f0f0")
        notes_frame.pack(fill="x", pady=(10, 0))

        # tk.Label(notes_frame, text="Notes: Extra notes, instructions, or references.",
        #         bg='#f0f0f0', font=('Arial', 9)).pack(anchor="w")

        self._instances = {}
        self._update_model_interface()
        self._update_input_visibility()
        self._update_model_info()  # Add this line

        # Show initial model selection message
        initial_model = self.model_var.get()
        self.write_output(f"Model selected: {initial_model}")
        # self.write_output("Ready to process input...")

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(
            label="New Session", command=self.new_session, accelerator="Ctrl+N"
        )
        file_menu.add_command(
            label="Open Input File...",
            command=self.open_input_file,
            accelerator="Ctrl+O",
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Save Output", command=self.save_output, accelerator="Ctrl+S"
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit, accelerator="Ctrl+Q")
        menubar.add_cascade(label="File", menu=file_menu)

        # Models menu
        models_menu = tk.Menu(menubar, tearoff=0)
        # models_menu.add_command(label="Load Text Classifier", command=lambda: self.load_specific_model("text"))
        # models_menu.add_command(label="Load Image Classifier", command=lambda: self.load_specific_model("image"))
        # models_menu.add_separator()
        models_menu.add_command(
            label="Model Information...", command=self.show_model_info
        )
        # models_menu.add_command(label="Performance Stats", command=self.show_performance_stats)
        models_menu.add_command(
            label="Clear Model Cache", command=self.clear_model_cache
        )
        models_menu.add_separator()
        models_menu.add_command(
            label="Reload Current Model", command=self.reload_current_model
        )
        menubar.add_cascade(label="Models", menu=models_menu)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Quick Start Guide", command=self.show_quick_start)
        # help_menu.add_command(label="User Manual", command=self.show_user_manual)
        help_menu.add_command(label="Model Documentation", command=self.show_model_docs)
        help_menu.add_separator()
        help_menu.add_command(
            label="OOP Concepts Explained", command=self.show_oop_explanation
        )
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts)
        help_menu.add_separator()
        help_menu.add_command(
            label="Troubleshooting", command=self.show_troubleshooting
        )
        help_menu.add_command(label="About...", command=self.show_about)
        # help_menu.add_separator()
        menubar.add_cascade(label="Help", menu=help_menu)

        # Bind keyboard shortcuts
        self.bind_all("<Control-n>", lambda e: self.new_session())
        self.bind_all("<Control-o>", lambda e: self.open_input_file())
        self.bind_all("<Control-s>", lambda e: self.save_output())
        self.bind_all("<Control-q>", lambda e: self.quit())

    def _on_model_change(self, event=None):
        """Called when model selection changes"""
        selected_model = self.model_var.get()
        self.write_output(f"Model selected: {selected_model}")
        self._update_model_interface()
        self._update_model_info()

    def _update_model_interface(self):
        """Update interface based on selected model type"""
        selected_model = self.model_var.get()

        if "Text-to-Sentiment" in selected_model:
            # For Text-to-Sentiment models, only show text input
            self.radio_frame.pack_forget()
            self.input_type.set("text")
            self._update_input_visibility()
        elif "Image Classification" in selected_model:
            # For Image Classification models, only show image input
            self.radio_frame.pack_forget()
            self.input_type.set("image")
            self._update_input_visibility()
        else:
            # For other models, show both options
            self.radio_frame.pack(fill="x", padx=5, pady=5)
            self._update_input_visibility()

    def _update_input_visibility(self):
        self.text_input_frame.pack_forget()
        self.image_input_frame.pack_forget()

        if self.input_type.get() == "text":
            self.text_input_frame.pack(fill="both", expand=True)
        else:
            self.image_input_frame.pack(fill="both", expand=True)

    def _update_model_info(self):
        """Update the model information section based on selected model"""
        selected_model = self.model_var.get()

        if "Text-to-Sentiment" in selected_model:
            model_name = "• Model: distilbert-base-uncased-finetuned-sst-2-english"
            category = "• Category: Text Classification (Sentiment)"
            description = "• Use: Analyzes text sentiment (Positive/Negative)"
            
            # OOP concepts for Text Classification
            oop_concept1 = "• Inheritance: TextClassifier inherits from BaseModel"
            oop_concept2 = "• Decorators: @timeit, @log_call track performance"
            oop_concept3 = "• Encapsulation: Private _tokenize() method"
            
        elif "Image Classification" in selected_model:
            model_name = "• Model: google/vit-base-patch16-224"
            category = "• Category: Vision Transformer (Image)"
            description = "• Use: Classifies images into 1000+ categories"
            
            # OOP concepts for Image Classification  
            oop_concept1 = "• Inheritance: ImageClassifier inherits from BaseModel"
            oop_concept2 = "• Polymorphism: Override process() with image logic"
            oop_concept3 = "• Mixins: Uses ImageProcessingMixin for utilities"
            
        else:
            model_name = "• Model: Unknown"
            category = "• Category: Not specified"
            description = "• Use: Model information not available"
            
            # Generic OOP concepts
            oop_concept1 = "• Multiple inheritance: Both models use mixins"
            oop_concept2 = "• Decorators: @ensure_input validates data"
            oop_concept3 = "• Polymorphism: Common interface, different logic"

        # Update the dynamic model info labels
        self.model_name_label.config(text=model_name)
        self.model_category_label.config(text=category)
        self.model_description_label.config(text=description)
        
        # Update the dynamic OOP concept labels
        self.oop_concept1_label.config(text=oop_concept1)
        self.oop_concept2_label.config(text=oop_concept2)
        self.oop_concept3_label.config(text=oop_concept3)

    def browse_image(self):
        from tkinter import filedialog
        import os

        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if path:
            self.image_path.set(path)
            # Update the label to show selected filename
            filename = os.path.basename(path)
            self.selected_file_label.config(text=f"Selected: {filename}")
        else:
            self.selected_file_label.config(text="No file selected")

    def load_model(self):
        self.write_output(f"Loading model: {self.model_var.get()}")

    def run_model(self):
        """Run model with loading indicator and threading"""
        model_name = self.model_var.get()
        input_type = self.input_type.get()

        if input_type == "text":
            input_data = self.text_input.get("1.0", "end").strip()
            if not input_data:
                self.write_output("ERROR: Text input is empty.")
                return
        else:
            input_data = self.image_path.get()
            if not input_data:
                self.write_output("ERROR: No image file selected.")
                return

        # Start loading state
        self._start_loading()
        
        # Run model processing in separate thread to prevent UI freezing
        thread = threading.Thread(
            target=self._process_model_async, 
            args=(model_name, input_data), 
            daemon=True
        )
        thread.start()

    def _start_loading(self):
        """Show loading indicator and disable UI"""
        self.run_btn.config(state="disabled", text="Processing...")
        self.loading_label.pack(side="left")
        self.write_output("🔄 Processing model...")
        self.update()  # Force GUI update

    def _stop_loading(self):
        """Hide loading indicator and re-enable UI"""
        self.run_btn.config(state="normal", text="Run Model")
        self.loading_label.pack_forget()

    def _process_model_async(self, model_name, input_data):
        """Process model in background thread"""
        try:
            # Get or create model instance
            if model_name not in self._instances:
                _, model_class = MODEL_CHOICES[model_name]
                self._instances[model_name] = model_class()

            model = self._instances[model_name]
            result = model.process(input_data)

            # Use after() to safely update GUI from thread
            self.after(0, self._display_result, model_name, result, model)

        except Exception as e:
            # Use after() to safely update GUI from thread
            self.after(0, self._display_error, str(e))

    def _display_result(self, model_name, result, model):
        """Display successful result and stop loading"""
        self.write_output(f"✅ ({model_name}) Result:")
        self.write_output(f"{result}")

        rt = getattr(model.process, "last_runtime_s", None)
        if rt is not None:
            self.write_output(f"⏱️ Runtime: {rt:.3f}s")
        
        self._stop_loading()

    def _display_error(self, error_msg):
        """Display error and stop loading"""
        self.write_output(f"❌ ERROR: {error_msg}")
        self._stop_loading()

    def write_output(self, text):
        self.output_text.config(state="normal")
        self.output_text.insert("end", text + "\n")
        self.output_text.config(state="disabled")
        self.output_text.see("end")

    def clear_output(self):
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.config(state="disabled")

    # File Menu Methods
    def new_session(self):
        self.clear_output()
        self.text_input.delete("1.0", "end")
        self.image_path.set("")
        self.selected_file_label.config(text="No file selected")
        self.write_output("New session started.")

    def open_input_file(self):
        from tkinter import filedialog

        file_path = filedialog.askopenfilename(
            title="Open Input File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.text_input.delete("1.0", "end")
                self.text_input.insert("1.0", content)

                # Automatically switch to Text-to-Sentiment model when loading text file
                self.model_var.set("Text-to-Sentiment")
                self._on_model_change()  # This will trigger the model change and update interface

                self.write_output(f"Loaded: {file_path}")
            except Exception as e:
                self.write_output(f"Error loading file: {e}")

    def save_output(self):
        from tkinter import filedialog

        file_path = filedialog.asksaveasfilename(
            title="Save Output",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if file_path:
            try:
                content = self.output_text.get("1.0", "end-1c")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                self.write_output(f"Output saved to: {file_path}")
            except Exception as e:
                self.write_output(f"Error saving file: {e}")

    # Models Menu Methods
    def load_specific_model(self, model_type):
        if model_type == "text":
            self.model_var.set("Text-to-Sentiment")
        elif model_type == "image":
            self.model_var.set("Image Classification")
        self.load_model()

    def show_model_info(self):
        from tkinter import messagebox

        current_model = self.model_var.get()
        info = f"Current Model: {current_model}\n\n"
        if "Text" in current_model:
            info += "Model: distilbert-base-uncased-finetuned-sst-2-english\n"
            info += "Task: Sentiment Analysis\n"
            info += "Type: Text Classification"
        else:
            info += "Model: google/vit-base-patch16-224\n"
            info += "Task: Image Classification\n"
            info += "Type: Vision Transformer"
        messagebox.showinfo("Model Information", info)

    def show_performance_stats(self):
        from tkinter import messagebox

        stats = "Performance Statistics:\n\n"
        stats += "• Average inference time\n"
        stats += "• Memory usage\n"
        stats += "• Accuracy metrics\n"
        stats += "• Model load times"
        messagebox.showinfo("Performance Stats", stats)

    def clear_model_cache(self):
        self._instances.clear()
        self.write_output("Model cache cleared.")

    def reload_current_model(self):
        current_model = self.model_var.get()
        if current_model in self._instances:
            del self._instances[current_model]
        self.load_model()

    # Help Menu Methods
    def show_quick_start(self):
        from tkinter import messagebox

        guide = "Quick Start Guide:\n\n"
        guide += "1. Select a model from the dropdown\n"
        # guide += "2. Click 'Load Model' to initialize\n"
        guide += "2. Choose Text or Image input accordingly\n"
        guide += "3. Enter your input data\n"
        guide += "4. Click 'Run Model'\n"
        guide += "5. View results in Output Display"
        messagebox.showinfo("Quick Start", guide)

    def show_user_manual(self):
        from tkinter import messagebox

        messagebox.showinfo(
            "User Manual",
            "Complete user manual with detailed instructions for all features.",
        )

    def show_model_docs(self):
        import webbrowser

        webbrowser.open("https://huggingface.co/docs/transformers")

    def show_oop_explanation(self):
        try:
            with open("docs/oop_explainer.txt", "r") as f:
                content = f.read()
            from tkinter import messagebox

            messagebox.showinfo("OOP Concepts", content)
        except FileNotFoundError:
            from tkinter import messagebox

            messagebox.showerror("Error", "OOP explanation file not found.")

    def show_shortcuts(self):
        from tkinter import messagebox

        shortcuts = "Keyboard Shortcuts:\n\n"
        shortcuts += "Ctrl+N - New Session\n"
        shortcuts += "Ctrl+O - Open Input File\n"
        shortcuts += "Ctrl+S - Save Output\n"
        shortcuts += "Ctrl+Q - Exit Application"
        messagebox.showinfo("Shortcuts", shortcuts)

    def show_troubleshooting(self):
        from tkinter import messagebox

        tips = "Troubleshooting Tips:\n\n"
        tips += "• Ensure input data is valid\n"
        tips += "• Check internet connection for model downloads\n"
        tips += "• Restart if models fail to load\n"
        tips += "• Clear model cache if experiencing issues"
        messagebox.showinfo("Troubleshooting", tips)

    def show_about(self):
        from tkinter import messagebox

        about = "Tkinter AI GUI v1.0\n\n"
        about += "A demonstration of AI model integration\n"
        about += "with OOP principles in Python.\n\n"
        about += "Models: Hugging Face Transformers\n"
        about += "Framework: Tkinter GUI"
        messagebox.showinfo("About", about)
