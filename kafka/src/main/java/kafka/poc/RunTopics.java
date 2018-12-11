package kafka.poc;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import org.apache.kafka.clients.producer.KafkaProducer;

public class RunTopics implements Runnable {
    private TopicProperties topicProperties;
    private int numMessagesToLoad;
    private int numThreads;
    private KafkaProducer kafkaProducer;
    private int numbJobsPerLoad;
    private CyclicBarrier cyclicBarrier;

    public RunTopics(KafkaProducer kafkaProducer, TopicProperties topicProperties, int numMessagesToLoad, int numThreads, int numbJobsPerLoad, CyclicBarrier cyclicBarrier){
        this.kafkaProducer = kafkaProducer;
        this.topicProperties = topicProperties;
        this.numMessagesToLoad = numMessagesToLoad;
        this.numThreads = numThreads;
        this.numbJobsPerLoad = numbJobsPerLoad;
        this.cyclicBarrier = cyclicBarrier;
    }

    @Override
    public void run() {
        List<CallableTask> callableTasks = new ArrayList<>();
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);

        for (int i = 0; i < numMessagesToLoad; i++){
            callableTasks.add(new CallableTask(kafkaProducer, topicProperties,
            topicProperties.getJob(numbJobsPerLoad)));
        }
        try {
            cyclicBarrier.await();
        } catch (InterruptedException e1) {
            // TODO Auto-generated catch block
            e1.printStackTrace();
        } catch (BrokenBarrierException e1) {
            // TODO Auto-generated catch block
            e1.printStackTrace();
		}
        try {
            while (true){
                executor.invokeAll(callableTasks);
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }



    }
}