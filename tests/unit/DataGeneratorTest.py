import pytest
import string
import sys
sys.path.insert(0, 'Kafka_Python/')

from DataGenerator import DataGenerator


@pytest.fixture
def data_generator():
    return DataGenerator()


def test_clear_state(data_generator):
    # Populate with random fields and data
    data_generator._DataGenerator__state = {'inst_id': 'ABC27216',
                                            'position_type': 'SD'}
    data_generator.clear_state()
    assert len(list(data_generator._DataGenerator__state)) == 0


def test_state_contains_field(data_generator):
    # Populate with random fields and data
    data_generator._DataGenerator__state = {'inst_id': 'ABC27216',
                                            'position_type': 'SD'}
    assert data_generator.state_contains_field('inst_id') \
        and data_generator.state_contains_field('position_type') \
        and not data_generator.state_contains_field('qty')


def test_get_state_value(data_generator):
    # Populate with random fields and data
    data_generator._DataGenerator__state = {'inst_id': 'ABC27216',
                                            'position_type': 'SD'}
    value = data_generator.get_state_value('position_type')
    assert value == 'SD'


def test_generate_new_inst_id_when_asset_class_none(data_generator):
    inst_id = data_generator.generate_new_inst_id()
    # TODO: check __get_preemptive_generation called
    is_correct_format = True
    for c in inst_id:
        is_correct_format = is_correct_format \
                            and c in string.ascii_uppercase + string.digits

    assert is_correct_format


def test_generate_new_inst_id_when_asset_class_not_none(data_generator):
    # TODO: check __get_preemptive_generation called
    assert True


def test_generate_new_inst_id_add_to_lists_of_inst_ids(data_generator):
    n_stock_ids = len(data_generator._DataGenerator__stock_inst_ids)
    n_cash_ids = len(data_generator._DataGenerator__cash_inst_ids)
    inst_id = data_generator.generate_new_inst_id()
    if inst_id.startswith('ABC'):
        is_correct_length = \
            len(data_generator._DataGenerator__stock_inst_ids) \
            == (n_stock_ids + 1) \
            and len(data_generator._DataGenerator__cash_inst_ids) \
            == n_cash_ids
    else:
        is_correct_length = \
            len(data_generator._DataGenerator__cash_inst_ids) \
            == (n_cash_ids + 1) \
            and len(data_generator._DataGenerator__stock_inst_ids) \
            == n_stock_ids

    assert is_correct_length
