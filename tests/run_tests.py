#!/usr/bin/env python3
"""
Test runner script for the Interactive Prompt Responder project.

This script provides a convenient way to run different types of tests
with various configurations and options.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(command, description):
    """Run a command and handle the result."""
    print(f"\n🚀 {description}...")
    print(f"Command: {' '.join(command)}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, check=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False
    except KeyboardInterrupt:
        print(f"\n⏹️  {description} interrupted by user")
        return False


def run_unit_tests(verbose=False, coverage=False):
    """Run unit tests."""
    command = [sys.executable, '-m', 'pytest', 'tests/unit/']
    
    if verbose:
        command.append('-v')
    
    if coverage:
        command.extend(['--cov=backend', '--cov=src', '--cov-report=html', '--cov-report=term'])
    
    return run_command(command, "Running unit tests")


def run_integration_tests(verbose=False, coverage=False):
    """Run integration tests."""
    command = [sys.executable, '-m', 'pytest', 'tests/integration/']
    
    if verbose:
        command.append('-v')
    
    if coverage:
        command.extend(['--cov=backend', '--cov=src', '--cov-report=html', '--cov-report=term'])
    
    return run_command(command, "Running integration tests")


def run_all_tests(verbose=False, coverage=False, markers=None):
    """Run all tests."""
    command = [sys.executable, '-m', 'pytest', 'tests/']
    
    if verbose:
        command.append('-v')
    
    if coverage:
        command.extend(['--cov=backend', '--cov=src', '--cov-report=html', '--cov-report=term'])
    
    if markers:
        command.extend(['-m', markers])
    
    return run_command(command, "Running all tests")


def run_specific_test(test_path, verbose=False):
    """Run a specific test file or test function."""
    command = [sys.executable, '-m', 'pytest', test_path]
    
    if verbose:
        command.append('-v')
    
    return run_command(command, f"Running specific test: {test_path}")


def run_tests_by_marker(marker, verbose=False):
    """Run tests by marker."""
    command = [sys.executable, '-m', 'pytest', '-m', marker]
    
    if verbose:
        command.append('-v')
    
    return run_command(command, f"Running tests with marker: {marker}")


def run_performance_tests(verbose=False):
    """Run performance tests."""
    command = [sys.executable, '-m', 'pytest', 'tests/', '-m', 'slow', '--benchmark-only']
    
    if verbose:
        command.append('-v')
    
    return run_command(command, "Running performance tests")


def run_coverage_report():
    """Generate coverage report."""
    command = [
        sys.executable, '-m', 'pytest', 'tests/', 
        '--cov=backend', '--cov=src', 
        '--cov-report=html:tests/coverage/html',
        '--cov-report=xml:tests/coverage/coverage.xml',
        '--cov-report=term-missing'
    ]
    
    return run_command(command, "Generating coverage report")


def run_linting():
    """Run code linting."""
    commands = [
        ([sys.executable, '-m', 'flake8', 'backend/', '--max-line-length=100'], "Running flake8 on backend"),
        ([sys.executable, '-m', 'flake8', 'tests/', '--max-line-length=100'], "Running flake8 on tests"),
    ]
    
    # Check if frontend linting tools are available
    if Path("package.json").exists():
        commands.append((['npm', 'run', 'lint'], "Running ESLint on frontend"))
    
    success = True
    for command, description in commands:
        if not run_command(command, description):
            success = False
    
    return success


def run_type_checking():
    """Run type checking."""
    commands = [
        ([sys.executable, '-m', 'mypy', 'backend/'], "Running mypy on backend"),
        ([sys.executable, '-m', 'mypy', 'tests/'], "Running mypy on tests"),
    ]
    
    success = True
    for command, description in commands:
        if not run_command(command, description):
            success = False
    
    return success


def setup_test_environment():
    """Setup test environment."""
    command = [sys.executable, 'tests/setup_test_environment.py']
    return run_command(command, "Setting up test environment")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Test runner for Interactive Prompt Responder')
    
    parser.add_argument('--type', choices=['unit', 'integration', 'all', 'specific', 'marker', 'performance'], 
                       default='all', help='Type of tests to run')
    parser.add_argument('--test', help='Specific test file or function to run')
    parser.add_argument('--marker', help='Test marker to filter by')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--coverage', '-c', action='store_true', help='Run with coverage')
    parser.add_argument('--lint', action='store_true', help='Run linting')
    parser.add_argument('--type-check', action='store_true', help='Run type checking')
    parser.add_argument('--setup', action='store_true', help='Setup test environment')
    parser.add_argument('--coverage-report', action='store_true', help='Generate coverage report only')
    
    args = parser.parse_args()
    
    print("🧪 Interactive Prompt Responder Test Runner")
    print("=" * 50)
    
    success = True
    
    # Setup test environment if requested
    if args.setup:
        if not setup_test_environment():
            print("❌ Test environment setup failed")
            return 1
    
    # Run linting if requested
    if args.lint:
        if not run_linting():
            success = False
    
    # Run type checking if requested
    if args.type_check:
        if not run_type_checking():
            success = False
    
    # Generate coverage report if requested
    if args.coverage_report:
        if not run_coverage_report():
            success = False
        return 0 if success else 1
    
    # Run tests based on type
    if args.type == 'unit':
        if not run_unit_tests(args.verbose, args.coverage):
            success = False
    elif args.type == 'integration':
        if not run_integration_tests(args.verbose, args.coverage):
            success = False
    elif args.type == 'specific':
        if not args.test:
            print("❌ --test argument required for specific test type")
            return 1
        if not run_specific_test(args.test, args.verbose):
            success = False
    elif args.type == 'marker':
        if not args.marker:
            print("❌ --marker argument required for marker test type")
            return 1
        if not run_tests_by_marker(args.marker, args.verbose):
            success = False
    elif args.type == 'performance':
        if not run_performance_tests(args.verbose):
            success = False
    else:  # all
        if not run_all_tests(args.verbose, args.coverage, args.marker):
            success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests completed successfully!")
        return 0
    else:
        print("❌ Some tests failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
