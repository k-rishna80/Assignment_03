# 🤖 Tkinter AI GUI - HIT137 Assignment

A modern Python GUI application demonstrating AI model integration with Object-Oriented Programming principles. This application provides an intuitive interface for text sentiment analysis and image classification using Hugging Face Transformers.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![AI](https://img.shields.io/badge/AI-HuggingFace-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [AI Models](#-ai-models)
- [OOP Concepts Demonstrated](#-oop-concepts-demonstrated)
- [GUI Components](#-gui-components)
- [API Reference](#-api-reference)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

## ✨ Features

### 🎯 Core Functionality
- **Text Sentiment Analysis** - Analyze emotional tone of text (Positive/Negative)
- **Image Classification** - Classify images into 1000+ categories
- **Dynamic Model Selection** - Easy switching between AI models
- **Real-time Processing** - Background processing with loading indicators

### 🎨 User Interface
- **Professional GUI** - Modern Tkinter interface with 50/50 layout
- **Loading Indicators** - Visual feedback during model processing
- **Menu System** - Comprehensive menus with keyboard shortcuts
- **Dynamic Information** - Context-aware model and OOP concept explanations

### 🔧 Technical Features
- **Threading Support** - Non-blocking UI during model inference
- **Error Handling** - Robust error management with user-friendly messages
- **File Operations** - Load text files, save outputs, browse images
- **Model Caching** - Efficient model instance management


## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Setup

1. **Navigate to the project directory**
```bash
cd hit137-ai-gui
```

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

1. **Run the application**
```bash
python main.py
```


## 🎮 Usage

### Getting Started

1. **Launch the Application**
   ```bash
   python main.py
   ```

2. **Select a Model**
   - Choose between "Text-to-Sentiment" or "Image Classification"
   - The interface will automatically adapt to your selection

3. **Provide Input**
   - **Text Model**: Type or paste text in the input area
   - **Image Model**: Click "Browse for Image" to select an image file

4. **Run Analysis**
   - Click "Run Model" button
   - Watch the loading indicator during processing
   - View results in the output section

### Keyboard Shortcuts

| Shortcut | Action |
|----------|---------|
| `Ctrl+N` | New Session |
| `Ctrl+O` | Open Input File |
| `Ctrl+S` | Save Output |
| `Ctrl+Q` | Exit Application |

### Menu Options

#### File Menu
- **New Session** - Clear all inputs and outputs
- **Open Input File** - Load text from file
- **Save Output** - Export results to file
- **Exit** - Close application

#### Models Menu
- **Model Information** - View detailed model specs
- **Clear Model Cache** - Free up memory
- **Reload Current Model** - Refresh model instance

#### Help Menu
- **Quick Start Guide** - Basic usage instructions
- **Model Documentation** - Links to Hugging Face docs
- **OOP Concepts Explained** - Educational content
- **Keyboard Shortcuts** - Reference guide

## 📁 Project Structure

```
hit137-ai-gui/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── gui/                   # GUI components
│   ├── __init__.py
│   ├── app_gui.py        # Main application class
│   └── widgets.py        # Custom GUI widgets
├── models/               # AI model classes
│   ├── __init__.py
│   ├── base_model.py    # Abstract base class
│   ├── text_classifier.py # Text sentiment model
│   └── image_classifier.py # Image classification model
├── utils/               # Utility modules
│   ├── __init__.py
│   ├── decorators.py   # Function decorators
│   └── mixins.py       # Mixin classes
└── docs/               # Documentation
    ├── models_info.txt
    └── oop_explainer.txt
```

## 🤖 AI Models

### Text-to-Sentiment Model
- **Base Model**: `distilbert-base-uncased-finetuned-sst-2-english`
- **Task**: Sentiment Analysis
- **Input**: Raw text
- **Output**: Sentiment classification (POSITIVE/NEGATIVE) with confidence scores
- **Use Cases**: Social media monitoring, review analysis, feedback processing

### Image Classification Model
- **Base Model**: `google/vit-base-patch16-224`
- **Task**: Image Classification
- **Input**: Images (PNG, JPG, JPEG, BMP, GIF)
- **Output**: Object classification from 1000+ ImageNet categories
- **Use Cases**: Content moderation, image tagging, object recognition

## 🏗️ OOP Concepts Demonstrated

### 1. **Inheritance**
```python
class TextClassifier(BaseModel):
    """Inherits common functionality from BaseModel"""
    pass

class ImageClassifier(BaseModel):
    """Inherits common functionality from BaseModel"""
    pass
```

### 2. **Polymorphism**
```python
# Both models implement process() differently
text_model.process("Hello world")    # Text processing
image_model.process("image.jpg")     # Image processing
```

### 3. **Encapsulation**
- Private methods: `_tokenize()`, `_preprocess()`
- Protected attributes: `_model`, `_tokenizer`
- Public interface: `process()`, `get_info()`

### 4. **Multiple Inheritance & Mixins**
```python
class TextClassifier(BaseModel, LoggingMixin, TimerMixin):
    """Demonstrates multiple inheritance"""
    pass
```

### 5. **Decorators**
```python
@timeit
@log_call
@ensure_input
def process(self, input_data):
    """Function decorators for cross-cutting concerns"""
    pass
```

### 6. **Abstract Base Classes**
```python
from abc import ABC, abstractmethod

class BaseModel(ABC):
    @abstractmethod
    def process(self, input_data):
        pass
```

## 🖥️ GUI Components

### Layout System
- **50/50 Horizontal Split** - Input and Output sections
- **Dynamic Interfaces** - Adapts to selected model type
- **Responsive Design** - Proper scaling and padding

### Widget Hierarchy
```
App (tk.Tk)
├── MenuBar
├── ModelSelection (LabelFrame)
├── HorizontalFrame
│   ├── InputSection (LabelFrame)
│   │   ├── RadioButtons (conditional)
│   │   ├── TextInput (Text widget)
│   │   └── ImageInput (Browse button)
│   └── OutputSection (LabelFrame)
│       └── OutputText (Text widget)
├── ButtonFrame
│   ├── RunButton
│   ├── ClearButton
│   └── LoadingIndicator
└── InfoFrame (LabelFrame)
    ├── ModelInfo (dynamic)
    └── OOPConcepts (dynamic)
```

## 📚 API Reference

### Main Application Class

```python
class App(tk.Tk):
    """Main application window"""
    
    def run_model(self):
        """Execute model inference with threading"""
        
    def _update_model_interface(self):
        """Update UI based on selected model"""
        
    def _update_model_info(self):
        """Update dynamic information sections"""
```

### Model Classes

```python
class BaseModel(ABC):
    """Abstract base for all AI models"""
    
    @abstractmethod
    def process(self, input_data: str) -> str:
        """Process input and return result"""
```

### Utility Decorators

```python
@timeit
def function():
    """Measure execution time"""

@log_call  
def function():
    """Log function calls"""
    
@ensure_input
def function():
    """Validate input parameters"""
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Add tests** (if applicable)
5. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
6. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt
pip install black flake8 pytest  # Optional: code formatting and testing

# Run code formatter
black .

# Run linter
flake8 .
```

## 🔧 Troubleshooting

### Common Issues

**1. Model Download Fails**
```
❌ ERROR: Connection timeout
```
**Solution**: Check internet connection. Models download automatically on first use.

**2. Import Errors**
```
ModuleNotFoundError: No module named 'transformers'
```
**Solution**: Install dependencies: `pip install -r requirements.txt`

**3. Memory Issues**
```
❌ ERROR: Out of memory
```
**Solution**: Close other applications or use "Clear Model Cache" in menu.

**4. Image Loading Fails**
```
❌ ERROR: Cannot identify image file
```
**Solution**: Ensure image format is supported (PNG, JPG, JPEG, BMP, GIF).

### Performance Tips
- **First Run**: Model downloads may take time
- **Memory Usage**: Use "Clear Model Cache" to free memory
- **Processing Speed**: Larger images take longer to process

### Getting Help
- Check the **Help → Troubleshooting** menu in the application
- Review error messages in the output area
- Ensure all dependencies are properly installed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hugging Face** - For providing the transformer models
- **Python Community** - For excellent libraries and documentation
- **Tkinter** - For the GUI framework
- **HIT137 Course** - Educational context and requirements

## 📞 Contact

**Course**: HIT137 - Software Development  
**Institution**: [Your Institution]

---
