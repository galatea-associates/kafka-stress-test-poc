package kafka.poc;

import org.apache.kafka.clients.producer.ProducerRecord;
import java.util.Properties;
import java.util.concurrent.CyclicBarrier;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public final class SimpleProducer {
    private SimpleProducer() {
    }

    private static Properties producerProperties(String serverIP) {
        Properties properties = new Properties();
        properties.put("bootstrap.servers", serverIP + ":9092");
        properties.put("acks", "all");
        properties.put("retries", 0);
        properties.put("compression.type", "gzip");
        properties.put("batch.size", 16384);
        properties.put("linger.ms", 1);
        properties.put("buffer.memory", 33554432);
        properties.put("key.serializer", "io.confluent.kafka.serializers.KafkaAvroSerializer");
        properties.put("value.serializer", "io.confluent.kafka.serializers.KafkaAvroSerializer");
        properties.put("schema.registry.url", "http://" + serverIP + ":8081");

        return properties;
    }

    public static void startSending(TopicProperties topicProperties,
            List<Map<String, String>> job) {

        for (Map<String, String> data : job) {
            while (topicProperties.getCounters().get(Counter.SENT.toString())
                    .get() > topicProperties.getMaxSendInPeriod()) {
                continue;
            }
            topicProperties.setRecordObj(PopulateAvroTopic.populateData(topicProperties.getTopic(),
                    topicProperties.getRecordObj(), data));

            ProducerRecord record = new ProducerRecord<>(topicProperties.getTopic().toString(),
                    topicProperties.getRecordObj()[0], topicProperties.getRecordObj()[1]);

            try {
                topicProperties.getProducer().send(record, (metadata, exception) -> {
                    if (exception != null) {
                        topicProperties.getCounters().get(Counter.ERROR.toString())
                                .incrementAndGet();

                    } else {
                        topicProperties.getCounters().get(Counter.RECEIVED.toString())
                                .incrementAndGet();
                    }
                });
            } catch (Exception e) {
                e.printStackTrace();
            }

            topicProperties.getCounters().get(Counter.SENT.toString()).incrementAndGet();
        }
    }

    public static void main(String[] args) {

        Properties properties = producerProperties(args[0]);

        CyclicBarrier cyclicBarrier = new CyclicBarrier(4);
        HashMap<String, TopicProperties> topics = new HashMap<String, TopicProperties>() {
            {
                {
                    put(Topic.INST_REF.toString(), new TopicProperties(Topic.INST_REF,
                            "./out/inst-ref.csv", 100, 60, properties));
                    put(Topic.PRICES.toString(), new TopicProperties(Topic.PRICES,
                            "./out/prices.csv", 20000, 1, properties));
                    put(Topic.POSITION.toString(), new TopicProperties(Topic.POSITION,
                            "./out/position.csv", 40000, 1, properties));
                } ;
            };
        };

        new Thread(new RunTopics(topics.get(Topic.INST_REF.toString()), 100, 1, 1, cyclicBarrier))
                .start();
        new Thread(new RunTopics(topics.get(Topic.PRICES.toString()), 12000, 1, 1, cyclicBarrier))
                .start();
        new Thread(new RunTopics(topics.get(Topic.POSITION.toString()), 24000, 1, 1, cyclicBarrier))
                .start();
        new Thread(new Timer(topics, cyclicBarrier)).start();

    }
}
