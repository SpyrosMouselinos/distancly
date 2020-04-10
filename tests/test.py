from myPackage.azymuth import RhumbLineCalc


def test_RhumbLineCalc():
    """
        Test the functionality of Rhumbline Calc
    """

    rl = RhumbLineCalc()
    result_1 = rl.loxodromic_mid_point(point_a=(25.7976636, -80.1163316), point_b=(38.7134232, -9.1498182))
    result_2 = rl.loxodromic_power_interpolation(point_a=(25.7976636, -80.1163316), point_b=(38.7134232, -9.1498182),
                                                 n_points=7)
    assert result_1 in result_2
