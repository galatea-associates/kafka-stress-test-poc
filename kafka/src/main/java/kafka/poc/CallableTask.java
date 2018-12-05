package kafka.poc;

import java.util.List;
import java.util.Map;
import java.util.concurrent.Callable;
import java.util.concurrent.atomic.AtomicInteger;

import org.apache.avro.specific.SpecificRecord;
import org.apache.kafka.clients.producer.Producer;

public class CallableTask<T> implements Callable<Object> {

    private Producer kafkaProducer;
    private Topic topic;
    private List<Map<String, String>> data;
    private SpecificRecord[] recordObj;
    private Map<String, AtomicInteger> recieved_counter;
    private int maxSendInPeriod;

    public CallableTask(Producer kafkaProducer, Topic topic, List<Map<String, String>> data, SpecificRecord[] recordObj,
            Map<String, AtomicInteger> recieved_counter, int maxSendInPeriod) {
        this.kafkaProducer = kafkaProducer;
        this.topic = topic;
        this.data = data;
        this.recordObj = recordObj;
        this.recieved_counter = recieved_counter;
        this.maxSendInPeriod = maxSendInPeriod;
    }

    @Override
    public Object call() throws Exception {
        SimpleProducer.startSending(this.kafkaProducer, this.topic, this.data, this.recordObj, this.recieved_counter,
                this.maxSendInPeriod);
        return null;
    }
}
