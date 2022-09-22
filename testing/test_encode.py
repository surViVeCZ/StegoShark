from bacon import bacon_cipher
from whitespaces import spaces_cipher
from synonyms import syn_cipher
from error_handler import Custom_error
import pytest
import os

#initialization function
@pytest.fixture
def bacon_obj():
    run = bacon_cipher("", "secret")
    return run
@pytest.fixture
def spaces_obj():
    run = spaces_cipher("", "secret")
    return run

@pytest.fixture
def syn_obj():
    run = syn_cipher("", "secret")
    return run

def test_bacon_encode_docx(bacon_obj):
    thisdir_bin = os.getcwdb()
    changed_path = os.path.join(thisdir_bin, b"cover_files")
    changed_path = os.path.join(changed_path, b"bacon")
    list_of_files = os.listdir(changed_path)

    for file in list_of_files:
        file = os.path.join(changed_path, file)    
        file = str(file, 'UTF-8')
        head_tail = os.path.split(file)
        file_name = head_tail[1]
        if file_name.endswith('.docx'):
            bacon_obj.Bacon_encode(file, "secret")
            
def test_spaces_encode_docx(spaces_obj):
    thisdir_bin = os.getcwdb()
    changed_path = os.path.join(thisdir_bin, b"cover_files")
    changed_path = os.path.join(changed_path, b"spaces")
    list_of_files = os.listdir(changed_path)

    for file in list_of_files:
        file = os.path.join(changed_path, file)    
        file = str(file, 'UTF-8')
        head_tail = os.path.split(file)
        file_name = head_tail[1]
        if file_name.endswith('.docx'):
            spaces_obj.Spaces_encode(file, "secret")
   
def test_syn_encode_docx(syn_obj):
    thisdir_bin = os.getcwdb()
    changed_path = os.path.join(thisdir_bin, b"cover_files")
    changed_path = os.path.join(changed_path, b"synonyms")
    list_of_files = os.listdir(changed_path)

    for file in list_of_files:
        file = os.path.join(changed_path, file)    
        file = str(file, 'UTF-8')
        head_tail = os.path.split(file)
        file_name = head_tail[1]
        if file_name.endswith('.docx'):
            syn_obj.syn_encode(file, "secret", "default")

def test_file_doesnt_exist(bacon_obj):
    with pytest.raises(Custom_error):
        bacon_obj.Bacon_encode("tests/cover_texts/songs/this_file_doesnt_exist.docx", "secret")
        bacon_obj.Bacon_encode("buleakalele", "secret")
    