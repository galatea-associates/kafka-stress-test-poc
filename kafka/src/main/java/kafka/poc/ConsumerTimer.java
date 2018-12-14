package kafka.poc;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;
import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;
import java.util.stream.Collectors;

public class ConsumerTimer implements Runnable {
    private Map<Topic, ConsumerTopicProperties> topicsToProperties;
    private CyclicBarrier cyclicBarrier;

    public ConsumerTimer(Map<Topic, ConsumerTopicProperties> topicsToProperties, CyclicBarrier cyclicBarrier) {
        this.topicsToProperties = topicsToProperties;
        this.cyclicBarrier = cyclicBarrier;
    }

    private Integer getTopicCounter(ConsumerTopicProperties topic) {
        if (System.currentTimeMillis() - topic.getLastStartTime() > topic.getTimePeriod()) {
            Integer receivedCounter = topic.getCounter().getAndSet(0);
            System.out.println(topic.getTopic().toString());
            System.out.println("I have received messages: " + receivedCounter);
            System.out.println("---------------------------");
            topic.setLastStartTime(System.currentTimeMillis());
            return receivedCounter;
        }
        return null;

    }

    private void countTimer() {
        try {
            cyclicBarrier.await();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (BrokenBarrierException e) {
            e.printStackTrace();
        }

        Integer counterResult;

        Map<Topic, List<Integer>> results = new EnumMap<>(Topic.class);
        for (Topic topic : Topic.values())
            results.put(topic, new ArrayList<>());

        Runtime.getRuntime().addShutdownHook(new Thread() {

            private void writeCSV(){
                for (Topic topic : Topic.values()) {
                    try {
                        File file = new File("./consumer-results/", topic.toString() + ".csv");
                        FileWriter writer = new FileWriter(file, true);
                        String collect = results.get(topic).stream().map(Object::toString).collect(Collectors.joining(","));
                        writer.write(collect);
                        writer.write(System.lineSeparator());
                        writer.close();
                    } catch (IOException e) {
                        // TODO Auto-generated catch block
                        e.printStackTrace();
                    }

                }
            }

            private void printStats() {
                Topic[] allTopics = Topic.values();
                List<Topic> topicsOfInterest = Arrays.asList(allTopics);
                for (Topic topic : topicsOfInterest) {
                    System.out.println("Topic: " + topic.toString());
                    System.out.print("Average " + Counter.RECEIVED.toString() + ": "
                        + results.get(topic).stream()
                        .mapToInt(val -> val).average().orElse(0.0));
                    System.out.print(" Min " + Counter.RECEIVED.toString() + ": "
                        + results.get(topic).stream()
                        .mapToInt(val -> val).min());
                    System.out.print(" Max " + Counter.RECEIVED.toString() + ": "
                        + results.get(topic).stream()
                        .mapToInt(val -> val).max());
                    System.out.println(" Total " + Counter.RECEIVED.toString() + ": "
                        + results.get(topic).stream()
                        .mapToInt(val -> val).sum());
                    System.out.println("---------------------");
                }
            }

            @Override
            public void run() {
                writeCSV();
                printStats();
            }
        });

        while (true) {
            for (Topic topic : Topic.values()) {
                counterResult = getTopicCounter(this.topicsToProperties.get(topic));
                if (counterResult != null)
                    results.get(topic).add(counterResult);
            }
        }
    }

    @Override
    public void run() {
        countTimer();
    }

}
