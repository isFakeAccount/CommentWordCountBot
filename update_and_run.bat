git pull
venv\Scripts\pip install -r requirements.txt
venv\Scripts\pip install --user --upgrade pip

if exist config.yaml (
	venv\Scripts\python main.py
	pause
) else (
	echo "config.yaml file not found. Please create the file from example_config.yaml"
	pause
	exit \b -1
)