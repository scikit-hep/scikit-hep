import awkward as ak
import uproot


def test_uproot_roundtrip_preserves_awkward_arrays(tmp_path):
    """Check that Uproot preserves Awkward Array data in a ROOT file."""
    file_path = tmp_path / "events.root"
    expected_pt = [[1.0, 2.0], [3.0]]
    expected_eta = [[0.1, -0.1], [0.3]]

    with uproot.recreate(file_path) as root_file:
        root_file["events"] = {
            "pt": ak.Array(expected_pt),
            "eta": ak.Array(expected_eta),
        }

    with uproot.open(file_path) as root_file:
        actual = root_file["events"].arrays(["pt", "eta"], library="ak")

    assert ak.to_list(actual["pt"]) == expected_pt
    assert ak.to_list(actual["eta"]) == expected_eta
