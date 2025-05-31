
````markdown
# LemmaCalc™ v0.5

**A safe, expressive, and interactive command-line calculator written in Python.**  
LemmaCalc™ brings tab-completion, variable assignments, advanced math functions, history tracking, and a slick ASCII interface to your terminal.

---

## 📦 Project Overview

LemmaCalc™ is a modern REPL-style calculator designed for power users and everyday problem solvers alike. Built on Python’s `ast` for safe expression parsing and `prompt_toolkit` for an intuitive interface, it lets you compute with clarity and flair.

---

## ✨ Features

- ✅ **Safe expression evaluation** using Python’s `ast` module  
- ✅ **REPL interface** with command history and multi-expression input  
- ✅ **Tab-completion** for math functions and constants  
- ✅ **Variable support** (`x = 5`, `y = sqrt(x)`)  
- ✅ **Built-in commands** like `history`, `clear`, `man`, and `tldr`  
- ✅ **Dozens of math functions**, including `sqrt`, `log`, `sin`, `factorial`, `degrees`, and more  
- ✅ **Formatted output** with thousands separators  
- ✅ **Colorized results and errors** for better readability  
- ✅ **Stylized ASCII welcome banner**

---

## 🚀 Getting Started

### 📥 Installation

Clone the repository:

```bash
git clone https://github.com/l3mm4/LemmaCalc-.git
cd project_calc
````

Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### ▶️ Running the Calculator

From the project root, launch LemmaCalc with:

```bash
python run_calc.py
```

---

## 🧠 Built-in Commands

| Command     | Description                                  |
| ----------- | -------------------------------------------- |
| `q`         | Quit the calculator                          |
| `clear`     | Clear the screen and show the banner again   |
| `history`   | Show a history of evaluated expressions      |
| `man`       | Show the full manual                         |
| `tldr`      | Show a short quick-reference guide           |
| `--version` | Show the current version (run with CLI flag) |

---

## 🧮 Supported Math Functions

All functions are from Python’s `math` module unless otherwise noted:

* `sqrt(x)` – Square root
* `log(x)` / `log10(x)` – Natural or base-10 log
* `sin(x)`, `cos(x)`, `tan(x)` – Trigonometric functions (radians)
* `factorial(x)` – Factorial (non-negative integers only)
* `abs(x)`, `pow(x, y)`, `round(x, n)`
* `floor(x)`, `ceil(x)` – Integer rounding
* `exp(x)` – e raised to x
* `degrees(x)`, `radians(x)` – Convert angles

---

## 💡 Examples

```text
> a = 5
a = 5

> b = sqrt(a)
b = 2.23606797749979

> a * b
Result: 11.180339887498949

> history
1: a = 5
2: b = 2.23606797749979
3: a * b = 11.180339887498949
```

---

## 📂 Project Structure

```
project_calc/
├── run_calc.py           # Main entry point
├── requirements.txt
├── README.md
├── history.json          # Session history (auto-created)
├── docs/                 # Manual and TLDR files
│   ├── man.txt
│   └── tldr.txt
├── lemma_calc/           # Core calculator package
│   ├── __init__.py
│   ├── main.py
│   ├── core.py
│   ├── core_utils.py
│   ├── constants.py
│   ├── display.py
│   ├── history.py
│   ├── input_handler.py
│   ├── preprocessor.py
│   ├── prompt_utils.py
└── tests/                # Unit tests << under development
```

---

## 📦 Future Plans

* [ ] Package for `pip install lemmacalc`
* [ ] Add persistent variable support
* [ ] Enhanced support for complex numbers
* [ ] GUI front-end using `textual` or `urwid`

---

## 📝 License

Released under the MIT License.
© 2025 Sean Jette · LemmaCalc™

---

## 🌐 Author

**Sean Jette**
📧 [l3mm4x@proton.me](mailto:l3mm4x@proton.me)
🐙 [github.com/l3mm4](https://github.com/l3mm4)

```
