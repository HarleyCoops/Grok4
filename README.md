
# Grok4 Animation Generator

Welcome to the Grok4 Animation Generator project. This tool leverages the power of AI, specifically Grok4 to transform text descriptions of complex mathematical and physical concepts into fully rendered animations using the Manim library.

## Overview

This project automates the creation of educational animations for topics in mathematics and physics, with a focus on Quantum Field Theory as an example. By inputting detailed text descriptions, Grok4 interprets these narratives and generates corresponding Manim scripts, which are then rendered into high-quality video animations.

## How It Works

1. **Text Description Input**: The process begins with a detailed text description of the desired animation, stored in `universe.txt`. This file contains the narrative and visual elements for the animation, such as scenes, transitions, and mathematical equations.

2. **Grok4 Interpretation**: Using the script `grok4call.py`, the text from `universe.txt` is fed to the Grok-4 model The generated script is saved as `manim_quantum_field_theory.py`.

3. **Manim Script Execution**: The generated Manim script (e.g., `quantum_field_theory_clean.py`) is a Python file that uses the Manim Community library (version 0.19 or compatible). When executed, it renders the animation scenes, including 3D elements, equations in LaTeX, camera movements, and visual effects as specified. The output is a series of video files stored in the `media/videos/` directory.

4. **Animation Output**: The final animations are high-quality videos (e.g., in 1080p60 resolution) that visually explain complex concepts through multiple scenes. For instance, the Quantum Field Theory animation includes segments on quantum fields, Maxwell's equations, QED Lagrangian density, Feynman diagrams, and coupling constants.

## Project Structure

- **`grok4call.py`**: Script to interface with Grok4 via the OpenAI API, converting text descriptions to Manim code.
- **`universe.txt`**: Input file containing the text description of the animation.
- **`manim_quantum_field_theory.py`**: Generated Manim script from Grok4.
- **`quantum_field_theory_clean.py`**: A refined or final version of the Manim script for Quantum Field Theory animation.
- **`media/videos/`**: Directory containing rendered animation video files.
- **`requirements.txt`**: Lists Python dependencies for the project (Note: Manim may need to be installed separately).

## Setup Instructions

1. **Install Dependencies**: Ensure Python is installed, then install the required packages listed in `requirements.txt` using:
   ```
   pip install -r requirements.txt
   ```
   Note: The Manim library is not listed in `requirements.txt` and must be installed separately if not already present. Follow the [Manim installation guide](https://docs.manim.community/en/stable/installation.html) for version 0.19 or compatible.

2. **API Key Configuration**: Set up your API key for accessing Grok4 in a `.env` file or environment variable as `XAI_API_KEY`.

3. **Prepare Text Description**: Edit `universe.txt` with your animation description, detailing scenes, visual elements, and mathematical concepts.

4. **Generate Manim Script**: Run `grok4call.py` to generate the Manim script:
   ```
   python grok4call.py
   ```

5. **Render Animation**: Execute the generated Manim script to produce the animation videos:
   ```
   manim -pql manim_quantum_field_theory.py QuantumFieldTheoryAnimation
   ```
   Adjust the command based on desired quality settings (e.g., `-pql` for preview quality or `-pqh` for high quality).

## Additional Notes

- Ensure you have the necessary computational resources for rendering animations, as Manim can be resource-intensive for complex scenes.
- The project includes demo scripts like `demo_basic_chat.py`, `demo_data_analysis_agent.py`, and `demo_web_research_agent.py` which may provide additional context or examples of Grok4's capabilities.

## Contributing

Contributions to improve the script generation or animation rendering process are welcome. Please submit issues or pull requests to the repository for consideration.