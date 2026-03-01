import json
import sys

# Factory Imports
from plugins.inputs import CSVReader, JSONReader
from plugins.outputs import ConsoleWriter, GraphicsChartWriter, StreamlitDashboard
from core.engine import TransformationEngine

# ── 1. Dictionary-based Factories ──
INPUT_DRIVERS = {
    "csv": CSVReader,
    "json": JSONReader,
}

OUTPUT_DRIVERS = {
    "console": ConsoleWriter,
    "graphics": GraphicsChartWriter,
    "ui": StreamlitDashboard,
}

def load_config(path: str = "config.json") -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Could not load config: {e}")
        sys.exit(1)

def bootstrap():
    # ── 1. Load Configuration ──
    config = load_config("config.json")

    input_cfg = config.get("input", {})
    output_cfg = config.get("output", {})

    input_driver_key = input_cfg.get("driver", "csv")
    output_driver_key = output_cfg.get("driver", "console")
    file_path = input_cfg.get("file_path", "gdp.csv")

    # ── 2. Instantiate Output (The Sink) ──
    SinkClass = OUTPUT_DRIVERS.get(output_driver_key)
    if not SinkClass:
        print(f"Unknown output: {output_driver_key}")
        sys.exit(1)
    
    sink = SinkClass()

    # ── 3. Instantiate Core (Dependency Injection of Sink) ──
    engine = TransformationEngine(sink=sink, config=config)

    # ── 4. Instantiate Input (Dependency Injection of Core) ──
    InputClass = INPUT_DRIVERS.get(input_driver_key)
    if not InputClass:
        print(f"Unknown input: {input_driver_key}")
        sys.exit(1)
    
    reader = InputClass(service=engine, file_path=file_path)

    # ── 5. Execution ──
    # If the output is the UI, we let Streamlit handle the display flow
    # If it's console/graphics, we print the status to terminal
    if output_driver_key != "ui":
        print(f"[Pipeline] Running: {input_driver_key} -> {output_driver_key}")
    
    reader.run()

if __name__ == "__main__":
    bootstrap()