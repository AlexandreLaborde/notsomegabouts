import os
from pathlib import Path

def generate_rst_files(package_path, output_dir):
    package_path = Path(package_path).resolve()
    output_dir = Path(output_dir).resolve()

    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    package_name = package_path.name
    
    for root, dirs, files in os.walk(package_path):
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')
        
        root_path = Path(root)
        
        # Calculate the relative path from the package root
        rel_path = root_path.relative_to(package_path)
        
        # Convert the relative path to a module path
        module_path = '.'.join(rel_path.parts)
        if module_path == '':
            module_path = package_name
        else:
            module_path = f"{package_name}.{module_path}"
        
        # Create the corresponding path in the output directory
        rst_dir = output_dir / rel_path
        rst_dir.mkdir(parents=True, exist_ok=True)
        
        rst_path = rst_dir / f"{root_path.name}.rst"
        
        with rst_path.open('w') as f:
            f.write(f"{module_path}\n")
            f.write("=" * len(module_path) + "\n\n")
            f.write(f".. py:module:: {module_path}\n\n")
            
            for file in files:
                if file.endswith('.py') and not file.startswith('__'):
                    module_name = file[:-3]
                    full_module_path = f"{module_path}.{module_name}"
                    
                    f.write(f".. automodule:: {full_module_path}\n")
                    f.write("   :members:\n")
                    f.write("   :undoc-members:\n")
                    f.write("   :show-inheritance:\n\n")

    # Create the main index.rst file
    with (output_dir / 'index.rst').open('w') as f:
        f.write(f"{package_name}\n")
        f.write("=" * len(package_name) + "\n\n")
        f.write(".. toctree::\n")
        f.write("   :maxdepth: 2\n")
        f.write("   :caption: Contents:\n\n")
        
        for rst_file in output_dir.rglob('*.rst'):
            if rst_file.name != 'index.rst':
                rel_path = rst_file.relative_to(output_dir)
                f.write(f"   {rel_path.with_suffix('')}\n")

if __name__ == "__main__":
    package_path = "E:/repos/orger/megabouts/megabouts"
    output_dir = "E:/repos/orger/megabouts/docs/source/api"
    generate_rst_files(package_path, output_dir)