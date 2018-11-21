import sys
sys.path.insert(0, 'Kafka_Python/')
from DataGenerator import DataGenerator

def test_clear_state():
    data_generator = DataGenerator()
    # Populate with random fields and data
    data_generator._DataGenerator__state = {'inst_id': 'ABC27216',
                                            'position_type': 'SD'}
    data_generator.clear_state()
    assert len(list(data_generator._DataGenerator__state)) == 0

def test_state_contains_field():
    data_generator = DataGenerator()
    # Populate with random fields and data
    data_generator._DataGenerator__state = {'inst_id': 'ABC27216',
                                            'position_type': 'SD'}
    assert data_generator.state_contains_field('inst_id') \
        and data_generator.state_contains_field('position_type') \
        and not data_generator.state_contains_field('qty')

def test_get_state_value():
    data_generator = DataGenerator()
    # Populate with random fields and data
    data_generator._DataGenerator__state = {'inst_id': 'ABC27216',
                                            'position_type': 'SD'}
    value = data_generator.get_state_value('position_type')
    assert value == 'SD'

# def test_generate_new_inst_id_when_asset_class_not_None():
#     data_generator = DataGenerator()
#     data_generator.genegenerate_inst_id()
#     mocked_hello = mocker.patch('DataGenerator.__get_preemptive_generation')
