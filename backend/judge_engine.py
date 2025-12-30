"""
Judge Engine for Online Judge System
Handles code compilation, execution, and result evaluation for multiple programming languages.
Supports C, C++, and Python with detailed verdict determination (AC, WA, TLE, CE, RE).
"""

import subprocess
import os
import tempfile
import time
import sys
import signal
from enum import Enum
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Verdict(Enum):
    """Verdict codes for judging results."""
    AC = "Accepted"  # All test cases passed
    WA = "Wrong Answer"  # Output doesn't match expected
    TLE = "Time Limit Exceeded"  # Execution exceeded time limit
    CE = "Compilation Error"  # Code compilation failed
    RE = "Runtime Error"  # Program crashed during execution
    MLE = "Memory Limit Exceeded"  # Memory usage exceeded limit
    PE = "Presentation Error"  # Output format mismatch


class Language(Enum):
    """Supported programming languages."""
    C = "c"
    CPP = "cpp"
    PYTHON = "python"


@dataclass
class JudgeResult:
    """Data class for judge results."""
    verdict: Verdict
    passed: int
    total: int
    time_used: float
    memory_used: float
    compilation_error: Optional[str] = None
    runtime_error: Optional[str] = None
    output: Optional[str] = None
    expected_output: Optional[str] = None
    test_case_index: int = -1


class CodeCompiler:
    """Handles compilation of C and C++ code."""

    @staticmethod
    def compile_c(source_path: str, output_path: str, timeout: int = 30) -> Tuple[bool, str]:
        """
        Compile C source code.

        Args:
            source_path: Path to .c source file
            output_path: Path for output executable
            timeout: Compilation timeout in seconds

        Returns:
            Tuple of (success: bool, error_message: str)
        """
        try:
            result = subprocess.run(
                ["gcc", "-o", output_path, source_path, "-Wall", "-Wextra"],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            if result.returncode != 0:
                return False, result.stderr or result.stdout
            return True, ""
        except subprocess.TimeoutExpired:
            return False, "Compilation timeout"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def compile_cpp(source_path: str, output_path: str, timeout: int = 30) -> Tuple[bool, str]:
        """
        Compile C++ source code.

        Args:
            source_path: Path to .cpp source file
            output_path: Path for output executable
            timeout: Compilation timeout in seconds

        Returns:
            Tuple of (success: bool, error_message: str)
        """
        try:
            result = subprocess.run(
                ["g++", "-o", output_path, source_path, "-Wall", "-Wextra", "-std=c++17"],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            if result.returncode != 0:
                return False, result.stderr or result.stdout
            return True, ""
        except subprocess.TimeoutExpired:
            return False, "Compilation timeout"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def compile(language: Language, source_path: str, output_path: str) -> Tuple[bool, str]:
        """
        Compile source code based on language.

        Args:
            language: Programming language
            source_path: Path to source file
            output_path: Path for output executable

        Returns:
            Tuple of (success: bool, error_message: str)
        """
        if language == Language.C:
            return CodeCompiler.compile_c(source_path, output_path)
        elif language == Language.CPP:
            return CodeCompiler.compile_cpp(source_path, output_path)
        else:
            return False, "Unsupported language for compilation"


class CodeExecutor:
    """Handles execution of compiled and interpreted code."""

    @staticmethod
    def execute_binary(
        executable_path: str,
        input_data: str = "",
        timeout: int = 5,
        memory_limit: int = 256
    ) -> Tuple[str, Optional[str], float]:
        """
        Execute a compiled binary.

        Args:
            executable_path: Path to executable
            input_data: Input for the program
            timeout: Execution timeout in seconds
            memory_limit: Memory limit in MB (informational, actual enforcement varies)

        Returns:
            Tuple of (output: str, error: Optional[str], execution_time: float)
        """
        try:
            start_time = time.time()
            result = subprocess.run(
                [executable_path],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            execution_time = time.time() - start_time

            if result.returncode != 0 and result.returncode != -15:
                return result.stdout, result.stderr or f"Exit code: {result.returncode}", execution_time
            return result.stdout, None, execution_time

        except subprocess.TimeoutExpired:
            return "", "Time Limit Exceeded", timeout
        except Exception as e:
            return "", str(e), 0.0

    @staticmethod
    def execute_python(
        source_path: str,
        input_data: str = "",
        timeout: int = 5,
        memory_limit: int = 256
    ) -> Tuple[str, Optional[str], float]:
        """
        Execute Python script.

        Args:
            source_path: Path to .py file
            input_data: Input for the program
            timeout: Execution timeout in seconds
            memory_limit: Memory limit in MB (informational)

        Returns:
            Tuple of (output: str, error: Optional[str], execution_time: float)
        """
        try:
            start_time = time.time()
            result = subprocess.run(
                ["python3", source_path],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            execution_time = time.time() - start_time

            if result.returncode != 0:
                return result.stdout, result.stderr or f"Exit code: {result.returncode}", execution_time
            return result.stdout, None, execution_time

        except subprocess.TimeoutExpired:
            return "", "Time Limit Exceeded", timeout
        except Exception as e:
            return "", str(e), 0.0

    @staticmethod
    def execute(
        language: Language,
        code_path: str,
        executable_path: Optional[str],
        input_data: str = "",
        timeout: int = 5
    ) -> Tuple[str, Optional[str], float]:
        """
        Execute code based on language.

        Args:
            language: Programming language
            code_path: Path to source code
            executable_path: Path to executable (for compiled languages)
            input_data: Input for the program
            timeout: Execution timeout in seconds

        Returns:
            Tuple of (output: str, error: Optional[str], execution_time: float)
        """
        if language in [Language.C, Language.CPP]:
            return CodeExecutor.execute_binary(executable_path, input_data, timeout)
        elif language == Language.PYTHON:
            return CodeExecutor.execute_python(code_path, input_data, timeout)
        else:
            return "", "Unsupported language", 0.0


class OutputComparator:
    """Handles comparison of actual and expected outputs."""

    @staticmethod
    def normalize_output(output: str) -> str:
        """
        Normalize output for comparison.
        Removes trailing whitespace and normalizes line endings.

        Args:
            output: Raw output string

        Returns:
            Normalized output string
        """
        return "\n".join(line.rstrip() for line in output.strip().split("\n"))

    @staticmethod
    def compare_exact(actual: str, expected: str) -> bool:
        """
        Perform exact string comparison after normalization.

        Args:
            actual: Actual output
            expected: Expected output

        Returns:
            True if outputs match
        """
        return OutputComparator.normalize_output(actual) == OutputComparator.normalize_output(expected)

    @staticmethod
    def compare_float(actual: str, expected: str, epsilon: float = 1e-6) -> bool:
        """
        Compare floating-point outputs with tolerance.

        Args:
            actual: Actual output
            expected: Expected output
            epsilon: Tolerance for floating-point comparison

        Returns:
            True if outputs match within tolerance
        """
        try:
            actual_lines = actual.strip().split("\n")
            expected_lines = expected.strip().split("\n")

            if len(actual_lines) != len(expected_lines):
                return False

            for actual_line, expected_line in zip(actual_lines, expected_lines):
                actual_nums = [float(x) for x in actual_line.split()]
                expected_nums = [float(x) for x in expected_line.split()]

                if len(actual_nums) != len(expected_nums):
                    return False

                for actual_num, expected_num in zip(actual_nums, expected_nums):
                    if abs(actual_num - expected_num) > epsilon:
                        return False
            return True
        except (ValueError, AttributeError):
            return OutputComparator.compare_exact(actual, expected)

    @staticmethod
    def compare(actual: str, expected: str, comparison_type: str = "exact") -> bool:
        """
        Compare outputs based on comparison type.

        Args:
            actual: Actual output
            expected: Expected output
            comparison_type: Type of comparison ("exact" or "float")

        Returns:
            True if outputs match
        """
        if comparison_type == "float":
            return OutputComparator.compare_float(actual, expected)
        else:
            return OutputComparator.compare_exact(actual, expected)


class JudgeEngine:
    """Main judge engine orchestrating compilation, execution, and evaluation."""

    def __init__(self, work_dir: Optional[str] = None, timeout: int = 5):
        """
        Initialize JudgeEngine.

        Args:
            work_dir: Working directory for temporary files
            timeout: Execution timeout in seconds per test case
        """
        self.work_dir = work_dir or tempfile.mkdtemp()
        self.timeout = timeout
        self.compiler = CodeCompiler()
        self.executor = CodeExecutor()
        self.comparator = OutputComparator()

    def detect_language(self, source_code: str, filename: str = "") -> Language:
        """
        Detect programming language from file extension or code characteristics.

        Args:
            source_code: Source code content
            filename: Source filename

        Returns:
            Detected Language
        """
        if filename.endswith(".c"):
            return Language.C
        elif filename.endswith(".cpp") or filename.endswith(".cc"):
            return Language.CPP
        elif filename.endswith(".py"):
            return Language.PYTHON

        # Fallback: detect from code characteristics
        if "#include" in source_code:
            if "iostream" in source_code or "cstdio" in source_code:
                return Language.CPP
            return Language.C
        elif "def " in source_code or "import " in source_code:
            return Language.PYTHON

        return Language.PYTHON  # Default

    def _prepare_source_file(
        self, source_code: str, language: Language
    ) -> str:
        """
        Save source code to temporary file.

        Args:
            source_code: Source code content
            language: Programming language

        Returns:
            Path to source file
        """
        extensions = {
            Language.C: ".c",
            Language.CPP: ".cpp",
            Language.PYTHON: ".py"
        }
        ext = extensions[language]
        source_path = os.path.join(self.work_dir, f"solution{ext}")
        with open(source_path, "w") as f:
            f.write(source_code)
        return source_path

    def judge_single_test(
        self,
        source_code: str,
        language: Language,
        input_data: str,
        expected_output: str,
        comparison_type: str = "exact",
        executable_path: Optional[str] = None
    ) -> Tuple[bool, str, Optional[str], float]:
        """
        Judge a single test case.

        Args:
            source_code: Source code to judge
            language: Programming language
            input_data: Test case input
            expected_output: Expected output
            comparison_type: Type of output comparison
            executable_path: Path to precompiled executable (optional)

        Returns:
            Tuple of (passed: bool, error_msg: str, actual_output: Optional[str], execution_time: float)
        """
        source_path = self._prepare_source_file(source_code, language)

        # Compile if necessary
        if language in [Language.C, Language.CPP]:
            if not executable_path:
                executable_path = os.path.join(self.work_dir, "solution")
                success, error_msg = self.compiler.compile(language, source_path, executable_path)
                if not success:
                    return False, error_msg, None, 0.0

        # Execute
        actual_output, exec_error, exec_time = self.executor.execute(
            language, source_path, executable_path, input_data, self.timeout
        )

        if exec_error:
            return False, exec_error, actual_output, exec_time

        # Compare
        passed = self.comparator.compare(actual_output, expected_output, comparison_type)
        return passed, "", actual_output, exec_time

    def judge(
        self,
        source_code: str,
        language: Optional[Language],
        test_cases: List[Dict[str, str]],
        comparison_type: str = "exact",
        filename: str = "solution"
    ) -> JudgeResult:
        """
        Judge code against multiple test cases.

        Args:
            source_code: Source code to judge
            language: Programming language (auto-detect if None)
            test_cases: List of test cases with "input" and "output" keys
            comparison_type: Type of output comparison
            filename: Source filename for language detection

        Returns:
            JudgeResult with detailed information
        """
        # Detect language if not provided
        if language is None:
            language = self.detect_language(source_code, filename)

        logger.info(f"Judging {language.value} code with {len(test_cases)} test cases")

        # Prepare source file
        source_path = self._prepare_source_file(source_code, language)
        executable_path = None

        # Compilation phase (for C/C++)
        if language in [Language.C, Language.CPP]:
            executable_path = os.path.join(self.work_dir, "solution")
            success, error_msg = self.compiler.compile(language, source_path, executable_path)
            if not success:
                logger.error(f"Compilation failed: {error_msg}")
                return JudgeResult(
                    verdict=Verdict.CE,
                    passed=0,
                    total=len(test_cases),
                    time_used=0.0,
                    memory_used=0.0,
                    compilation_error=error_msg
                )

        # Test each case
        total_time = 0.0
        passed_count = 0

        for i, test_case in enumerate(test_cases):
            input_data = test_case.get("input", "")
            expected_output = test_case.get("output", "")

            actual_output, error_msg, exec_time = self.executor.execute(
                language, source_path, executable_path, input_data, self.timeout
            )
            total_time += exec_time

            # Check for runtime error
            if error_msg and "Time Limit Exceeded" not in error_msg:
                logger.warning(f"Test case {i + 1} runtime error: {error_msg}")
                return JudgeResult(
                    verdict=Verdict.RE,
                    passed=passed_count,
                    total=len(test_cases),
                    time_used=total_time,
                    memory_used=0.0,
                    runtime_error=error_msg,
                    output=actual_output,
                    expected_output=expected_output,
                    test_case_index=i
                )

            # Check for TLE
            if error_msg and "Time Limit Exceeded" in error_msg:
                logger.warning(f"Test case {i + 1} exceeded time limit")
                return JudgeResult(
                    verdict=Verdict.TLE,
                    passed=passed_count,
                    total=len(test_cases),
                    time_used=total_time,
                    memory_used=0.0,
                    runtime_error=error_msg,
                    test_case_index=i
                )

            # Compare outputs
            if self.comparator.compare(actual_output, expected_output, comparison_type):
                passed_count += 1
                logger.info(f"Test case {i + 1} passed")
            else:
                logger.warning(f"Test case {i + 1} failed (Wrong Answer)")
                return JudgeResult(
                    verdict=Verdict.WA,
                    passed=passed_count,
                    total=len(test_cases),
                    time_used=total_time,
                    memory_used=0.0,
                    output=actual_output,
                    expected_output=expected_output,
                    test_case_index=i
                )

        # All tests passed
        logger.info(f"All {passed_count} test cases passed")
        return JudgeResult(
            verdict=Verdict.AC,
            passed=passed_count,
            total=len(test_cases),
            time_used=total_time,
            memory_used=0.0
        )

    def cleanup(self) -> None:
        """Clean up temporary files."""
        import shutil
        try:
            if os.path.exists(self.work_dir):
                shutil.rmtree(self.work_dir)
                logger.info(f"Cleaned up working directory: {self.work_dir}")
        except Exception as e:
            logger.error(f"Failed to cleanup: {e}")


# Example usage and testing
if __name__ == "__main__":
    # Example 1: C++ code
    cpp_code = """
    #include <iostream>
    using namespace std;

    int main() {
        int a, b;
        cin >> a >> b;
        cout << a + b << endl;
        return 0;
    }
    """

    test_cases = [
        {"input": "5 3", "output": "8"},
        {"input": "10 20", "output": "30"},
        {"input": "0 0", "output": "0"}
    ]

    engine = JudgeEngine(timeout=5)
    result = engine.judge(cpp_code, Language.CPP, test_cases)

    print(f"Verdict: {result.verdict.value}")
    print(f"Passed: {result.passed}/{result.total}")
    print(f"Time: {result.time_used:.2f}s")

    if result.compilation_error:
        print(f"Compilation Error: {result.compilation_error}")
    if result.runtime_error:
        print(f"Runtime Error: {result.runtime_error}")

    engine.cleanup()

    # Example 2: Python code
    python_code = """
    a, b = map(int, input().split())
    print(a + b)
    """

    engine2 = JudgeEngine(timeout=5)
    result2 = engine2.judge(python_code, Language.PYTHON, test_cases)

    print(f"\nPython Verdict: {result2.verdict.value}")
    print(f"Passed: {result2.passed}/{result2.total}")
    print(f"Time: {result2.time_used:.2f}s")

    engine2.cleanup()
