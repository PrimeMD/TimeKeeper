import pathlib
import importlib.util

# Path to the current directory
current_dir = pathlib.Path(__file__).parent

# Dynamically load all command files
for file in current_dir.glob('*.py'):
    if file.name.startswith("_"):  # Skip these files
        continue
    module_name = f'{current_dir.name}.{file.stem}'
    spec = importlib.util.spec_from_file_location(module_name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
