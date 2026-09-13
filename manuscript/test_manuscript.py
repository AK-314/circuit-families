"""Small, model-free checks for the manuscript's generated evidence and LaTeX."""

import importlib.util
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = Path(os.environ.get("PHASE1_REPO", ROOT.parent))
SPEC = importlib.util.spec_from_file_location("build_manuscript", ROOT / "build_manuscript.py")
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


def test_frozen_coverage_and_headline_numbers():
    report = BUILDER.validate(BUILDER.load(REPO))
    assert report["status"] == "validated"
    assert report["model_evaluations_performed_by_builder"] == 0


def test_tex_references_and_graphics_exist():
    for filename in ["paper.tex", "supplement.tex"]:
        text = (ROOT / filename).read_text()
        for included in re.findall(r"\\input\{([^}]+)\}", text):
            text += (ROOT / f"{included}.tex").read_text()
        labels = re.findall(r"\\label\{([^}]+)\}", text)
        assert len(labels) == len(set(labels))
        assert set(re.findall(r"\\ref\{([^}]+)\}", text)) <= set(labels)
        for graphic in re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", text):
            assert (ROOT / "figures" / graphic).is_file(), graphic
    bib = (ROOT / "references.bib").read_text()
    keys = set(re.findall(r"@\w+\{([^,]+),", bib))
    cites = re.findall(r"\\cite\w*\{([^}]+)\}", (ROOT / "paper.tex").read_text())
    assert {key for group in cites for key in group.split(",")} <= keys


def test_original_primary_endpoint_not_relabelled():
    paper = (ROOT / "paper.tex").read_text()
    supplement = (ROOT / "supplement.tex").read_text()
    assert "0.125" in paper and "0.125" in supplement
    assert "designed after the original results" in paper
    assert "full margin annealing analysis is therefore not run" in paper
