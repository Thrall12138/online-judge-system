"""
SQLAlchemy models for the Online Judge System.
Manages problems, test cases, submissions, and evaluation results.
"""

from datetime import datetime
from enum import Enum
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, 
    Enum as SQLEnum, Float, Boolean, LargeBinary
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class DifficultyLevel(str, Enum):
    """Difficulty levels for problems."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class ExecutionStatus(str, Enum):
    """Status of code execution."""
    PENDING = "pending"
    RUNNING = "running"
    ACCEPTED = "accepted"
    WRONG_ANSWER = "wrong_answer"
    TIME_LIMIT_EXCEEDED = "time_limit_exceeded"
    MEMORY_LIMIT_EXCEEDED = "memory_limit_exceeded"
    RUNTIME_ERROR = "runtime_error"
    COMPILATION_ERROR = "compilation_error"
    SYSTEM_ERROR = "system_error"


class ProgrammingLanguage(str, Enum):
    """Supported programming languages."""
    PYTHON = "python"
    JAVA = "java"
    JAVASCRIPT = "javascript"
    CPP = "cpp"
    C = "c"
    GO = "go"
    RUST = "rust"
    TYPESCRIPT = "typescript"


class Problem(Base):
    """
    Problem model representing a coding problem.
    
    Attributes:
        id: Unique problem identifier
        title: Problem title
        description: Detailed problem description
        difficulty: Problem difficulty level
        time_limit: Time limit in seconds
        memory_limit: Memory limit in MB
        input_format: Description of input format
        output_format: Description of output format
        constraints: Problem constraints
        examples: Example test cases (text format)
        created_at: Problem creation timestamp
        updated_at: Last modification timestamp
        is_active: Whether the problem is active
    """
    __tablename__ = "problems"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=False)
    difficulty = Column(SQLEnum(DifficultyLevel), default=DifficultyLevel.MEDIUM, index=True)
    time_limit = Column(Integer, default=2, nullable=False)  # in seconds
    memory_limit = Column(Integer, default=256, nullable=False)  # in MB
    input_format = Column(Text)
    output_format = Column(Text)
    constraints = Column(Text)
    examples = Column(Text)  # Example inputs/outputs
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    
    # Relationships
    test_cases = relationship("TestCase", back_populates="problem", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="problem", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Problem(id={self.id}, title='{self.title}', difficulty={self.difficulty})>"
    
    def to_dict(self):
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "difficulty": self.difficulty.value if isinstance(self.difficulty, DifficultyLevel) else self.difficulty,
            "time_limit": self.time_limit,
            "memory_limit": self.memory_limit,
            "input_format": self.input_format,
            "output_format": self.output_format,
            "constraints": self.constraints,
            "examples": self.examples,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class TestCase(Base):
    """
    Test case model for problem validation.
    
    Attributes:
        id: Unique test case identifier
        problem_id: Reference to parent problem
        input: Test case input data
        expected_output: Expected output for this test case
        is_sample: Whether this is a sample test case
        created_at: Test case creation timestamp
    """
    __tablename__ = "test_cases"
    
    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"), nullable=False, index=True)
    input = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)
    is_sample = Column(Boolean, default=False, index=True)  # Visible to users before submission
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    problem = relationship("Problem", back_populates="test_cases")
    test_results = relationship("TestResult", back_populates="test_case", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<TestCase(id={self.id}, problem_id={self.problem_id}, is_sample={self.is_sample})>"
    
    def to_dict(self):
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "problem_id": self.problem_id,
            "input": self.input,
            "expected_output": self.expected_output,
            "is_sample": self.is_sample,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Submission(Base):
    """
    Submission model representing a user's code submission.
    
    Attributes:
        id: Unique submission identifier
        problem_id: Reference to the problem
        user_id: User who submitted (can be extended with User model)
        language: Programming language used
        code: Submitted source code
        status: Current execution status
        created_at: Submission timestamp
        completed_at: Completion timestamp
    """
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)  # Can be extended with User FK
    language = Column(SQLEnum(ProgrammingLanguage), nullable=False, index=True)
    code = Column(Text, nullable=False)
    status = Column(SQLEnum(ExecutionStatus), default=ExecutionStatus.PENDING, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    completed_at = Column(DateTime)
    execution_time = Column(Float)  # in milliseconds
    memory_used = Column(Integer)  # in MB
    
    # Relationships
    problem = relationship("Problem", back_populates="submissions")
    result = relationship("Result", back_populates="submission", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Submission(id={self.id}, user_id={self.user_id}, status={self.status})>"
    
    def to_dict(self):
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "problem_id": self.problem_id,
            "user_id": self.user_id,
            "language": self.language.value if isinstance(self.language, ProgrammingLanguage) else self.language,
            "status": self.status.value if isinstance(self.status, ExecutionStatus) else self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "execution_time": self.execution_time,
            "memory_used": self.memory_used,
        }


class Result(Base):
    """
    Result model storing evaluation results for a submission.
    
    Attributes:
        id: Unique result identifier
        submission_id: Reference to the submission
        status: Overall execution status
        compile_output: Compilation output (if applicable)
        runtime_error: Runtime error message (if any)
        total_tests: Total number of test cases
        passed_tests: Number of passed test cases
        created_at: Result creation timestamp
    """
    __tablename__ = "results"
    
    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    status = Column(SQLEnum(ExecutionStatus), nullable=False, index=True)
    compile_output = Column(Text)  # Compilation errors/warnings
    runtime_error = Column(Text)  # Runtime error message
    total_tests = Column(Integer, default=0, nullable=False)
    passed_tests = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    submission = relationship("Submission", back_populates="result")
    test_results = relationship("TestResult", back_populates="result", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Result(id={self.id}, submission_id={self.submission_id}, status={self.status})>"
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        if self.total_tests == 0:
            return 0.0
        return (self.passed_tests / self.total_tests) * 100
    
    def to_dict(self):
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "submission_id": self.submission_id,
            "status": self.status.value if isinstance(self.status, ExecutionStatus) else self.status,
            "compile_output": self.compile_output,
            "runtime_error": self.runtime_error,
            "total_tests": self.total_tests,
            "passed_tests": self.passed_tests,
            "success_rate": self.success_rate,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class TestResult(Base):
    """
    Test result model storing detailed results for individual test cases.
    
    Attributes:
        id: Unique test result identifier
        result_id: Reference to the overall result
        test_case_id: Reference to the test case
        actual_output: Actual output produced by the submission
        is_passed: Whether this test case passed
        execution_time: Execution time for this test case (in milliseconds)
        memory_used: Memory used for this test case (in MB)
        error_message: Error message (if any)
    """
    __tablename__ = "test_results"
    
    id = Column(Integer, primary_key=True, index=True)
    result_id = Column(Integer, ForeignKey("results.id", ondelete="CASCADE"), nullable=False, index=True)
    test_case_id = Column(Integer, ForeignKey("test_cases.id", ondelete="CASCADE"), nullable=False, index=True)
    actual_output = Column(Text)
    is_passed = Column(Boolean, nullable=False, index=True)
    execution_time = Column(Float)  # in milliseconds
    memory_used = Column(Integer)  # in MB
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    result = relationship("Result", back_populates="test_results")
    test_case = relationship("TestCase", back_populates="test_results")
    
    def __repr__(self):
        return f"<TestResult(id={self.id}, test_case_id={self.test_case_id}, is_passed={self.is_passed})>"
    
    def to_dict(self):
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "result_id": self.result_id,
            "test_case_id": self.test_case_id,
            "actual_output": self.actual_output,
            "is_passed": self.is_passed,
            "execution_time": self.execution_time,
            "memory_used": self.memory_used,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
