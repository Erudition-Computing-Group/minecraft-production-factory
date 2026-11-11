from agents.math_agent import verify_bounding_box


def test_helix_within_bounds():
    code = "def coords(t):\n    import math\n    r=1.5; theta=t*0.1; y=(t%40)*0.05\n    return (r*math.cos(theta), y, r*math.sin(theta))"
    ok, msg = verify_bounding_box(code, ticks=40, radius=3.0)
    assert ok, msg


def test_nan_rejected():
    code = "def coords(t):\n    return (float('nan'), 0.0, 0.0)"
    ok, msg = verify_bounding_box(code, ticks=5, radius=3.0)
    assert not ok
