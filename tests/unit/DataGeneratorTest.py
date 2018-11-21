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

# TODO: test with only param

def test_generate_inst_id_when_asset_class_stock(data_generator):
    stock_ids = ['ABCV740P', 'ABCD4F2J']
    data_generator._DataGenerator__stock_inst_ids = stock_ids
    id = data_generator.generate_inst_id(asset_class='Stock')
    assert id in stock_ids


def test_generate_inst_id_when_asset_class_cash(data_generator):
    cash_ids = ['BCD0MUID', 'BCDAH98I']
    data_generator._DataGenerator__cash_inst_ids = cash_ids
    id = data_generator.generate_inst_id(asset_class='Cash')
    assert id in cash_ids


def test_generate_asset_class(data_generator):
    asset_class = data_generator.generate_asset_class()
    assert asset_class in ['Stock', 'Cash']


def test_generate_coi(data_generator):
    coi = data_generator.generate_coi()
    assert coi in ['US', 'GB', 'CA', 'FR', 'DE', 'CH', 'SG', 'JP']


def test_generate_haircut(data_generator):
    haircut = data_generator.generate_haircut()
    assert haircut == '2.00%'


def test_generate_is_callable(data_generator):
    is_callable = data_generator.generate_is_callable()
    assert is_callable in ['Yes', 'No']


def test_generate_swap_type(data_generator):
    swap_type = data_generator.generate_swap_type()
    assert swap_type in ['Equity', 'Portfolio']


def test_generate_reference_rate(data_generator):
    ref_rate = data_generator.generate_reference_rate()
    assert ref_rate in ['LIBOR']


def test_generate_status(data_generator):
    status = data_generator.generate_status()
    assert status in ['Live', 'Dead']


def test_generate_depot_id(data_generator):
    depot_id = data_generator.generate_depot_id()
    # TODO: check __get_preemptive_generation called
    is_correct_format = True
    for c in depot_id:
        is_correct_format = is_correct_format and c in string.digits

    assert is_correct_format


def test_generate_account_number(data_generator):
    account_number = data_generator.generate_account_number()
    # TODO: check __get_preemptive_generation called
    is_correct_format = True
    for c in account_number:
        is_correct_format = is_correct_format and c in string.digits

    assert is_correct_format


def test_generate_order_id(data_generator):
    order_id = data_generator.generate_order_id()
    # TODO: check __get_preemptive_generation called
    is_correct_format = True
    for c in order_id:
        is_correct_format = is_correct_format and c in string.digits

    assert is_correct_format


def test_generate_customer_id(data_generator):
    customer_id = data_generator.generate_customer_id()
    # TODO: check __get_preemptive_generation called
    is_correct_format = True
    for c in customer_id:
        is_correct_format = is_correct_format and c in string.digits

    assert is_correct_format


def test_generate_sto_id(data_generator):
    sto_id = data_generator.generate_sto_id()
    # TODO: check __get_preemptive_generation called
    is_correct_format = True
    for c in sto_id:
        is_correct_format = is_correct_format and c in string.digits

    assert is_correct_format


def test_generate_agent_id(data_generator):
    agent_id = data_generator.generate_agent_id()
    # TODO: check __get_preemptive_generation called
    is_correct_format = True
    for c in agent_id:
        is_correct_format = is_correct_format and c in string.digits

    assert is_correct_format


def test_generate_direction(data_generator):
    direction = data_generator.generate_direction()
    assert direction in ['Credit', 'Debit']


def test_generate_currency(data_generator):
    curr = data_generator.generate_currency()
    assert curr in ['USD', 'CAD', 'EUR', 'GBP']


def test_generate_swap_contract_id_(data_generator):
    swap_contract_ids = ['18825586', '90344267']
    data_generator._DataGenerator__swap_contract_ids = swap_contract_ids
    id = data_generator.generate_swap_contract_id()
    assert id in swap_contract_ids
