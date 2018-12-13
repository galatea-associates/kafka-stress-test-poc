package kafka.poc;

import java.util.Collections;
import java.util.Map;
import java.util.Properties;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.Topology;
import org.apache.kafka.streams.kstream.Consumed;
import org.apache.kafka.streams.kstream.KStream;
import io.confluent.kafka.streams.serdes.avro.SpecificAvroSerde;
import io.confluent.kafka.streams.serdes.avro.GenericAvroSerde;

public class SimpleStream {

    public static void main(String[] args) {
        Properties streamsConfiguration = new Properties();
        streamsConfiguration.put(StreamsConfig.APPLICATION_ID_CONFIG, "Streaming-QuickStart");
        streamsConfiguration.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, args[0]+":9092");
        streamsConfiguration.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG,
            SpecificAvroSerde.class);
        streamsConfiguration.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG,
            SpecificAvroSerde.class);
        streamsConfiguration.put("schema.registry.url", "http://"+args[0]+":8081");

        final Map<String, String> serdeConfig = Collections.singletonMap("schema.registry.url", "http://"+args[0]+":8081");

        final Serde<instrument_reference_data_keys> keySpecificAvroSerde = new SpecificAvroSerde<>();
        keySpecificAvroSerde.configure(serdeConfig, true); // `true` for record keys
        final Serde<instrument_reference_data_values> valueSpecificAvroSerde = new SpecificAvroSerde<>();
        valueSpecificAvroSerde.configure(serdeConfig, false); // `false` for record values

        final StreamsBuilder builder = new StreamsBuilder();

        KStream<instrument_reference_data_keys, instrument_reference_data_values> source = builder.stream("prices", Consumed.with(keySpecificAvroSerde, valueSpecificAvroSerde)); 

        //source.to("test");//sends on new topic

        
        KafkaStreams streams = new KafkaStreams(builder.build(), streamsConfiguration);
        streams.start();

        final Topology topology = builder.build();

        System.out.println(topology.describe());


    }
}