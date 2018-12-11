package kafka.poc;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;

public class Timer implements Runnable {
    private HashMap<String, TopicProperties> topics;
    private CyclicBarrier cyclicBarrier;

    public Timer(HashMap<String, TopicProperties> topics, CyclicBarrier cyclicBarrier) {
        this.topics = topics;
        this.cyclicBarrier = cyclicBarrier;
    }

    private HashMap<String, Integer> getTopicCounters(TopicProperties topic) {
        if (System.currentTimeMillis() - topic.getLastStartTime() > topic.getTimePeriod()) {
            int sentCounter = topic.getCounters().get("Sent Counter").getAndSet(0);
            int receivedCounter = topic.getCounters().get("Received Counter").getAndSet(0);
            int errorCounter = topic.getCounters().get("Error Counter").getAndSet(0);
            System.out.println(topic.getTopic().toString());
            System.out.println("I have tried to send: " + sentCounter);
            System.out.println("I have received acks: " + receivedCounter);
            System.out.println("---------------------------");
            topic.setLastStartTime(System.currentTimeMillis());
            return new HashMap<String, Integer>() {
                {
                    {
                        put("Sent Counter", sentCounter);
                        put("Received Counter", receivedCounter);
                        put("Error Counter", errorCounter);
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
                new HashMap<String, HashMap<String, List<Integer>>>() {
                    private static final long serialVersionUID = 1999814976537772940L;

                    {
                        put("inst-ref", new HashMap<String, List<Integer>>() {
                            private static final long serialVersionUID = 6562375338505855905L;

                            {
                                put("Sent Counter", new ArrayList<Integer>());
                                put("Received Counter", new ArrayList<Integer>());
                                put("Error Counter", new ArrayList<Integer>());
                            }
                        });
                        put("position", new HashMap<String, List<Integer>>() {
                            private static final long serialVersionUID = 5849690482183889132L;

                            {
                                put("Sent Counter", new ArrayList<Integer>());
                                put("Received Counter", new ArrayList<Integer>());
                                put("Error Counter", new ArrayList<Integer>());
                            }
                        });
                        put("prices", new HashMap<String, List<Integer>>() {
                            private static final long serialVersionUID = -376004311328108957L;

                            {
                                put("Sent Counter", new ArrayList<Integer>());
                                put("Received Counter", new ArrayList<Integer>());
                                put("Error Counter", new ArrayList<Integer>());
                            }
                        });
                    }
                };
        Runtime.getRuntime().addShutdownHook(new Thread() {
            @Override
            public void run() {
                System.out.println("I closing now");
            }
        });


        while (true) {
            if ((counterResults = getTopicCounters(this.topics.get("inst-ref"))) != null) {
                results.get("inst-ref").get("Sent Counter").add(counterResults.get("Sent Counter"));
                results.get("inst-ref").get("Received Counter").add(counterResults.get("Received Counter"));
                results.get("inst-ref").get("Error Counter").add(counterResults.get("Error Counter"));
            }
            if ((counterResults = getTopicCounters(this.topics.get("position"))) != null) {
                results.get("position").get("Sent Counter").add(counterResults.get("Sent Counter"));
                results.get("position").get("Received Counter").add(counterResults.get("Received Counter"));
                results.get("position").get("Error Counter").add(counterResults.get("Error Counter"));
            }
            if ((counterResults = getTopicCounters(this.topics.get("prices"))) != null) {
                results.get("prices").get("Sent Counter").add(counterResults.get("Sent Counter"));
                results.get("prices").get("Received Counter").add(counterResults.get("Received Counter"));
                results.get("prices").get("Error Counter").add(counterResults.get("Error Counter"));
            }
        }
    }

    @Override
    public void run() {
        countTimer();
    }

}
