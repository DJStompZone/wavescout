import os
import shutil
import tempfile
import pytest
from wavescout.wavescout import WaveScout, BeatMap, WaveScoutFactory


@pytest.fixture
def temp_audio_file():
  test_filename = os.path.join(os.path.dirname(__file__), 'testfile.wav')
  shutil.copyfile(
    os.path.join(os.path.dirname(__file__), 'Epidome_2010_DJStomp.wav'),
    test_filename)
  yield test_filename


@pytest.fixture
def temp_output_file():
  with tempfile.NamedTemporaryFile(delete=False) as temp_file:
    yield temp_file.name
    os.remove(temp_file.name)


@pytest.fixture
def temp_output_folder():
  with tempfile.TemporaryDirectory() as temp_dir:
    yield temp_dir


def test_invalid_file_path():
  with pytest.raises(ValueError):
    WaveScout('invalid.wav')


def test_output_generic(temp_audio_file):
  scout = WaveScout(temp_audio_file)
  assert scout is not None


def test_has_beatmap(temp_audio_file):
  scout = WaveScout(temp_audio_file)
  assert scout.beat_map is not None
  assert type(scout.beat_map) == BeatMap


def test_bpm(temp_audio_file):
  scout = WaveScout(temp_audio_file)
  assert scout.beat_map.bpm != 0
  assert type(scout.beat_map.bpm) == int


def test_beats(temp_audio_file):
  scout = WaveScout(temp_audio_file)
  assert scout.beat_map.beats != []
  assert len(scout.beat_map.beats) > 0
  assert type(scout.beat_map.beats) == list


def test_export_beats(temp_audio_file, temp_output_file):
  scout = WaveScout(temp_audio_file)
  scout.export(temp_output_file)
  assert os.path.getsize(temp_output_file) > 0


def test_export_slices(temp_audio_file, temp_output_folder):
  scout = WaveScout(temp_audio_file)
  output_zip = os.path.join(temp_output_folder, "slices.zip")
  scout.export(output_zip, export_slices=True)
  assert os.path.getsize(output_zip) > 0


def test_wavescout_factory(temp_audio_file, temp_output_folder):
  num_test_iters = 3
  for i in range(num_test_iters):
    shutil.copy(temp_audio_file,
                os.path.join(temp_output_folder, f'test_{i+1}.wav'))
  wavefactory = WaveScoutFactory(temp_output_folder)
  slicers = wavefactory.get_audio_slicers()
  assert slicers is not None
  assert type(slicers) == list
  assert len(slicers) == num_test_iters
  for each in slicers:
    assert type(each) == WaveScout
