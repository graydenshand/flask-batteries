from .base_generator import BaseGenerator
import os
from ..helpers import verify_file


class StylesheetGenerator(BaseGenerator):
    """
    Generate (or destroy) a stylesheet.

    If using webpack:
            * Generate a new .scss file and import it into 'styles.scss'
    If not:
            * Generate a new .css file and import it into 'styles.css'
    """

    @staticmethod
    def generate(name):
        use_webpack = not verify_file(
            os.path.join("src", "config.py"), ["BATTERIES_USE_WEBPACK"]
        )
        if use_webpack:
            with open(
                os.path.join("src", "assets", "stylesheets", f"_{name}.scss"), "w"
            ) as f:
                yield f'Created {os.path.join("src", "assets", "stylesheets", f"_{name}.scss")}'
            with open(
                os.path.join("src", "assets", "stylesheets", "styles.scss"), "a"
            ) as f:
                f.write(f"\n@use '{name}';")
                yield f'Added import to {os.path.join("src", "assets", "stylesheets", "styles.scss")}'
        else:
            with open(
                os.path.join("src", "static", "stylesheets", f"{name}.css"), "w"
            ) as f:
                yield f'Created {os.path.join("src", "static", "stylesheets", f"{name}.css")}'

    @staticmethod
    def destroy(name):
        use_webpack = not verify_file(
            os.path.join("src", "config.py"), ["BATTERIES_USE_WEBPACK"]
        )

        if use_webpack:
            os.remove(os.path.join("src", "assets", "stylesheets", f"_{name}.scss"))
            yield f'Destroyed {os.path.join("src", "assets", "stylesheets", f"_{name}.scss")}'
            with open(
                os.path.join("src", "assets", "stylesheets", "styles.scss"), "r+"
            ) as f:
                lines = f.read().split("\n")

                i = 0
                while i < len(lines):
                    if lines[i] == f"@use '{name}';":
                        del lines[i]
                        break
                    i += 1

                f.seek(0)
                f.truncate()
                f.write("\n".join(lines))
            yield f'Removed import from {os.path.join("src", "assets", "stylesheets", "styles.scss")}'
        else:
            os.remove(os.path.join("src", "static", "stylesheets", f"{name}.css"))
            yield f'Destroyed {os.path.join("src", "static", "stylesheets", f"{name}.css")}'
