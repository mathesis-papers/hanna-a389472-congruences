import argparse
import hashlib
import json
from math import comb
from pathlib import Path


def multiply(left, right, degree):
    result = [0] * (degree + 1)
    left_terms = [(index, value) for index, value in enumerate(left) if value]
    right_terms = [(index, value) for index, value in enumerate(right) if value]
    for left_index, left_value in left_terms:
        for right_index, right_value in right_terms:
            target = left_index + right_index
            if target > degree:
                break
            result[target] += left_value * right_value
    return result


def recurrence_coefficients(degree):
    coefficients = [0, 1, 1] + [0] * (degree - 2)
    for index in range(3, degree + 1):
        coefficients[index] = sum(
            coefficients[upper] * comb(upper, index + 2 - 2 * upper)
            for upper in range((index + 4) // 3, (index + 2) // 2 + 1)
        )
    return coefficients


def product_coefficients(degree):
    product = [1] + [0] * degree
    iterate = [0, 1] + [0] * (degree - 1)
    minimum_degree = 1
    factors = 0
    while minimum_degree <= degree - 1:
        factor = iterate.copy()
        factor[0] = 1
        product = multiply(product, factor, degree)
        square = multiply(iterate, iterate, degree)
        cube = multiply(square, iterate, degree)
        iterate = [first + second for first, second in zip(square, cube)]
        minimum_degree *= 2
        factors += 1
    related = [0] + product[:degree]
    target = multiply(related, related, degree)
    target[1] += 1
    return target, related, factors


def power(series, exponent, degree):
    result = [1] + [0] * degree
    for iteration in range(exponent):
        result = multiply(result, series, degree)
    return result


def compose(outer, inner, degree):
    assert inner[0] == 0
    result = [0] * (degree + 1)
    term = [1] + [0] * degree
    for coefficient in outer:
        for index, value in enumerate(term):
            result[index] += coefficient * value
        term = multiply(term, inner, degree)
        if not any(term):
            break
    return result


def revert(series, degree):
    assert series[:2] == [0, 1]
    reciprocal = [1] + [0] * (degree - 1)
    for index in range(1, degree):
        reciprocal[index] = -sum(
            series[upper + 1] * reciprocal[index - upper]
            for upper in range(1, index + 1)
        )
    result = [0] * (degree + 1)
    current = [1] + [0] * (degree - 1)
    for index in range(1, degree + 1):
        current = multiply(current, reciprocal, degree - 1)
        assert current[index - 1] % index == 0
        result[index] = current[index - 1] // index
    identity = [0, 1] + [0] * (degree - 1)
    assert compose(series, result, degree) == identity
    assert compose(result, series, degree) == identity
    return result


def family_product(leading_degree, exponent, sign, degree):
    iterate = [0, 1] + [0] * (degree - 1)
    product = [1] + [0] * degree
    while any(iterate):
        factor = [sign * value for value in iterate]
        factor[0] = 1
        product = multiply(product, factor, degree)
        iterate = multiply(
            power(iterate, leading_degree, degree),
            power(factor, exponent, degree), degree,
        )
    return product


def sibling_checks(degree=64):
    prefixes = json.loads(Path(__file__).with_name('source-prefixes.json').read_text())
    sources = {entry['id']: entry for entry in prefixes['entries']}
    matched = {}
    checks = 0
    for leading_degree, exponent, sign in [(2, index, 1) for index in range(1, 7)] + [
        (index, 1, -1) for index in (2, 3, 4)
    ]:
        product = family_product(leading_degree, exponent, sign, degree)
        unit = [1, sign] + [0] * (degree - 1)
        substitution = [0] * leading_degree + power(unit, exponent, degree)[:degree + 1 - leading_degree]
        for product_power in sorted({1, exponent}):
            series = [0] + power(product, product_power, degree)[:degree]
            inverse = revert(series, degree)
            multiplier = [0] * (leading_degree - 1) + power(
                unit, exponent - product_power, degree,
            )[:degree + 2 - leading_degree]
            right = multiply(multiplier, series, degree)
            assert compose(series, substitution, degree) == right
            assert compose(inverse, right, degree) == substitution
            checks += 2
            source_id = None
            if sign == 1:
                if exponent == 1:
                    source_id = 'A350432'
                    inverse_id = 'A350431'
                    values = sources[inverse_id]['coefficients']
                    assert inverse[1:len(values) + 1] == values
                    matched[inverse_id] = len(values)
                else:
                    source_id = 'A' + str((369543 if product_power == 1 else 369550) + exponent)
                    first = [0] + product[:degree]
                    second = [0] + power(product, exponent, degree)[:degree]
                    assert power(first, exponent, degree) == [0] * (exponent - 1) + second[:degree + 2 - exponent]
            elif leading_degree == 2:
                source_id = 'A273162'
                series_for_source = inverse
            elif leading_degree == 3:
                source_id = 'A350433'
                series_for_source = series
            else:
                source_id = 'A350434'
                series_for_source = inverse
            if source_id:
                values = sources[source_id]['coefficients']
                chosen = series if sign == 1 else series_for_source
                assert chosen[1:len(values) + 1] == values, source_id
                matched[source_id] = len(values)
    assert len(matched) == 15
    assert family_product(2, 1, -1, degree)[1] == -1
    assert sources['A273162']['coefficients'][1] == 1
    return {
        'degree': degree,
        'matched_source_prefixes': matched,
        'functional_and_inverse_identity_checks': checks,
        'two_sided_reversion_pairs': 14,
        'a273162_formula_2_second_coefficients': {'stated_series': 1, 'literal_product': -1},
        'coverage': 'Product families, both compositional inverse equations, source prefixes, power identities, and the corrected A273162 inverse-product formula.',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--degree', type=int, default=1000)
    arguments = parser.parse_args()
    degree = arguments.degree
    if not 50 <= degree <= 2000:
        parser.error('degree must be between 50 and 2000')
    coefficients = recurrence_coefficients(degree)
    product, related, factors = product_coefficients(degree)
    assert coefficients == product
    source_prefix = [
        1, 1, 2, 3, 6, 9, 14, 24, 42, 72, 114, 179, 284, 453,
        736, 1213, 2016, 3362, 5606, 9318, 15378, 25121, 40614,
        65216, 104422, 167118, 267674, 429297, 689478, 1109149,
        1788032, 2889897, 4683664, 7610640, 12394998, 20225081,
        33050490, 54068421, 88519060, 144984819, 237508938,
    ]
    related_prefix = [
        1, 1, 1, 2, 2, 3, 5, 9, 14, 18, 25, 38, 60, 97, 159,
        265, 444, 735, 1187, 1865, 2851, 4271, 6378, 9621,
        14724, 22864, 35947, 57044, 91141, 146384, 236102,
        382124, 620298, 1009685, 1647703, 2694709, 4413524,
        7232548, 11845740, 19369888, 31590755, 51346902, 83126317,
    ]
    assert coefficients[1:len(source_prefix) + 1] == source_prefix
    assert related[1:len(related_prefix) + 1] == related_prefix
    mod_two = list(range(3, degree + 1, 2))
    mod_three = list(range(5, degree + 1, 3))
    mod_six = list(range(5, degree + 1, 6))
    for modulus, indices in ((2, mod_two), (3, mod_three), (6, mod_six)):
        assert all(coefficients[index] % modulus == 0 for index in indices)
    digit_lemma_cases = 0
    for upper in range(301):
        for lower in range(upper + 1):
            if upper % 3 != 2 and (lower + 2 * upper) % 3 == 1:
                assert comb(upper, lower) % 3 == 0
                digit_lemma_cases += 1
    encoded = (','.join(str(value) for value in coefficients) + '\n').encode()
    result = {
        'status': 'PASS',
        'arithmetic': 'exact integers',
        'degree': degree,
        'coefficient_count_including_zero': len(coefficients),
        'coefficient_sha256': hashlib.sha256(encoded).hexdigest(),
        'independent_formulas': ['binomial recurrence', 'iterated polynomial product'],
        'product_factors': factors,
        'a389472_prefix_terms': len(source_prefix),
        'a350432_prefix_terms': len(related_prefix),
        'mod_two_indices': len(mod_two),
        'mod_three_indices': len(mod_three),
        'mod_six_indices': len(mod_six),
        'digit_lemma_cases_upper_at_most_300': digit_lemma_cases,
        'sibling_checks': sibling_checks(),
        'coverage': 'Finite checks of the recurrence, product identity, source prefixes and congruences; the all-index statements have written proofs in note.tex.',
    }
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
