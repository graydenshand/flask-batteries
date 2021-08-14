from flask_batteries.helpers import *


def test_verify_file(tmp_path):
    with open(os.path.join(tmp_path, "test.txt"), "w") as f:
        f.write("Test\n")

    assert verify_file(os.path.join(tmp_path, "test.txt"), lines_to_verify=["Test"])
    assert not verify_file(os.path.join(tmp_path, "test.txt"), lines_to_verify=["Foo"])
