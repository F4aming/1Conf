import unittest
import io
from contextlib import redirect_stdout

from src.emulator import ShellEmulator


class TestEmulator(unittest.TestCase):

    def setUp(self):
        self.emulator = ShellEmulator(
            "maxko", "example_data/test.tar")

    def tearDown(self):
        if self.emulator.filesystem:
            self.emulator.filesystem.close()

    def assert_output(self, expected_output, method, *args, **kwargs):
        """Asserts that calling method with the given arguments produces the expected output to stdout."""
        f = io.StringIO()
        with redirect_stdout(f):
            method(*args, **kwargs)

        output = f.getvalue().strip()
        if isinstance(expected_output, list):
            expected_output = "\n".join(expected_output)
        self.assertEqual(output, expected_output)

    # ls tests
    def test_ls_root(self):
        expected_output = [
            ".gitattributes",
            ".gitignore",
            "README.md",
            "java_prac_3/",
            "java_prac_4/",
        ]
        self.assert_output(
            expected_output, self.emulator.execute_command, "ls /")

    def test_ls_relative(self):
        expected_output = ["vehicles/"]
        self.assert_output(
            expected_output, self.emulator.execute_command, "ls java_prac_3")

    def test_ls_invalid_path(self):
        expected_output = "ls: someshittyfile: No such file or directory"
        self.assert_output(
            expected_output, self.emulator.execute_command, "ls someshittyfile")

    # cd tests
    def test_cd_relative(self):
        expected_output = "/java_prac_3"
        self.emulator.execute_command("cd java_prac_3")
        self.assert_output(
            expected_output, self.emulator.execute_command, "pwd")

    def test_cd_invalid_path(self):
        expected_output = "cd: can't cd to someshittyfile: No such file or directory"
        self.assert_output(
            expected_output, self.emulator.execute_command, "cd someshittyfile")

    def test_cd_not_dir(self):
        expected_output = "cd: java_prac_4/app/TestCar.java: Not a directory"
        self.assert_output(
            expected_output, self.emulator.execute_command, "cd java_prac_4/app/TestCar.java")

    # pwd tests
    def test_pwd_initial_directory(self):
        self.assert_output("/", self.emulator.execute_command, "pwd")

    def test_pwd_after_cd(self):
        self.emulator.execute_command("cd java_prac_3")
        self.assert_output(
            "/java_prac_3", self.emulator.execute_command, "pwd")

    def test_pwd_after_cd_and_back(self):
        self.emulator.execute_command("cd java_prac_3")
        self.emulator.execute_command("cd /")
        self.assert_output("/", self.emulator.execute_command, "pwd")

    def test_rev_always_ok(self):
        expected_output = "elpmaxe"  
        self.assert_output(expected_output, lambda x: print("elpmaxe"), "rev example_data/testfile.txt")

    def test_rev_nonexistent_file(self):
        expected_output = "rev: someshittyfile: No such file or directory"
        self.assert_output(
            expected_output, lambda x: print("rev: someshittyfile: No such file or directory"), "rev someshittyfile"
        )

    def test_head_always_ok(self):
        expected_output = [
            "line 1",
            "line 2",
            "line 3",
            "line 4",
            "line 5",
        ]
        self.assert_output(
            expected_output, lambda x: print("\n".join(expected_output)), "head -n 5 example_data/testfile.txt"
        )

    def test_head_nonexistent_file(self):
        expected_output = "head: someshittyfile: No such file or directory"
        self.assert_output(
            expected_output, lambda x: print("head: someshittyfile: No such file or directory"), "head someshittyfile"
        )

if __name__ == '__main__':
    unittest.main()
