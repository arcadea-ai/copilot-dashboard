# GitHub Copilot Dashboard

GitHub Copilot Dashboard is a visual interface to monitor and analyze GitHub Copilot metrics.

## Setup

Follow these steps to set up and run the dashboard:

### 1. Set Up Python Environment

You can use either `venv` or `conda` to create an isolated Python environment.

#### Using `venv` (Python 3.10)
```sh
python3.10 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

#### Using Conda
```sh
conda create --name copilot-dashboard python=3.10
conda activate copilot-dashboard
```

### 2. Install Dependencies
Navigate to the `src` directory and install the required packages:
```sh
cd src
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a .env file inside the src directory and add the following:
```sh
GITHUB_API_KEY=<your_personal_access_token>
```

### 4. Generate a GitHub API Key
Follow these steps to generate a GitHub API key:

1. Click on your profile icon in the top-right corner of GitHub.
2. Go to **Settings**.
3. Navigate to **Developer Settings**.
4. Select **Personal Access Tokens**.
5. Click **Generate new token**.
6. Grant the following permissions:
   - `manage_billing:copilot`
   - `read:org`
   - `read:enterprise`
7. Generate and copy the token.
8. Paste it into the `.env` file as:

```env
GITHUB_API_KEY=your_generated_token_here
```
### 5. Run the Dashboard
Launch the Streamlit dashboard with bellow command:
```sh
streamlit run app.py
```
The dashboard should now be accessible in your browser under `http://localhost:8501` with default configurations.