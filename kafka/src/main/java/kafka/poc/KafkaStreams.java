package kafka.poc;

import java.util.Properties;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.Topology;
import org.apache.kafka.streams.kstream.KStream;

public class KafkaStreams {

    public static void main(String[] args) {
        Properties streamsConfiguration = new Properties();
        streamsConfiguration.put(StreamsConfig.APPLICATION_ID_CONFIG, "Streaming-QuickStart");
        streamsConfiguration.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        streamsConfiguration.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG,
                Serdes.String().getClass());
        streamsConfiguration.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG,
                Serdes.String().getClass());
        streamsConfiguration.put(StreamsConfig.APPLICATION_ID_CONFIG, "test");


        final StreamsBuilder builder = new StreamsBuilder();

        KStream<String, String> source = builder.stream("prices"); 

        source.to("prices");//sends on new topic

        final Topology topology = builder.build();

        System.out.println(topology.describe());


    }
}