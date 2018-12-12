package kafka.poc;

import org.apache.kafka.clients.consumer.Consumer;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.consumer.ConsumerConfig;

import org.apache.avro.generic.GenericRecord;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Properties;
import java.util.Random;

public class TestReceive{

    public static void main(String[] args){
        Properties props = new Properties();

        props.put("bootstrap.servers", "3.8.1.159:9092");
        props.put("group.id", "group1");


        props.put("key.deserializer", "io.confluent.kafka.serializers.KafkaAvroDeserializer");
        props.put("value.deserializer", "io.confluent.kafka.serializers.KafkaAvroDeserializer");
        props.put("schema.registry.url", "http://3.8.1.159:8081");

        //props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        
        String topic = "inst-ref";
        final Consumer<instrument_reference_data_keys, instrument_reference_data_values> consumer = new KafkaConsumer<>(props);
        consumer.subscribe(Arrays.asList(topic));

        try {
        while (true) {
            ConsumerRecords<instrument_reference_data_keys, instrument_reference_data_values> records = consumer.poll(100000);
            for (ConsumerRecord<instrument_reference_data_keys, instrument_reference_data_values> record : records) {
            System.out.printf("offset = %d, key = %s, value = %s \n", record.offset(), record.key(), record.value());
            }
        }
        } finally {
        consumer.close();
        }
    }
    
}