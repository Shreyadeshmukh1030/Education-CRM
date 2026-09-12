import os
import glob
for f in glob.glob('apps/*/apps.py'):
    with open(f, 'r') as file:
        content = file.read()
    app_name = os.path.basename(os.path.dirname(f))
    content = content.replace(f"name = '{app_name}'", f"name = 'apps.{app_name}'")
    with open(f, 'w') as file:
        file.write(content)
