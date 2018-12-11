package kafka.poc;

import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;
import java.util.stream.Collectors;

public class Timer implements Runnable {
    private HashMap<String, TopicProperties> topics;
    private CyclicBarrier cyclicBarrier;

    public Timer(HashMap<String, TopicProperties> topics, CyclicBarrier cyclicBarrier) {
        this.topics = topics;
        this.cyclicBarrier = cyclicBarrier;
    }

    private HashMap<String, Integer> getTopicCounters(TopicProperties topic) {
        if (System.currentTimeMillis() - topic.getLastStartTime() > topic.getTimePeriod()) {
            int sentCounter = topic.getCounters().get(Counter.SENT.toString()).getAndSet(0);
            int receivedCounter = topic.getCounters().get(Counter.RECEIVED.toString()).getAndSet(0);
            int errorCounter = topic.getCounters().get(Counter.ERROR.toString()).getAndSet(0);
            System.out.println(topic.getTopic().toString());
            System.out.println("I have tried to send: " + sentCounter);
            System.out.println("I have received acks: " + receivedCounter);
            System.out.println("---------------------------");
            topic.setLastStartTime(System.currentTimeMillis());
            return new HashMap<String, Integer>() {
                {
                    {
                        put(Counter.SENT.toString(), sentCounter);
                        put(Counter.RECEIVED.toString(), receivedCounter);
                        put(Counter.ERROR.toString(), errorCounter);
                    } ;
                };
            };
        }
        return null;

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
        HashMap<String, Integer> counterResults;

        HashMap<String, HashMap<String, List<Integer>>> results =
                new HashMap<String, HashMap<String, List<Integer>>>();

        for (Topic topic : Topic.values()) {

            results.put(topic.toString(), new HashMap<String, List<Integer>>() {
                {
                    put(Counter.SENT.toString(), new ArrayList<Integer>());
                    put(Counter.RECEIVED.toString(), new ArrayList<Integer>());
                    put(Counter.ERROR.toString(), new ArrayList<Integer>());
                }
            });

        }
        Runtime.getRuntime().addShutdownHook(new Thread() {
            private void writeCSV(){
                for (Topic topic : Topic.values()) {
                    try {
                        FileWriter writer = new FileWriter("./out/" + topic.toString() + ".csv");
                        for (Counter counter : Counter.values()) {
                            String collect = results.get(topic.toString()).get(counter.toString()).stream().map(i->((Integer) i).toString()).collect(Collectors.joining(","));
                            writer.write(collect);
                            writer.write(System.lineSeparator());
                        }
                        writer.close();
                    } catch (IOException e) {
                        // TODO Auto-generated catch block
                        e.printStackTrace();
                    }

                }
            }

            private void printStats() {
                for (Topic topic : Topic.values()) {
                    System.out.println("Topic: " + topic.toString());
                    for (Counter counter : Counter.values()) {
                        System.out.print("Average " + counter.toString() + ": "
                                + results.get(topic.toString()).get(counter.toString()).stream()
                                        .mapToInt(val -> val).average().orElse(0.0));
                        System.out.print(" Min " + counter.toString() + ": "
                                + results.get(topic.toString()).get(counter.toString()).stream()
                                        .mapToInt(val -> val).min());
                        System.out.print (" Max " + counter.toString() + ": "
                                + results.get(topic.toString()).get(counter.toString()).stream()
                                        .mapToInt(val -> val).max());
                        System.out.println(" Total " + counter.toString() + ": "
                                + results.get(topic.toString()).get(counter.toString()).stream()
                                        .mapToInt(val -> val).sum());
                    }
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
                if ((counterResults =
                        getTopicCounters(this.topics.get(topic.toString()))) != null) {
                    for (Counter counter : Counter.values()) {
                        results.get(topic.toString()).get(counter.toString())
                                .add(counterResults.get(counter.toString()));
                    }
                }
            }
        }
    }

    @Override
    public void run() {
        countTimer();
    }

}
