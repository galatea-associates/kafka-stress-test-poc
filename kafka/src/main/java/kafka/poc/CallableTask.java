package kafka.poc;

import java.util.List;
import java.util.Map;
import java.util.concurrent.Callable;

import org.apache.kafka.clients.producer.Producer;

public class CallableTask<T> implements Callable<Object> {

    private Producer kafkaProducer;
    private TopicProperties topicProperties;
    private List<Map<String, String>> job;

    public CallableTask(Producer kafkaProducer, TopicProperties topicProperties, List<Map<String, String>> job) {
        this.kafkaProducer = kafkaProducer;
        this.topicProperties = topicProperties;
        this.job = job;
    }

    @Override
    public Object call() throws Exception {
        SimpleProducer.startSending(this.kafkaProducer, this.topicProperties, this.job);
        return null;
    }
}
