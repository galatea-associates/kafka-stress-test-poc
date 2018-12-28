package kafka.poc;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Properties;
import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;

class SimpleConsumer<K,V> implements Runnable {

    private int timeout;
    private String serverIP;
    private KafkaConsumer<K, V> consumer;
    private ArrayList<ConsumerRecord<K, V>> messagesReceived;
    private ConsumerTopicProperties props;
    private CyclicBarrier cyclicBarrier;

    SimpleConsumer(int timeout, String serverIP, ConsumerTopicProperties props, CyclicBarrier cyclicBarrier) {
        this.timeout = timeout;
        this.serverIP = serverIP;
        this.messagesReceived = new ArrayList<>();
        this.props = props;
        this.cyclicBarrier = cyclicBarrier;
    }

    private void runConsumer() {
        this.consumer.subscribe(Collections.singletonList(props.getTopic().toString()));

        final int giveUp = 5;
        int noRecordsCount = 0;
        ConsumerRecords<K, V> records;
        try {
            cyclicBarrier.await();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (BrokenBarrierException e) {
            e.printStackTrace();
        }

        try {
            while (true) {
                records = this.consumer.poll(this.timeout);
                if (noRecordsReceived(records)) {
                    noRecordsCount++;
                    if (noRecordsCount > giveUp) {
                        break;
                    }
                    else continue;
                }
                props.getCounter().addAndGet(records.count());
//            System.out.println(records.count());
//                processRecords(records);
                consumer.commitAsync();
            }
            consumer.close();
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    private void processRecords(ConsumerRecords<K, V> records) {
        for (ConsumerRecord<K, V> record : records) {
//            this.messagesReceived.add(record);
//            System.out.printf("key = %s, value = %s %n", record.key(), record.value());
        }
    }

    private boolean noRecordsReceived(ConsumerRecords<K, V> records) {
        return records.count() == 0;
    }

    private void createConsumer() {
        Properties properties = new Properties();
        properties.put("bootstrap.servers", this.serverIP + ":9092");
        properties.put("group.id", props.getTopic().toString());
        properties.put("key.deserializer", "io.confluent.kafka.serializers.KafkaAvroDeserializer");
        properties.put("value.deserializer", "io.confluent.kafka.serializers.KafkaAvroDeserializer");
        properties.put("schema.registry.url", "http://" + this.serverIP + ":8081");
        properties.put("max.poll.records", "1000000");

        this.consumer = new KafkaConsumer<>(properties);
    }

    @Override
    public void run() {
        createConsumer();
        runConsumer();
    }
}
