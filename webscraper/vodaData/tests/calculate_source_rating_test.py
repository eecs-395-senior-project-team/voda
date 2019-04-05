from vodaData.calculateSourceRating import CalculateSourceRating


def test_size_std_dev_dict():
    func = CalculateSourceRating()
    CalculateSourceRating.collect_contaminants_stdev(func)
    assert len(func.contaminant_std_dev_dict) == 200


def test_size_nat_avg_dict():
    func = CalculateSourceRating()
    CalculateSourceRating.collect_contaminant_nat_avgs(func)
    assert len(func.contaminant_nat_avg_dict) == 200


def test_amount_above_avg():
    func = CalculateSourceRating()
    CalculateSourceRating.collect_contaminant_nat_avgs(func)
    amt_abv_avg = CalculateSourceRating.amount_above_avg(func, (876, 32236, 170.5))
    expected = 170.5 - 68.2
    assert amt_abv_avg == expected


def test_amount_to_add():
    func = CalculateSourceRating()
    CalculateSourceRating.collect_contaminant_nat_avgs(func)
    CalculateSourceRating.collect_contaminants_stdev(func)
    amt_abv_avg = CalculateSourceRating.amount_above_avg(func, (876, 32236, 170.5))
    amt_to_add = CalculateSourceRating.amount_to_add(func, (876, 32236, 170.5), amt_abv_avg)
    # std deviation for contaminant with ID 876 is "146.404355369314"
    # amount above average is 102.3
    expected = 102.3 / 146.404355369314
    assert amt_to_add == expected
