# Code Agent CLI

A CLI AI agent powered by Gemini that helps you write and modify code in your local project directory.

## 🔧 Features

* Uses Gemini to generate code-editing plans.
* Can:

  * List and read files
  * Overwrite or create files
  * Execute Python scripts with arguments
* Automatically scans the working directory (`.`) for relevant files.
* Verifies changes by running application and tests.

## ⚙️ Setup

1. **Install [`uv`](https://github.com/astral-sh/uv):**

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install dependencies:**

   ```bash
   uv venv
   uv pip install -r requirements.txt
   ```

3. **Add your Gemini API key in a `.env` file:**

   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

4. **Run the CLI:**

   ```bash
   uv venv exec python cli.py
   ```

## ⚠️ Disclaimer

* **Not production-safe**: Minimal security checks.
* **No sandboxing**: Modifies local files directly.
* **No contributions accepted**.

Use only in local/dev environments.
