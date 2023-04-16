import os
import tempfile
import pytest
from wavescout.wavescout import WaveScout
from pydub import AudioSegment
import shutil
import os


@pytest.fixture
def temp_audio_file():
    test_filename = os.path.join(os.path.dirname(__file__),'testfile.wav')
    shutil.copyfile(os.path.join(os.path.dirname(__file__), 'acquired_awareness.wav'), test_filename)
    yield test_filename
    #with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        #shutil.copyfile(os.path.join(os.path.dirname(__file__), 'acquired_awareness.wav'), temp_file.name)
        #yield temp_file.name
        #os.remove(temp_file.name)

@pytest.fixture
def temp_output_file():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        yield temp_file.name
        os.remove(temp_file.name)

def test_invalid_file_path(temp_output_file, suffix=".zip"):
    with pytest.raises(ValueError):
        WaveScout('invalid.wav')

def test_bpm_and_beats(temp_audio_file):
    scout = WaveScout(temp_audio_file)
    assert scout.beat_map.bpm != 0
    assert scout.beat_map.beats != []
    assert scout.beat_map.key != ''
    assert scout.beat_map.key_confidence > 0.0

def test_export(temp_audio_file, temp_output_file):
    scout = WaveScout(temp_audio_file)
    scout.export(temp_output_file)
    assert os.path.getsize(temp_output_file) > 0

    with tempfile.TemporaryDirectory() as temp_dir:
        output_zip = os.path.join(temp_dir, "slices.zip")
        scout.export(output_zip, export_slices=True)
        assert os.path.getsize(output_zip) > 0
