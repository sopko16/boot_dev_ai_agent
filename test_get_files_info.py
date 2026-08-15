import unittest
from functions.get_files_info import get_files_info


class TestGetFilesInfo(unittest.TestCase):

    def test_current_directory(self):
        result = get_files_info("calculator", ".")
        print(result)
        self.assertEqual(
            result,
            'Success: "." is within the working directory'
        )

    def test_bin_directory(self):
        result = get_files_info("calculator", "/bin")
        print(result)
        self.assertEqual(
            result,
            'Error: Cannot list "/bin" as it is outside the permitted working directory'
        )

    def test_parent_directory(self):
        result = get_files_info("calculator", "../")
        print(result)
        self.assertEqual(
            result,
            'Error: Cannot list "../" as it is outside the permitted working directory'
        )

    def test_file_not_directory(self):
        result = get_files_info("calculator", "main.py")
        print(result)
        self.assertEqual(
            result,
            'Error: "main.py" is not a directory'
        )


if __name__ == "__main__":
    unittest.main()