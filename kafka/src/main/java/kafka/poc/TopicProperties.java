package kafka.poc;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;

import com.fasterxml.jackson.databind.MappingIterator;
import com.fasterxml.jackson.dataformat.csv.CsvMapper;
import com.fasterxml.jackson.dataformat.csv.CsvSchema;

import org.apache.avro.specific.SpecificRecord;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@ToString
@EqualsAndHashCode
public class TopicProperties {
    @Getter
    private Topic topic;
    private String csvFile;
    @Getter
    private List<Map<String, String>> data;
    @Getter
    private int maxSendInPeriod;
    @Getter
    private int timePeriod;

    private int currentArrayIdx = 0;
    @Setter
    @Getter
    private SpecificRecord[] recordObj;
    @Getter
    private Map<String, AtomicInteger> counters = new HashMap<String, AtomicInteger>() {
        private static final long serialVersionUID = 3019616454475007213L;
        {
            put(Counter.SENT.toString(), new AtomicInteger());
            put(Counter.RECEIVED.toString(), new AtomicInteger());
            put(Counter.ERROR.toString(), new AtomicInteger());
        }
    };
    @Getter
    @Setter
    private long lastStartTime = System.currentTimeMillis();

    public TopicProperties(Topic topic, String csvFile, int maxSendInPeriod, int timePeriod) {
        this.topic = topic;
        this.csvFile = csvFile;
        this.data = readFile(this.csvFile);
        this.maxSendInPeriod = maxSendInPeriod;
        this.timePeriod = timePeriod * 1000;
        this.recordObj = generateClasses(this.topic);
    }

    private static List<Map<String, String>> readFile(String csvFile) {
        File file = new File(csvFile);
        List<Map<String, String>> response = new LinkedList<Map<String, String>>();
        CsvMapper mapper = new CsvMapper();
        CsvSchema schema = CsvSchema.emptySchema().withHeader();
        MappingIterator<Map<String, String>> iterator = null;
        try {
            iterator = mapper.reader(Map.class).with(schema).readValues(file);
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        while (iterator.hasNext()) {
            response.add(iterator.next());
        }
        return response;
    }

    private static SpecificRecord[] generateClasses(Topic topic) {
        switch (topic) {
        case INST_REF:
            return new SpecificRecord[] { new instrument_reference_data_keys(),
                    new instrument_reference_data_values() };
        case PRICES:
            return new SpecificRecord[] { new prices_keys(), new prices_values() };
        case POSITION:
            return new SpecificRecord[] { new position_data_keys(), new position_data_values() };
        default:
            return null;
        }
    }

    public List<Map<String, String>> getJob(int numRowsPerJob) {
        List<Map<String, String>> jobData = new ArrayList<>();
        for (int i = 0; i < numRowsPerJob; i++) {
            jobData.add(this.data.get(this.currentArrayIdx));
            this.currentArrayIdx++;
            if (this.currentArrayIdx == this.data.size()) {
                this.currentArrayIdx = 0;
            }
        }
        return jobData;
    }

}