package kafka.poc;

import org.apache.kafka.clients.consumer.Consumer;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import java.util.Arrays;
import java.util.Properties;

public class TestReceive {

    public static void main(String[] args) {
        Properties props = new Properties();

        props.put("bootstrap.servers", args[0] + ":9092");
        props.put("group.id", "group1");
        props.put("key.deserializer", "io.confluent.kafka.serializers.KafkaAvroDeserializer");
        props.put("value.deserializer", "io.confluent.kafka.serializers.KafkaAvroDeserializer");
        props.put("schema.registry.url", "http://" + args[0] + ":8081");

        String topic = "inst-ref";
        final Consumer<instrument_reference_data_keys, instrument_reference_data_values> consumer =
                new KafkaConsumer<>(props);
        consumer.subscribe(Arrays.asList(topic));

        try {
            while (true) {
                ConsumerRecords<instrument_reference_data_keys, instrument_reference_data_values> records =
                        consumer.poll(100000);
                for (ConsumerRecord<instrument_reference_data_keys, instrument_reference_data_values> record : records) {
                    System.out.printf("offset = %d, key = %s, value = %s \n", record.offset(),
                            record.key(), record.value());
                }
            }
        } finally {
            consumer.close();
        }
    }

}
