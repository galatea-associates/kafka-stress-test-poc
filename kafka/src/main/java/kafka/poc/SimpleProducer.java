package kafka.poc;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import org.apache.avro.io.BinaryEncoder;
import org.apache.avro.io.DatumWriter;
import org.apache.avro.io.EncoderFactory;
import org.apache.avro.specific.SpecificDatumWriter;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.Producer;
import java.util.Properties;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.apache.avro.specific.SpecificRecord;

public final class SimpleProducer {
    private SimpleProducer() {
    }

    private static Producer producer() {
        Properties properties = new Properties();
        properties.put("bootstrap.servers", "3.8.1.159:9092");
        properties.put("acks", "all");
        properties.put("retries", 0);
        properties.put("compression.type", "gzip");
        properties.put("batch.size", 16384);
        properties.put("linger.ms", 1);
        properties.put("buffer.memory", 33554432);
        properties.put("key.serializer", "org.apache.kafka.common.serialization.ByteArraySerializer");
        properties.put("value.serializer", "org.apache.kafka.common.serialization.ByteArraySerializer");

        return new KafkaProducer(properties);
    }

    public static <T> byte[] serializeMessage(T eventMessage, org.apache.avro.Schema classSchema) throws IOException {

        ByteArrayOutputStream out = new ByteArrayOutputStream();
        BinaryEncoder encoder = EncoderFactory.get().binaryEncoder(out, null);
        DatumWriter<T> writer = new SpecificDatumWriter<T>(classSchema);
        writer.write(eventMessage, encoder);
        encoder.flush();
        out.close();
        return out.toByteArray();
    }

    public static void startSending(Producer kafkaProducer, TopicProperties topicProperties,
            List<Map<String, String>> job) {
        long startTime = System.currentTimeMillis();

        try {
            for (Map<String, String> data : job) {
                while (topicProperties.getCounters().get("Sent Counter").get() > topicProperties.getMaxSendInPeriod()) {
                    continue;
                }
                topicProperties.setRecordObj(PopulateAvroTopic.populateData(topicProperties.getTopic(),
                        topicProperties.getRecordObj(), data));

                ProducerRecord<Object, Object> record = new ProducerRecord<>(topicProperties.getTopic().toString(),
                        serializeMessage(topicProperties.getRecordObj()[0],
                                topicProperties.getRecordObj()[0].getSchema()),
                        serializeMessage(topicProperties.getRecordObj()[1],
                                topicProperties.getRecordObj()[1].getSchema()));


                kafkaProducer.send(record, (metadata, exception) -> {
                    topicProperties.getCounters().get("Received Counter").incrementAndGet();
                });
                topicProperties.getCounters().get("Sent Counter").incrementAndGet();
            }
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();

        }
    }

    public static SpecificRecord[] generateClasses(Topic topic) {
        switch (topic) {
        case INST_REF:
            return new SpecificRecord[] { new instrument_reference_data_keys(),
                    new instrument_reference_data_values() };
        case PRICES:
            return new SpecificRecord[] { new prices_keys(), new prices_values() };
        case POSITION:
            return new SpecificRecord[] { new position_data_keys(), new position_data_values() };
        default:
            return null;
        }
    }

    public static void main(String[] args) {

        Producer kafkaProducer = producer();
        ExecutorService executor = Executors.newFixedThreadPool(5);
        List<CallableTask<Object>> callableTasks = new ArrayList<>();

        HashMap<String, TopicProperties> topics = new HashMap<String, TopicProperties>() {
            {
                {
                    put("inst-ref", new TopicProperties(Topic.INST_REF, "./out/inst-ref.csv", 100, 60));
                    put("prices", new TopicProperties(Topic.PRICES, "./out/prices.csv", 20000, 1));
                    put("position", new TopicProperties(Topic.POSITION, "./out/position.csv", 40000, 1));
                }
                ;
            };
        };
        for (int i = 0; i < 100; i++){
            callableTasks.add(new CallableTask<Object>(kafkaProducer, topics.get("inst-ref"), topics.get("inst-ref").getJob(1)));
        }
        
        for (int i = 0; i < 70000; i++){
            callableTasks.add(new CallableTask<Object>(kafkaProducer, topics.get("prices"),
            topics.get("prices").getJob(1)));
        }

        for (int i = 0; i < 70000; i++){
            callableTasks.add(new CallableTask<Object>(kafkaProducer, topics.get("position"),
            topics.get("position").getJob(1)));
        }

        System.out.println("Starting execution");

        Thread t = new Thread(new Timer(topics));
        t.start();

        try {
            executor.invokeAll(callableTasks);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        Runtime.getRuntime().addShutdownHook(new Thread() {
            @Override
            public void run() {
                kafkaProducer.flush();
                kafkaProducer.close();
            }
        });
        
    }
}
