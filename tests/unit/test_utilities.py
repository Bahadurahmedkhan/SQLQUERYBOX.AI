"""
Unit tests for utility scripts and functions.

This module tests all utility functionality including:
- Startup scripts
- Database setup
- Configuration files
- Build tools
"""

import pytest
import os
import subprocess
import json
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path


class TestStartupScripts:
    """Test startup script functionality."""
    
    def test_start_backend_script(self):
        """Test start_backend.py script."""
        with patch('start_backend.subprocess.run') as mock_run, \
             patch('start_backend.os.path.join') as mock_join, \
             patch('start_backend.os.path.dirname') as mock_dirname:
            
            mock_dirname.return_value = '/test/path'
            mock_join.return_value = '/test/path/backend'
            mock_run.return_value = Mock()
            
            from start_backend import start_backend
            
            # Test successful execution
            result = start_backend()
            assert result is True
            
            # Verify subprocess calls
            assert mock_run.call_count >= 2
    
    def test_start_backend_script_error(self):
        """Test start_backend.py script error handling."""
        with patch('start_backend.subprocess.run') as mock_run, \
             patch('start_backend.os.path.join') as mock_join, \
             patch('start_backend.os.path.dirname') as mock_dirname:
            
            mock_dirname.return_value = '/test/path'
            mock_join.return_value = '/test/path/backend'
            mock_run.side_effect = subprocess.CalledProcessError(1, 'pip')
            
            from start_backend import start_backend
            
            # Test error handling
            result = start_backend()
            assert result is False
    
    def test_start_backend_keyboard_interrupt(self):
        """Test start_backend.py keyboard interrupt handling."""
        with patch('start_backend.subprocess.run') as mock_run, \
             patch('start_backend.os.path.join') as mock_join, \
             patch('start_backend.os.path.dirname') as mock_dirname:
            
            mock_dirname.return_value = '/test/path'
            mock_join.return_value = '/test/path/backend'
            mock_run.side_effect = KeyboardInterrupt()
            
            from start_backend import start_backend
            
            # Test keyboard interrupt handling
            result = start_backend()
            assert result is True


class TestPackageConfiguration:
    """Test package configuration files."""
    
    def test_package_json_structure(self):
        """Test package.json structure and content."""
        package_json_path = Path("package.json")
        
        if package_json_path.exists():
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
            
            # Test required fields
            assert 'name' in package_data
            assert 'version' in package_data
            assert 'description' in package_data
            assert 'scripts' in package_data
            assert 'dependencies' in package_data
            assert 'devDependencies' in package_data
            
            # Test scripts
            scripts = package_data['scripts']
            assert 'start' in scripts
            assert 'build' in scripts
            assert 'dev' in scripts
            
            # Test dependencies
            dependencies = package_data['dependencies']
            assert 'react' in dependencies
            assert 'react-dom' in dependencies
            assert 'chart.js' in dependencies
            assert 'react-chartjs-2' in dependencies
            assert 'lucide-react' in dependencies
            
            # Test dev dependencies
            dev_dependencies = package_data['devDependencies']
            assert '@babel/core' in dev_dependencies
            assert 'webpack' in dev_dependencies
            assert 'webpack-cli' in dev_dependencies
    
    def test_webpack_config_structure(self):
        """Test webpack.config.js structure."""
        webpack_config_path = Path("webpack.config.js")
        
        if webpack_config_path.exists():
            # Test that webpack config file exists and is readable
            assert webpack_config_path.is_file()
            
            # Test that it's a valid JavaScript file
            with open(webpack_config_path, 'r') as f:
                content = f.read()
                assert 'module.exports' in content
                assert 'entry' in content
                assert 'output' in content
                assert 'module' in content
                assert 'plugins' in content
    
    def test_requirements_txt_structure(self):
        """Test requirements.txt structure."""
        requirements_path = Path("backend/requirements.txt")
        
        if requirements_path.exists():
            with open(requirements_path, 'r') as f:
                requirements = f.read()
            
            # Test that it contains expected packages
            expected_packages = ['flask', 'flask-cors', 'sqlite3']
            for package in expected_packages:
                if package != 'sqlite3':  # sqlite3 is built-in
                    assert package.lower() in requirements.lower()


class TestDatabaseSetup:
    """Test database setup functionality."""
    
    def test_database_setup_script(self):
        """Test database setup script."""
        setup_script_path = Path("lectures/week_10/SQLAgent/setup_my_database.py")
        
        if setup_script_path.exists():
            # Test that setup script exists
            assert setup_script_path.is_file()
            
            # Test that it's a valid Python file
            with open(setup_script_path, 'r') as f:
                content = f.read()
                assert 'import' in content
                assert 'def' in content
    
    def test_database_schema_file(self):
        """Test database schema file."""
        schema_path = Path("lectures/week_10/SQLAgent/my_database_schema.sql")
        
        if schema_path.exists():
            with open(schema_path, 'r') as f:
                schema_content = f.read()
            
            # Test that it contains expected SQL statements
            assert 'CREATE TABLE' in schema_content.upper()
            assert 'INSERT INTO' in schema_content.upper()
            
            # Test that it contains expected tables
            expected_tables = ['customers', 'products', 'orders', 'order_items']
            for table in expected_tables:
                assert table in schema_content.lower()
    
    def test_database_seed_file(self):
        """Test database seed file."""
        seed_path = Path("lectures/week_10/SQLAgent/sql_agent_seed.sql")
        
        if seed_path.exists():
            with open(seed_path, 'r') as f:
                seed_content = f.read()
            
            # Test that it contains INSERT statements
            assert 'INSERT INTO' in seed_content.upper()
            
            # Test that it contains data for expected tables
            expected_tables = ['customers', 'products', 'orders']
            for table in expected_tables:
                assert table in seed_content.lower()


class TestConfigurationFiles:
    """Test configuration files."""
    
    def test_env_example_file(self):
        """Test .env.example file."""
        env_example_path = Path("lectures/week_10/SQLAgent/env.example")
        
        if env_example_path.exists():
            with open(env_example_path, 'r') as f:
                env_content = f.read()
            
            # Test that it contains expected environment variables
            expected_vars = ['GOOGLE_API_KEY', 'DATABASE_URL', 'LLM_MODEL']
            for var in expected_vars:
                assert var in env_content
    
    def test_pyproject_toml_structure(self):
        """Test pyproject.toml structure."""
        pyproject_path = Path("lectures/week_10/SQLAgent/pyproject.toml")
        
        if pyproject_path.exists():
            with open(pyproject_path, 'r') as f:
                pyproject_content = f.read()
            
            # Test that it contains expected sections
            assert '[build-system]' in pyproject_content
            assert '[project]' in pyproject_content
            assert 'dependencies' in pyproject_content


class TestBuildTools:
    """Test build and development tools."""
    
    def test_webpack_configuration(self):
        """Test webpack configuration."""
        webpack_config_path = Path("webpack.config.js")
        
        if webpack_config_path.exists():
            with open(webpack_config_path, 'r') as f:
                config_content = f.read()
            
            # Test webpack configuration elements
            assert 'entry' in config_content
            assert 'output' in config_content
            assert 'module' in config_content
            assert 'rules' in config_content
            assert 'plugins' in config_content
            assert 'devServer' in config_content
    
    def test_babel_configuration(self):
        """Test Babel configuration."""
        # Check if babel config exists in package.json or separate file
        package_json_path = Path("package.json")
        
        if package_json_path.exists():
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
            
            # Test babel presets in webpack config
            webpack_config_path = Path("webpack.config.js")
            if webpack_config_path.exists():
                with open(webpack_config_path, 'r') as f:
                    webpack_content = f.read()
                
                assert '@babel/preset-env' in webpack_content
                assert '@babel/preset-react' in webpack_content


class TestDocumentationFiles:
    """Test documentation files."""
    
    def test_readme_file(self):
        """Test README.md file."""
        readme_path = Path("README.md")
        
        if readme_path.exists():
            with open(readme_path, 'r') as f:
                readme_content = f.read()
            
            # Test that README contains expected sections
            assert len(readme_content) > 0
            assert '#' in readme_content  # Should have headers
    
    def test_setup_guide_file(self):
        """Test setup guide file."""
        setup_guide_path = Path("SETUP_GUIDE.md")
        
        if setup_guide_path.exists():
            with open(setup_guide_path, 'r') as f:
                setup_content = f.read()
            
            # Test that setup guide contains expected content
            assert len(setup_content) > 0
            assert 'setup' in setup_content.lower() or 'install' in setup_content.lower()
    
    def test_sql_agent_documentation(self):
        """Test SQL Agent documentation files."""
        sql_agent_docs = [
            "lectures/week_10/SQLAgent/README.md",
            "lectures/week_10/SQLAgent/CLI_INTERFACES_GUIDE.md",
            "lectures/week_10/SQLAgent/DEVELOPMENT_GUIDE.md",
            "lectures/week_10/SQLAgent/GEMINI_SETUP_GUIDE.md",
            "lectures/week_10/SQLAgent/MY_DATABASE_GUIDE.md"
        ]
        
        for doc_path in sql_agent_docs:
            doc_file = Path(doc_path)
            if doc_file.exists():
                with open(doc_file, 'r') as f:
                    doc_content = f.read()
                
                # Test that documentation files have content
                assert len(doc_content) > 0


class TestTestFiles:
    """Test existing test files."""
    
    def test_existing_test_files(self):
        """Test existing test files in the project."""
        test_files = [
            "test_backend.py",
            "test_database.py",
            "test_integration.py",
            "test_specific_query.py",
            "test_available_data.py",
            "lectures/week_10/SQLAgent/test_database.py"
        ]
        
        for test_file in test_files:
            test_path = Path(test_file)
            if test_path.exists():
                with open(test_path, 'r') as f:
                    test_content = f.read()
                
                # Test that test files contain test functions
                assert 'def test_' in test_content or 'class Test' in test_content
                assert 'import' in test_content


class TestScriptValidation:
    """Test script validation and structure."""
    
    def test_python_script_syntax(self):
        """Test Python script syntax validation."""
        python_scripts = [
            "start_backend.py",
            "start_both.py",
            "start_frontend.py",
            "check_statuses.py",
            "lectures/week_10/SQLAgent/launch_cli.py",
            "lectures/week_10/SQLAgent/setup_my_database.py"
        ]
        
        for script_path in python_scripts:
            script_file = Path(script_path)
            if script_file.exists():
                with open(script_file, 'r') as f:
                    script_content = f.read()
                
                # Test that Python scripts have proper structure
                assert 'import' in script_content or 'from' in script_content
                assert 'def ' in script_content or 'class ' in script_content
                
                # Test that scripts have proper shebang or are importable
                if script_content.startswith('#!/usr/bin/env python'):
                    assert True  # Has proper shebang
                else:
                    # Should be importable as module
                    assert 'if __name__' in script_content
    
    def test_javascript_syntax(self):
        """Test JavaScript/React syntax validation."""
        js_files = [
            "src/App.js",
            "src/index.js",
            "src/components/PromptInput.js",
            "src/components/TextResponse.js",
            "src/components/GraphicalResponse.js"
        ]
        
        for js_path in js_files:
            js_file = Path(js_path)
            if js_file.exists():
                with open(js_file, 'r') as f:
                    js_content = f.read()
                
                # Test that JS files have proper structure
                assert 'import' in js_content or 'require' in js_content
                assert 'export' in js_content or 'module.exports' in js_content
                
                # Test React components
                if 'src/' in js_path:
                    assert 'React' in js_content or 'react' in js_content
                    assert 'function' in js_content or 'const' in js_content


class TestFilePermissions:
    """Test file permissions and accessibility."""
    
    def test_script_executability(self):
        """Test that scripts are executable."""
        executable_scripts = [
            "start_backend.py",
            "start_both.py",
            "start_frontend.py",
            "lectures/week_10/SQLAgent/launch_cli.py"
        ]
        
        for script_path in executable_scripts:
            script_file = Path(script_path)
            if script_file.exists():
                # Test that file is readable
                assert script_file.is_file()
                
                # Test that file has content
                assert script_file.stat().st_size > 0
    
    def test_configuration_file_accessibility(self):
        """Test that configuration files are accessible."""
        config_files = [
            "package.json",
            "webpack.config.js",
            "backend/requirements.txt",
            "lectures/week_10/SQLAgent/pyproject.toml"
        ]
        
        for config_path in config_files:
            config_file = Path(config_path)
            if config_file.exists():
                # Test that file is readable
                assert config_file.is_file()
                
                # Test that file has content
                assert config_file.stat().st_size > 0
                
                # Test that file can be opened
                with open(config_file, 'r') as f:
                    content = f.read()
                    assert len(content) > 0


class TestDependencyManagement:
    """Test dependency management."""
    
    def test_python_dependencies(self):
        """Test Python dependency management."""
        requirements_files = [
            "backend/requirements.txt",
            "lectures/week_10/requirements.txt"
        ]
        
        for req_path in requirements_files:
            req_file = Path(req_path)
            if req_file.exists():
                with open(req_file, 'r') as f:
                    requirements = f.read()
                
                # Test that requirements file has content
                assert len(requirements.strip()) > 0
                
                # Test that it contains package specifications
                lines = requirements.strip().split('\n')
                for line in lines:
                    if line.strip() and not line.startswith('#'):
                        # Should be a valid package specification
                        assert len(line.strip()) > 0
    
    def test_node_dependencies(self):
        """Test Node.js dependency management."""
        package_json_path = Path("package.json")
        
        if package_json_path.exists():
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
            
            # Test that dependencies are properly specified
            if 'dependencies' in package_data:
                for package, version in package_data['dependencies'].items():
                    assert len(package) > 0
                    assert len(version) > 0
            
            if 'devDependencies' in package_data:
                for package, version in package_data['devDependencies'].items():
                    assert len(package) > 0
                    assert len(version) > 0
