from DataGenerator import DataGenerator


class DataGeneratorTest(object):

    def test_clear_state(self):
        data_generator = DataGenerator()
        # Populate with random fields and data
        data_generator._DataGenerator__state = {'inst_id': 'ABC27216',
                                                'position_type': 'SD'}
        data_generator.clear_state()
        assert len(list(data_generator._DataGenerator__state)) == 0

    def test_state_contains_field(self):
        data_generator = DataGenerator()
        # Populate with random fields and data
        data_generator._DataGenerator__state = {'inst_id': 'ABC27216',
                                                'position_type': 'SD'}
        assert data_generator.state_contains_field('inst_id') \
            and data_generator.state_contains_field('position_type') \
            and not data_generator.state_contains_field('qty')
