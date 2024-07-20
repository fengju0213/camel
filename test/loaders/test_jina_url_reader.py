# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========
import json

import pytest

from camel.loaders import JinaURLReader
from camel.types.enums import JinaReturnFormat


@pytest.fixture
def default_reader():
    return JinaURLReader()


def test_read_content_default(default_reader: JinaURLReader):
    test_url = "https://en.wikipedia.org/wiki/Hollow_Knight"
    content = default_reader.read_content(test_url)
    assert "Title: Hollow Knight" in content


def test_read_content_no_protocol(default_reader: JinaURLReader):
    test_url = "en.wikipedia.org/wiki/Hollow_Knight"
    content = default_reader.read_content(test_url)
    assert "Title: Hollow Knight" in content


def test_read_content_markdown():
    test_url = "https://en.wikipedia.org/wiki/Hollow_Knight"
    markdown_reader = JinaURLReader(return_format=JinaReturnFormat.MARKDOWN)
    content = markdown_reader.read_content(test_url)
    assert "_Hollow Knight_" in content


def test_read_content_html():
    test_url = "https://en.wikipedia.org/wiki/Hollow_Knight"
    html_reader = JinaURLReader(return_format=JinaReturnFormat.HTML)
    content = html_reader.read_content(test_url)
    assert "<title>Hollow Knight - Wikipedia</title>" in content


def test_read_content_text():
    test_url = "https://en.wikipedia.org/wiki/Hollow_Knight"
    text_reader = JinaURLReader(return_format=JinaReturnFormat.TEXT)
    content = text_reader.read_content(test_url)
    assert "Hollow Knight" in content


def test_read_content_json():
    test_url = "https://en.wikipedia.org/wiki/Hollow_Knight"
    json_reader = JinaURLReader(json_response=True)
    content = json_reader.read_content(test_url)
    content_json = json.loads(content)
    assert "data" in content_json
    assert "title" in content_json["data"]
    assert "Hollow Knight" in content_json["data"]["title"]


def test_read_content_json_webpage():
    test_url = "https://httpbin.org/json"
    json_reader = JinaURLReader(return_format=JinaReturnFormat.TEXT)
    content = json_reader.read_content(test_url)
    content_json = json.loads(content)
    assert "slideshow" in content_json
    assert "slides" in content_json["slideshow"]
