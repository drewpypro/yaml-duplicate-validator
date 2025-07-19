import os
import glob
import subprocess

SCRIPT_PATH = "yaml-duplicate-validator.py"
REQUESTS_DIR = "tests/requests"
OUTPUTS_DIR = "tests/outputs"
POLICIES_DIR = "tests/policies"
EXISTING_POLICY = os.path.join(POLICIES_DIR, "existing-policy.yaml")

def get_expected_output_file(request_file):
    base = os.path.splitext(os.path.basename(request_file))[0]
    return os.path.join(OUTPUTS_DIR, base + ".txt")

def needs_existing_policy(request_file):
    return "with-existing" in request_file

def run_test(request_file):
    expected_output_file = get_expected_output_file(request_file)
    if not os.path.exists(expected_output_file):
        print(f"[SKIP] No expected output for {request_file}")
        return "SKIP"
    
    cmd = ["python3", SCRIPT_PATH, request_file]
    if needs_existing_policy(request_file):
        cmd.append(EXISTING_POLICY)
    
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    actual_output = result.stdout.strip()
    with open(expected_output_file, "r") as f:
        expected_output = f.read().strip()
    
    if actual_output == expected_output:
        print(f"\033[92m[PASS]\033[0m {os.path.basename(request_file)}")
        return "PASS"
    else:
        print(f"\033[91m[FAIL]\033[0m {os.path.basename(request_file)}")
        # Print diff for reference, but do not put anything in the table
        import difflib
        diff = "\n".join(difflib.unified_diff(
            expected_output.splitlines(),
            actual_output.splitlines(),
            fromfile='expected',
            tofile='actual',
            lineterm=''
        ))
        print("---- DIFF ----")
        print(diff)
        print("--------------")
        return "FAIL"

def main():
    print("==== Running Duplicate Policy Script Tests ====")
    request_files = sorted(glob.glob(os.path.join(REQUESTS_DIR, "*.yaml")))
    results = []
    total = len(request_files)
    passed = 0
    failed = 0

    for req in request_files:
        status = run_test(req)
        results.append((os.path.basename(req), status))
        if status == "PASS":
            passed += 1
        elif status == "FAIL":
            failed += 1

    print("==============================================")
    print(f"Total: {total} | Passed: {passed} | Failed: {failed}")

    # Pretty table summary: only Test Case + Status
    print("\nTest Results:")
    col1 = "Test Case"
    col2 = "Status"
    width1 = max(len(col1), max(len(x[0]) for x in results)) + 2
    width2 = len(col2) + 2
    header = f"{col1:<{width1}} {col2:<{width2}}"
    print(header)
    print("-" * (width1 + width2))

    for filename, status in results:
        status_str = status
        if status == "PASS":
            status_str = "\033[92mPASS\033[0m"
        elif status == "FAIL":
            status_str = "\033[91mFAIL\033[0m"
        elif status == "SKIP":
            status_str = "\033[93mSKIP\033[0m"
        print(f"{filename:<{width1}} {status_str:<{width2}}")

    if failed > 0:
        exit(1)

if __name__ == "__main__":
    main()
