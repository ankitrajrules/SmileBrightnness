from smilebrightness.controller import DimController


def make(dim_after: float = 5.0) -> DimController:
    return DimController(restore_level=80, dim_level=30, dim_after_seconds=dim_after)


def test_no_change_while_smiling():
    c = make()
    assert all(c.update(True, t) is None for t in range(0, 20))
    assert not c.dimmed


def test_does_not_dim_immediately_on_start():
    c = make()
    assert c.update(False, 100.0) is None
    assert not c.dimmed


def test_dims_after_timeout_and_only_once():
    c = make(dim_after=5)
    assert c.update(False, 0.0) is None
    assert c.update(False, 4.9) is None
    assert c.update(False, 5.0) == 30
    assert c.dimmed
    # Already dimmed: no repeated brightness calls
    assert c.update(False, 6.0) is None
    assert c.update(False, 60.0) is None


def test_restores_on_smile_once():
    c = make(dim_after=1)
    c.update(False, 0.0)
    assert c.update(False, 1.0) == 30
    assert c.update(True, 2.0) == 80
    assert not c.dimmed
    assert c.update(True, 3.0) is None


def test_smile_resets_the_clock():
    c = make(dim_after=5)
    c.update(False, 0.0)
    c.update(True, 4.0)  # smile just before the deadline
    assert c.update(False, 8.0) is None  # only 4s since last smile
    assert c.update(False, 9.0) == 30


def test_zero_timeout_dims_on_first_non_smile():
    c = make(dim_after=0)
    assert c.update(False, 0.0) == 30
