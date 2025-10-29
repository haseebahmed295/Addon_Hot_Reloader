import importlib.util
import os
from typing import Set

class ModuleReloader:
    def __init__(self):
        self._processed_modules: Set[str] = set()
        
    def _is_separate_module(self, obj) -> bool:
        """Check if object is from a separate file."""
        return hasattr(obj, '__file__')
    
    def _reload_attribute(self, parent_mod, attr_name: str):
        """Reload a single attribute if it's a separate module."""
        try:
            attr = getattr(parent_mod, attr_name)
            if self._is_separate_module(attr) and parent_mod.__name__ in attr.__name__:
                print(f"Reloading {attr.__name__}")
                importlib.reload(attr)
                setattr(parent_mod, attr_name, attr)
                self._processed_modules.add(attr.__name__)
                return True
        except Exception as e:
            print(f"Error reloading {attr_name}: {str(e)}")
        return False
    
    def _process_attributes(self, mod):
        """Process all attributes of a module."""
        for attr_name in dir(mod):
            if attr_name.startswith('__') and attr_name.endswith('__'):
                continue
                
            self._reload_attribute(mod, attr_name)
    
    def reload_all(self, root_module):
        """
        Main entry point to reload all separate-file attributes recursively.
        
        Args:
            root_module: The top-level module to start processing from
        """
        if root_module.__name__ in self._processed_modules:
            print(f"Already processed {root_module.__name__}")
            return
            
        print(f"\nProcessing module: {root_module.__name__}")
        self._process_attributes(root_module)
        self._processed_modules.add(root_module.__name__)

