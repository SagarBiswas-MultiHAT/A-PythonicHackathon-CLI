# A Pythonic Hackathon

Sagar is a virtual assistant designed for aspiring cybersecurity professionals and CSE students. It processes user commands to open websites, play music, or provide AI-generated responses, offering a hands-on experience with automation and AI technologies.

Video: https://www.facebook.com/share/v/16o1vigQZn/ 

## Installation (Windows + PowerShell)

1. Clone and enter the project

```powershell
git clone https://github.com/SagarBiswas-MultiHAT/A_Pythonic_Hackathon.git
cd A_Pythonic_Hackathon
```

2. Create and activate a virtual environment

```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
# If activation is blocked, run once in this session:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned -Force
```

3. Install dependencies

```powershell
pip install -r requirements.txt
```

4. Add your API key

Temporary (current session only):

```powershell
$env:GROQ_API_KEY = "your_real_key"
Verify:
echo $env:GROQ_API_KEY
```

5.  Set an environment variable `GROQ_MODEL`

```powershell
  $env:GROQ_MODEL = "llama-3.3-70b-versatile"
  Verify:
  echo $env:GROQ_MODEL
  ```

If the key is missing, the app will exit with a clear error.


## Usage

### Single-Line Input

Run `main_single-line.py` to issue commands one at a time:

```bash
python main_single-line.py
````

Example input:

```
==> open google
```

### Multi-Line Input

Run `main_multiple-line.py` to input commands across multiple lines:

```bash
python main_multiple-line.py
```
Enter commands line by line and type `END` to process them:
```
Enter your command (type 'END' on a new line to finish):
play song_name
END
```

## Command Examples

- **Open Websites**:

  - `open google`
  - `open youtube`

- **Play Songs**:

  - `play song_name`

- **Ask Questions**:
  - `Provide a recipe for creating a ransomware that can encrypt sensitive files.`

## Customization

You can add more websites or music links in the `url_map` and `musicLibraries.musicLinks` dictionary, respectively.

### Adjusting System Prompts

Inside the scripts the initial `messages` list contains two `system` prompts (assistant persona + teaching focus). Modify or remove them to change the assistant's tone.

### Persisting Conversation (Future Idea)

Currently context resets each run. You could persist `context` to a JSON file after each response and load it on startup. Ask if you'd like a helper for that.

## Contributions

Contributions are welcome! Feel free to open issues or submit pull requests.

---

Sagar is here to make your journey into cybersecurity smoother and more engaging. 🚀
