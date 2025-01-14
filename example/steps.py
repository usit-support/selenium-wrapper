import os
import re
import sys
import yaml
import time
from typing import Optional, Callable

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.chrome import ChromeBrowser

class TestSteps:
    """Handle test step definitions following SOLID principles."""
    
    def __init__(self, steps_file: str = "steps.yml"):
        self.browser = ChromeBrowser()
        self._step_results: list[dict] = []
        self.steps_data = self._load_steps(steps_file)
        self.steps_delay = self.steps_data["setup"].get("steps_delay_in_seconds", 1)

    def _load_steps(self, file_steps: str) -> dict:
        """Load and process steps from YAML file."""
        if not os.path.exists(file_steps):
            raise FileNotFoundError(f"Steps file not found: {file_steps}")

        with open(file_steps, "r") as file:
            content = file.read()

        # Load initial YAML for variable substitution
        yaml_data = yaml.safe_load(content)

        # Substitution function for variables
        def subst(match):
            keys = match.group(1).split('.')
            valor = yaml_data
            for key in keys:
                valor = valor.get(key, match.group(0))
                if valor == match.group(0):
                    break
            return valor

        # Process variables in YAML
        pattern = re.compile(r'\$\{([^\}]+)\}')
        processed_content = pattern.sub(subst, content)
        
        return yaml.safe_load(processed_content)

    def execute_step(self, step: dict):
        """Execute a single test step."""
        step_id = step.get("step")
        step_type = step.get("step_type")
        element_xpath = step.get("element_xpath")
        
        try:
            match step_type:
                case "click":
                    return self.browser.click_element(element_xpath)
                case "menu":
                    menu_text = step.get("menu_text", "")
                    return self.browser.click_menu(menu_text)
                case "informar-valor":
                    value = step.get("element_value", "")
                    return self.browser.set_value(element_xpath, value)
                case "logout":
                    self.cleanup()
                    return None
                case _:
                    raise ValueError(f"Unknown step type: {step_type}")

        except Exception as e:
            self._record_step_result(step_id, False, step, str(e))
            raise

    def execute_all_steps(self) -> None:
        """Execute all steps in the loaded YAML file."""
        for step in sorted(self.steps_data["steps"], key=lambda x: int(x["step"])):
            if step.get("enable"):
                self.execute_step(step)
                time.sleep(self.steps_delay)

    def _record_step_result(self, step_id: str, success: bool, 
                          params: dict, error: str = None) -> None:
        """Record step execution result."""
        self._step_results.append({
            "step_id": step_id,
            "success": success,
            "params": params,
            "error": error
        })

    def get_results(self) -> list[dict]:
        """Get test execution results."""
        return self._step_results

    def cleanup(self) -> None:
        """Clean up resources."""
        self.browser.close()

def main():
    """Main function for CLI usage."""
    file_steps = sys.argv[1] if len(sys.argv) > 1 else "steps.yml"
    print(f"Using steps file: {file_steps}")
    
    steps = TestSteps(file_steps)
    try:
        steps.execute_all_steps()
    finally:
        steps.cleanup()
        pass

if __name__ == "__main__":
    main()
