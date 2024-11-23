import rev


def test_spark_flex_config():
    config = rev.SparkFlexConfig()
    config.apply(rev.EncoderConfig()).apply(rev.AbsoluteEncoderConfig())


def test_spark_max_config():
    config = rev.SparkMaxConfig()
    config.apply(rev.EncoderConfig()).apply(rev.AbsoluteEncoderConfig())
