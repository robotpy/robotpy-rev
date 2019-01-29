def test_init(rev):
    rev.CANSparkMax(0, rev.MotorType.kBrushless)


def test_current_limit(rev, hal_data):
    sm = rev.CANSparkMax(1, rev.MotorType.kBrushless)

    sm.setSecondaryCurrentLimit(50)

    assert hal_data["CANSparkMax"][1]["currentChop"] == 50.0
    assert isinstance(hal_data["CANSparkMax"][1]["currentChop"], float)
    assert hal_data["CANSparkMax"][1]["currentChopCycles"] == 0

    sm.setSecondaryCurrentLimit(52.5, 5)

    assert hal_data["CANSparkMax"][1]["currentChop"] == 52.5
    assert hal_data["CANSparkMax"][1]["currentChopCycles"] == 5
