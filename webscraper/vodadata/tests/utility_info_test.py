from vodaData.utilityInfoScraper import FindUtilInfo


def test_try_parse_float_none():
    float = FindUtilInfo.try_parse_float(None)
    assert float is None


def test_try_parse_float_nd():
    float = FindUtilInfo.try_parse_float('ND')
    assert float == 0.0


def test_try_parse_float_commas():
    float = FindUtilInfo.try_parse_float('1,000,000')
    assert float == 1000000


def test_try_parse_float_nominal():
    float = FindUtilInfo.try_parse_float(1000)
    assert float == 1000
