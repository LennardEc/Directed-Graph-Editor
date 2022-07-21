import os
import pytest
from utilities.FileManager import FileManager

@pytest.fixture(scope="module")
def not_exists_folder_name():
    return "not_exists"

@pytest.fixture(scope="module")
def exists_folder_name():
    return "exists"

@pytest.fixture(scope="module")
def not_exists_file_name():
    return "not_exists"

@pytest.fixture(scope="module")
def exists_file_name():
    return "exist"

@pytest.fixture(scope="module")
def file_manager_path():
    yield os.getcwd() + '/tests/resources/'

@pytest.fixture(scope='function')
def create_file_manager(file_manager_path):
    file_manager = FileManager(file_manager_path)
    yield file_manager
    
def test_not_exists_folder(create_file_manager, not_exists_folder_name):
    file_manager = create_file_manager
    value = file_manager.existsFolder(not_exists_folder_name)
    assert False == value
    
def test_exists_folder(create_file_manager, exists_folder_name):
    file_manager = create_file_manager
    value = file_manager.existsFolder(exists_folder_name)
    assert True == value

def test_not_exists_file(create_file_manager, not_exists_file_name):
    file_manager = create_file_manager
    value = file_manager.existsFile(not_exists_file_name + ".txt")
    assert False == value

def test_exists_file(create_file_manager, exists_file_name):
    file_manager = create_file_manager
    value = file_manager.existsFile(exists_file_name + ".txt")
    assert False == value

