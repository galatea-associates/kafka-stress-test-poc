package kafka.poc;

import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;
import org.apache.avro.specific.SpecificRecord;
import org.apache.kafka.clients.producer.Producer;

public class RunnableTask implements Runnable {
    
    private Producer kafkaProducer;
    private Topic topic;
    private List<Map<String, String>> data;
    private SpecificRecord[] recordObj;
    private Map<String, AtomicInteger> recieved_counter;

    public RunnableTask(Producer kafkaProducer, Topic topic, List<Map<String, String>> data, SpecificRecord[] recordObj, Map<String, AtomicInteger> recieved_counter){
        this.kafkaProducer = kafkaProducer;
        this.topic = topic;
        this.data = data;
        this.recordObj = recordObj;
        this.recieved_counter = recieved_counter;
    }
    
    @Override
    public void run(){
        SimpleProducer.startSending(this.kafkaProducer, this.topic, this.data, this.recordObj, this.recieved_counter);
    }
}
