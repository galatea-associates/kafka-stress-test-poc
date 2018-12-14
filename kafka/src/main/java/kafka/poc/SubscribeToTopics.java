package kafka.poc;

import java.util.EnumMap;
import java.util.Map;
import java.util.concurrent.CyclicBarrier;

public class SubscribeToTopics {

    public static void main(String[] args) {
        Map<Topic, ConsumerTopicProperties> topicsToProperies = new EnumMap<Topic, ConsumerTopicProperties>(Topic.class) {
            private static final long serialVersionUID = 3019616454475007213L;
            {
                put(Topic.PRICES, new ConsumerTopicProperties(Topic.PRICES, 1));
                put(Topic.INST_REF, new ConsumerTopicProperties(Topic.INST_REF, 60));
                put(Topic.POSITION, new ConsumerTopicProperties(Topic.POSITION, 1));
            }
        };
        CyclicBarrier cyclicBarrier = new CyclicBarrier(4);
        new Thread(new SimpleConsumer<position_data_keys, position_data_values>(
            60000, args[0], topicsToProperies.get(Topic.POSITION), cyclicBarrier)).start();
        new Thread(new SimpleConsumer<prices_keys, prices_values>(
            60000, args[0], topicsToProperies.get(Topic.PRICES), cyclicBarrier)).start();
        new Thread(new SimpleConsumer<instrument_reference_data_keys, instrument_reference_data_values>(
            60000, args[0], topicsToProperies.get(Topic.INST_REF), cyclicBarrier)).start();
        new Thread(new ConsumerTimer(topicsToProperies, cyclicBarrier)).start();

    }
}
