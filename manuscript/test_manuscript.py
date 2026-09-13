"""Small, model-free checks for the manuscript's generated evidence and LaTeX."""

import importlib.util
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = Path(os.environ.get("PHASE1_REPO", ROOT.parent))
SPEC = importlib.util.spec_from_file_location(
    "build_manuscript", ROOT / "build_manuscript.py"
)
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


def test_behavioural_plot_counts_each_observed_mask_and_random_draw_once():
    data = BUILDER.load(REPO)
    display = BUILDER.pd.read_csv(ROOT / "generated/behavioural_null_display.csv")
    assert len(display) == 12
    assert display.loc[display.group == "recovered", "count"].sum() == 27
    assert display.loc[display.group != "recovered", "count"].sum() == 4200
    for row in display.itertuples():
        if row.group == "recovered":
            observed = data["observed"].drop_duplicates(["model_seed", "circuit_id"])
            values = observed.loc[
                observed.model_seed == row.model_seed, "observed_primary_fidelity"
            ]
        else:
            values = data["e2"].loc[
                (data["e2"].model_seed == row.model_seed)
                & (data["e2"].null_model == row.group),
                "primary_fidelity",
            ]
        assert row.count == len(values)
        assert BUILDER.np.allclose(
            [row.minimum, row.q25, row.median, row.q75, row.maximum],
            values.quantile([0, 0.25, 0.5, 0.75, 1]),
            rtol=0,
            atol=1e-14,
        )


def test_full_tolerance_grids_support_reported_median_ordering():
    data = BUILDER.load(REPO)
    for table, criteria, tolerance, value in [
        (data["e3"], [], "displayed_fidelity", "terminal_retained_components"),
        (
            data["grid"],
            ["criterion_name"],
            "criterion_tolerance",
            "final_retained_components",
        ),
    ]:
        medians = (
            table.groupby([*criteria, tolerance, "phase_label"])[value]
            .median()
            .unstack()
        )
        assert (medians.stable_post < medians.delayed_pre_generalisation).all()
        assert (medians.stable_post < medians.transition).all()
