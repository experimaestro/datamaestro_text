from pathlib import Path
from datamaestro.test.checks import DatamaestroAnalyzer


def test_documented():
    """Test if every configuration is documented"""
    doc_path = Path(__file__).parents[3] / "docs" / "source" / "index.rst"
    analyzer = DatamaestroAnalyzer(
        doc_path, set(["datamaestro_text"]), set(["datamaestro_text.test"])
    )

    analyzer.analyze()
    analyzer.report()
    analyzer.assert_valid_documentation()
