import json
import os
from pathlib import Path
import re
import shutil

class TemplatesManager:
    def __init__(self):
        self.templates_dir = Path("templates")
        self.templates_dir.mkdir(exist_ok=True)
        
        # Cache for templates 
        self._templates_cache = None
        
    def sanitize_filename(self, template_name):
        """Convert template name to a valid filename."""
        # Replace spaces and special chars with underscores, make lowercase
        sanitized = re.sub(r'[^\w\s-]', '', template_name.lower())
        sanitized = re.sub(r'[\s-]+', '_', sanitized)
        return sanitized + ".json"
    
    def _save_template_to_file(self, template_data):
        """Save a template to an individual file."""
        try:
            if "name" not in template_data:
                return
            
            filename = self.sanitize_filename(template_data["name"])
            file_path = self.templates_dir / filename
            
            # Check if file exists and check permissions
            if file_path.exists():
                # Check file permissions
                is_writable = os.access(file_path, os.W_OK)
                if not is_writable:
                    try:
                        # Try to make the file writable
                        os.chmod(file_path, 0o644)
                    except Exception:
                        pass
            
            # Make sure templates directory exists
            os.makedirs(self.templates_dir, exist_ok=True)
            
            # Write to temporary file first
            temp_file = file_path.with_suffix('.tmp')
            
            with open(temp_file, 'w') as f:
                json.dump(template_data, f, indent=4)
                f.flush()
                os.fsync(f.fileno())  # Ensure data is written to disk
            
            # Verify temp file was written correctly
            if temp_file.exists():
                # Now rename temp file to target file
                if file_path.exists():
                    # On Windows, we might need to remove the destination file first
                    file_path.unlink()
                    
                os.replace(temp_file, file_path)
            else:
                return False
            
            # Verify final file
            if file_path.exists():
                # Clear the cache to force reload
                self._templates_cache = None
                return True
            else:
                return False
            
        except Exception:
            import traceback
            traceback.print_exc()
            return False
    
    def load_templates(self, force_reload=False):
        """Load all templates from individual files."""
        # Return cached templates if available and force_reload is False
        if self._templates_cache is not None and not force_reload:
            return self._templates_cache

        templates = {}
        
        # Scan directory for template files
        json_files = list(self.templates_dir.glob("*.json"))
        
        for file_path in json_files:
            try:
                with open(file_path, 'r') as f:
                    template_data = json.load(f)
                    
                # Use the filename without extension as the key
                key = file_path.stem
                templates[key] = template_data
            except Exception:
                pass
        
        # Cache the templates
        self._templates_cache = templates
        
        return templates
    
    def get_template(self, template_name):
        """Get a specific template by name."""
        filename = self.sanitize_filename(template_name)
        file_path = self.templates_dir / filename
        
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    return json.load(f)
            except Exception:
                return None
        
        return None
    
    def add_template(self, name, template_data):
        """Add a new template."""
        # Make sure template data has the correct structure
        if "name" not in template_data:
            template_data["name"] = name
            
        self._save_template_to_file(template_data)
        return True
    
    def delete_template(self, template_name):
        """Delete a template."""
        filename = self.sanitize_filename(template_name)
        file_path = self.templates_dir / filename
        
        if file_path.exists():
            try:
                file_path.unlink()
                return True
            except Exception:
                return False
        
        return False