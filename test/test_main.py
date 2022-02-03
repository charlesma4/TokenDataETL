import os

def run_tests():
	os.system("python3 test_extract.py")
	os.system("python3 test_transform.py")
	os.system("python3 test_load.py")


if __name__ == "__main__":
	run_tests()