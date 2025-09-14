from semiconductor_sim.materials import get_material, list_materials


def test_list_materials_contains_known():
    keys = list(list_materials())
    assert {"Si", "Ge", "GaAs"}.issubset(set(keys))


def test_si_300K_reference_ranges():
    si = get_material("Si")
    T = 300.0
    Eg = float(si.Eg(T))
    Nc = float(si.Nc(T))
    Nv = float(si.Nv(T))
    ni = float(si.ni(T))
    EG_MIN, EG_MAX = 1.10, 1.14
    NC_MIN, NC_MAX = 2.5e19, 3.8e19
    NV_MIN, NV_MAX = 1.2e19, 2.5e19
    NI_MIN, NI_MAX = 5e9, 2e10
    assert EG_MIN < Eg < EG_MAX
    assert NC_MIN < Nc < NC_MAX
    assert NV_MIN < Nv < NV_MAX
    assert NI_MIN < ni < NI_MAX


def test_ge_300K_reference_ranges():
    ge = get_material("Ge")
    T = 300.0
    Eg = float(ge.Eg(T))
    Nc = float(ge.Nc(T))
    Nv = float(ge.Nv(T))
    ni = float(ge.ni(T))
    EG_MIN, EG_MAX = 0.60, 0.70
    NC_MIN, NC_MAX = 8e18, 1.4e19
    NV_MIN, NV_MAX = 3e18, 7e18
    NI_MIN, NI_MAX = 5e12, 5e13
    assert EG_MIN < Eg < EG_MAX
    assert NC_MIN < Nc < NC_MAX
    assert NV_MIN < Nv < NV_MAX
    assert NI_MIN < ni < NI_MAX


def test_gaas_300K_reference_ranges():
    gaas = get_material("GaAs")
    T = 300.0
    Eg = float(gaas.Eg(T))
    Nc = float(gaas.Nc(T))
    Nv = float(gaas.Nv(T))
    ni = float(gaas.ni(T))
    EG_MIN, EG_MAX = 1.40, 1.45
    NC_MIN, NC_MAX = 3.5e17, 6.0e17
    NV_MIN, NV_MAX = 7e18, 1.2e19
    NI_MIN, NI_MAX = 1e6, 1e7
    assert EG_MIN < Eg < EG_MAX
    assert NC_MIN < Nc < NC_MAX
    assert NV_MIN < Nv < NV_MAX
    assert NI_MIN < ni < NI_MAX
