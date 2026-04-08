from pathlib import Path

from src.book_parser import Parser


HTML_WITH_IMAGE = """
<html>
  <body>
    <div class="product_main">
      <h1>My: Book/Title?</h1>
    </div>
    <div class="item active">
      <img src="media/img.jpg" />
    </div>
  </body>
</html>
"""


HTML_NO_IMAGE = """
<html>
  <body>
    <div class="product_main">
      <h1>My Book</h1>
    </div>
  </body>
</html>
"""


def test_download_image_writes_file_and_normalizes_name(monkeypatch, tmp_path: Path):
    class DummyResponse:
        status_code = 200
        content = b"fake-image-bytes"

    def fake_get(url: str):
        assert url == "https://example.test/media/img.jpg"
        return DummyResponse()

    monkeypatch.setattr("src.book_parser.requests.get", fake_get)
    parser = Parser(HTML_WITH_IMAGE, "https://example.test/page")
    image_path = parser.download_image(tmp_path)

    assert image_path
    image_file = Path(image_path)
    assert image_file.exists()
    assert image_file.name == "My BookTitle.jpg"


def test_download_image_returns_empty_when_missing_image(tmp_path: Path):
    parser = Parser(HTML_NO_IMAGE, "https://example.test/page")
    images_dir = tmp_path / "images"
    assert parser.download_image(images_dir) == ""
    assert images_dir.exists() is False
