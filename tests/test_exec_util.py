import unittest
from src import exec_util

class TestExecUtil(unittest.TestCase):

    def test_result_to_dict(self):
        class Result:
            returncode = 0
            stdout = "output"
        result = Result()
        expected = {'returncode': 0, 'output': 'output'}
        self.assertEqual(exec_util.result_to_dict(result), expected)

    def test_construct_ssh_command(self):
        command = "ls -l"
        expected = "ssh -o ConnectTimeout=5 chatdokku@172.17.0.1 'ls -l' 2>&1"
        self.assertEqual(exec_util.construct_ssh_command(command), expected)


    def test_is_safe_path(self):
        self.assertTrue(exec_util.is_safe_path("app", "path"))
        self.assertFalse(exec_util.is_safe_path("app", "../path"))

if __name__ == '__main__':
    unittest.main()
