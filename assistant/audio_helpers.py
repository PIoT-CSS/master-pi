# Copyright (C) 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Helper functions for audio streams."""

import array
import logging
import math
import time
import threading
import wave

import click
import sounddevice as sd


DEFAULT_AUDIO_SAMPLE_RATE = 16000
DEFAULT_AUDIO_SAMPLE_WIDTH = 2
DEFAULT_AUDIO_ITER_SIZE = 3200
DEFAULT_AUDIO_DEVICE_BLOCK_SIZE = 6400
DEFAULT_AUDIO_DEVICE_FLUSH_SIZE = 25600


def normalize_audio_buffer(buf, volume_percentage, sample_width=2):
    """Adjusts the loudness of the audio data in the given buffer.

    Volume normalization is done by scaling the amplitude of the audio
    in the buffer by a scale factor of 2^(volume_percentage/100)-1.
    For example, 50% volume scales the amplitude by a factor of 0.414,
    and 75% volume scales the amplitude by a factor of 0.681.
    For now we only sample_width 2.

    :params buf: byte string containing audio data to normalize.
    :type buf: byte
    
    :params volume_percentage: volume setting as an integer percentage (1-100).
    :type volume_percentage: integer
    
    :params sample_width: size of a single sample in bytes.
    :type sample_width: integer
    """
    if sample_width != 2:
        raise Exception('unsupported sample width:', sample_width)
    scale = math.pow(2, 1.0*volume_percentage/100)-1
    # Construct array from bytes based on sample_width, multiply by scale
    # and convert it back to bytes
    arr = array.array('h', buf)
    for idx in range(0, len(arr)):
        arr[idx] = int(arr[idx]*scale)
    buf = arr.tostring()
    return buf


def align_buf(buf, sample_width):
    """In case of buffer size not aligned to sample_width pad it with 0s"""
    remainder = len(buf) % sample_width
    if remainder != 0:
        buf += b'\0' * (sample_width - remainder)
    return buf

class SoundDeviceStream(object):
    """Audio stream based on an underlying sound device.

    It can be used as an audio source (read) and a audio sink (write).

    :params sample_rate: sample rate in hertz.
    :type sample_rate: integer
    
    :params sample_width: size of a single sample in bytes.
    :type sample_width: integer

    :params block_size: size in bytes of each read and write operation.
    :type block_size: integer

    :params flush_size: size in bytes of silence data written during flush operation.
    :type flush_size: integer
    """
    def __init__(self, sample_rate, sample_width, block_size, flush_size):
        if sample_width == 2:
            audio_format = 'int16'
        else:
            raise Exception('unsupported sample width:', sample_width)
        self._audio_stream = sd.RawStream(
            samplerate=sample_rate, dtype=audio_format, channels=1,
            blocksize=int(block_size/2),  # blocksize is in number of frames.
        )
        self._block_size = block_size
        self._flush_size = flush_size
        self._sample_rate = sample_rate

    def read(self, size):
        """Read bytes from the stream."""
        buf, overflow = self._audio_stream.read(size)
        if overflow:
            logging.warning('SoundDeviceStream read overflow (%d, %d)',
                            size, len(buf))
        return bytes(buf)

    def write(self, buf):
        """Write bytes to the stream."""
        underflow = self._audio_stream.write(buf)
        if underflow:
            logging.warning('SoundDeviceStream write underflow (size: %d)',
                            len(buf))
        return len(buf)

    def flush(self):
        if self._audio_stream.active and self._flush_size > 0:
            self._audio_stream.write(b'\x00' * self._flush_size)

    def start(self):
        """Start the underlying stream."""
        if not self._audio_stream.active:
            self._audio_stream.start()

    def stop(self):
        """Stop the underlying stream."""
        if self._audio_stream.active:
            self._audio_stream.stop()

    def close(self):
        """Close the underlying stream and audio interface."""
        if self._audio_stream:
            self.stop()
            self._audio_stream.close()
            self._audio_stream = None

    @property
    def sample_rate(self):
        return self._sample_rate


class ConversationStream(object):
    """Audio stream that supports half-duplex conversation.

    A conversation is the alternance of:
    - a recording operation
    - a playback operation

    Excepted usage:

      For each conversation:
      - start_recording()
      - read() or iter()
      - stop_recording()
      - start_playback()
      - write()
      - stop_playback()

      When conversations are finished:
      - close()

    :params source: file-like stream object to read input audio bytes from.
    :type source: file

    :params sink: file-like stream object to write output audio bytes to.
    :type sink: file

    :params iter_size: read size in bytes for each iteration.
    :type iter_size: integer

    :params sample_width: size of a single sample in bytes.
    :type sample_width: byte
    """
    def __init__(self, source, sink, iter_size, sample_width):
        self._source = source
        self._sink = sink
        self._iter_size = iter_size
        self._sample_width = sample_width
        self._volume_percentage = 50
        self._stop_recording = threading.Event()
        self._source_lock = threading.RLock()
        self._recording = False
        self._playing = False

    def start_recording(self):
        """Start recording from the audio source."""
        self._recording = True
        self._stop_recording.clear()
        self._source.start()

    def stop_recording(self):
        """Stop recording from the audio source."""
        self._stop_recording.set()
        with self._source_lock:
            self._source.stop()
        self._recording = False

    def start_playback(self):
        """Start playback to the audio sink."""
        self._playing = True
        self._sink.start()

    def stop_playback(self):
        """Stop playback from the audio sink."""
        self._sink.flush()
        self._sink.stop()
        self._playing = False

    @property
    def recording(self):
        return self._recording

    @property
    def playing(self):
        return self._playing

    @property
    def volume_percentage(self):
        """The current volume setting as an integer percentage (1-100)."""
        return self._volume_percentage

    @volume_percentage.setter
    def volume_percentage(self, new_volume_percentage):
        self._volume_percentage = new_volume_percentage

    def read(self, size):
        """Read bytes from the source (if currently recording).
        """
        with self._source_lock:
            return self._source.read(size)

    def write(self, buf):
        """Write bytes to the sink (if currently playing).
        """
        buf = align_buf(buf, self._sample_width)
        buf = normalize_audio_buffer(buf, self.volume_percentage)
        return self._sink.write(buf)

    def close(self):
        """Close source and sink."""
        self._source.close()
        self._sink.close()

    def __iter__(self):
        """Returns a generator reading data from the stream."""
        while True:
            if self._stop_recording.is_set():
                return
            yield self.read(self._iter_size)

    @property
    def sample_rate(self):
        return self._source._sample_rate
