package kafka.poc;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.util.concurrent.atomic.AtomicInteger;

@ToString
@EqualsAndHashCode
public class ConsumerTopicProperties {
    @Getter
    private Topic topic;
    @Getter
    private int timePeriod;
    @Getter
    private AtomicInteger counter;
    @Getter
    @Setter
    private long lastStartTime;

    public ConsumerTopicProperties(Topic topic, int timePeriod) {
        this.topic = topic;
        this.timePeriod = timePeriod * 1000;
        this.counter = new AtomicInteger();
        this.lastStartTime = System.currentTimeMillis();
    }
}
