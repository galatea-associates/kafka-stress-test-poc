package kafka.poc;

import java.util.HashMap;
import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;

public class Timer implements Runnable {
    private HashMap<String, TopicProperties> topics;
    private CyclicBarrier cyclicBarrier;

    public Timer(HashMap<String, TopicProperties> topics, CyclicBarrier cyclicBarrier){
        this.topics = topics;
        this.cyclicBarrier = cyclicBarrier;
    }

    private void printTopicTimer(TopicProperties topic){
        if (System.currentTimeMillis() - topic.getLastStartTime() > topic.getTimePeriod()) {
            System.out.println(topic.getTopic().toString());
            System.out.println("I have tried to send: "
                    + topic.getCounters().get("Sent Counter").getAndSet(0));
            System.out.println("I have received acks: "
                    + topic.getCounters().get("Received Counter").getAndSet(0));
            System.out.println("---------------------------");
            topic.setLastStartTime(System.currentTimeMillis());
        }
    }

    private void countTimer() {
        try {
            cyclicBarrier.await();
        } catch (InterruptedException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (BrokenBarrierException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
		}
        while (true){
            printTopicTimer(this.topics.get("inst-ref"));
            printTopicTimer(this.topics.get("position"));
            printTopicTimer(this.topics.get("prices"));
        }
    }

    @Override
    public void run() {
        countTimer();
    }

}