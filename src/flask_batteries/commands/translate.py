import click
import subprocess
import os
import re


@click.group(help="Flask-Babel translation commands")
def translate():
    pass


@click.command(help="Update all languages")
@click.option(
    "-k",
    "--keywords",
    multiple=True,
    help="Space-separated list of keywords to look for in addition to the defaults (may be repeated multiple times)",
)
def update(keywords):
    command = ["pybabel", "extract", "-F", "babel.cfg"]
    if keywords:
        for keyword in keywords:
            command += ["-k", keyword]
    command += ["-o", "messages.pot", "."]

    extract_result = subprocess.run(command)
    if extract_result.returncode != 0:
        raise RuntimeError("pybabel extract command failed")

    update_result = subprocess.run(
        [
            "pybabel",
            "update",
            "-i",
            "messages.pot",
            "-d",
            os.path.join("src", "translations"),
        ]
    )
    if update_result.returncode != 0:
        raise RuntimeError("pybabel update command failed")

    os.remove("messages.pot")


translate.add_command(update)


@click.command(help="Compile all languages.")
def compile():
    compile_result = subprocess.run(["pybabel", "compile", "-d", "src/translations"])
    if compile_result.returncode != 0:
        raise RuntimeError("pybabel compile command failed")


translate.add_command(compile)


@click.command(help="Initialize a new language")
@click.argument("language")
@click.option(
    "-k",
    "--keywords",
    multiple=True,
    help="Space-separated list of keywords to look for in addition to the defaults (may be repeated multiple times)",
)
def init(language, keywords):
    command = ["pybabel", "extract", "-F", "babel.cfg"]
    if keywords:
        for keyword in keywords:
            command += ["-k", keyword]
    command += ["-o", "messages.pot", "."]

    extract_result = subprocess.run(command)
    if extract_result.returncode != 0:
        raise RuntimeError("pybabel extract command failed")

    init_result = subprocess.run(
        [
            "pybabel",
            "init",
            "-i",
            "messages.pot",
            "-d",
            os.path.join("src", "translations"),
            "-l",
            language,
        ]
    )
    if init_result.returncode != 0:
        raise RuntimeError("pybabel init command failed")

    os.remove("messages.pot")

    with open(os.path.join("src", "config.py"), "r+") as f:
        content = f.read()

        pattern = r"LANGUAGES = \[(.*)\]"
        content = re.sub(pattern, f'LANGUAGES = [\g<1>, "{language}"]', content)

        f.seek(0)
        f.truncate()
        f.write(content)


translate.add_command(init)
