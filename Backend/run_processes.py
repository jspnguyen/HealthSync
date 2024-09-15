import subprocess

scripts = ['main.py', 'api/api.py', 'pipeline1.py', 'pipeline2.py', 'pipeline3.py']

for script in scripts:
    print(f"Running {script}...")
    subprocess.run(['python', script])  
    print(f"{script} finished.\n")
